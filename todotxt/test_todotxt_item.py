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


import unittest

from todotxt_item import TodoTxtItem


class TestTodoTxtItem(unittest.TestCase):

    def test_init_from_text_completion(self):
        completed_item = 'x This is a completed item'
        completed_whitespace = '    x Also completed    '
        not_completed = 'xNope, not even close'
        also_not_completed = '   Nope, not even close'

        test_item = TodoTxtItem()
        test_item.init_from_text(completed_item)
        self.assertTrue(test_item.is_completed)
        self.assertEqual(test_item.text, 'This is a completed item')

        test_item.init_from_text(completed_whitespace)
        self.assertTrue(test_item.is_completed)
        self.assertEqual(test_item.text, 'Also completed')

        test_item.init_from_text(not_completed)
        self.assertFalse(test_item.is_completed)
        self.assertEqual(test_item.text, 'xNope, not even close')

        test_item.init_from_text(also_not_completed)
        self.assertFalse(test_item.is_completed)
        self.assertEqual(test_item.text, 'Nope, not even close')

    def test_init_from_text_priority(self):
        item_with_priority = '(A) This item is pretty important'
        item_with_priority2 = '(Z) Not so important'
        no_priority = 'Just some item'
        no_priority2 = '(b) Only caps should work here'

        test_item = TodoTxtItem()
        test_item.init_from_text(item_with_priority)
        self.assertEqual(test_item.priority, 'A')
        self.assertEqual(test_item.text, 'This item is pretty important')

        test_item.init_from_text(item_with_priority2)
        self.assertEqual(test_item.priority, 'Z')
        self.assertEqual(test_item.text, 'Not so important')

        test_item.init_from_text(no_priority)
        self.assertEqual(test_item.priority, None)
        self.assertEqual(test_item.text, 'Just some item')

        test_item.init_from_text(no_priority2)
        self.assertEqual(test_item.priority, None)
        self.assertEqual(test_item.text, '(b) Only caps should work here')

    def test_init_from_text_completion_and_priority(self):
        item = 'x (R) Good thing I completed this'

        test_item = TodoTxtItem()
        test_item.init_from_text(item)

        self.assertTrue(test_item.is_completed)
        self.assertEqual(test_item.priority, 'R')
        self.assertEqual(test_item.text, 'Good thing I completed this')

    def test_to_string(self):
        test_item = TodoTxtItem('This is some task', 'F', True)
        self.assertEqual(test_item.to_string(), 'x (F) This is some task')

        test_item = TodoTxtItem('This is some task', None, False)
        self.assertEqual(test_item.to_string(), 'This is some task')

    def test_from_string_back_to_string(self):
        original_item = 'x (Z) Here we go again'
        some_whitespace = 'x    (B)    This one is pretty weird'

        test_item = TodoTxtItem()
        test_item.init_from_text(original_item)
        self.assertEqual(original_item, test_item.to_string())

        test_item.init_from_text(some_whitespace)
        self.assertEqual('x (B) This one is pretty weird', test_item.to_string())


if __name__ == '__main__':
    unittest.main()
