#!/usr/bin/env python


import os

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator


DARK_PANEL_ICON = "gtg-panel"
TESTING_TODO_FILE = "sample-todo.txt"
EDITOR = "gvim"


class TodoIndicator(object):

    def __init__(self):
        self.todo_list = self._read_todo_file(TESTING_TODO_FILE)
        self.ind = self._build_indicator(self.todo_list)

    def _read_todo_file(self, filename):
        """Returns a list of todo items read from the given file name."""
        todo_file = open(filename)
        todo_list = todo_file.read().split("\n")
        todo_file.close()
        todo_list = filter(None, todo_list) # kill empty items
        return sorted(todo_list)

    def _edit_handler(self, event):
        """Opens the todo.txt file with selected editor."""
        os.system(EDITOR + " " + TESTING_TODO_FILE)

    def _refresh_handler(self, event):
        """Refreshes the list."""
        # TODO: gives odd warning about removing a child...
        self.todo_list = self._read_todo_file(TESTING_TODO_FILE)
        self.ind = self._build_indicator(self.todo_list)

    def _quit_handler(self, event):
        """Quits our fancy little program."""
        Gtk.main_quit()

    def _build_indicator(self, todo_list):
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
        menu_item.connect("activate", self._edit_handler)
        menu_item.show()
        menu.append(menu_item)

        # add "refresh" menu item
        menu_item = Gtk.MenuItem("Refresh")
        menu_item.connect("activate", self._refresh_handler)
        menu_item.show()
        menu.append(menu_item)

        # add quit menu item
        menu_item = Gtk.MenuItem("Quit")
        menu_item.connect("activate", self._quit_handler)
        menu_item.show()
        menu.append(menu_item)

        ind.set_menu(menu)

        return ind

    def main(self):
        """The indicator's main loop."""
        Gtk.main()


if __name__ == "__main__":
    ind = TodoIndicator()
    ind.main()
