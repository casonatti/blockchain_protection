import gi
import os
from Log import *
from scylla import *
import subprocess
import threading
import time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas

# Global Var
clef_gpid = 0
textview_buffer = []
log = Log()
prot_files = []

with open("../evaluation/config/protected_inodes.txt","r") as file:
  for line in file.readlines():
    temp = line.split()
    prot_files.append([int(temp[0]), temp[1]])

file.close()

class ScyllaGUI(Gtk.Window):
  def __init__(self):
    super().__init__(title="Scylla")

    global clef_gpid
    global textview_buffer

    # Main Window config
    self.set_border_width(5)
    self.set_default_size(1280, 720)
    super().connect("destroy", Gtk.main_quit)

    # Elements declaration
    hpaned = Gtk.Paned()
    vpaned_status = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
    vpaned_prot_files = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
    vpaned_info = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)

    grid_prot_files = Gtk.Grid()
    grid_btn = Gtk.Grid()

    self.prot_files_list = Gtk.ListStore(bool, int, str)

    self.prot_files_treeview = Gtk.TreeView(model=self.prot_files_list)

    self.scrollable_treelist = Gtk.ScrolledWindow()

    notebook = Gtk.Notebook()

    log_page = Gtk.ScrolledWindow()
    self.log_buffer = Gtk.TextBuffer()
    self.log_textview = Gtk.TextView(buffer=self.log_buffer)

    graph_page = Gtk.Box()

    status_vbox = Gtk.Box(orientation="vertical")
    prot_files_vbox = Gtk.Box(orientation="vertical")
    self.switch = Gtk.Switch()
    self.add_file_btn = Gtk.Button(label="Add")
    self.remove_file_btn = Gtk.Button(label="Remove")

    # Setting parameters
    hpaned.set_position(320)
    vpaned_status.set_position(80)
    vpaned_prot_files.set_position(120)
    vpaned_info.set_position(650)

    prot_files_vbox.set_spacing(10)
    prot_files_vbox.set_margin_top(5)

    grid_prot_files.set_column_homogeneous(True)
    grid_prot_files.set_row_homogeneous(True)
    grid_btn.set_column_homogeneous(True)
    grid_btn.set_margin_right(5)

    self.scrollable_treelist.set_vexpand(True)

    if len(prot_files) == 0:
      self.switch.set_sensitive(False)

    self.switch.connect("notify::active", self.on_switch_activated)
    self.switch.set_active(False)
    self.switch.set_halign(3)
    self.switch.set_margin_bottom(10)

    self.add_file_btn.connect("clicked", self.add_files)
    self.remove_file_btn.connect("clicked", self.remove_files)

    log_page.set_border_width(5)

    self.log_textview.set_editable(False)
    self.log_textview.set_cursor_visible(False)
    self.log_textview.set_wrap_mode(Gtk.WrapMode.WORD)

    self.log_buffer_line_limit = 200

    # Adding elements
    hpaned.pack1(vpaned_status, False, False)
    hpaned.pack2(vpaned_info, True, False)

    for item in prot_files:
      self.prot_files_list.append([False] + list(item))

    for i, column_title in enumerate([None, "Inode", "File Name"]):
      if column_title == None:
        toggle_renderer = Gtk.CellRendererToggle()
        tvcolumn = Gtk.TreeViewColumn(column_title, toggle_renderer, active=i)
        toggle_renderer.connect("toggled", self.on_button_toggled)
      else:
        text_renderer = Gtk.CellRendererText()
        tvcolumn = Gtk.TreeViewColumn(column_title, text_renderer, text=i)
      self.prot_files_treeview.append_column(tvcolumn)

    self.scrollable_treelist.add(self.prot_files_treeview)

    grid_prot_files.attach(self.scrollable_treelist, 0, 0, 8, 10)
    
    grid_btn.add(self.add_file_btn)
    grid_btn.attach(self.remove_file_btn, 1, 0, 1, 1)

    label = Gtk.Label(label="Scylla Status")
    status_vbox.pack_start(label, True, True, 1)
    status_vbox.pack_start(self.switch, False, False, 1)
    vpaned_status.pack1(status_vbox, False, False)

    label = Gtk.Label(label=f"Clef PID:\n{clef_gpid}")
    vpaned_prot_files.pack1(label, False, False)

    label = Gtk.Label(label="Protected Files")
    prot_files_vbox.pack_start(label, False, False, 1)
    prot_files_vbox.pack_start(grid_prot_files, True, True, 1)
    prot_files_vbox.pack_end(grid_btn, False, False, 1)
    
    vpaned_prot_files.pack2(prot_files_vbox, False, False)

    vpaned_status.pack2(vpaned_prot_files, True, True)

    log_page.add(self.log_textview)

    canvas = self.plot_graph()

    graph_page.pack_start(canvas, True, True, 1)

    notebook.append_page(log_page, Gtk.Label(label="Log"))
    notebook.append_page(graph_page, Gtk.Label(label="Graphs"))

    vpaned_info.add1(notebook)

    label = Gtk.Label(label='Warnings')
    vpaned_info.add2(label)

    self.add(hpaned)

    self.feed_log()

    self.timeout_id = GLib.timeout_add(300, self.feed_log)

    super().show_all()

  # Elements functions
  def on_switch_activated(self, switch, gparam):
    time_s = time.time()
    dt = datetime.fromtimestamp(time_s)
    log_timestamp = dt.strftime("%Y-%m-%d %H:%M")
    
    if switch.get_active():
      self.add_file_btn.set_sensitive(False)
      self.remove_file_btn.set_sensitive(False)
      self.ebpf_thr = self.turn_on_scylla()
      state = f"[{log_timestamp}] [INFO] Scylla turned ON"
    else:
      self.add_file_btn.set_sensitive(True)
      self.remove_file_btn.set_sensitive(True)
      self.turn_off_scylla()
      state = f"[{log_timestamp}] [INFO] Scylla turned OFF"

    log.append(state)

  def on_button_toggled(self, cell_renderer, path):
    iter = self.prot_files_list.get_iter(path)
    if iter:
      self.prot_files_list[iter][0] = not self.prot_files_list[iter][0]

  def add_files(self, button):
    if not self.switch.get_active():
      dialog = Gtk.FileChooserDialog(title="Select a file to protect", parent=self, action=Gtk.FileChooserAction.OPEN)
      dialog.add_buttons(
        Gtk.STOCK_CANCEL,
        Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN,
        Gtk.ResponseType.OK,
      )

      response = dialog.run()

      if response == Gtk.ResponseType.OK:
        filename = dialog.get_filename().split('/')[-1]
        inode = os.stat(dialog.get_filename()).st_ino

        repeated_inode = False

        for path in range(len(self.prot_files_list)):
          iter = self.prot_files_list.get_iter(path)
          temp = self.prot_files_list[iter][1]

          if inode != 0 and temp == inode:
            repeated_inode = True
            print("Failed to add file. Repeated Inode.")

        if not repeated_inode:
          time_s = time.time()
          dt = datetime.fromtimestamp(time_s)
          log_timestamp = dt.strftime("%Y-%m-%d %H:%M")

          with open("../evaluation/config/protected_inodes.txt","a") as file:
            text = str(inode) + ' ' + filename + '\n'
            file.write(text)
          file.close()
          self.prot_files_list.append([False, inode, filename])
          log_message = f"[{log_timestamp}] [INFO] Adding file [{filename}] to the list."
          log.append(log_message)

      if len(self.prot_files_list) != 0:
        self.switch.set_sensitive(True)

      dialog.destroy()

  def remove_files(self, button):
    for path in reversed(range(len(self.prot_files_list))):
      iter = self.prot_files_list.get_iter(path)

      if self.prot_files_list[iter][0]:
        temp_inode = self.prot_files_list[iter][1]
        temp_name = self.prot_files_list[iter][2]
        self.prot_files_list.remove(iter)

        text = str(temp_inode) + ' ' + str(temp_name) + '\n'

        time_s = time.time()
        dt = datetime.fromtimestamp(time_s)
        log_timestamp = dt.strftime("%Y-%m-%d %H:%M")
        
        with open("../evaluation/config/protected_inodes.txt","r+") as file:
          lines = file.readlines()
          file.seek(0)
          for line in lines:
            if line != text:
              file.write(line)
          file.truncate()
          file.close()

        log_message = f"[{log_timestamp}] [INFO] Removed file [{str(temp_name)}] from the list."
        log.append(log_message)

    if len(self.prot_files_list) == 0:
      self.switch.set_sensitive(False)

  def feed_log(self):
    while len(textview_buffer) > 0:
      iter_end = self.log_buffer.get_end_iter()
      self.log_buffer.insert(iter_end, textview_buffer[0])
      textview_buffer.pop(0)

      line_count = self.log_buffer.get_line_count()

      if line_count >= self.log_buffer_line_limit:
        iter_start = self.log_buffer.get_start_iter()
        self.log_buffer.delete(iter_start, self.log_buffer.get_iter_at_line(line_count - self.log_buffer_line_limit))
      
      GLib.idle_add(self.scroll_to_end)

    return True

  def scroll_to_end(self):
    self.log_textview.scroll_to_mark(self.log_buffer.get_insert(), 0, False, 0, 0)
    
    return False    

  def plot_graph(self):
    figure = Figure(figsize=(5, 4), dpi=100)
    ax = figure.add_subplot(111)
    ax.plot([1, 2, 3, 4], [10, 20, 25, 30], linestyle="-")

    canvas = FigureCanvas(figure)

    return canvas
  
  def turn_on_scylla(self):
    self.ebpf_prog = Scylla(log)

    ebpf_thread = threading.Thread(target=self.ebpf_prog.run, name="Scylla_Thread", daemon=True)

    ebpf_thread.start()

    return ebpf_thread
  
  def turn_off_scylla(self):
    self.ebpf_prog.close()

    self.ebpf_thr.join()

    return True
    
