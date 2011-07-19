import pickle
import re
import keygenerator

class TaskFileStorage():
	def __init__(self):
		self.file_name = 'taskfile'

#TODO:Add error handing for malformed file
#	* Make private?
#	* Make it return an empty list instead of raise?
#   * Duplicate functionality of read() in TaskFileStorage?
	def read(self):
		task_file = open(self.file_name, 'r')
		try:
			task_list = pickle.load(task_file)
			task_file.close()
		except (EOFError, IOError):	#EOFError: empty file IOError: no file
			raise
		
		return task_list

#TODO:Make private?
	def write(self, task_list):
		task_file = open(self.file_name, 'w')
		pickle.dump(task_list, task_file, 0)
		task_file.close()

#TODO:Auto create ID's (make KeyGenerator class)
	def add(self, task_item):
		try:
			task_list = self.read()
		except (EOFError, IOError):	#No tasks
			task_list = []

		key_gen = keygenerator.KeyGenerator()
		task_item.id = key_gen.get_key()
		
		task_list.append(task_item)
		self.write(task_list)

		return task_item.id

#TODO:Validate the input regular expression here or somewhere
#	* Return an int instead of a list when id is specified?
	def find(self, regex=None, id=None):
		if regex and id:
			raise TypeError('find() takes exactly 1 argument (2 given)')
		match_list = []
		try:
			task_list = self.read()
		except (EOFError, IOError):	#No tasks
			return match_list
		
		if regex != None:
			for task_item in task_list:
				if re.search(r'' + regex + '', task_item.title):
					match_list.append(task_item)
		elif id != None:
			for task_item in task_list:
				if id == task_item.id:
					match_list.append(task_item)


		return match_list
	def delx(self):
		pass
