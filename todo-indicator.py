#!/usr/bin/env python


import os

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator


DARK_PANEL_ICON = "gtg-panel"
TESTING_TODO_FILE = "todo.txt"
EDITOR = "gvim"


def read_todo_file(filename):
    """Returns a list of todo items read from the given file name."""
    todo_file = open(filename)
    todo_list = todo_file.read().split("\n")
    todo_file.close()
    todo_list = filter(None, todo_list) # kill empty items
    return sorted(todo_list)


def edit_handler(event):
    """Opens the todo.txt file with selected editor."""
    os.system(EDITOR + " " + TESTING_TODO_FILE)


def quit_handler(event):
    """Quits our fancy little program."""
    Gtk.main_quit()


def build_indicator(todo_list):
    """Builds the Indicator object."""
    ind = appindicator.Indicator.new("todo-txt-indicator", DARK_PANEL_ICON,
                                     appindicator.IndicatorCategory.OTHER)
    ind.set_status(appindicator.IndicatorStatus.ACTIVE)

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
    menu_item = Gtk.MenuItem("Edit todo.txt")
    menu_item.connect("activate", edit_handler)
    menu_item.show()
    menu.append(menu_item)

    # add quit menu item
    menu_item = Gtk.MenuItem("Quit")
    menu_item.connect("activate", quit_handler)
    menu_item.show()
    menu.append(menu_item)

    ind.set_menu(menu)

    return ind


def main():
    """Our main man!"""
    todo_list = read_todo_file(TESTING_TODO_FILE)

    ind = build_indicator(todo_list)
    Gtk.main()


if __name__ == "__main__":
    main()
