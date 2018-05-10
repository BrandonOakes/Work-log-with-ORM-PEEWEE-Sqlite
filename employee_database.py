import os, sys, datetime, pdb, re

from peewee import *


db = SqliteDatabase('employee_log.db')


def clear():
	"""clears command line"""
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')

def space():
	 print('_' * 75)

def initialize():
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
				if selection == 1:
					selection = str(selection)
					return selection
				elif selection == 2:
					lis = []
					data = Employee.select(Employee.first_name,Employee.last_name, Employee.task_name, Employee.task_notes)
					for item in data:
						lis.append(item)
					if len(lis) >= 1:
						selection = str(selection)
						return selection
					else:
						print('''There are no entries in the database,
to enter a new employee log press 1, to quit press 3''')
						space()
				else:
					sys.exit()
			else:
				selection = str(selection)
				print('''{} is not a valid entry, select your desired option by entering a
numerical value between 1-3.'''.format(selection))

		except ValueError:
			print('''Sorry {} is not an option, select your desired option by entering a
numerical value between 1-3.\n'''.format(selection))

class Entry():
	"""allows user to enter new task log which includes user input for
	   first name, last name, task name, time spent, notes, date performed
	   """

	def __init__(self, first=None, last=None, task=None, time=None, notes=None, date=None):
		self.first = first
		self.last = last
		self.task = task
		self.time = time
		self.notes = notes
		self.date = date

	def name_first(self):
		self.first = input("Enter your first name:\n>").title()
		clear()
		return self.first

	def name_last(self):
		self.last = input("Enter your last name:\n>").title()
		clear()
		return self.last

	def name_task(self):
		self.task = input("Enter the task name:\n>")
		clear()
		return self.task

	def name_time(self):

		value = True
		while value:
			self.time = input("How much time was spent on your task in minutes:\n> ")
			try:
				int(self.time)
				str(self.time)
				clear()
				return self.time
				value = False
			except ValueError:
				clear()
				print(f"""{self.time} is not a valid entry,
please enter time spent in minutes with a numerical value
(ex. 30)\n""")
		clear()

	def name_notes(self):

		self.notes = input("Enter any desired associated notes or enter none if you have no additiionl notes\n>")
		clear()
		return self.notes

	def name_date(self):

		choice = True
		while choice:
			self.date = input("Enter the date the task was worked on.\n (enter date as year-mm-dd-> ex.2018-04-28)\n> ")
			regexpattern = re.compile(r"\w{4}-\w{2}-\w{2}")
			correct_response = regexpattern.findall(self.date)
			if len(correct_response) >= 1:
				clear()
				choice = False
				return self.date
				clear()
			else:
				clear()
				print(f"""{self.date} is not a valid entry:
(enter date as year-mm-dd-> ex.2018-04-28)\n\n>""")
				space()

	def entry_displayed(self):
		print(f"""Entry:\n
First name: {self.first}
Last name: {self.last}
Task name: {self.task}
Time spent: {self.time} minutes
Notes: {self.notes}
Date: {self.date} \n""")
		space()
		if input("Confirm that would like to save your entry by entering yes, if you do not want to save enter no.\n ").lower() !='no':
			Employee.create(first_name=self.first, last_name=self.last, task_name=self.task, time_spent=self.time, task_notes=self.notes, log_date=self.date)
			clear()
			print("Sucessfully saved entry!\n")
		else:
			clear()

