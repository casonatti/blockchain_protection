import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# list of tuples for each software, containing the software name, initial release, and main programming languages used
software_list = [
    ("","Firefox", 2002),
    ("","Eclipse", 2004),
    ("","Pitivi", 2004),
    ("","Netbeans", 1996),
    ("","Chrome", 2008),
    ("","Filezilla", 2001),
    ("","Bazaar", 2005),
    ("","Git", 2005),
    ("","Linux Kernel", 1991),
    ("","GCC", 1987),
    ("","Frostwire", 2004),
]


class TreeViewFilterWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Treeview Filter Demo")
        self.set_border_width(10)
        self.set_default_size(500,500)

        # Setting up the self.grid in which the elements are to be positioned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        # Creating the ListStore model
        self.software_liststore = Gtk.ListStore(str, str, int)
        for software_ref in software_list:
            self.software_liststore.append(list(software_ref))

        # creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView(model=self.software_liststore)

        for i, column_title in enumerate(
            [None,"Software", "Release Year"]
        ):
            renderer = Gtk.CellRendererText()
            self.cell = Gtk.CellRendererToggle()
            self.tvcolumn = Gtk.TreeViewColumn(column_title, renderer, text=i)
            if column_title == None:
                self.tvcolumn.pack_start(self.cell, True)
            self.treeview.append_column(self.tvcolumn)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        
        self.scrollable_treelist.add(self.treeview)

        self.show_all()

    def on_selection_button_clicked(self, widget):
        """Called on any of the button clicks"""
        # we set the current language filter to the button's label
        self.current_filter_language = widget.get_label()
        print("%s language selected!" % self.current_filter_language)
        # we update the filter, which updates in turn the view
        self.language_filter.refilter()


win = TreeViewFilterWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()