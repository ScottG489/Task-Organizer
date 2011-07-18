import unittest
import task
import taskfilestorage
## Is ther a simple way to test non-returning functions?
class TestTaskFileStorage(unittest.TestCase):
	def setUp(self):
		self.my_task = task.Task()
		self.file_storage = taskfilestorage.TaskFileStorage()
		pass

	def test_add(self):
		#self.file_storage().add(my_task)
		pass
	
	def test_find(self):
		pass

if __name__ == '__main__':
	unittest.main()
