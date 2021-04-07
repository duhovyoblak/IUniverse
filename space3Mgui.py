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

#_WIN            = '1680x1050'
_WIN            = '1300x740'
_DPI            = 100

_FIG_W          = 0.8
_FIG_H          = 1.0

_SC_RED         = 1.4

_BTN_AXE_W      = 0.81
_BTN_AXE_H      = 0.03

_BTN_VAL_W      = 0.81
_BTN_VAL_H      = 0.10

_BTN_DIS_W      = 0.1
_BTN_DIS_H      = 0.025

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
        
        self.axes    = {1:'Scatter', 2:'Quiver', 3:'3D projection'}
        self.actAxe  = 1
        
        self.values  = { 1:'x',      2:'y',      3:'z',      4:'t', 
#                         5:'reDs',   6:'imDs',   7:'abDs',  
                         5:'reDt',   6:'imDt',   7:'abDt',   8:'phi',
                         9:'reAmp', 10:'imAmp', 11:'abAmp', 12:'P'}

        self.actValX = 1
        self.actValY = 4
        self.actValU = 7
        self.actValV = 11
        
        self.setActValS()
        
        #----------------------------------------------------------------------
        # Ziskanie realnych dat na zobrazenie z podkladoveho priestoru
        dat  = self.space3M.getPlotData()
        self.meta    = dat['meta']
        self.data    = dat['data']
        self.reScale()
        
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
        
        self.butAx1 = tk.Radiobutton(win, text='Scatter chart', variable=self.butAxeMap, value=1, command=self.onButAxe)
        self.butAx1.place(x=self.w * _BTN_AXE_W, y = self.h * (_BTN_AXE_H + 0 * _BTN_DIS_H) )

        self.butAx2 = tk.Radiobutton(win, text='Quiver chart',  variable=self.butAxeMap, value=2, command=self.onButAxe)
        self.butAx2.place(x=self.w * _BTN_AXE_W, y = self.h * (_BTN_AXE_H + 1 * _BTN_DIS_H) )

        self.butAx3 = tk.Radiobutton(win, text='3D projection', variable=self.butAxeMap, value=3, command=self.onButAxe)
        self.butAx3.place(x=self.w * _BTN_AXE_W, y = self.h * (_BTN_AXE_H + 2 * _BTN_DIS_H) )

        self.butAx1.select()
        
        #----------------------------------------------------------------------
        # Value buttons X setup
        
        self.butValMapX = tk.IntVar()
        
        for i, val in self.values.items():
            self.butX = tk.Radiobutton(win, text="{} [{}]".format(val, self.meta[val]['dim']), variable=self.butValMapX, value=i, command=self.onButValX)
            self.butX.place(x=self.w * _BTN_VAL_W, y = self.h * (_BTN_VAL_H + i * _BTN_DIS_H))

        self.butX.select()
        self.butValMapX.set(self.actValX)
        
        #----------------------------------------------------------------------
        # Value buttons Y setup
        
        self.butValMapY = tk.IntVar()

        for i, val in self.values.items():
            self.butY = tk.Radiobutton(win, text="{} [{}]".format(val, self.meta[val]['dim']), variable=self.butValMapY, value=i, command=self.onButValY)
            self.butY.place(x=self.w * (_BTN_VAL_W + _BTN_DIS_W), y = self.h * (_BTN_VAL_H + i * _BTN_DIS_H))

        self.butY.select()
        self.butValMapY.set(self.actValY)

        #----------------------------------------------------------------------
        # Value buttons U setup
        
        self.butValMapU = tk.IntVar()

        for i, val in self.values.items():
            self.butU = tk.Radiobutton(win, text="{} [{}]".format(val, self.meta[val]['dim']), variable=self.butValMapU, value=i, command=self.onButValU)
            self.butU.place(x=self.w * _BTN_VAL_W, y = self.h * (_BTN_VAL_H + (i+15) * _BTN_DIS_H))

        self.butU.select()
        self.butValMapU.set(self.actValU)

        #----------------------------------------------------------------------
        # Value buttons V setup
        
        self.butValMapV = tk.IntVar()

        for i, val in self.values.items():
            self.butV = tk.Radiobutton(win, text="{} [{}]".format(val, self.meta[val]['dim']), variable=self.butValMapV, value=i, command=self.onButValV)
            self.butV.place(x=self.w * (_BTN_VAL_W + _BTN_DIS_W), y = self.h * (_BTN_VAL_H + (i+15) * _BTN_DIS_H))

        self.butV.select()
        self.butValMapV.set(self.actValV)

        #----------------------------------------------------------------------
        # Slider for slider axis Z setup
        
        sMin = self.meta['g'+self.values[self.actValS]]['min']
        sMax = self.meta['g'+self.values[self.actValS]]['max']
        
        self.sldS = tk.Scale(win, from_=sMin, to=sMax, resolution=1, orient=tk.HORIZONTAL, length=self.w*0.18, command=self.onSlider, label="Data are sliced by ")
        self.sldS.place(x=self.w * 0.81, y=self.h * 0.9)
        self.sVal = 0
        
        self.sLabMap = tk.StringVar()
        self.sLab = tk.Label(win, textvariable = self.sLabMap)
        self.sLab.place(x=self.w * 0.89, y=self.h * 0.9)
        
        self.sLabMap.set("Test")
        
        #----------------------------------------------------------------------
        # Initialisation
        
        self.show()   # Initial drawing
        journal.O( 'Space3Mgui created for space {}'.format(self.title), 10 )

        win.mainloop()       # Start listening for events

    #--------------------------------------------------------------------------
    def sliderSetup(self):

        gv  = self.sVal
        key = self.values[self.actValS]
        v   = self.getValByGrid(gv, key)
        
        self.sLabMap.set("dim '{}' with value {:.3f}".format(key, v) )
    
    #==========================================================================
    # Tools for figure setting
    #--------------------------------------------------------------------------
    def reScale(self):
        "Re-scale all data vectors for better understability"
        
        journal.I( 'Space3Mgui {} reScale...'.format(self.title), 10 )
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
                
        journal.O( 'Space3Mgui {} reScale done'.format(self.title), 10 )
    
    #--------------------------------------------------------------------------
    def getDataLabel(self, key):
        "Return data label for given data's key"
        
        return "${}$ [{}{}]".format(key, self.meta[key]['unit'], 
                                         self.meta[key]['dim' ])
    
    #--------------------------------------------------------------------------
    def getValByGrid(self, gv, key):
        "Return rescaled value for given grid's value and data's key"
        
        gl = self.meta['g'+key]['max'] - self.meta['g'+key]['min']
        vl = self.meta[    key]['max'] - self.meta[    key]['min']
        
        return (gv/gl) * vl * self.meta[key]['coeff']
    
    #--------------------------------------------------------------------------
    def setActValS(self):
        "Choose hidden variable for slider axis for given actX and actY"
        
        self.actValS = 2

        lst = [1, 2, 4]
        
        try   :lst.remove(self.actValX)
        except: pass
    
        try   :lst.remove(self.actValY)
        except: pass
        
        try   : lst.remove(self.actValU)
        except: pass

        self.actValS = lst[0]

        journal.M( 'Space3Mgui {} setActValS choose for X={}, Y={}, U={} slider value S = {}'.format(self.title, self.actValX, self.actValY, self.actValU, self.actValS), 10 )
        
    #--------------------------------------------------------------------------
    def getDataSlice(self):
        "Return a slice of data for given actValS"
        
        sDim = 'g' + self.values[self.actValS]
        sCut = self.sVal
        
        journal.I( "Space3Mgui {} getDataSlice will use Dim='{}' with cut={}".format(self.title, sDim, sCut), 10 )

        x = []
        y = []
        u = []
        v = []

        xDim = self.values[self.actValX]
        yDim = self.values[self.actValY]
        uDim = self.values[self.actValU]
        vDim = self.values[self.actValV]

        i = 0
        for sValue in self.data[sDim]:
            
            if sValue == sCut:
                x.append( self.data[xDim][i] )
                y.append( self.data[yDim][i] )
                u.append( self.data[uDim][i] )
                v.append( self.data[vDim][i] )
            i += 1
        
        X = np.array(x)
        journal.M( "Space3Mgui {} getDataSlice X dimension is {} in <{:.3}, {:.3}>".format(self.title, xDim, X.min(), X.max()), 10 )

        Y = np.array(y)
        journal.M( "Space3Mgui {} getDataSlice Y dimension is {} in <{:.3}, {:.3}>".format(self.title, yDim, Y.min(), Y.max()), 10 )

        U = np.array(u)
        journal.M( "Space3Mgui {} getDataSlice U dimension is {} in <{:.3}, {:.3}>".format(self.title, uDim, U.min(), U.max()), 10 )

        V = np.array(v)
        journal.M( "Space3Mgui {} getDataSlice V dimension is {} in <{:.3}, {:.3}>".format(self.title, vDim, V.min(), V.max()), 10 )


        journal.O( "Space3Mgui {} getDataSlice return 4 x {} data points".format(self.title, len(x)), 10 )
        
        return (X, Y, U, V)
        
    #==========================================================================
    # GUI methods
    #--------------------------------------------------------------------------
    def show(self):
        "Show Minkovski space according to given parameters"
        
        journal.I( 'Space3Mgui {} show {}'.format(self.title, self.axes[self.actAxe]), 10 )
        
        # Odstranenie vsetkych axes
        while len(self.fig.axes)>0: self.fig.axes[0].remove()
        
        # Rozhodnutie o slider dimezii
        self.setActValS()

        # Vytvorenie rezu udajov na zobrazenie
        (X, Y, U, V) = self.getDataSlice()
    
        # Priprava novych axes
        self.sliderSetup()
        valX = self.values[self.actValX]
        valY = self.values[self.actValY]

        if self.actAxe == 1:
            
            self.ax = self.fig.add_subplot(1,1,1)
            self.ax.set_title("{}".format( self.axes[self.actAxe]), fontsize=14)
            self.ax.grid(True)
            self.ax.set_xlabel( self.getDataLabel(valX) )
            self.ax.set_ylabel( self.getDataLabel(valY) )
            
            sctr = self.ax.scatter( x=X, y=Y, c=U, cmap='RdYlBu_r')
            self.fig.colorbar(sctr, ax=self.ax)
            
        elif self.actAxe == 2:
            
            self.ax = self.fig.add_subplot(1,1,1)
            self.ax.set_title("Amplitude's phase in <0, 2Pi>", fontsize=14)
            self.ax.grid(True)
            self.ax.set_xlabel( self.getDataLabel(valX) )
            self.ax.set_ylabel( self.getDataLabel(valY) )
            self.ax.quiver( X, Y, U, V )
            
        elif self.actAxe == 3:
            
            self.ax = self.fig.add_subplot(1,1,1, projection='3d')
            self.ax.set_title("Phi angle as phi = omega*t - abs(k*r) in [rad]", fontsize=14)
            self.ax.grid(True)
            self.ax.set_xlabel( self.getDataLabel(valX) )
            self.ax.set_ylabel( self.getDataLabel(valY) )
            
            # Reduction z-axis 
            a = U.min()
            b = U.max()
            
            if abs(a) > abs(b): 
                vMax = a * _SC_RED
                vMin = b
            else              : 
                vMax = b * _SC_RED
                vMin = a
                
            if a * b > 0: vMin = vMin / _SC_RED
            else        : vMin = vMin * _SC_RED
                
            self.ax.set_zlim(vMin, vMax)
            
            surf = self.ax.plot_trisurf( X, Y, U, linewidth=0.2, cmap='RdYlBu_r', antialiased=False)
            self.fig.colorbar(surf, ax=self.ax)
        
        # Vykreslenie noveho grafu
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
    def onButValU(self):
        "Resolve radio buttons selection for active U Value in plot"
        
        self.actValU = self.butValMapU.get() # get integer value for selected button
        self.show()
    
    #--------------------------------------------------------------------------
    def onButValV(self):
        "Resolve radio buttons selection for active V Value in plot"
        
        self.actValV = self.butValMapV.get() # get integer value for selected button
        self.show()
    
    #--------------------------------------------------------------------------
    def onSlider(self, new_val):
        "Resolve change of Slider"

        self.sVal = self.sldS.get()
        self.show()
    
    #--------------------------------------------------------------------------
    def on_click(self, event):
        "Print information about mouse-given position"
        
        if event.inaxes is not None:
            
            x = float(event.xdata)
            y = float(event.ydata)

            # Ziskanie nastavenia grafu
            valX = self.values[self.actValX]
            valY = self.values[self.actValY]
            valS = self.values[self.actValS]
            
            x = x                                  / self.meta[valX]['coeff']
            y = y                                  / self.meta[valY]['coeff']
            s = self.getValByGrid(self.sVal, valS) / self.meta[valS]['coeff']
            
            pos = {'x':0, 'y':0, 'z':0, 't':0}
            pos[valX] = x
            pos[valY] = y
            pos[valS] = s
            
            id = self.space3M.getIdFromPos(pos)
            self.space3M.printCell(id)
            
        else:
            print('Clicked ouside axes bounds but inside plot window')
    
    #--------------------------------------------------------------------------

#------------------------------------------------------------------------------
print('Minkowski space class GUI ver 0.34')
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
