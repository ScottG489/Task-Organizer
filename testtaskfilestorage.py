import unittest
import taskfilestorage
import task
import os

## Is there a simple way to test non-returning functions?
class TestTaskFileStorage(unittest.TestCase):
	def setUp(self):
		# Initialize task object with attributes
		self.my_task = task.Task('title', 'note')

		# Initialize test file names
		self.test_task_file_name = 'testtaskfile'
		self.test_key_file_name = 'testkeyfile'

		# Initialize file storage object using test-specific file names
		self.file_storage = taskfilestorage.TaskFileStorage(
			self.test_task_file_name,
			self.test_key_file_name
		)
		
		# Clear/Create test files
		temp_file_handler = open(self.test_task_file_name, 'w').close()
		temp_file_handler = open(self.test_key_file_name, 'w').close()

	def tearDown(self):
		# Delete test files
		os.remove(self.test_task_file_name)
		os.remove(self.test_key_file_name)
		
		# Clear the my_task Task object
		self.my_task = None


	def test_read(self):
		self.my_task.key = self.file_storage.add(self.my_task)
		task_list = self.file_storage.read()

		self.assertEqual(self.my_task, task_list[0])
	
	def test_write(self):
		self.file_storage.write([self.my_task])
		task_list = self.file_storage.read()
		
		self.assertEqual(self.my_task, task_list[0])

	def test_validate(self):
		self.my_task.key = self.file_storage.add(self.my_task)
		task_list = self.file_storage.read()

		self.assertTrue(self.file_storage.validate(task_list))


	def test_add(self):
		#new_task = self.my_task
		#self.my_task.key = self.file_storage.add(self.my_task)
		#new_task.key = self.file_storage.add(new_task)
		print self.file_storage.add(self.my_task)
		print self.file_storage.add(self.my_task)
		print self.file_storage.add(self.my_task)
		print self.file_storage.add(self.my_task)
		print self.file_storage.add(self.my_task)
		print self.file_storage.add(self.my_task)

		#self.my_task = self.file_storage.find(self.my_task.key)
		print self.my_task
		print '-----'
		#print new_task
		
		self.assertEqual(self.my_task.key, new_task.key - 1)
	
	def test_find(self):
		self.my_task.key = self.file_storage.add(self.my_task)
		new_task = self.file_storage.find(self.my_task.key)

		self.assertEqual(self.my_task, new_task)

	def test_update(self):
		self.my_task.key = self.file_storage.add(self.my_task)

		self.my_task.title = 'foo'
		key = self.file_storage.update(self.my_task)
		new_task = self.file_storage.find(key)

		self.assertEqual(self.my_task, new_task)

	def test_delete(self):
		self.my_task.key = self.file_storage.add(self.my_task)

		key = self.file_storage.delete(self.my_task.key)
		new_task = self.file_storage.find(key)

		self.assertIsNone(new_task)
	

if __name__ == '__main__':
	unittest.main()
