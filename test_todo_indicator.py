#!/usr/bin/env python


import unittest

from todo_indicator import TodoTxtItem, TodoTxtList


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
