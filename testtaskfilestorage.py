import unittest
import taskfilestorage
import task
import os
import logging
import testtaskstorage

#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference
class TestTaskFileStorage(testtaskstorage.TestTaskStorage):
    def setUp(self):
        # Initialize task object with attributes
        self.my_task = task.Task('title', 'note')

        # Initialize test file names
        self.test_task_filename = 'testtaskfile'
        self.test_key_filename = 'testkeyfile'

        # Initialize file storage object using test-specific file names
        self.storage = taskfilestorage.TaskFileStorage(
            self.test_task_filename,
            self.test_key_filename
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
        open(self.test_task_filename, 'w').close()
        open(self.test_key_filename, 'w').close()

        print   # So output from tests is on a new linex

    def tearDown(self):
        # Delete test files
        os.remove(self.test_task_filename)
        os.remove(self.test_key_filename)

        # Clear the my_task Task object
        self.my_task = None

        # Remove handler so loggers aren't continuously created
        self.logger.removeHandler(self.stderr)


    def test_read(self):
        self.my_task.key = self.storage.add(self.my_task)
        task_list = self.storage.read()

        self.assertEqual(self.my_task, task_list[0])

    def test_write(self):
        self.storage.write([self.my_task])
        task_list = self.storage.read()

        self.assertEqual(self.my_task, task_list[0])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTaskFileStorage)
    unittest.TextTestRunner(verbosity=2).run(suite)
