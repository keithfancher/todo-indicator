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


import tempfile
import unittest

from list import TodoTxtList


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

    def test_reload_from_file(self):
        test_list = TodoTxtList() # Start with an empty list
        test_list.reload_from_file() # Should do nothing

        test_list.todo_filename = 'sample-todo.txt'
        test_list.reload_from_file()

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

    def test_has_items(self):
        test_list = TodoTxtList()
        self.assertFalse(test_list.has_items())

        test_list = TodoTxtList(None, 'An item')
        self.assertTrue(test_list.has_items())

    def test_remove_item(self):
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

    def test_remove_completed_items(self):
        todo_text = "(A) Item one\n(Z) Item two\nx Item three\n\n \n"
        test_list = TodoTxtList(None, todo_text)

        self.assertEqual(3, test_list.num_items())
        test_list.remove_completed_items()
        self.assertEqual(2, test_list.num_items())

        self.assertEqual('Item one', test_list.items[0].text)
        self.assertEqual('A', test_list.items[0].priority)
        self.assertFalse(test_list.items[0].is_completed)

        self.assertEqual('Item two', test_list.items[1].text)
        self.assertEqual('Z', test_list.items[1].priority)
        self.assertFalse(test_list.items[1].is_completed)

    def test_mark_item_completed(self):
        todo_text = "(A) Item one\n(Z) Item two\nx Item three\n\n \n"
        test_list = TodoTxtList(None, todo_text)

        test_list.mark_item_completed('Item two')

        self.assertEqual('Item one', test_list.items[0].text)
        self.assertEqual('A', test_list.items[0].priority)
        self.assertFalse(test_list.items[0].is_completed)

        self.assertEqual('Item two', test_list.items[1].text)
        self.assertEqual('Z', test_list.items[1].priority)
        self.assertTrue(test_list.items[1].is_completed)

        self.assertEqual('Item three', test_list.items[2].text)
        self.assertEqual(None, test_list.items[2].priority)
        self.assertTrue(test_list.items[2].is_completed)

    def test_mark_item_completed_with_full_text(self):
        todo_text = "(A) Item one\n(Z) Item two\nx Item three\n\n \n"
        test_list = TodoTxtList(None, todo_text)

        test_list.mark_item_completed_with_full_text('(Z) Item two')

        self.assertEqual('Item one', test_list.items[0].text)
        self.assertEqual('A', test_list.items[0].priority)
        self.assertFalse(test_list.items[0].is_completed)

        self.assertEqual('Item two', test_list.items[1].text)
        self.assertEqual('Z', test_list.items[1].priority)
        self.assertTrue(test_list.items[1].is_completed)

        self.assertEqual('Item three', test_list.items[2].text)
        self.assertEqual(None, test_list.items[2].priority)
        self.assertTrue(test_list.items[2].is_completed)

    def test_sort_list(self):
        todo_text = "x (C) No biggie\n(Z) aaaaa\nNothing\n(B) hey hey\n(Z) bbbbb\n(A) aaaaa\nx Item three\n\nx (B) Done it\n"
        test_list = TodoTxtList(None, todo_text)

        test_list.sort_list()

        self.assertEqual(8, test_list.num_items())

        self.assertEqual('aaaaa', test_list.items[0].text)
        self.assertEqual('A', test_list.items[0].priority)
        self.assertFalse(test_list.items[0].is_completed)

        self.assertEqual('hey hey', test_list.items[1].text)
        self.assertEqual('B', test_list.items[1].priority)
        self.assertFalse(test_list.items[1].is_completed)

        self.assertEqual('aaaaa', test_list.items[2].text)
        self.assertEqual('Z', test_list.items[2].priority)
        self.assertFalse(test_list.items[2].is_completed)

        self.assertEqual('bbbbb', test_list.items[3].text)
        self.assertEqual('Z', test_list.items[3].priority)
        self.assertFalse(test_list.items[3].is_completed)

        self.assertEqual('Nothing', test_list.items[4].text)
        self.assertEqual(None, test_list.items[4].priority)
        self.assertFalse(test_list.items[4].is_completed)

        self.assertEqual('Done it', test_list.items[5].text)
        self.assertEqual('B', test_list.items[5].priority)
        self.assertTrue(test_list.items[5].is_completed)

        self.assertEqual('No biggie', test_list.items[6].text)
        self.assertEqual('C', test_list.items[6].priority)
        self.assertTrue(test_list.items[6].is_completed)

        self.assertEqual('Item three', test_list.items[7].text)
        self.assertEqual(None, test_list.items[7].priority)
        self.assertTrue(test_list.items[7].is_completed)

    def test_to_text(self):
        test_list = TodoTxtList()

        # Empty list yields empty string:
        self.assertEqual('', str(test_list))

        todo_text = "(A) Do one thing\n         (B) Do another thing\n x One last thing"
        expected_output = "(A) Do one thing\n(B) Do another thing\nx One last thing"
        test_list.init_from_text(todo_text)
        self.assertEqual(expected_output, str(test_list))

    def test_write_to_file(self):
        todo_text = "(A) Do one thing\n         (B) Do another thing\n x One last thing"
        expected_output = "(A) Do one thing\n(B) Do another thing\nx One last thing"
        test_list = TodoTxtList(None, todo_text)

        # Write to a temporary output file:
        output_file = tempfile.NamedTemporaryFile(mode='w+')
        test_list.todo_filename = output_file.name
        test_list.write_to_file()

        # Now read the file in and see that it all matches up:
        self.assertEqual(expected_output, output_file.read())


if __name__ == '__main__':
    unittest.main()
