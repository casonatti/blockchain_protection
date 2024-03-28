import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class ScrollingTextView:
    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_title("Scrolling Text View Example")
        self.window.set_default_size(300, 250)
        self.window.connect("destroy", Gtk.main_quit)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        self.textview.set_border_width(5)

        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.add(self.textview)

        self.button = Gtk.Button(label="Insert 5 Lines")
        self.button.connect("clicked", self.on_button_clicked)

        self.vbox = Gtk.VBox(spacing=6)
        self.vbox.pack_start(self.scrolled_window, True, True, 0)
        self.vbox.pack_start(self.button, False, False, 0)

        self.window.add(self.vbox)
        self.window.show_all()

        self.buffer = self.textview.get_buffer()
        self.buffer.connect("insert-text", self.on_text_inserted)

        self.line_counter = 0

    def on_text_inserted(self, buffer, iter, text, length):
        self.line_counter += 1
        GLib.idle_add(self.scroll_to_end)
        GLib.idle_add(self.delete_excess_lines)

    def on_button_clicked(self, button):
        lines_to_insert = 5
        for i in range(lines_to_insert):
            self.line_counter += 1
            line_text = f"Line {self.line_counter}\n"
            self.buffer.insert_at_cursor(line_text)

    def scroll_to_end(self):
        # Scroll to the end of the buffer
        self.textview.scroll_to_mark(self.buffer.get_insert(), 0.0, True, 0.0, 1.0)
        return False

    def delete_excess_lines(self):
        start_iter = self.buffer.get_start_iter()
        end_iter = self.buffer.get_end_iter()
        line_count = self.buffer.get_line_count()
        if line_count > 20:
            self.buffer.delete(start_iter, self.buffer.get_iter_at_line(line_count - 20))
        return False

if __name__ == "__main__":
    scrolling_text_view = ScrollingTextView()
    Gtk.main()
