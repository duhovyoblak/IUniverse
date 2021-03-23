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
        
        self.values  = {1:'reDs', 2:'imDs', 3:'phi', 4:'phs'}
        self.actVal  = 1
        
        self.data = self.space3M.getPlotData()
        
 #       for key, lst in self.data['data'].items(): print( "Data list '{}' has length {}".format(key, len(lst)) )
        
        self.reUnit()
        
        #----------------------------------------------------------------------
        # Create output window
        win = tk.Tk()
        win.title(self.title)
        win.geometry('1280x1000')
        win.resizable(False,False)
        win.update()
        self.w = win.winfo_width()
        self.h = win.winfo_height()
        
        #----------------------------------------------------------------------
        # Create layout

        self.fig = plt.figure(figsize=(self.w*0.9/100, self.h*0.8/100), dpi=100)
        self.ax = self.fig.add_subplot(1,1,1)

        self.canvas = FigureCanvasTkAgg(self.fig, master=win)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=self.w*0.0, y=self.h*0.0)
        
        self.fig.canvas.callbacks.connect('button_press_event', self.on_click)

        #----------------------------------------------------------------------
        # Axes buttons setup
        
        self.param_map_var = tk.IntVar()
        
        self.butAx1 = tk.Radiobutton(win, text='pm_text 1', variable=self.param_map_var, value=1, command=self.on_butAxe)
        self.butAx1.place(x=self.w * 0.91, y = self.h * (0.1 + 3 * 0.03))

        self.butAx2 = tk.Radiobutton(win, text='pm_text 2', variable=self.param_map_var, value=2, command=self.on_butAxe)
        self.butAx2.place(x=self.w * 0.91, y = self.h * (0.1 + 4 * 0.03))

        self.butAx1.select()
        
        #----------------------------------------------------------------------
        # Value buttons setup
        
        self.map_var = tk.IntVar()
        
        self.butReDs = tk.Radiobutton(win, text='real Ds', variable=self.map_var, value=1, command=self.on_butVal)
        self.butReDs.place(x=self.w * 0.91, y = self.h * (0.1 + 7 * 0.03))

        self.butImDs = tk.Radiobutton(win, text='im Ds', variable=self.map_var, value=2, command=self.on_butVal)
        self.butImDs.place(x=self.w * 0.91, y = self.h * (0.1 + 8 * 0.03))

        self.butPhi  = tk.Radiobutton(win, text='Phi', variable=self.map_var, value=3, command=self.on_butVal)
        self.butPhi.place(x=self.w * 0.91, y = self.h * (0.1 + 9 * 0.03))

        self.butPhs  = tk.Radiobutton(win, text='Phasei', variable=self.map_var, value=4, command=self.on_butVal)
        self.butPhs.place(x=self.w * 0.91, y = self.h * (0.1 + 10 * 0.03))

        self.butReDs.select()
        
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
        for key, lst in self.data['data'].items():
            
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
            self.data['meta'][key]['unit'] = c[0]
            
            journal.M( 'Space3Mgui {} Data list {} was re-scaled by {:e} with preposition {}'.format(self.title, key, c[1], c[0]), 10 )
                
        journal.O( 'Space3Mgui {} reUnit done'.format(self.title), 10 )
    
    #--------------------------------------------------------------------------
    def getDataLabel(self, key):
        "Return data label for given data's key"
        
        return "${}$ [{}{}]".format(key, self.data['meta'][key]['unit'], 
                                         self.data['meta'][key]['dim' ])
        
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
            
            X = np.array(self.data['data']['x' ])
            Y = np.array(self.data['data']['t' ])
            
            val = self.values[self.actVal]
            Z = np.array(self.data['data'][val])
            
            self.ax.plot_trisurf( X, Y, Z, linewidth=0.2, cmap='RdYlGn', antialiased=False)
            
        elif self.actAxe == 2:
            
            self.ax.remove()
            self.ax = self.fig.add_subplot(1,1,1)
            
            # Vykreslenie phi plochy
            self.ax.set_title("Amplitude's phase in <0, 2Pi>", fontsize=14)
            self.ax.grid(True)
            self.ax.set_xlabel( self.getDataLabel('x') )
            self.ax.set_ylabel( self.getDataLabel('t') )

            X = np.array(self.data['data']['x' ])
            Y = np.array(self.data['data']['t' ])

            U = np.array(self.data['data']['phs_x' ])
            V = np.array(self.data['data']['phs_y' ])
            
            self.ax.quiver( X, Y, U, V )
        
        # Vykreslenie diagramu
        self.fig.tight_layout()
        self.canvas.draw()
    
        journal.O( 'Space3Mgui {} show done'.format(self.title), 10 )
        
    #--------------------------------------------------------------------------
    def on_butAxe(self):
        "Resolve radio buttons selection for active Axe of figure"
        
        self.actAxe = self.param_map_var.get() # get integer value for selected button
        self.show()
    
    #--------------------------------------------------------------------------
    def on_butVal(self):
        "Resolve radio buttons selection for active Value in plot"
        
        self.actVal = self.map_var.get() # get integer value for selected button
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
            
            x = event.xdata
            y = event.ydata
            id = self.space3M.getIdFromPos({'x':x, 'y':0, 'z':0, 't':y})
            
            self.space3M.printCell(id)
            
        else:
            print('Clicked ouside axes bounds but inside plot window')
    
    #--------------------------------------------------------------------------

#------------------------------------------------------------------------------
print('Minkowski space class GUI ver 0.20')
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
