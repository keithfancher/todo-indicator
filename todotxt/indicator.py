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


import os
import pyinotify

from gi.repository import AppIndicator3 as appindicator, \
                          GObject, \
                          Gtk

from todotxt_list import TodoTxtList


IMG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/img/'
LIGHT_ICON = IMG_PATH + 'panel-icon-light.svg' # Light icon for dark panel background
DARK_ICON = IMG_PATH + 'panel-icon-dark.svg'   # Dark icon for light panel background
DEFAULT_EDITOR = "xdg-open"


class TodoIndicator(object):

    def __init__(self, todo_filename, text_editor=None, invert_icon=False):
        """Sets the filename, loads the list of items from the file, builds the
        indicator, &c."""
        if text_editor:
            self.text_editor = text_editor
        else:
            self.text_editor = DEFAULT_EDITOR

        if invert_icon:
            self.icon_path = DARK_ICON
        else:
            # Default to light icon, assuming dark panel background:
            self.icon_path = LIGHT_ICON

        # Initialize the main list object:
        self.todo_list = TodoTxtList(todo_filename)
        # TODO: keep list sorted implicitly?
        self.todo_list.sort_list()

        # Non-list menu items:
        self._setup_menu_items()

        # Necessary for threaded notifications:
        GObject.threads_init()

        # Does the GUI need to catch up with our list file?
        self.list_updated_flag = False

        # Creates self.ind, the main indicator object:
        self._build_indicator()

        # Starts up inotify, watches our list file:
        self._setup_inotify()

        # Add timeout function, allows threading to not fart all over itself.
        # Can't use Gobject.idle_add() since it rudely 100%s the CPU.
        GObject.timeout_add(500, self._update_if_todo_file_changed)

    def _setup_inotify(self):
        """Watch for modifications of the todo file with pyinotify. We have to
        watch the entire path, since inotify is very inconsistent about what
        events it catches for a single file."""
        self.wm = pyinotify.WatchManager()
        self.notifier = pyinotify.ThreadedNotifier(self.wm,
                                                   self._process_inotify_event)
        self.notifier.start()

        # The IN_MOVED_TO watch catches Dropbox updates, which don't trigger
        # normal IN_MODIFY events.
        todo_path = os.path.dirname(self.todo_list.todo_filename)
        self.wm.add_watch(todo_path,
                          pyinotify.IN_MODIFY | pyinotify.IN_MOVED_TO)

    def _setup_menu_items(self):
        """Menu items (aside from the todo items themselves). An association of
        text and callback functions. Can't use a dict because we need to
        preserve order."""
        self._menu_items = [ ('Edit todo.txt', self._edit_handler),
                             ('Clear completed', self._clear_completed_handler),
                             ('Refresh', self._refresh_handler),
                             ('Quit', self._quit_handler) ]

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
        if event.pathname == self.todo_list.todo_filename:
            self.list_updated_flag = True

    def _load_todo_file(self):
        """Populates the list of todo items from the todo file."""
        self.todo_list.reload_from_file()
        self.todo_list.sort_list()

    def _check_off_item_with_label(self, label):
        """Checks off the item in our list that matches the clicked label. If
        you have multiple todo items that are exactly the same, this will check
        them all off. Also, you're stupid for doing that."""
        self.todo_list.mark_item_completed_with_full_text(label)
        self.todo_list.sort_list()
        self.todo_list.write_to_file()

    def _remove_checked_off_items(self):
        """Remove checked items from the file itself."""
        self.todo_list.remove_completed_items()
        self.todo_list.write_to_file()

    def _check_off_handler(self, menu_item):
        """Callback to check items off the list."""
        self._check_off_item_with_label(menu_item.get_label()) # write file
        self._build_indicator() # rebuild!

    def _edit_handler(self, menu_item):
        """Opens the todo.txt file with selected editor."""
        os.system(self.text_editor + " " + self.todo_list.todo_filename)

    def _clear_completed_handler(self, menu_item):
        """Remove checked off items, rebuild list menu."""
        self._remove_checked_off_items()
        self._build_indicator()

    def _refresh_handler(self, menu_item):
        """Manually refreshes the list."""
        self._build_indicator() # rebuild indicator

    def _quit_handler(self, menu_item):
        """Quits our fancy little program."""
        self.notifier.stop() # stop watching the file!
        Gtk.main_quit()

    def _build_list_menu_items(self, menu):
        """Creates menu items for each of our todo list items. Pass it a GTK
        menu object, it returns that object with menu items added."""
        for todo_item in self.todo_list.items:
            menu_item = Gtk.MenuItem(todo_item.to_string())
            if todo_item.is_completed: # gray out completed items
                menu_item.set_sensitive(False)
            menu_item.connect("activate", self._check_off_handler)
            menu_item.show()
            menu.append(menu_item)
        return menu

    def _build_indicator(self):
        """Builds the Indicator object."""
        if not hasattr(self, 'ind'): # self.ind needs to be created
            self.ind = appindicator.Indicator.new("todo-txt-indicator",
                self.icon_path, appindicator.IndicatorCategory.OTHER)
            self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

        # make sure the list is loaded
        # TODO: don't really need to do this every time anymore...
        self._load_todo_file()

        menu = Gtk.Menu()
        if self.todo_list.has_items():
            # Create todo menu items, if they exist:
            self._build_list_menu_items(menu)
        else:
            # If the list is empty, show helpful message:
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
