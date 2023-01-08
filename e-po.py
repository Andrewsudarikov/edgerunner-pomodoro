from ast import If
import configparser
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gio, Pango
import time
import threading

# Declare ConfigParser, read the configuration file into memory:
config = configparser.ConfigParser()
config.read('e-po_config.ini')


# Declare global variables

## The "Period" variable reads the config value for the first countdown period 
## from the configuration file.

global Period
Period = config.getint('TIMER', 'focus-period')

## The "BreakNumber" variable shows how many short break periods are left before the long one.

global BreakNumber
BreakNumber = config.getint('TIMER','rests-before-break')

## The "PauseBuffer" variable will be used to store the remaining number of seconds 
## in the current period after the Pause button is clicked.

global PauseBuffer
PauseBuffer = 0

## The "StopDeliberate" variable will help detect if the end of the period was natural (the time has run out) 
## or deliberate (the user clicked the Sopt button).

global StopDeliberate
StopDeliberate = False


class OperationsWindow(Gtk.Window):


    def __init__(self):

        global Period, BreakNumber

        # Set timer handles
        self.timer = None
        self.event = None

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
        self.btnStart.connect("clicked", self.btnStart_clicked)
        self.btnStart.show()
        
        ## Configure the Pause button
        self.btnPause = Gtk.Button()
        icon = Gio.ThemedIcon(name = config.get('GUI-INTERFACE','btnPause_icon'))
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        image.show()
        self.btnPause.add(image)
        self.HeaderBar.pack_start(self.btnPause)
        self.btnPause.connect("clicked", self.btnPause_clicked)
 
        ## Configure the Stop button:
        self.btnStop = Gtk.Button()
        icon = Gio.ThemedIcon(name = config.get('GUI-INTERFACE','btnStop_icon'))
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        image.show()
        self.btnStop.add(image)
        self.btnStop.set_sensitive(False)
        self.HeaderBar.pack_start(self.btnStop)
        self.btnStop.connect("clicked", self.btnStop_clicked)
        self.btnStop.show()
        
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
        
        mins, secs = divmod(Period, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        self.lbl_Time = Gtk.Label(label = str(timer))

        self.lbl_Time.set_use_markup(True)
        self.lbl_Time.modify_font(Pango.FontDescription(config.get('DISPLAY','timer_font_size')))
        self.timerContainer.pack_start(self.lbl_Time, True, True, 0)
        self.lbl_Time.show()
        
        self.periodCounter = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.lbl_counter_legend = Gtk.Label(label = "Periods until big break:", xalign = 0)
        self.lbl_counter_number = Gtk.Label(label = str(BreakNumber))
        self.periodCounter.pack_start(self.lbl_counter_legend, False, True, 3)
        self.periodCounter.pack_end(self.lbl_counter_number, False, True, 3)
        self.mainContainer.pack_start(self.periodCounter, False, True, 10)
        self.periodCounter.show_all()
        
        self.optionsContainer = Gtk.ListBox()
        self.optionsContainer.set_selection_mode(Gtk.SelectionMode.NONE)
        
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        row.add(hbox)
        self.period_name_1 = Gtk.Label(label = "Work & Focus time", xalign = 0)
        self.period_time_1 = Gtk.Label(label = str(config.getint('TIMER','focus-period') // 60) + " min.")
        self.period_selector_1 = Gtk.Switch()
        self.period_selector_1.set_active(True)
        hbox.pack_start(self.period_name_1, True, True, 3)
        hbox.pack_start(self.period_time_1, False, True, 15)
        hbox.pack_end(self.period_selector_1, False, True, 3)
        self.optionsContainer.add(row)
    
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        row.add(hbox)
        self.period_name_2 = Gtk.Label(label = "Short break", xalign = 0)
        self.period_time_2 = Gtk.Label(label = str(config.getint('TIMER','break-period') // 60) + " min.")
        self.period_selector_2 = Gtk.Switch()
        self.period_selector_2.set_active(False)
        hbox.pack_start(self.period_name_2, True, True, 3)
        hbox.pack_start(self.period_time_2, False, True, 15)
        hbox.pack_end(self.period_selector_2, False, True, 3)
        self.optionsContainer.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        row.add(hbox)
        self.period_name_3 = Gtk.Label(label = "Rest period", xalign = 0)
        self.period_time_3 = Gtk.Label(label = str(config.getint('TIMER','rest-period') // 60) + " min.")
        self.period_selector_3 = Gtk.Switch()
        self.period_selector_3.set_active(False)
        hbox.pack_start(self.period_name_3, True, True, 3)
        hbox.pack_start(self.period_time_3, False, True, 15)
        hbox.pack_end(self.period_selector_3, False, True, 3)
        self.optionsContainer.add(row)
        
        self.mainContainer.pack_end(self.optionsContainer, False, True, 0)
        self.optionsContainer.show_all()

    def countdown(self):
        
        global Period, StopDeliberate, BreakNumber
        
        while(Period):
            
            mins, secs = divmod(Period, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            self.lbl_Time.set_text(str(timer))
            Period -= 1
            StopDeliberate = False
            time.sleep(1)

        else:

            if StopDeliberate == False:

                if config.getboolean('TIMER', 'focus-period_select') == True:

                    if BreakNumber > 1:

                        config.set('TIMER', 'focus-period_select', 'False')
                        self.period_selector_1.set_active(False)

                        config.set('TIMER', 'break-period_select', 'True')
                        self.period_selector_2.set_active(True)

                        config.set('TIMER', 'rest-period_select', 'False')
                        self.period_selector_3.set_active(False)

                        BreakNumber -= 1
                        self.lbl_counter_number.set_text(str(BreakNumber))
                        print('Short breaks left before long one: ' + str(BreakNumber))

                        Period = config.getint('TIMER', 'break-period')

                        print('Automatic timer sequence start: short pause.')

                    if BreakNumber == 1:

                        config.set('TIMER', 'focus-period_select', 'False')
                        self.period_selector_1.set_active(False)

                        config.set('TIMER', 'break-period_select', 'True')
                        self.period_selector_2.set_active(True)

                        config.set('TIMER', 'rest-period_select', 'False')
                        self.period_selector_3.set_active(False)                        

                        BreakNumber -= 1
                        self.lbl_counter_number.set_text("Rest period next")
                        print('Short breaks left before long one: ' + str(BreakNumber))                    

                    self.timer = threading.Thread(target=self.countdown)
                    self.event = threading.Event()
                    self.timer.daemon=True
                    self.timer.start()

                #if config.getboolean('TIMER', 'break-period_select') == True and config.getboolean('TIMER', 'focus-period_select',) == False:

                    #config.set('TIMER', 'focus-period_select', 'True')
                    #self.period_selector_1.set_active(True)

                    #config.set('TIMER', 'break-period_select', 'False')
                    #self.period_selector_2.set_active(False)

                    #config.set('TIMER', 'rest-period_select', 'False')
                    #self.period_selector_3.set_active(False)

                    #Period = config.getint('TIMER', 'focus-period')

                    #print('Automatic timer sequence start: focus period.')  

                    #self.timer = threading.Thread(target=self.countdown)
                    #self.event = threading.Event()
                    #self.timer.daemon=True
                    #self.timer.start()

            with open('e-po_config.ini', 'w') as ConfigFile:
                config.write(ConfigFile)


    def btnStart_clicked(self,btnStart):

        global Period

        if config.getboolean('TIMER', 'focus-period_select') == True and config.getboolean('TIMER', 'pause-trigger') == False:
            Period = config.getint('TIMER', 'focus-period')

        elif config.getboolean('TIMER', 'break-period_select') == True and config.getboolean('TIMER', 'pause-trigger') == False:
            Period = config.getint('TIMER', 'break-period')

        elif config.getboolean('TIMER', 'rest-period_select') == True and config.getboolean('TIMER', 'pause-trigger') == False:
            Period = config.getint('TIMER', 'rest-period')

        else:
            Period = PauseBuffer + 1

        if config.getboolean('TIMER', 'pause-trigger') == False:
            print('start')
        else:
            print('restart after pause')

        self.timer = threading.Thread(target=self.countdown)
        self.event = threading.Event()
        self.timer.daemon=True
        self.timer.start()
        
        config.set('TIMER', 'pause-trigger', "False")
        
        self.btnStop.set_sensitive(True)
        self.btnStart.hide()
        self.btnPause.show()


    def btnPause_clicked(self,btnPause):
        
        global Period, PauseBuffer, StopDeliberate
        
        PauseBuffer = Period       
        
        print('pause; pausebuffer = ' + str(PauseBuffer))
        Period = 0
        config.set('TIMER', 'pause-trigger', "True")
        
        StopDeliberate = True

        self.btnPause.hide()
        self.btnStart.show()


    def btnStop_clicked(self,btnStop):
        
        global Period, StopDeliberate
        
        print('stop')
        Period = 0
        mins, secs = divmod(Period, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        self.lbl_Time.set_text(str(timer))
        
        config.set('TIMER', 'pause-trigger', "False")

        config.set('TIMER', 'focus-period_select', 'True')
        self.period_selector_1.set_active(True)

        config.set('TIMER', 'break-period_select', 'False')
        self.period_selector_2.set_active(False)

        config.set('TIMER', 'rest-period_select', 'False')
        self.period_selector_3.set_active(False)

        config.set('TIMER','rests-before-break', '4')

        with open('e-po_config.ini', 'w') as ConfigFile:
            config.write(ConfigFile)
        
        StopDeliberate = True

        self.btnStop.set_sensitive(False)
        
        
window = OperationsWindow()
window.connect("delete-event", Gtk.main_quit)
window.show()
Gtk.main()