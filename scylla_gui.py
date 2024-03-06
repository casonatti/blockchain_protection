import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio

class ScyllaGUI(Gtk.Window):
  def __init__(self):
      super().__init__(title="Scylla")

      # Main Window config
      self.set_border_width(10)
      self.set_default_size(1280, 720)

      # Elements declaration
      hpaned = Gtk.Paned()
      vpaned1 = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
      vpaned2 = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
      vpaned_info = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)

      grid = Gtk.Grid()

      prot_files_btn = []

      for i in range(15):
        prot_files_btn.append(Gtk.CheckButton(label=f"Teste [{i}]"))

      logs = Gtk.TextView()
      logs = logs.get_buffer()
      logs.set_text(
          "This is some text inside of a Gtk.TextView. "
          + "Select text and click one of the buttons 'bold', 'italic', "
          + "or 'underline' to modify the text accordingly."
      )

      status_vbox = Gtk.Box(orientation="vertical")
      prot_files_vbox = Gtk.Box(orientation="vertical")
      switch = Gtk.Switch()
      add_file_btn = Gtk.Button(label="Add")
      remove_file_btn = Gtk.Button(label="Remove")

      # Setting parameters
      hpaned.set_position(320)
      vpaned1.set_position(80)
      vpaned2.set_position(120)
      vpaned_info.set_position(600)

      grid.set_column_homogeneous(True)
      grid.set_margin_right(5)

      for i, cb in enumerate(prot_files_btn):
        cb.connect("toggled", self.on_button_toggled, i)

      switch.connect("notify::active", self.on_switch_activated)
      switch.set_active(False)
      switch.set_halign(3)
      switch.set_margin_bottom(10)

      add_file_btn.connect("clicked", self.add_files)
      remove_file_btn.connect("clicked", self.remove_files)

      # Adding elements
      hpaned.pack1(vpaned1, False, False)
      hpaned.pack2(vpaned_info, True, False)
      
      grid.add(add_file_btn)
      grid.attach(remove_file_btn, 1, 0, 1, 1)

      label = Gtk.Label(label='Scylla Status')
      status_vbox.pack_start(label, True, True, 1)
      status_vbox.pack_start(switch, False, False, 1)
      vpaned1.pack1(status_vbox, False, False)

      label = Gtk.Label(label='Clef PID:\nXXXX')
      vpaned2.pack1(label, True, True)

      label = Gtk.Label(label='Protected Files')
      prot_files_vbox.pack_start(label, True, True, 1)

      for cb in prot_files_btn:
        prot_files_vbox.pack_start(cb, True, True, 1)

      prot_files_vbox.pack_start(grid, True, True, 1)
      vpaned2.pack2(prot_files_vbox, True, True)

      vpaned1.pack2(vpaned2, True, True)

      label = Gtk.Label(label='Logs')
      vpaned_info.add1(label)

      label = Gtk.Label(label='Warnings')
      vpaned_info.add2(label)

      self.add(hpaned)

  # Elements functions
  def on_switch_activated(self, switch, gparam):
      if switch.get_active():
          state = "ON"
      else:
          state = "OFF"

      print("Switch was turned", state)

  def on_button_toggled(self, button, name):
    if button.get_active():
      state = "ON"
    else:
      state = "OFF"

    print("CheckBox", name, "was turned", state)

  def add_files(self, button):
      print("Adding new files to the Protected Files List")

  def remove_files(self, button):
      print("Removing files from the Protection Files List")

win = ScyllaGUI()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()