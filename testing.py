import unittest
from unittest.mock import patch

import employee_database

class TestEmployeeDB(unittest.TestCase):


	def test_space(self):
		spaces = employee_database.space()
		self.assertEqual(spaces, print('_' * 75))

	@patch('employee_database.search_log', return_value = '5')
	def test_search_log(self, input):
		self.assertEqual(employee_database.search_log(), '5')

	@patch('employee_database.Entry.name_first', return_value = 'Brandon')
	def test_new_first_name(self, input):
		self.assertEqual(employee_database.Entry.name_first(), 'Brandon')

	@patch('employee_database.Entry.name_last', return_value = 'Gonzo')
	def test_new_last_name(self, input):
		self.assertEqual(employee_database.Entry.name_last(), 'Gonzo')

	@patch('employee_database.Entry.name_task', return_value = 'Python')
	def test_new_task(self, input):
		self.assertEqual(employee_database.Entry.name_task(), 'Python')

	@patch('employee_database.Entry.name_notes', return_value = 'testing')
	def test_new_notes(self, input):
		self.assertEqual(employee_database.Entry.name_notes(), 'testing')

	@patch('employee_database.Entry.name_date', return_value = '2018-04-28')
	def test_new_date(self,input):
		self.assertEqual(employee_database.Entry.name_date(), '2018-04-28')

	@patch('employee_database.menu', return_value = '1')
	def test_menu(self, input):
		self.assertEqual(employee_database.menu(), '1')

	


if __name__ == '__main__':
    unittest.main()
