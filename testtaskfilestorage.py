import unittest
import taskfilestorage
import keygenerator
import pickle
import task
import os

## Is there a simple way to test non-returning functions?
class TestTaskFileStorage(unittest.TestCase):
	def setUp(self):
		self.my_task = task.Task()
		self.file_storage = taskfilestorage.TaskFileStorage()
		self.key_gen = keygenerator.KeyGenerator()
		try:
			os.remove(self.file_storage.file_name)
		except:
			pass
		try:
			os.remove(self.key_gen.file_name)
		except:
			pass
	
#	def test_read(self):
#		file_storage = taskfilestorage.TaskFileStorage()
#		file_storage.file_name
#		task_file = open(file_storage.file_name, 'r')
#		task_file.close()
#		task_list = pickle.load(task_file)
#		self.assertEqual(task_list, file_storage.read())
#		pass

	def test_add(self):
		my_task = task.Task()
		my_task.title = 'title'
		my_task.notes = 'note'

		key = self.file_storage.add(my_task)

		task_file = open(self.file_storage.file_name, 'r')
		new_task = pickle.load(task_file)

		self.assertEqual(my_task.key, new_task[0].key, key)
	
	def test_find(self):
		pass

if __name__ == '__main__':
	unittest.main()
