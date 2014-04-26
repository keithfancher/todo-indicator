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
import sys

from todotxt_item import TodoTxtItem


class TodoTxtList(object):

    def __init__(self, todo_filename=None, todo_text=None):
        """Can initialize from either a file, or from text directly."""
        self.items = []
        self.items_as_text = ''
        self.todo_filename = ''

        if todo_filename:
            self.init_from_file(todo_filename)
        elif todo_text:
            self.init_from_text(todo_text)

    def init_from_text(self, list_text):
        """Init the list object from a plaintext todo.txt list."""
        todo_lines = list_text.split("\n")
        for todo_line in todo_lines:
            self.add_item(todo_line)

    def init_from_file(self, file_name):
        """Init the list object from the *filename* of a todo.txt list."""
        self.todo_filename = os.path.abspath(file_name)  # absolute path!

        try:
            with open(self.todo_filename, 'a+') as f:
                todo_lines = f.read()
        except IOError:
            # TODO: Consider moving this check into calling class
            print "Error opening file:\n" + self.todo_filename
            sys.exit(1)

        self.init_from_text(todo_lines)

    def reload_from_file(self):
        """Reload the list from already-set filename."""
        self.items = [] # Clear out existing items
        self.init_from_file(self.todo_filename)

    def add_item(self, item_text):
        """Turn a line of text into a TodoTxtItem object, then append it to our
        list of those objects."""
        if item_text.strip():
            new_list_item = TodoTxtItem()
            new_list_item.init_from_text(item_text)
            self.items.append(new_list_item)

    def num_items(self):
        return len(self.items)

    def remove_item(self, item_text):
        """Remove item with matching item text."""
        self.items = filter(lambda x: x.text != item_text, self.items)

    def mark_item_completed(self, item_text):
        """Mark item with matching text completed."""
        for item in self.items:
            if item.text == item_text:
                item.is_completed = True

    def mark_item_completed_with_full_text(self, full_text):
        """Matches the full text of an item, which includes the priority and
        completion. This is useful/necessary for matching a list item with its
        menu item in the UI."""
        for item in self.items:
            if item.to_string() == full_text:
                item.is_completed = True

    def sort_list(self):
        """Thank you for being magical, magic methods."""
        self.items = sorted(self.items)

    def to_text(self):
        """Return the list as plaintext."""
        list_text = ''
        for item in self.items:
            list_text = list_text + item.to_string() + "\n"
        return list_text.strip()

    def write_to_file(self):
        """Output the list to a file."""
        try:
            with open(self.todo_filename, 'w') as f:
                f.write(self.to_text())
        except IOError:
            # TODO: Consider moving this check into calling class
            print "Error writing to file:\n" + self.todo_filename
            sys.exit(1)
