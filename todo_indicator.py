#!/usr/bin/env python


# Copyright 2012-2014 Keith Fancher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import argparse
import fileinput
import os
import pyinotify
import re
import sys

from gi.repository import Gtk, GObject
from gi.repository import AppIndicator3 as appindicator


PANEL_ICON = "gtg-panel"
DEFAULT_EDITOR = "xdg-open"


class TodoTxtItem(object):

    def __init__(self, text=None, priority=None, is_completed=False):
        self.text = text
        self.priority = priority
        self.is_completed = is_completed

    def init_from_text(self, item_text):
        item_text = item_text.strip()

        # First get completion:
        if item_text[:2] == 'x ':
            self.is_completed = True
            item_text = item_text[2:].strip()
        else:
            self.is_completed = False

        # Now get priority, if it exists:
        priority_regex = r'^\(([A-Z])\) '
        match = re.search(priority_regex, item_text)
        if match:
            self.priority = match.group(1)
            item_text = item_text[3:].strip()
        else:
            self.priority = None

        self.text = item_text

    def to_string(self):
        pass


class TodoTxtList(object):

    def __init__(self, todo_filename=None, todo_text=None):
        """Can initialize from either a file, or from text directly?"""

        if todo_filename:
            self.todo_filename = os.path.abspath(todo_filename)  # absolute path!
            self.todo_path = os.path.dirname(self.todo_filename) # useful

        self.items = []
        self.items_as_text = ''

    def add_item(self):
        pass
    def remove_item(self):
        pass
    def mark_item_completed(self):
        pass
    def sort_list(self):
        pass
    def build_list_from_text(self, list_text):
        pass
    def read_from_file(self):
        pass
    def write_to_file(self):
        pass


class TodoIndicator(object):

    def __init__(self, todo_filename, text_editor=None):
        """Sets the filename, loads the list of items from the file, builds the
        indicator."""
        if text_editor:
            self.text_editor = text_editor
        else:
            self.text_editor = DEFAULT_EDITOR

        # Menu items (aside from the todo items themselves). An association of
        # text and callback functions. Can't use a dict because we need to
        # preserve order.
        self._menu_items = [ ('Edit todo.txt', self._edit_handler),
                             ('Clear completed', self._clear_completed_handler),
                             ('Refresh', self._refresh_handler),
                             ('Quit', self._quit_handler) ]

        GObject.threads_init() # necessary for threaded notifications
        self.list_updated_flag = False # does the GUI need to catch up?
        self.todo_filename = os.path.abspath(todo_filename) # absolute path!
        self.todo_path = os.path.dirname(self.todo_filename) # useful
        self._build_indicator() # creates self.ind

        # Watch for modifications of the todo file with pyinotify. We have to
        # watch the entire path, since inotify is very inconsistent about what
        # events it catches for a single file.
        self.wm = pyinotify.WatchManager()
        self.notifier = pyinotify.ThreadedNotifier(self.wm,
                                                   self._process_inotify_event)
        self.notifier.start()

        # The IN_MOVED_TO watch catches Dropbox updates, which don't trigger
        # normal IN_MODIFY events.
        self.wm.add_watch(self.todo_path,
                          pyinotify.IN_MODIFY | pyinotify.IN_MOVED_TO)

        # Add timeout function, allows threading to not fart all over itself.
        # Can't use Gobject.idle_add() since it rudely 100%s the CPU.
        GObject.timeout_add(500, self._update_if_todo_file_changed)

    def _update_if_todo_file_changed(self):
        """This will be called by the main GTK thread every half second or so.
        If the self.list_updated_flag is False, it will immediately return. If
        it's True, it will rebuild the GUI with the updated list and reset the
        flag.  This is necessary since threads + GTK are wonky as fuck."""
        if self.list_updated_flag:
            self._build_indicator() # rebuild
            self.list_updated_flag = False # reset flag

        # if we don't explicitly return True here the callback will be removed
        # from the queue after one call and will never be called again
        return True

    def _process_inotify_event(self, event):
        """This callback is typically an instance of the ProcessEvent class,
        but after digging through the pyinotify source it looks like it can
        also be a function? This makes things much easier in our case, avoids
        nested classes, etc.

        This function can't explicitly update the GUI since it's on a different
        thread, so it just flips a flag and lets another function called by the
        GTK main loop do the real work."""
        if event.pathname == self.todo_filename:
            self.list_updated_flag = True

    def _load_todo_file(self):
        """Populates the list of todo items from the todo file."""
        try:
            with open(self.todo_filename, 'a+') as f:
                todo_list = f.read().split("\n")
                # kill empty items/lines, sort list alphabetically (but with
                # checked-off items bumped to end of the list):
                self.todo_list = sorted(filter(None, todo_list),
                    key=lambda a: 'z' * 10 + a if a[:2] == 'x ' else a)
        except IOError:
            print "Error opening file:\n" + self.todo_filename
            sys.exit(1)

    def _check_off_item_with_label(self, label):
        """Matches the given todo item, finds it in the file, and "checks it
        off" by adding "x " to the beginning of the string. If you have
        multiple todo items that are exactly the same, this will check them all
        off. Also, you're stupid for doing that."""
        for line in fileinput.input(self.todo_filename, inplace=1):
            if line.strip() == label.strip():
                print "x " + line, # magic!
            else:
                print line,

    def _remove_checked_off_items(self):
        """Remove checked items from the file itself."""
        for line in fileinput.input(self.todo_filename, inplace=1):
            if line[:2] == 'x ':
                pass
            else:
                print line,

    def _check_off_handler(self, menu_item):
        """Callback to check items off the list."""
        self._check_off_item_with_label(menu_item.get_label()) # write file
        self._build_indicator() # rebuild!

    def _edit_handler(self, menu_item):
        """Opens the todo.txt file with selected editor."""
        os.system(self.text_editor + " " + self.todo_filename)

    def _clear_completed_handler(self, menu_item):
        """Remove checked off items, rebuild list menu."""
        self._remove_checked_off_items()
        self._build_indicator()

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
            self.ind = appindicator.Indicator.new("todo-txt-indicator",
                PANEL_ICON, appindicator.IndicatorCategory.OTHER)
            self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

        # make sure the list is loaded
        self._load_todo_file()

        # create todo menu items
        menu = Gtk.Menu()
        if self.todo_list:
            for todo_item in self.todo_list:
                menu_item = Gtk.MenuItem(todo_item)
                if todo_item[0:2] == 'x ': # gray out completed items
                    menu_item.set_sensitive(False)
                menu_item.connect("activate", self._check_off_handler)
                menu_item.show()
                menu.append(menu_item)
        # empty list
        else:
            menu_item = Gtk.MenuItem('[ No items. Click \'Edit\' to add some! ]')
            menu_item.set_sensitive(False)
            menu_item.show()
            menu.append(menu_item)

        # add a separator
        menu_item = Gtk.SeparatorMenuItem()
        menu_item.show()
        menu.append(menu_item)

        # our menu
        for text, callback in self._menu_items:
            menu_item = Gtk.MenuItem(text)
            menu_item.connect("activate", callback)
            menu_item.show()
            menu.append(menu_item)

        # do it!
        self.ind.set_menu(menu)

    def main(self):
        """The indicator's main loop."""
        Gtk.main()


def get_args():
    """Gets and parses command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--editor', action='store',
                        help='your favorite text editor')
    parser.add_argument('todo_filename', action='store',
                        help='your todo.txt file')
    return parser.parse_args()


def main():
    """My main() man."""
    args = get_args()
    ind = TodoIndicator(args.todo_filename, args.editor)
    ind.main()


if __name__ == "__main__":
    main()
