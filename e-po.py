import configparser
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio, Pango

# Declare ConfigParser, read the configuration file into memory:
config = configparser.ConfigParser()
config.read('e-po_config.ini')

class OperationsWindow(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title = config.get('GUI-INTERFACE', 'window_title'))

        # Read the parameters from config and set the form properties:
        self.set_default_size(config.getint('GUI-INTERFACE','window_width'), config.getint('GUI-INTERFACE', 'window_height'))
        self.set_border_width(config.getint('GUI-INTERFACE', 'window_border_width'))
        self.set_resizable(config.getboolean('GUI-INTERFACE', 'window_resizable'))

        # Set up the HeaderBar:
        self.HeaderBar = Gtk.HeaderBar()
        self.HeaderBar.set_show_close_button(True)
        self.HeaderBar.set_title(self.get_title())
        self.set_titlebar(self.HeaderBar)
        self.HeaderBar.show()

window = OperationsWindow()
window.connect("delete-event", Gtk.main_quit)
window.show()
Gtk.main()