def get_clef_gpid():
  global clef_gpid
  try:
    clef_gpid_search = subprocess.run(["ps", "-e", "-o", "pid,comm"], stdout=subprocess.PIPE, text=True, check=True) # Run the ps command to get information about processes with the specified command name
    lines = clef_gpid_search.stdout.strip().split('\n')
    clef_gpid = [int(line.split()[0]) for line in lines[1:] if line.split()[-1] == 'clef'] # Split the output into lines and extract the PIDs for the specified program name
    with open('../evaluation/config/permitted_pids.txt', 'w') as file:
      file.write(str(clef_gpid[0]))
  except subprocess.CalledProcessError:
    print(f"Error retrieving PIDs for 'clef'.")
    exit()
  
def main():
  global textview_buffer

  get_clef_gpid()

  log.config_initialization(textview_buffer)

  threads = []

  reading_thread = threading.Thread(target=log.read_log_file, args=(textview_buffer,), name="Reading_Thread", daemon=True)
  threads.append(reading_thread)

  writing_thread = threading.Thread(target=log.write_log_file, name="Writing_Thread", daemon=True)
  threads.append(writing_thread)

  for thread in threads:
    thread.start()

  time.sleep(1)

  ScyllaGUI()

  Gtk.main()

  # for thread in threads:
  #   thread.join()
  
  return 0

if __name__ == '__main__':
  main()