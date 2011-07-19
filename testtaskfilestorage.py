import unittest
import taskfilestorage
import task
import pickle

## Is there a simple way to test non-returning functions?
class TestTaskFileStorage(unittest.TestCase):
	def setUp(self):
		
		pass
	
	def test_read(self):
#		file_storage = taskfilestorage.TaskFileStorage()
#		file_storage.file_name
#		task_file = open(file_storage.file_name, 'r')
#		task_file.close()
#		task_list = pickle.load(task_file)
#		self.assertEqual(task_list, file_storage.read())
		pass

	def test_add(self):
		my_task = task.Task()
		my_task.title = 'title'
		my_task.notes = 'note'
		file_storage = taskfilestorage.TaskFileStorage()
		id = file_storage.add(my_task)
		new_task = file_storage.find(id)

	
	def test_find(self):
		pass

if __name__ == '__main__':
	unittest.main()
