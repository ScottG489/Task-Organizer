import unittest
import teststorage
import filestorage
import task
import os
import logging

#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference
class TestTaskFileStorage(teststorage.TestStorage):
    def setUp(self):
        # Initialize task object with attributes
        self.my_task = task.Task(title='title', notes='note')

        # Initialize test file names
        self.test_task_filename = 'testtaskfile'
        self.test_key_filename = 'testkeyfile'

        # Initialize file storage object using test-specific file names
        self.storage = filestorage.FileStorage(
            self.test_task_filename,
            self.test_key_filename
        )

        logging.basicConfig(
            level=logging.WARNING,
            format='[%(asctime)s] %(levelname)s:%(name)s:'
            '%(module)s.%(funcName)s(): %(message)s'
        )

        # Clear/Create test files
        open(self.test_task_filename, 'w').close()
        open(self.test_key_filename, 'w').close()

        #print   # So output from tests is on a new linex

    def tearDown(self):
        # Delete test files
        os.remove(self.test_task_filename)
        os.remove(self.test_key_filename)

        # Clear the my_task Task object
        self.my_task = None


    def test_read(self):
        self.my_task.key = self.storage.add(self.my_task)
        task_list = self.storage.read()

        self.assertEqual(self.my_task, task_list[0])

# TODO: Not sure why this doesn't work.
#    def test_read_fail(self):
#        file_handler = open(self.test_task_filename, 'w')
#        file_handler.write('Mock corrupt data')
#        file_handler.close()
#
#        self.assertRaises(KeyError, self.storage.read())

    def test_write(self):
        self.storage.write([self.my_task])
        task_list = self.storage.read()

        self.assertEqual(self.my_task, task_list[0])


if __name__ == '__main__':
    unittest.main()
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestTaskFileStorage)
#    unittest.TextTestRunner(verbosity=2).run(suite)
