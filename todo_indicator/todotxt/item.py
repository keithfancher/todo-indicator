#!/usr/bin/env python


# Copyright 2012-2014, 2022 Keith Fancher
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


import functools
import re


@functools.total_ordering
class TodoTxtItem(object):
    def __init__(self, text=None, priority=None, is_completed=False):
        self.text = text
        self.priority = priority
        self.is_completed = is_completed

    def init_from_text(self, item_text):
        item_text = item_text.strip()

        # First get completion:
        if item_text[:2] == "x ":
            self.is_completed = True
            item_text = item_text[2:].strip()
        else:
            self.is_completed = False

        # Now get priority, if it exists:
        priority_regex = r"^\(([A-Z])\) "
        match = re.search(priority_regex, item_text)
        if match:
            self.priority = match.group(1)
            item_text = item_text[3:].strip()
        else:
            self.priority = None

        self.text = item_text

    def has_priority(self):
        """This is useful when sorting list items."""
        return self.priority != None

    def __str__(self):
        if self.is_completed:
            output = "x "
        else:
            output = ""

        if self.priority:
            output = output + "(" + self.priority + ") "

        return output + self.text

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.is_completed == other.is_completed
            and self.priority == other.priority
        )

    def __lt__(self, other):
        # First sort by completion:
        if not self.is_completed and other.is_completed:
            return True
        if self.is_completed and not other.is_completed:
            return False

        # Then sort by whether an item is prioritized:
        if self.has_priority() and not other.has_priority():
            return True
        if not self.has_priority() and other.has_priority():
            return False

        if self.has_priority() and other.has_priority():
            # Now we know both have priority, so sort by that next:
            if self.priority < other.priority:
                return True
            if self.priority > other.priority:
                return False

        # Priorities are equal, so sort by actual text:
        if self.text < other.text:
            return True

        # Otherwise this item is not less than t'other!
        return False
