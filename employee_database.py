import os, sys, datetime, pdb

from peewee import *


db = SqliteDatabase('employee_log.db')


def clear():
	"""clears command line"""
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')


def intialize():
	"""connects database and creates tables"""
	db.connect()
	db.create_tables([Employee], safe=True)


class Employee(Model):
	"""creates employee instance to be stored in database table with associaed 
	   field attributes(table columns)"""
	first_name = CharField()
	last_name = CharField()
	task_name = CharField()
	time_spent = CharField()
	task_notes = TextField()
	log_date = DateField(default=datetime.date.today)

	class Meta:
		"""meta class"""
		database = db


def menu():
	"""gives user option to add entry, search entries, or quit"""

	selection = None
	while selection != '1' or '2':
		print("\t\t\tMain menu\n\n\n")
		selection = input('''
1.) For a new task log enter 1.
2.) To search prior employee task logs enter  2.
3.) To quit enter 3.
\n>''')
		clear()
		try:
			selection = int(selection)
			if selection in list(range(1,4)):
				if selection in list(range(1,3)):
					selection = str(selection)
					return selection
				else:
					sys.exit()
			else:
				selection = str(selection)
				print('''{} is not a valid entry, select your desired option by entering a 
numerical value between 1-3.'''.format(selection))

		except ValueError:
			print('''Sorry {} is not an option, select your desired option by entering a
numerical value between 1-3.\n'''.format(selection))


def new_entry():
	"""allows user to enter new task log which includes user input for
	   first name, last name, task name, time spent, notes, date performed
	   """
	first = input("Enter your first name:\n>").title()
	clear()
	last = input("Enter your last name:\n>").title()
	clear()
	task = input("Enter the task name:\n>")
	clear()
	time = input("How much time was spent on your task in minutes:\n>")
	clear()
	notes = input("Enter any desired associated notes or enter none if you have no additiionl notes\n>")
	clear()
	date = input("Enter the date the task was worked on.\n (enter date as year-mm-dd-> ex.2018-04-28)\n>")

	if input("Confirm that would like to save your entry by entering yes, if you do not want to save enter no.\n>").lower() !='no':
		Employee.create(first_name=first, last_name=last, task_name=task, time_spent=time, task_notes=notes, log_date=date)
		clear()
		print("Sucessfully saved entry!\n")


def search_log():
	"""Allows user to search previous entries"""
	searching_entries = None
	while searching_entries != '5':
		searching_entries = input('''How would you like to search prior entries?\n
1.) To search by employee name enter 1.
2.) To search by entry date enter 2.
3.) To search by time spent on task (minutes) enter 3.
4.) To search by search term enter 4.
5.) Enter 5 to return to main menu.
\n>''')
		clear()
		if searching_entries == '1':
			#gives list of employee names with entries in database 
			full_name = Employee.select(Employee.first_name, Employee.last_name).get()
			print("Listed below are employee names with associated database entries:\n")
			for name in full_name.select():
				print(name.first_name + ' ' + name.last_name)
			print('\n')
			print('-' * 75)
			found_entries = Employee.select()
			prior_entries = input("Please enter the first or last name of the employee entry you would like to view.\n>").title()
			clear()
			entries = found_entries.where((Employee.first_name.contains(prior_entries))|(Employee.last_name.contains(prior_entries)))
			print("Entries related to your search section are listed below:\n")
			for entry in entries:
				timestamp = entry.log_date.strftime('%Y-%m-%d')
				print('''Employee name: {} {}
Task date: {}
Task name: {}
Time spent: {} minutes
Task notes: {}
'''.format(entry.first_name, entry.last_name, timestamp, entry.task_name, entry.time_spent, entry.task_notes))

		elif searching_entries == '2':
			lis =[]
			date_list = Employee.select(Employee.log_date)
			print("Listed below are all possible entry dates to search from:\n")
			for log in date_list:
				print(log.log_date)
			print('\n')
			found_entries = Employee.select()
			prior_entries = input("Please enter the journal entry date you would like to view.\n(enter date as year-mm-dd-> ex.2018-04-28)\n>")
			clear()
			entries = found_entries.where(Employee.log_date.contains(prior_entries))
			print("Entries related to your search section are listed below:\n")
			for entry in entries:
				timestamp = entry.log_date.strftime('%Y-%m-%d')
				print('''Employee name: {} {}
Task date: {}
Task name: {}
Time spent: {} minutes
Task notes: {}
'''.format(entry.first_name, entry.last_name, timestamp, entry.task_name, entry.time_spent, entry.task_notes))
		elif searching_entries == '3':
			found_entries = Employee.select()
			prior_entries = input("Enter the time (minutes) of the entry you would like to search.\n>")
			clear()
			entries = found_entries.where(Employee.time_spent.contains(prior_entries))
			print("Entries related to your search section are listed below:\n")
			for entry in entries:
				timestamp = entry.log_date.strftime('%Y-%m-%d')
				print('''Employee name: {} {}
Task date: {}
Task name: {}
Time spent: {} minutes
Task notes: {}
'''.format(entry.first_name, entry.last_name, timestamp, entry.task_name, entry.time_spent, entry.task_notes))
		elif searching_entries == '4':
			found_entries = Employee.select()
			prior_entries = input("Enter the search term you would like to use to search the employee database in regards to task name or notes:\n>")
			clear()
			entries = found_entries.where((Employee.task_name.contains(prior_entries))|(Employee.task_notes.contains(prior_entries)))
			print("Entries related to your search section are listed below:\n")
			for entry in entries:
				timestamp = entry.log_date.strftime('%Y-%m-%d')
				print('''Employee name: {} {}
Task date: {}
Task name: {}
Time spent: {} minutes
Task notes: {}
'''.format(entry.first_name, entry.last_name, timestamp, entry.task_name, entry.time_spent, entry.task_notes))

def menu_loop():
	while True:
		user_selection = menu()
		if user_selection == '1':
			new_entry()
		elif user_selection == '2':
			search_log()


if __name__=='__main__':
	intialize()
	menu_loop()




