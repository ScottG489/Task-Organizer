import task
import pickle
import keygenerator
import os

class TaskFileStorage():
	def __init__(self, task_file_name='taskfile', key_file_name='keyfile'):
		self.task_file_name = task_file_name
		self.key_file_name = key_file_name

	#TODO:Make private?
	#	* raise more informative messages? (ex. if path exists as a dir)
	def read(self):
		try:
			# Try to open file for reading
			task_file = open(self.task_file_name, 'r')
			# Try to load task_list
			try:
				task_list = pickle.load(task_file)
				task_file.close()
				# Try to validate file contents.
				try:
					self.validate(task_list)
				# If file is not valid; raise
				except TypeError:
					raise
			# If task list won't load, check if it's empty
			except:
				# If the file is empty there are no tasks; return empty list
				if os.stat(self.task_file_name).st_size == 0:
					task_list = []
				# If also not empty, file is in an unreadable format; raise
				else:
					raise
		# If file won't open for reading, check that it exists as a file
		except:
			# If path doesn't exist as a file, create it and return empty list
			if not os.path.exists(self.task_file_name):
				temp_file_handler = open(self.task_file_name, 'w').close()
				task_list = []
			# If it also exists then we can't use it; raise.
			else:
				raise

		return task_list

	#TODO:Make private?
	def write(self, task_list):
		try:
			# Try to open file for	writing 
			task_file = open(self.task_file_name, 'w')
			# Try to load task_list
			try:
				temp_task_list = pickle.load(task_file)
				task_file.close()
				# Try to validate file contents.
				try:
					self.validate(temp_task_list)
				# If file is not valid; raise
				except TypeError:
					raise
				# If the file is valid, write to it
				pickle.dump(task_list, task_file, 0)
			# If task list won't load, check if it's empty
			except:
				# If the file is empty there are no tasks to validate
				if os.stat(self.task_file_name).st_size == 0:
					pickle.dump(task_list, task_file, 0)
				# If also not empty, file is in an unreadable format; raise
				else:
					raise
		# If file won't open for writing, we can't do anything; raise
		except:
			raise


	def validate(self, task_list):
		for item in task_list:
			if not isinstance(item, task.Task):
				raise TypeError('invalid or corrupt task file')
		return True

	#TODO:Auto create ID's (make KeyGenerator class)
	def add(self, task_item):
		try:
			task_list = self.read()
		except:
			raise

		key_gen = keygenerator.KeyGenerator(self.key_file_name)
		task_item.key = key_gen.get()

		task_list.append(task_item)
		try:
			self.write(task_list)
		except:
			raise

		return task_item.key

	#TODO:Validate the input regular expression here or somewhere
	#	* Return a task instead of a list when key is specified?
	def find(self, key):
		task_item = None

		try:
			task_list = self.read()
		except:
			raise
		
		for task_item in task_list:
			if key == task_item.key:
				return task_item

		return task_item

	def update(self, task_item):
		pass
	#	return key

	def delete(self, key):
		pass
#		return key
