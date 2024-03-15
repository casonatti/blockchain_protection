# import gi
# gi.require_version('Gtk', '3.0')
# from gi.repository import Gtk

# from matplotlib.backends.backend_gtk3agg import (
#     FigureCanvasGTK3Agg as FigureCanvas)
# from matplotlib.figure import Figure
# import numpy as np

# win = Gtk.Window()
# win.connect("delete-event", Gtk.main_quit)
# win.set_default_size(400, 300)
# win.set_title("Embedding in GTK")

# f = Figure(figsize=(5, 4), dpi=100)
# a = f.add_subplot(111)
# t = np.arange(0.0, 3.0, 0.01)
# s = np.sin(2*np.pi*t)
# a.plot(t, s)

# sw = Gtk.ScrolledWindow()
# win.add(sw)
# # A scrolled window border goes outside the scrollbars and viewport
# sw.set_border_width(10)

# canvas = FigureCanvas(f)  # a Gtk.DrawingArea
# canvas.set_size_request(800, 600)
# sw.add_with_viewport(canvas)

# win.show_all()
# Gtk.main()

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

class GraphWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Graph with PyGTK3 and Matplotlib")
        self.set_default_size(800, 600)

        # Create a Gtk.Paned widget
        self.paned = Gtk.Paned()
        self.add(self.paned)

        # Create Matplotlib Figure and Axes
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.plot([1, 2, 3, 4], [10, 20, 25, 30], linestyle='-')

        # Create a canvas to display the Matplotlib plot
        self.canvas = FigureCanvas(self.figure)
        self.paned.add1(self.canvas)

        # Create a label for the title
        self.title_label = Gtk.Label(label="Graph Title")
        self.title_label.set_halign(Gtk.Align.CENTER)
        self.paned.add2(self.title_label)

        # Set the position of the separator
        self.paned.set_position(400)

win = GraphWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()