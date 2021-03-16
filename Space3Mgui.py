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

from matplotlib.figure                 import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk

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

        self.fig = Figure(figsize=(self.w*0.9/100, self.h*0.8/100), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=win)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=self.w*0.0, y=self.h*0.0)
        
        self.fig.canvas.callbacks.connect('button_press_event', self.on_click)

        #----------------------------------------------------------------------
        # Radio buttons setup
        
        self.param_map_var = tk.IntVar()
        
        self.but1 = tk.Radiobutton(win, text='pm_text 1', variable=self.param_map_var, value=1, command=self.on_button)
        self.but1.place(x=self.w * 0.91, y = self.h * (0.1 + 3 * 0.03))

        self.but2 = tk.Radiobutton(win, text='pm_text 2', variable=self.param_map_var, value=2, command=self.on_button)
        self.but2.place(x=self.w * 0.91, y = self.h * (0.1 + 4 * 0.03))

        self.but1.select()
        
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
    # Tools for setting
    #--------------------------------------------------------------------------
    
    #==========================================================================
    # Private methods
    #--------------------------------------------------------------------------
    def show(self):
        "Show Minkovski space according to given parameters"

        print(self.g)
        
        self.ax.clear()
        self.ax.set_xlabel('$x$ [meter]')
        self.ax.set_ylabel('$t$ [nanosecond]')
        
        data = self.space3M.getPlotData()
        
        self.ax.quiver(data['x'], data['t'], data['x'], data['t'])

                
        self.fig.tight_layout()
        self.canvas.draw()
    
    #--------------------------------------------------------------------------
    def on_gSlider(self, new_val=1.0):
        "Resolve change of g-Slider"

        print('new val', new_val)
        
        self.g   = new_val  # same as self.g_slider.get()
        self.show()
    
    #--------------------------------------------------------------------------
    def on_click(self, event):
        "Print information about mouse-given position"
        
        if event.inaxes is not None:
            print(event.xdata, event.ydata)
        else:
            print('Clicked ouside axes bounds but inside plot window')
    
    #--------------------------------------------------------------------------
    def on_button(self):
        "Resolve radio buttons selection"
        
        i = self.param_map_var.get() # get integer value for selected button
        print('button_cmd', i)
    
    #--------------------------------------------------------------------------

#------------------------------------------------------------------------------
print('Minkowski space class GUI ver 0.10')
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
