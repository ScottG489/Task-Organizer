import pickle
import task
import re

file_name = 'taskfile'

class TaskFileStorage():
#TODO:Add error handing for malformed file
#	* Make private?
#	* Make it return an empty list instead of raise?
#   * Duplicate functionality of read() in TaskFileStorage?
	def read(self):
		task_file = open(file_name, 'r')
		try:
			task_list = pickle.load(task_file)
			task_file.close()
		except (EOFError, IOError):	#EOFError: empty file IOError: no file
			raise
		
		return task_list

#TODO:Make private?
	def write(self, task_list):
		task_file = open(file_name, 'w')
		pickle.dump(task_list, task_file, 0)
		task_file.close()

#TODO:Auto create ID's (make KeyGenerator class)
	def add(self, task_item):
		try:
			task_list = self.read()
		except (EOFError, IOError):	#No tasks
			task_list = []

		task_list.append(task_item)
		self.write(task_list)

	def find(self, regex):
		match_list = []
		try:
			task_list = self.read()
		except (EOFError, IOError):	#No tasks
			return match_list
		
##TODO:Validate the input regular expression here or somewhere
		for task_item in task_list:
			if re.search(r'' + regex + '', task_item.title):
				match_list.append(task_item)

		return match_list
	def delx(self):
		pass
