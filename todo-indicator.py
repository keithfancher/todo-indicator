#!/usr/bin/env python


import fileinput
import os
import pyinotify
import sys

from gi.repository import Gtk, GObject
from gi.repository import AppIndicator3 as appindicator


DARK_PANEL_ICON = "gtg-panel"
TESTING_TODO_FILE = "sample-todo.txt"
EDITOR = "xdg-open"


class TodoIndicator(object):

    def __init__(self, todo_filename):
        """Sets the filename, loads the list of items from the file, builds the
        indicator."""
        self.todo_filename = os.path.abspath(todo_filename) # absolute path!
        self.todo_path = os.path.dirname(self.todo_filename) # useful
        self._build_indicator() # creates self.ind

        # Watch for modifications of the todo file with pyinotify. We have to
        # watch the entire path, since inotify is very inconsistent about what
        # events it catches for a single file. Annoying.
        self.wm = pyinotify.WatchManager()
        self.notifier = pyinotify.ThreadedNotifier(self.wm,
                                                   self._process_inotify_event)
        self.notifier.start()
        self.wm.add_watch(self.todo_path, pyinotify.IN_MODIFY)

    def _process_inotify_event(self, event):
        """This callback is typically an instance of the ProcessEvent class,
        but after digging through the pyinotify source it looks like it can
        also be a function? This makes things much easier in our case, avoids
        nested classes, etc."""
        if event.pathname == self.todo_filename:
            self._build_indicator() # rebuild if file modified

    def _load_todo_file(self):
        """Populates the list of todo items from the todo file."""
        f = open(self.todo_filename)
        todo_list = f.read().split("\n")
        f.close()
        self.todo_list = sorted(filter(None, todo_list)) # kill empty items+sort

    def _check_off_item_with_label(self, label):
        """Matches the given todo item, finds it in the file, and "checks it
        off" by adding "x " to the beginning of the string. If you have
        multiple todo items that are exactly the same, this will check them all
        off. Also, you're stupid for doing that."""
        for line in fileinput.input(self.todo_filename, inplace=1):
            if line.strip() == label:
                print "x " + line, # magic!
            else:
                print line,

    def _check_off_handler(self, menu_item):
        self._check_off_item_with_label(menu_item.get_label()) # write file
        self._build_indicator() # rebuild!

    def _edit_handler(self, menu_item):
        """Opens the todo.txt file with selected editor."""
        os.system(EDITOR + " " + self.todo_filename)

    def _refresh_handler(self, menu_item):
        """Manually refreshes the list."""
        # TODO: gives odd warning about removing a child...
        self._build_indicator() # rebuild indicator

    def _quit_handler(self, menu_item):
        """Quits our fancy little program."""
        self.notifier.stop() # stop watching the file!
        Gtk.main_quit()

    def _build_indicator(self):
        """Builds the Indicator object."""
        if not hasattr(self, 'ind'): # self.ind needs to be created
            # TODO: creating self.ind every time causes segfaults when the file
            # is modified 2+ times and the thing rebuilds, but NOT creating it
            # every time causes the file to load incorrectly and the menu to be
            # created incorrectly. And occasional freezes? Need more indicator
            # info...
            self.ind = appindicator.Indicator.new("todo-txt-indicator",
                DARK_PANEL_ICON, appindicator.IndicatorCategory.OTHER)
            self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

        # make sure the list is loaded
        self._load_todo_file()

        # create todo menu items
        menu = Gtk.Menu()
        for todo_item in self.todo_list:
            menu_item = Gtk.MenuItem(todo_item)
            if todo_item[0:2] == 'x ': # gray out completed items
                menu_item.set_sensitive(False)
            menu_item.connect("activate", self._check_off_handler)
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

        # do it!
        self.ind.set_menu(menu)

    def main(self):
        """The indicator's main loop."""
        Gtk.main()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        todo_filename = sys.argv[1]
    else:
        todo_filename = TESTING_TODO_FILE

    GObject.threads_init() # necessary for threaded notifications
    ind = TodoIndicator(todo_filename)
    ind.main()
