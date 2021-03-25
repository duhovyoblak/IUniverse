#==============================================================================
# Minkowski space class GUI
#------------------------------------------------------------------------------
#
#    real position is given in meters for x,z,y and nanosecenods for t as real values
#    grid position means position in numpy-like 4D array as integers 0..ix, 0..iy, 0..iz, 0..it
#
#    phi means argument (omega*t - k*x) as real value in radians
#    phs means phi mod 2*PI in radians
#
#------------------------------------------------------------------------------
from siqo_lib import journal

#from matplotlib.figure                 import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits                      import mplot3d

import numpy             as np
import matplotlib.pyplot as plt
import tkinter           as tk

#==============================================================================
# package's constants
#------------------------------------------------------------------------------

_WIN            = '1680x1050'
#_WIN            = '1280x1000'
_DPI            = 100
_FIG_W          = 0.8
_FIG_H          = 0.9

_BTN_DIS_W      = 0.1
_BTN_DIS_H      = 0.03

_BTN_AXE_W      = 0.82
_BTN_AXE_H      = 0.1

_BTN_VAL_W      = 0.82
_BTN_VAL_H      = 0.2

#==============================================================================
# class Space3Mgui
#------------------------------------------------------------------------------
class Space3Mgui:
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, space):
        "Create and show GUI for Minkowski space"

        journal.I( 'Space3Mgui constructor...', 10 )
        
        #----------------------------------------------------------------------
        # Internal data
        
        self.space3M = space
        self.title   = self.space3M.name
        
        self.axes    = {1:'Phi manifold', 2:'Phase map'}
        self.actAxe  = 1
        
        self.values  = {1:'x', 2:'y', 3:'z', 4:'t', 5:'phi', 6:'reDs', 7:'imDs', 8:'reAmp', 9:'imAmp'}
        self.actValX = 8
        self.actValY = 9
        
        dat  = self.space3M.getPlotData()
        self.meta    = dat['meta']
        self.data    = dat['data']
        
        self.reUnit()
        
        #----------------------------------------------------------------------
        # Create output window
        win = tk.Tk()
        win.title(self.title)
        win.geometry(_WIN)
        win.resizable(False,False)
        win.update()
        self.w = win.winfo_width()
        self.h = win.winfo_height()
        
        #----------------------------------------------------------------------
        # Create layout

        self.fig = plt.figure(figsize=(self.w*_FIG_W/100, self.h*_FIG_H/100), dpi=_DPI)
        self.ax = self.fig.add_subplot(1,1,1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=win)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=self.w*0.0, y=self.h*0.0)
        
        self.fig.canvas.callbacks.connect('button_press_event', self.on_click)

        #----------------------------------------------------------------------
        # Axes buttons setup
        
        self.butAxeMap = tk.IntVar()
        
        self.butAx1 = tk.Radiobutton(win, text='pm_text 1', variable=self.butAxeMap, value=1, command=self.onButAxe)
        self.butAx1.place(x=self.w * (_BTN_AXE_W             ), y = self.h * _BTN_AXE_H)

        self.butAx2 = tk.Radiobutton(win, text='pm_text 2', variable=self.butAxeMap, value=2, command=self.onButAxe)
        self.butAx2.place(x=self.w * (_BTN_AXE_W + _BTN_DIS_W), y = self.h * _BTN_AXE_H)

        self.butAx1.select()
        
        #----------------------------------------------------------------------
        # Value buttons X setup
        
        self.butValMapX = tk.IntVar()
        
        for i, val in self.values.items():
            self.butReDs = tk.Radiobutton(win, text="{} [{}]".format(val, self.meta[val]['dim']), variable=self.butValMapX, value=i, command=self.onButValX)
            self.butReDs.place(x=self.w * _BTN_VAL_W, y = self.h * (_BTN_VAL_H + i * _BTN_DIS_H))

        self.butReDs.select()
        
        #----------------------------------------------------------------------
        # Value buttons Y setup
        
        self.butValMapY = tk.IntVar()

        for i, val in self.values.items():
            self.butY = tk.Radiobutton(win, text="{} [{}]".format(val, self.meta[val]['dim']), variable=self.butValMapY, value=i, command=self.onButValY)
            self.butY.place(x=self.w * (_BTN_VAL_W + _BTN_DIS_W), y = self.h * (_BTN_VAL_H + i * _BTN_DIS_H))

        #----------------------------------------------------------------------
        # Sliders setup
        
        self.g = 9.8
        self.g_slider = tk.Scale(win, from_=0.0, to=20.0, resolution=0.1, orient=tk.HORIZONTAL, length=self.w*0.4, command=self.on_gSlider, label="g")
        self.g_slider.place(x=self.w * 0.5, y=self.h * 0.9)
        self.g_slider.set(9.8)
        
        #----------------------------------------------------------------------
        # Initialisation
        
        self.show()   # Initial drawing
        journal.O( 'Space3Mgui created for space {}'.format(self.title), 10 )

        win.mainloop()       # Start listening for events

    #==========================================================================
    # Tools for figure setting
    #--------------------------------------------------------------------------
    def reUnit(self):
        "Re-scale all data vectors for better understability"
        
        journal.I( 'Space3Mgui {} reUnit...'.format(self.title), 10 )
        for key, lst in self.data.items():
            
            pL = list(lst)  # Urobim si kopiu listu na pokusy :-)
            pL.sort()
                
            # Najdem vhodny koeficient
            if pL[-1]-pL[0] > 1e-12 : c = ('p', 1e+12)
            if pL[-1]-pL[0] > 1e-09 : c = ('n', 1e+09)
            if pL[-1]-pL[0] > 1e-06 : c = ('µ', 1e+06)
            if pL[-1]-pL[0] > 1e-03 : c = ('m', 1e+03)
            if pL[-1]-pL[0] > 1e+00 : c = ('',  1e+00)
            if pL[-1]-pL[0] > 1e+03 : c = ('K', 1e-03)
            if pL[-1]-pL[0] > 1e+06 : c = ('M', 1e-06)
            if pL[-1]-pL[0] > 1e+09 : c = ('G', 1e-09)
            if pL[-1]-pL[0] > 1e+12 : c = ('T', 1e-12)
                
            # Preskalujem udaje
            for i in range(len(lst)): lst[i] = lst[i] * c[1]
            self.meta[key]['unit' ] = c[0]
            self.meta[key]['coeff'] = c[1]
            
            journal.M( 'Space3Mgui {} Data list {} was re-scaled by {:e} with preposition {}'.format(self.title, key, c[1], c[0]), 10 )
                
        journal.O( 'Space3Mgui {} reUnit done'.format(self.title), 10 )
    
    #--------------------------------------------------------------------------
    def getDataLabel(self, key):
        "Return data label for given data's key"
        
        return "${}$ [{}{}]".format(key, self.meta[key]['unit'], 
                                         self.meta[key]['dim' ])
        
    #==========================================================================
    # GUI methods
    #--------------------------------------------------------------------------
    def show(self):
        "Show Minkovski space according to given parameters"
        
        journal.I( 'Space3Mgui {} show {}'.format(self.title, self.axes[self.actAxe]), 10 )
        
        self.ax3 = self.fig.add_subplot(1,2,2, projection='3d')
        
        
        # Test aktivneho typu zobrazenia
        if self.actAxe == 1:
            
            self.ax.remove()
            self.ax = self.fig.add_subplot(1,1,1, projection='3d')
        
            # Vykreslenie phi plochy
            self.ax.set_title("Phi angle as phi = omega*t - abs(k*r) in [rad]", fontsize=14)
