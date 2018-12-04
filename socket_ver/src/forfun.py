from gi.repository import Gtk
from gi.repository import WebKit2

class  BrowserView:
    def __init__(self):
        window = Gtk.Window()
        window.connect('delete-event',Gtk.main_quit)

        self.view = WebKit2.WebView()
        self.view.load_uri('http://example.net')

        window.add(self.view)
        window.fullscreen()
        window.show_all()


if __name__ == "__main__":
    BrowserView()
    Gtk.main()