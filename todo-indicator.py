#!/usr/bin/env python


import os

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator


DARK_PANEL_ICON = "gtg-panel"
TESTING_TODO_FILE = "todo.txt"
EDITOR = "gvim"


def edit_handler(event):
    os.system(EDITOR + " " + TESTING_TODO_FILE)


def quit_handler(event):
    Gtk.main_quit()


def main():
    # open the file, read it
    todo_file = open(TESTING_TODO_FILE)
    todo_list = todo_file.read().split("\n")
    del todo_list[-1] # kill final empty entry
    todo_file.close()

    # indicator business
    ind = appindicator.Indicator.new("todo-txt-indicator", DARK_PANEL_ICON,
                                     appindicator.IndicatorCategory.OTHER)
    ind.set_status(appindicator.IndicatorStatus.ACTIVE)
#    ind.set_attention_icon("indicator-messages-new") # necessary?

    # create a menu
    menu = Gtk.Menu()

    # create todo menu items
    for todo_item in todo_list:
        menu_item = Gtk.MenuItem(todo_item)
        menu_item.show()
        menu.append(menu_item)

    # add a separator
    menu_item = Gtk.SeparatorMenuItem()
    menu_item.show()
    menu.append(menu_item)

    # add "edit list" menu item
    menu_item = Gtk.MenuItem("Edit")
    menu_item.connect("activate", edit_handler)
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
