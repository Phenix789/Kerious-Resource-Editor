import gtk
import logging

from activity import KSEActivityView
from interface import KSEToolBar

WINDOWTITLE="Kerious Ressources Editor"
WINWIDTH=1024
WINHEIGHT=768
BORDERWIDTH=2

class KSEWindow:
    def __init__(self, fileName = None, debug = False):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(WINWIDTH, WINHEIGHT)
        self.window.set_title(WINDOWTITLE)
        self.window.set_border_width(BORDERWIDTH)
        self._initLogging(debug)
 
        self.mainbox = gtk.VBox(False, 0)
        self.mainbox.show()
        self.window.add(self.mainbox)
        
        self.activityView = KSEActivityView(fileName, self.window)
        self.toolbar = KSEToolBar(self.activityView)
        
        self.mainbox.pack_start(self.toolbar, False, False, 2)
        self.mainbox.pack_start(self.activityView, True, True, 0)

        self.window.connect("delete_event", self.stop)
        self.window.maximize()
        self.window.show()

    def start(self):
        gtk.main()

    def stop(self, event, data = None):
        gtk.main_quit()

    #INTERNAL

    def _initLogging(self, debug):
        self.logger = logging.getLogger("KRFEditor")
        hdlr = logging.FileHandler('/var/tmp/KRFEditor.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        hdlr.setLevel(logging.WARNING)

        if debug:
            shdlr = logging.StreamHandler()
            self.logger.addHandler(shdlr)
            if debug == "debug":
                shdlr.setLevel(logging.DEBUG)
            elif debug == "info":
                shdlr.setLevel(logging.INFO)
            elif debug == "warning":
                shdlr.setLevel(logging.WARNING)
            elif debug == "error":
                shdlr.setLevel(logging.ERROR)
            elif debug == "critical":
                shdlr.setLevel(logging.CRITICAL)
        self.logger.setLevel(logging.INFO)