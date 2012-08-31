#!/usr/bin/env python


import sys

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator


DARK_PANEL_ICON = "gtg-panel"


def menuitem_response(w, buf):
    print buf
    sys.exit(0)


def main():
    ind = appindicator.Indicator.new(
        "todo-txt-indicator",
        DARK_PANEL_ICON,
        appindicator.IndicatorCategory.OTHER)
    ind.set_status(appindicator.IndicatorStatus.ACTIVE)
#    ind.set_attention_icon("indicator-messages-new") # necessary?

    # create a menu
    menu = Gtk.Menu()

    # create some
    for i in range(3):
        buf = "Test-undermenu - %d" % i
        menu_items = Gtk.MenuItem(buf)
        menu.append(menu_items)

        # this is where you would connect your menu item up with a function:
        menu_items.connect("activate", menuitem_response, buf)

        # show the items
        menu_items.show()

    ind.set_menu(menu)
    Gtk.main()


if __name__ == "__main__":
    main()
