import unittest
from unittest.mock import patch
import os
import sys
from peewee import *
import datetime

import employee_database


db = SqliteDatabase(':memory:')


ENTRY_DATA = ['first_name', 'last_name', 'task 1',
                10, 'notes about entry', '2018-05-11', 'n']


class TestEmployeeDB(unittest.TestCase):

    @patch('builtins.input', side_effect=ENTRY_DATA)
    def test_process_entry(self, mock_menu_loop):
        result = employee_database.process_entry()

        print(result)
        self.assertIsNone(result)


class TestEmployee(unittest.TestCase):

    def test_space(self):
        spaces = employee_database.space()
        self.assertEqual(spaces, print('_' * 75))

    @patch('builtins.input', return_value='Bill')
    def test_new_first_name(self, mock):
        entry = employee_database.Entry()
        self.assertEqual(entry.name_first(), 'Bill')

    @patch('builtins.input', return_value='Nye')
    def test_new_last_name(self, mock):
        entry = employee_database.Entry()
        self.assertEqual(entry.name_last(), 'Nye')

    @patch('builtins.input', return_value='science')
    def test_new_task(self, mock):
        entry = employee_database.Entry()
        self.assertEqual(entry.name_task(), 'science')

    @patch('builtins.input', return_value='10')
    def test_new_time(self, mock):
        entry = employee_database.Entry()
        self.assertEqual(entry.name_time(), '10')

    @patch('builtins.input', return_value='testing')
    def test_new_notes(self, mock):
        entry = employee_database.Entry()
        self.assertEqual(entry.name_notes(), 'testing')

    @patch('builtins.input', return_value='2018-04-28')
    def test_new_date(self, mock):
        entry = employee_database.Entry()
        self.assertEqual(entry.name_date(), '2018-04-28')

    @patch('builtins.input', return_value='1')
    def test_search_log(self, mock):
        result = employee_database.search_log()
        self.assertEqual(result, '1')

    @patch('builtins.input', return_value=1)
    def test_menu_selection_1(self, mock):
        result = employee_database.menu()
        self.assertIsNotNone(result)

    @patch('builtins.input', side_effect='3')
    def test_menu_selection_3(self, mock):
        result = employee_database.menu()
        self.assertTrue(result)

    @patch('builtins.input', side_effect=['5'])
    def test_search_log(self, mock_search_log):
        result = employee_database.search_log()
        self.assertEqual(result, '5')

    @patch('builtins.input', side_effect=['6', '4'])
    def test_search_log(self, mock_search_log):
        result = employee_database.search_log()
        self.assertTrue(result)


class TestEntry(unittest.TestCase):

    db = SqliteDatabase('test_entry_creation.db')
    employee_database.initialize(db)

    def setUp(self):
        self.test_entry = employee_database.Entry(
            first='Bill',
            last='Nye',
            task='science',
            time='90',
            notes='testing',
            date='2018-04-28',
        )

    def tearDown(self):
        pass

    def test_name_first(self):
        self.assertEqual(self.test_entry.first, 'Bill')

    def test_name_last(self):
        self.assertEqual(self.test_entry.last, 'Nye')

    def test_name_task(self):
        self.assertEqual(self.test_entry.task, 'science')

    def test_name_time(self):
        self.assertEqual(self.test_entry.time, '90')

    def test_name_notes(self):
        self.assertEqual(self.test_entry.notes, 'testing')

    def test_name_date(self):
        self.assertEqual(self.test_entry.date, '2018-04-28')

if __name__ == '__main__':

    with db:
        db.create_tables([employee_database.Employee], safe=True)
        unittest.main()