def process_entry():

	entry = Entry()
	entry.name_first()
	entry.name_last()
	entry.name_task()
	entry.name_time()
	entry.name_notes()
	entry.name_date()
	entry.entry_displayed()


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
\n> ''')
		if searching_entries in ['1', '2', '3', '4', '5']:
			clear()
			return searching_entries
		elif searching_entries not in ["1", "2", "3", "4", "5"]:
			clear()
			print(f"""Sorry {searching_entries} is not a valid response,
please choose between 1-5 for your desired selection
__________________________________________________""")
			space()

class Search():

	def __init__(self, entries=None, prior_entries=None):
		self.entries= entries
		self.prior_entries = prior_entries

	def search_name(self):
			"""gives list of employee names with entries in database"""
			duplicates = []
			full_name = Employee.select(Employee.first_name, Employee.last_name).get()
			print("Listed below are employee names with associated database entries:\n")
			for name in full_name.select():
				print(name.first_name + ' ' + name.last_name)
			print('\n')
			space()
			found_entries = Employee.select()
			self.prior_entries = input("Please enter the first or last name of the employee entry you would like to view.\n> ").title()
			clear()
			self.entries = found_entries.where((Employee.first_name == self.prior_entries)|(Employee.last_name == self.prior_entries))
			if len(self.entries) >=1:
				return self.entries

	def search_date(self):
		lis =[]
		date_list = Employee.select(Employee.log_date)
		for logs in date_list:
			logs = logs.log_date.strftime('%Y-%m-%d')
			if logs not in lis:
				lis.append(logs)
			else:
				continue
		choice = True
		while choice:
			print("Listed below are all possible entry dates to search from:\n")
			for log in lis:
				print(log)
			print('\n')
			found_entries = Employee.select()
			self.prior_entries = input("""Please enter the entry date you would like to view.
\n(enter date as year-mm-dd-> ex.2018-04-28)\n\n >""")
			regexpattern = re.compile(r"\w{4}-\w{2}-\w{2}")
			correct_response = regexpattern.findall(self.prior_entries)
			if len(correct_response) >= 1:
				choice = False
				clear()
			else:
				clear()
				print(f"""{self.prior_entries} is not a valid entry:
(enter date as year-mm-dd-> ex.2018-04-28)\n\n>""")
				space()

		clear()
		self.entries = found_entries.where(Employee.log_date == self.prior_entries)
		return self.entries

	def search_time(self):
		duplicates = []
		times = Employee.select(Employee.time_spent).get()
		print("Listed below are employee time logs with associated database entries:\n")
		for time in times.select():
			if time.time_spent == '1':
				print(time.time_spent + ' minute')
			else:
				print(time.time_spent + ' minutes')
		print('\n')
		space()
		found_entries = Employee.select()
		self.prior_entries = input("Enter the time (minutes) of the entry you would like to search.\n>")
		clear()
		self.entries = found_entries.where(Employee.time_spent == self.prior_entries)
		if len(self.entries) >=1:
			return self.entries

	def search_pattern(self):
		found_entries = Employee.select()
		self.prior_entries = input("""Enter the search term you would like to use
to search the employee database in regards to task name or notes:\n> """)
		clear()
		self.entries = found_entries.where((Employee.task_name.contains(self.prior_entries))|(Employee.task_notes.contains(self.prior_entries)))
		if len(self.entries) >=1:
			return self.entries

	def search_display(self):
		if len(self.entries) >=1:
			print("Entries related to your search section are listed below:\n")
			for entry in self.entries:
				timestamp = entry.log_date.strftime('%Y-%m-%d')
				print('''Employee name: {} {}
	Task date: {}
	Task name: {}
	Time spent: {} minutes
	Task notes: {}
	'''.format(entry.first_name, entry.last_name, timestamp, entry.task_name, entry.time_spent, entry.task_notes))
			input("Press Enter to continue: ")
			clear()
		else:
			print(f"""{self.prior_entries} was not found in the database.
	\n""")

def process_search():
	search_choice = search_log()
	search_object = Search()
	if search_choice == "1":
		search_object.search_name()
	elif search_choice == '2':
		search_object.search_date()
	elif search_choice == '3':
		search_object.search_time()
	elif search_choice == '4':
		search_object.search_pattern()
	search_object.search_display()

def menu_loop():
	while True:
		user_selection = menu()
		if user_selection == '1':
			process_entry()
		elif user_selection == '2':
			process_search()



if __name__=='__main__':
	initialize()
	menu_loop()
