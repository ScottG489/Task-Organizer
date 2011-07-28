import unittest
import taskfilestorage
import task
import os
import logging

#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference
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

        self.logger = logging.getLogger()
        self.stderr = logging.StreamHandler()
        self.stderr.setLevel(logging.WARNING)
        self.formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s:%(name)s:'
                '%(module)s.%(funcName)s(): %(message)s'
        )
        self.stderr.setFormatter(self.formatter)
        self.logger.addHandler(self.stderr)

        # Clear/Create test files
        open(self.test_task_file_name, 'w').close()
        open(self.test_key_file_name, 'w').close()

        print   # So output from tests is on a new linex

    def tearDown(self):
        # Delete test files
        os.remove(self.test_task_file_name)
        os.remove(self.test_key_file_name)

        # Clear the my_task Task object
        self.my_task = None

        # Remove handler so loggers aren't continuously created
        self.logger.removeHandler(self.stderr)


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
        self.my_task.key = self.file_storage.add(self.my_task)
        new_task = self.file_storage.find(self.my_task.key)
        new_task.key = self.file_storage.add(new_task)

        self.assertEqual(self.my_task.key, new_task.key - 1)

    def test_find(self):
        self.my_task.key = self.file_storage.add(self.my_task)
        new_task = self.file_storage.find(self.my_task.key)

        self.assertEqual(self.my_task, new_task)

    def test_find_all(self):
        self.my_task.key = self.file_storage.add(self.my_task)
        task_list = self.file_storage.find()

        self.assertEqual(task_list[0], self.my_task)

    def test_update(self):
        self.my_task.key = self.file_storage.add(self.my_task)

        self.my_task.title = 'foo'
        key = self.file_storage.update(self.my_task)
        new_task = self.file_storage.find(key)
        print type(key)
        self.assertEqual(self.my_task, new_task)

    def test_delete(self):
        self.my_task.key = self.file_storage.add(self.my_task)

        key = self.file_storage.delete(self.my_task.key)
        new_task = self.file_storage.find(key)

        self.assertIsNone(new_task)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTaskFileStorage)
    unittest.TextTestRunner(verbosity=2).run(suite)
