#!/usr/bin/env python


from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator


DARK_PANEL_ICON = "gtg-panel"
TESTING_LIST = ["(A) item 1", "(A) item 2", "(B) item 3", "(C) another item"]


def quit_handler(event):
    Gtk.main_quit()


def main():
    ind = appindicator.Indicator.new("todo-txt-indicator", DARK_PANEL_ICON,
                                     appindicator.IndicatorCategory.OTHER)
    ind.set_status(appindicator.IndicatorStatus.ACTIVE)
#    ind.set_attention_icon("indicator-messages-new") # necessary?

    # create a menu
    menu = Gtk.Menu()

    # create todo menu items
    for todo_item in TESTING_LIST:
        menu_item = Gtk.MenuItem(todo_item)
        menu_item.show()
        menu.append(menu_item)

    # add a separator
    menu_item = Gtk.SeparatorMenuItem()
    menu_item.show()
    menu.append(menu_item)

    # add quit menu item
    menu_item = Gtk.MenuItem("Quit")
    menu_item.connect("activate", quit_handler)
    menu_item.show()
    menu.append(menu_item)

    ind.set_menu(menu)
    Gtk.main()


if __name__ == "__main__":
    main()
