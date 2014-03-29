#!/usr/bin/env python


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


if __name__ == '__main__':
    unittest.main()
