import unittest
from unittest.mock import patch
import os
import sys
from peewee import *
import datetime

import employee_database



class TestEmployeeDB(unittest.TestCase):

    def test_space(self):
        spaces = employee_database.space()
        self.assertEqual(spaces, print('_' * 75))

    def test_initialize(self):
        self.assertTrue(employee_database.db.connect())

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

    @patch('builtins.input', return_value='1')
    def test_menu_selection_1(self, mock):
        result = employee_database.menu()
        self.assertEqual(result, '1')


    @patch('builtins.input', return_value='3')
    def test_menu_selection_3(self, mock):
        result = employee_database.menu()
        self.assertEqual(result, '3')

    @patch('employee_database.search_log', return_value='5')
    def test_search_log(self, input):
        self.assertEqual(employee_database.search_log(), '5')

def teardown():
    db.close()

if __name__ == '__main__':

    unittest.main()
