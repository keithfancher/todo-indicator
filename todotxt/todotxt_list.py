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
        self.todo_path = ''

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
        self.todo_path = os.path.dirname(self.todo_filename) # useful

        try:
            with open(self.todo_filename, 'a+') as f:
                todo_lines = f.read()
        except IOError:
            print "Error opening file:\n" + self.todo_filename
            sys.exit(1)

        self.init_from_text(todo_lines)

    def add_item(self, item_text):
        """Turn a line of text into a TodoTxtItem object, then append it to our
        list of those objects."""
        if item_text.strip():
            new_list_item = TodoTxtItem()
            new_list_item.init_from_text(item_text)
            self.items.append(new_list_item)

    def num_items(self):
        return len(self.items)

    def remove_item(self):
        pass
    def mark_item_completed(self):
        pass
    def sort_list(self):
        pass
    def write_to_file(self):
        pass
