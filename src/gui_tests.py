#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class TextView(Gtk.TextView):
  def __init__(self):
    Gtk.TextView.__init__(self)
    # create mark for scrolling
    text_buffer = self.get_buffer()
    text_iter_end = text_buffer.get_end_iter()
    self.text_mark_end = text_buffer.create_mark("", text_iter_end, False)

  def append_text(self, text):
    # append text
    text_buffer = self.get_buffer()
    text_iter_end = text_buffer.get_end_iter()
    text_buffer.insert(text_iter_end, text)
    # now scroll using mark
    self.scroll_to_mark(self.text_mark_end, 0, False, 0, 0)

class Window(Gtk.Window):
  def __init__(self):
    Gtk.Window.__init__(self)
    self.set_title('Test GtkTextView scrolling')
    self.set_default_size(400, 300)

    self.grid = Gtk.Grid()
    self.scrolled_win = Gtk.ScrolledWindow()
    self.text_view = TextView()
    self.button = Gtk.Button(label='Append text')
    self.scrolled_win.set_hexpand(True)
    self.scrolled_win.set_vexpand(True)

    self.scrolled_win.add(self.text_view)
    self.grid.add(self.scrolled_win)
    self.grid.add(self.button)
    self.add(self.grid)

    self.connect('destroy', Gtk.main_quit)
    self.button.connect('clicked', self.on_button_clicked)
    self.show_all()

  def on_button_clicked(self, widget):
    self.text_view.append_text('Hello\n' * 5);

if __name__ == '__main__':
  win = Window()
  Gtk.main()