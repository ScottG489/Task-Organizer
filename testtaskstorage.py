import unittest
import task

#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference
class TestTaskStorage(unittest.TestCase):
    def setUp(self):
        self.my_task = None
        
        # Initialize file storage object using test-specific file names
        self.storage = None

    def tearDown(self):
        pass

    def test_read(self):
        pass

    def test_write(self):
        pass

    def test_add(self):
        self.my_task.key = self.storage.add(self.my_task)
        new_task = self.storage.find(self.my_task.key)
        new_task.key = self.storage.add(new_task)

        self.assertEqual(self.my_task.key, new_task.key - 1)

    def test_find(self):
        self.my_task.key = self.storage.add(self.my_task)
        new_task = self.storage.find(self.my_task.key)

        self.assertEqual(self.my_task, new_task)

    def test_find_all(self):
        self.my_task.key = self.storage.add(self.my_task)
        task_list = self.storage.find()

        self.assertEqual(task_list[0], self.my_task)

    def test_update(self):
        self.my_task.key = self.storage.add(self.my_task)

        self.my_task.title = 'foo'
        key = self.storage.update(self.my_task)
        new_task = self.storage.find(key)

        self.assertEqual(self.my_task, new_task)

    def test_delete(self):
        self.my_task.key = self.storage.add(self.my_task)

        key = self.storage.delete(self.my_task.key)
        new_task = self.storage.find(key)

        self.assertIsNone(new_task)

    def test_search(self):
        self.storage.add(self.my_task)
        search_task = task.Task(title='title', notes='note')
        task_search_list = self.storage.search(search_task)

        self.assertTrue(self.my_task in task_search_list)
        # Do a matching AND on all attributes given.
        # search(Task)
        # return task_list

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTaskStorage)
    unittest.TextTestRunner(verbosity=2).run(suite)
