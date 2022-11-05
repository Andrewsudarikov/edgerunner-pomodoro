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

        # Set up the HeaderBar controls:
        
        ## Configure the Start button:
        self.btnStart = Gtk.Button()
        icon = Gio.ThemedIcon(name = config.get('GUI-INTERFACE','btnStart_icon'))
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        image.show()
        self.btnStart.add(image)
        self.HeaderBar.pack_start(self.btnStart) 
        self.btnStart.show()
 
         ## Configure the Stop button:
        self.btnStop = Gtk.Button()
        icon = Gio.ThemedIcon(name = config.get('GUI-INTERFACE','btnStop_icon'))
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        image.show()
        self.btnStop.add(image)
        self.btnStop.set_sensitive(False)
        self.HeaderBar.pack_start(self.btnStop) 
        self.btnStop.show()
        
        ## Configure the Settigns button:
        self.btnSettngs = Gtk.Button()
        icon = Gio.ThemedIcon(name = config.get('GUI-INTERFACE','btnSettings_icon'))
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        image.show()
        self.btnSettngs.add(image)
        self.HeaderBar.pack_end(self.btnSettngs) 
        self.btnSettngs.show()       

window = OperationsWindow()
window.connect("delete-event", Gtk.main_quit)
window.show()
Gtk.main()