#            self.ax.grid(True)
            self.ax.set_xlabel( self.getDataLabel('x') )
            self.ax.set_ylabel( self.getDataLabel('t') )
            
            X = np.array(self.data['x' ])
            Y = np.array(self.data['t' ])
            
            valX = self.values[self.actValX]
            Z = np.array(self.data[valX])
            
            self.ax.plot_trisurf( X, Y, Z, linewidth=0.2, cmap='RdYlGn', antialiased=False)
            
        elif self.actAxe == 2:
            
            self.ax.remove()
            self.ax = self.fig.add_subplot(1,1,1)
            
            # Vykreslenie phi plochy
            self.ax.set_title("Amplitude's phase in <0, 2Pi>", fontsize=14)
            self.ax.grid(True)
            self.ax.set_xlabel( self.getDataLabel('x') )
            self.ax.set_ylabel( self.getDataLabel('t') )

            X = np.array(self.data['x' ])
            Y = np.array(self.data['t' ])

            valX = self.values[self.actValX]
            U = np.array(self.data[valX])

            valY = self.values[self.actValY]
            V = np.array(self.data[valY])

            self.ax.quiver( X, Y, U, V )
        
        # Vykreslenie diagramu
        self.fig.tight_layout()
        self.canvas.draw()
    
        journal.O( 'Space3Mgui {} show done'.format(self.title), 10 )
        
    #--------------------------------------------------------------------------
    def onButAxe(self):
        "Resolve radio buttons selection for active Axe of figure"
        
        self.actAxe = self.butAxeMap.get() # get integer value for selected button
        self.show()
    
    #--------------------------------------------------------------------------
    def onButValX(self):
        "Resolve radio buttons selection for active X Value in plot"
        
        self.actValX = self.butValMapX.get() # get integer value for selected button
        self.show()
    
    #--------------------------------------------------------------------------
    def onButValY(self):
        "Resolve radio buttons selection for active Y Value in plot"
        
        self.actValY = self.butValMapY.get() # get integer value for selected button
        self.show()
    
    #--------------------------------------------------------------------------
    def on_gSlider(self, new_val=1.0):
        "Resolve change of g-Slider"

        self.g   = new_val  # same as self.g_slider.get()
        self.show()
    
    #--------------------------------------------------------------------------
    def on_click(self, event):
        "Print information about mouse-given position"
        
        if event.inaxes is not None:
            
            x = float(event.xdata)
            y = float(event.ydata)
            
            x = x / self.meta['x']['coeff']
            y = y / self.meta['t']['coeff']
            
            id = self.space3M.getIdFromPos({'x':x, 'y':0, 'z':0, 't':y})
            
            self.space3M.printCell(id)
            
        else:
            print('Clicked ouside axes bounds but inside plot window')
    
    #--------------------------------------------------------------------------

#------------------------------------------------------------------------------
print('Minkowski space class GUI ver 0.30')
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
