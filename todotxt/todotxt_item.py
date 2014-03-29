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


import re


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
        if self.is_completed:
            output = 'x '
        else:
            output = ''

        if self.priority:
            output = output + '(' + self.priority + ') '

        return output + self.text
