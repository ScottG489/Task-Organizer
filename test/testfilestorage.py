import unittest
import teststorage
import filestorage
import task
import os
import logging

#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference
class TestFileStorage(teststorage.TestStorage):
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
            level=logging.WARNING
            ,
            format='[%(asctime)s] %(levelname)s:%(name)s:'
            '%(module)s.%(funcName)s(): %(message)s'
        )

        print   # So output from tests is on a new linex

    def tearDown(self):
        # Delete test files
        os.remove(self.test_task_filename)
        os.remove(self.test_key_filename)

        # Clear the my_task Task object
        self.my_task = None

    def test_add_read_fail(self):
        """Tests add()'s handling of failed file reading"""
        file_handler = open(self.test_task_filename, 'w')
        file_handler.write('Mock corrupt data')
        file_handler.close()
        os.chmod(self.test_task_filename, 000)

        self.assertRaises(IOError, self.storage.add, self.my_task)

    def test_add_write_fail(self):
        """Tests add()'s handling of failed file writing"""
        os.chmod(self.test_task_filename, 0400)

        self.assertRaises(IOError, self.storage.add, self.my_task)

    def test_find_read_fail(self):
        """Tests find()'s handling of failed file reading"""
        file_handler = open(self.test_task_filename, 'w')
        file_handler.write('Mock corrupt data')
        file_handler.close()
        os.chmod(self.test_task_filename, 000)

        self.assertRaises(IOError, self.storage.find, self.my_task)

    def test_get_all_read_fail(self):
        """Tests get_all()'s handling of failed file reading"""
        file_handler = open(self.test_task_filename, 'w')
        file_handler.write('Mock corrupt data')
        file_handler.close()
        os.chmod(self.test_task_filename, 000)

        self.assertRaises(IOError, self.storage.get_all)

    def test_update_write_fail(self):
        """Tests update()'s handling of failed file writing"""
        self.storage.add(self.my_task)
        os.chmod(self.test_task_filename, 0400)

        self.assertRaises(IOError, self.storage.update, self.my_task)

    def test_delete_write_fail(self):
        """Tests delete()'s handling of failed file writing"""
        self.storage.add(self.my_task)
        os.chmod(self.test_task_filename, 0400)

        self.assertRaises(IOError, self.storage.delete, self.my_task.key)

    def test_search_not_found(self):
        """Tests search()'s behavior when no match is found"""
        self.storage.add(self.my_task)
        search_task = task.Task(title='title1', notes='note1')
        task_search_list = self.storage.search(search_task)

        self.assertEqual(task_search_list, None)

    def test_read(self):
        """Tests that read() correctly reads and returns the file contents"""
        self.my_task.key = self.storage.add(self.my_task)
        task_list = self.storage.read()

        self.assertEqual(self.my_task, task_list[0])

    def test_read_corrupt(self):
        """Tests read()'s handling of a corrupt file"""
        file_handler = open(self.test_task_filename, 'w')
        file_handler.write('Mock corrupt data')
        file_handler.close()

        self.assertRaises(KeyError, self.storage.read)

    def test_read_permission_fail(self):
        """Tests read()'s handling of denied file read permissions"""
        file_handler = open(self.test_task_filename, 'w')
        file_handler.write('Mock corrupt data')
        file_handler.close()

        os.chmod(self.test_task_filename, 000)
        # TODO: Make this assert it's errno 13 (Permission denied)
        self.assertRaises(IOError, self.storage.read)

    def test_write(self):
        """Tests that write() correctly writes to the file"""
        self.storage.write([self.my_task])
        task_list = self.storage.read()

        self.assertEqual(self.my_task, task_list[0])

    def test_write_permission_fail(self):
        """Tests write()'s handling of denied file write permissions"""
        os.chmod(self.test_task_filename, 000)

        self.assertRaises(IOError, self.storage.write, [self.my_task])


if __name__ == '__main__':
#    unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileStorage)
    unittest.TextTestRunner(verbosity=2).run(suite)
