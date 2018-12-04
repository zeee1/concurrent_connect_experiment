import webkit, gtk

def get_source(webobj, frame):
	print("loading...")
	x = web.get_main_frame().get_data_source().get_data()
	print(x)

win = gtk.Window()
win.set_position(gtk.WIN_POS_CENTER_ALWAYS)
win.resize(1024,768)
win.connect('destroy', lambda w: gtk.main_quit())
win.set_title('Titulo')
vbox = gtk.VBox(spacing=5)
vbox.set_border_width(5)
web = webkit.WebView()
vbox.pack_start(web, fill=True, expand=True)

web = webkit.WebView()
web.open("http://www.google.co.ve")
web.connect("load-finished", get_source)

browser_settings = web.get_settings()
browser_settings.set_property('user-agent', 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0')
browser_settings.set_property('enable-default-context-menu', True)
browser_settings.set_property('enable-accelerated-compositing', True)
browser_settings.set_property('enable-file-access-from-file-uris', True)
web.set_settings(browser_settings)

win.add(web)
win.show_all()
gtk.main()