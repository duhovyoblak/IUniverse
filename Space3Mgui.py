#==============================================================================
# Minkowski space class GUI
#------------------------------------------------------------------------------
#
#    real position is given in meters for x,z,y and microsecenods for t as real values
#    grid position means position in numpy-like 4D array as integers 0..ix, 0..iy, 0..iz, 0..it
#
#    phi means argument (omega*t - k*x) as real value in radians
#    phs means phi mod 2*PI in radians
#
#------------------------------------------------------------------------------
from siqo_lib import journal

import tkinter as tk
import numpy   as np

from matplotlib.figure                 import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    def __init__(self, title):
        "Create and show GUI for Minkowski space"
        
        # Create output window
        win = tk.Tk()
        win.title(title)
        win.geometry('1280x1000')
        win.resizable(False,False)
        win.update()
        self.w = win.winfo_width()
        self.h = win.winfo_height()
        
        #----------------------------------------------------------------------
        # Create layout

        self.fig = Figure(figsize=(self.w*0.78/100, self.h*0.6/100), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=win)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=self.w*0.0, y=self.h*0.01)
        
        self.fig.canvas.callbacks.connect('button_press_event', self.on_click)

        #----------------------------------------------------------------------
        # Radio buttons setup
        
        self.param_map_var = tk.IntVar()
        
        self.but1 = tk.Radiobutton(win, text='pm_text 1', variable=self.param_map_var, value=1, command=self.buttonCmd)
        self.but1.place(x=self.w * 0.05, y = self.h * (0.65 + 3 * 0.03))

        self.but2 = tk.Radiobutton(win, text='pm_text 2', variable=self.param_map_var, value=2, command=self.buttonCmd)
        self.but2.place(x=self.w * 0.05, y = self.h * (0.65 + 4 * 0.03))

        self.but1.select()
        
        #----------------------------------------------------------------------
        # Sliders setup
        
        self.g = 9.8
        self.g_slider = tk.Scale(win, from_=0.0, to=20.0, resolution=0.1, orient=tk.HORIZONTAL, length=self.w*0.4, command=self.updateG, label="g")
        self.g_slider.place(x=self.w * 0.5, y=self.h * 0.9)
        self.g_slider.set(9.8)
        
        #----------------------------------------------------------------------
        # Initialisation
        
        self.showSpace3M()   # Initial drawing
        win.mainloop()       # Start listening for events

    #--------------------------------------------------------------------------
    def showSpace3M(self):
        "Show Minkovski space according to given parameters"

        print(self.g)
        
        self.ax.clear()
        self.ax.set_xlabel('x_lab')
        self.ax.set_ylabel('y_lab')
                
        self.fig.tight_layout()
        self.canvas.draw()
    
    #--------------------------------------------------------------------------
    def updateG(self, new_val=1.0):
        "Change value of and show Minkowski space"
        #This method is called whenever the user moves any slider
        print('new val', new_val)
        
        self.g   = new_val  # same as self.g_slider.get()
        self.showSpace3M()
    
    #--------------------------------------------------------------------------
    def on_click(self, event):
        "Print information about mouse-given position"
        
        if event.inaxes is not None:
            print(event.xdata, event.ydata)
        else:
            print('Clicked ouside axes bounds but inside plot window')
    
    #--------------------------------------------------------------------------
    def buttonCmd(self):
        "Resolve radio buttons selection"
        
        i = self.param_map_var.get() # get integer value for selected button
        print('button_cmd', i)
    
    #--------------------------------------------------------------------------

#------------------------------------------------------------------------------
if __name__ =='__main__':   
    
    gui = Space3Mgui('Minkowski space class GUI')
    
#------------------------------------------------------------------------------
print('Minkowski space class GUI ver 0.10')
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
