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

from todotxt_list import TodoTxtList


class TestTodoTxtList(unittest.TestCase):

    def test_init_from_text(self):
        todo_text = "(A) Item one\n(Z) Item two\nx Item three\n\n \n"
        test_list = TodoTxtList(None, todo_text)

        self.assertEqual(3, test_list.num_items())

        self.assertEqual('Item one', test_list.items[0].text)
        self.assertEqual('A', test_list.items[0].priority)
        self.assertFalse(test_list.items[0].is_completed)

        self.assertEqual('Item two', test_list.items[1].text)
        self.assertEqual('Z', test_list.items[1].priority)
        self.assertFalse(test_list.items[1].is_completed)

        self.assertEqual('Item three', test_list.items[2].text)
        self.assertEqual(None, test_list.items[2].priority)
        self.assertTrue(test_list.items[2].is_completed)

    def test_init_from_file(self):
        file_name = 'sample-todo.txt'
        test_list = TodoTxtList(file_name)

        self.assertEqual(8, test_list.num_items())

        self.assertEqual('Do that really important thing', test_list.items[0].text)
        self.assertEqual('A', test_list.items[0].priority)
        self.assertFalse(test_list.items[0].is_completed)

        self.assertEqual('Summon AppIndicator documentation from my ass', test_list.items[1].text)
        self.assertEqual('D', test_list.items[1].priority)
        self.assertFalse(test_list.items[1].is_completed)

        self.assertEqual('This other important thing', test_list.items[2].text)
        self.assertEqual('A', test_list.items[2].priority)
        self.assertFalse(test_list.items[2].is_completed)

        self.assertEqual('Walk the cat', test_list.items[3].text)
        self.assertEqual('B', test_list.items[3].priority)
        self.assertFalse(test_list.items[3].is_completed)

        self.assertEqual('Something with no priority!', test_list.items[4].text)
        self.assertEqual(None, test_list.items[4].priority)
        self.assertFalse(test_list.items[4].is_completed)

        self.assertEqual('Cook the dog', test_list.items[5].text)
        self.assertEqual('C', test_list.items[5].priority)
        self.assertFalse(test_list.items[5].is_completed)

        self.assertEqual('Be annoyed at GTK3 docs', test_list.items[6].text)
        self.assertEqual(None, test_list.items[6].priority)
        self.assertTrue(test_list.items[6].is_completed)

        self.assertEqual('Something I already did', test_list.items[7].text)
        self.assertEqual(None, test_list.items[7].priority)
        self.assertTrue(test_list.items[7].is_completed)

    def test_remove_items(self):
        todo_text = "(A) Item one\n(Z) Item two\nx Item three\n\n \n"
        test_list = TodoTxtList(None, todo_text)

        self.assertEqual(3, test_list.num_items())
        test_list.remove_item('Item two')
        self.assertEqual(2, test_list.num_items())

        self.assertEqual('Item one', test_list.items[0].text)
        self.assertEqual('A', test_list.items[0].priority)
        self.assertFalse(test_list.items[0].is_completed)

        self.assertEqual('Item three', test_list.items[1].text)
        self.assertEqual(None, test_list.items[1].priority)
        self.assertTrue(test_list.items[1].is_completed)


if __name__ == '__main__':
    unittest.main()
