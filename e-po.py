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
        self.btn_start = Gtk.Button()
        icon = Gio.ThemedIcon(name = config.get('GUI-INTERFACE','btn_start_icon'))
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        image.show()
        self.btn_start.add(image)
        self.HeaderBar.pack_start(self.btn_start) 
        self.btn_start.show()
 
        ## Configure the Stop button:
        self.btn_stop = Gtk.Button()
        icon = Gio.ThemedIcon(name = config.get('GUI-INTERFACE','btn_stop_icon'))
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        image.show()
        self.btn_stop.add(image)
        self.btn_stop.set_sensitive(False)
        self.HeaderBar.pack_start(self.btn_stop) 
        self.btn_stop.show()
        
        ## Configure the Settigns button:
        self.btn_settings = Gtk.Button()
        icon = Gio.ThemedIcon(name = config.get('GUI-INTERFACE','btn_settings_icon'))
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        image.show()
        self.btn_settings.add(image)
        self.HeaderBar.pack_end(self.btn_settings) 
        self.btn_settings.show()       

        ## Add main OperationsWindow container and controls
        
        self.mainContainer = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.add(self.mainContainer)
        self.mainContainer.show()
        
        self.timerContainer = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.mainContainer.pack_start(self.timerContainer, True, True, 0)
        self.timerContainer.show()
        
        self.lbl_Time = Gtk.Label(label = config.get('TIMER','focus-period-mins') + ":" + "00")
        self.lbl_Time.set_use_markup(True)
        self.lbl_Time.modify_font(Pango.FontDescription(config.get('DISPLAY','timer_font_size')))
        self.timerContainer.pack_start(self.lbl_Time, True, True, 0)
        self.lbl_Time.show()
        
        self.periodCounter = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        lbl_counter_legend = Gtk.Label(label = "Periods until big break:", xalign = 0)
        lbl_counter_number = Gtk.Label(label = config.get('TIMER','rests-before-break'))
        self.periodCounter.pack_start(lbl_counter_legend, False, True, 3)
        self.periodCounter.pack_end(lbl_counter_number, False, True, 3)
        self.mainContainer.pack_start(self.periodCounter, False, True, 10)
        self.periodCounter.show_all()
        
        self.optionsContainer = Gtk.ListBox()
        self.optionsContainer.set_selection_mode(Gtk.SelectionMode.NONE)
        
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        row.add(hbox)
        period_name_1 = Gtk.Label(label = "Work & Focus time", xalign = 0)
        period_time_1 = Gtk.Label(label = config.get('TIMER','focus-period-mins'))
        period_selector_1 = Gtk.Switch()
        period_selector_1.set_active(True)
        hbox.pack_start(period_name_1, True, True, 3)
        hbox.pack_start(period_time_1, False, True, 15)
        hbox.pack_end(period_selector_1, False, True, 3)
        self.optionsContainer.add(row)
    
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        row.add(hbox)
        period_name_2 = Gtk.Label(label = "Short break", xalign = 0)
        period_time_2 = Gtk.Label(label = config.get('TIMER','break-period-mins'))
        period_selector_2 = Gtk.Switch()
        period_selector_2.set_active(False)
        hbox.pack_start(period_name_2, True, True, 3)
        hbox.pack_start(period_time_2, False, True, 15)
        hbox.pack_end(period_selector_2, False, True, 3)
        self.optionsContainer.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        row.add(hbox)
        period_name_3 = Gtk.Label(label = "Rest period", xalign = 0)
        period_time_3 = Gtk.Label(label = config.get('TIMER','rest-period-mins'))
        period_selector_3 = Gtk.Switch()
        period_selector_3.set_active(False)
        hbox.pack_start(period_name_3, True, True, 3)
        hbox.pack_start(period_time_3, False, True, 15)
        hbox.pack_end(period_selector_3, False, True, 3)
        self.optionsContainer.add(row)
        
        self.mainContainer.pack_end(self.optionsContainer, False, True, 0)
        self.optionsContainer.show_all()
        

window = OperationsWindow()
window.connect("delete-event", Gtk.main_quit)
window.show()
Gtk.main()