import unittest
import taskstorage
import task
import os
import sys
import logger
import logging

logger.LOG.setLevel(logging.CRITICAL)


#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference
#       Delete added tasks in tearDown()
class TestStorage(unittest.TestCase):
    def test_add(self):
        """Tests that add() correctly adds a Task to storage"""
        self.my_task.key = self.storage.add(self.my_task)
        new_task = self.storage.find(self.my_task.key)
        new_task.key = self.storage.add(new_task)

        self.assertNotEqual(self.my_task.key, new_task.key)
        self.storage.delete(new_task.key)

    def test_find(self):
        """Tests that find() correctly returns a Task given a key"""
        self.my_task.key = self.storage.add(self.my_task)
        new_task = self.storage.find(self.my_task.key)

        self.assertEqual(self.my_task, new_task)

    def test_get_all(self):
        """Tests that get_all() returns a list of all Tasks"""
        self.my_task.key = self.storage.add(self.my_task)
        task_list = self.storage.get_all()

        self.assertEqual(task_list[0], self.my_task)

    def test_update(self):
        """Tests that update() correctly updates a Task given a Task"""
        self.my_task.key = self.storage.add(self.my_task)

        self.my_task.title = 'foo'
        key = self.storage.update(self.my_task)
        new_task = self.storage.find(key)

        self.assertEqual(self.my_task, new_task)

    def test_update_no_match(self):
        """Tests updates()'s handling of no matching key"""
        self.my_task.key = self.storage.add(self.my_task)

        self.storage.delete(self.my_task.key)

        self.my_task.title = 'foo'

        self.key = self.storage.update(self.my_task)

        self.assertIsNone(self.key)

    def test_delete(self):
        """Tests that delete() correctly deletes a Task from storage"""
        new_task = task.Task()
        self.my_task.key = self.storage.add(self.my_task)

        key = self.storage.delete(self.my_task.key)
        new_task = self.storage.find(key)

        self.assertIsNone(new_task)

    def test_delete_no_match(self):
        """Tests delete()'s handling of no matching key"""
        self.my_task.key = self.storage.add(self.my_task)

        self.storage.delete(self.my_task.key)

        self.key = self.storage.delete(self.my_task.key)

        self.assertIsNone(self.key)

    def test_search(self):
        """Tests that search() correctly returns a matching Task given a Task"""
        self.storage.add(self.my_task)
        search_task = task.Task(title='title', notes='note')
        task_search_list = self.storage.search(search_task)

        self.assertTrue(self.my_task in task_search_list)
        #TODO: Do a matching AND on all attributes given.
        # search(Task)
        # return task_list


#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference

class TestFileStorage(TestStorage):
    def setUp(self):
        # Initialize task object with attributes
        self.my_task = task.Task(title='title', notes='note')

        # Initialize test file names
        self.test_task_filename = 'testtaskfile'
        self.test_key_filename = 'testkeyfile'

        # Initialize file storage object using test-specific file names
        self.storage = taskstorage.FileStorage(
            self.test_task_filename,
            self.test_key_filename
        )

        try:
            if sys.argv[1] == '-v':
                sys.stderr.write()   # So output from tests is on a new linex
        except:
            pass

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
        task_list = self.storage._read()

        self.assertEqual(self.my_task, task_list[0])

    def test_read_corrupt(self):
        """Tests read()'s handling of a corrupt file"""
        file_handler = open(self.test_task_filename, 'w')
        file_handler.write('Mock corrupt data')
        file_handler.close()

        self.assertRaises(KeyError, self.storage._read)

    def test_read_permission_fail(self):
        """Tests read()'s handling of denied file read permissions"""
        file_handler = open(self.test_task_filename, 'w')
        file_handler.write('Mock corrupt data')
        file_handler.close()

        os.chmod(self.test_task_filename, 000)
        # TODO: Make this assert it's errno 13 (Permission denied)
        self.assertRaises(IOError, self.storage._read)

    def test_write(self):
        """Tests that write() correctly writes to the file"""
        self.storage._write([self.my_task])
        task_list = self.storage._read()

        self.assertEqual(self.my_task, task_list[0])

    def test_write_permission_fail(self):
        """Tests write()'s handling of denied file write permissions"""
        os.chmod(self.test_task_filename, 000)

        self.assertRaises(IOError, self.storage._write, [self.my_task])



#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference
class TestGTaskStorage(TestStorage):
    def setUp(self):
        # Initialize task object with attributes
        self.my_task = task.Task(title='title', notes='note')

        # Initialize file storage object using test-specific file names
        self.storage = taskstorage.GTaskStorage()

        print_helper()

    def tearDown(self):
        self.storage.delete(self.my_task.key)

        # Clear the my_task Task object
        self.my_task = None

    def test_update_no_note(self):
        """Tests that update() acts correctly when no note is specified"""
        self.my_task.notes = None
        self.my_task.key = self.storage.add(self.my_task)

        self.my_task.title = 'foo'
        key = self.storage.update(self.my_task)
        new_task = self.storage.find(key)

        self.assertEqual(self.my_task, new_task)


## Is there a simple way to test non-returning functions?
class TestKeyGenerator(unittest.TestCase):
    def setUp(self):
        # Initialize test file names
        self.test_key_filename = 'testkeyfile'

        # Initialize file storage object using test-specific file names
        self.key_gen = taskstorage._KeyGenerator(
            self.test_key_filename
        )


        # Clear/Create test files
        open(self.test_key_filename, 'w').close()

        print_helper()

    def tearDown(self):
        # Delete test files
        os.remove(self.test_key_filename)


    def test_read(self):
        """Tests that read() correctly reads and returns the file contents"""
        key = self.key_gen.get()
        key2 = self.key_gen._read()

        self.assertEqual(key, key2 - 1)

    def test_read_corrupt(self):
        """Tests read()'s handling of a corrupt file"""
        file_handler = open(self.test_key_filename, 'w')
        file_handler.write('Mock corrupt data')
        file_handler.close()

        self.assertRaises(ValueError, self.key_gen._read)

    def test_write(self):
        """Tests that write() correctly writes to the file"""
        key = self.key_gen.get()
        self.key_gen._write(key)
        key2 = self.key_gen._read()

        self.assertEqual(key, key2)

    def test_write_permission_fail(self):
        """Tests write()'s handling of denied file write permissions"""
        os.chmod(self.test_key_filename, 000)

        self.assertRaises(IOError, self.key_gen._write, 0)

    def test_get(self):
        """Tests that get() updates and returns the correct key"""
        key = self.key_gen.get()
        key2 = self.key_gen.get()

        self.assertEqual(key, key2 - 1)

    def test_get_read_fail(self):
        """Tests add()'s handling of failed file reading"""
        file_handler = open(self.test_key_filename, 'w')
        file_handler.write('Mock corrupt data')
        file_handler.close()
        os.chmod(self.test_key_filename, 000)

        self.assertRaises(IOError, self.key_gen.get)

    def test_get_write_fail(self):
        """Tests get()'s handling of failed file writing"""
        os.chmod(self.test_key_filename, 0400)

        self.assertRaises(IOError, self.key_gen.get)

    def test_update(self):
        """Tests that update() correctly updates and writes key"""
        key = self.key_gen.get()
        key2 = self.key_gen._update(key)

        self.assertEqual(key, key2 - 1)

    def test_update_write_fail(self):
        """Tests update()'s handling of failed file writing"""
        os.chmod(self.test_key_filename, 0400)

        self.assertRaises(IOError, self.key_gen._update, 0)


#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference
class TestSQLiteStorage(TestStorage):
    def setUp(self):
        # Initialize task object with attributes
        self.my_task = task.Task(title='title', notes='note')

        # Initialize test database name
        self.test_task_dbname = 'testtaskdb'

        # Initialize file storage object using test-specific file names
        self.storage = taskstorage.SQLiteStorage(
            self.test_task_dbname)

        print_helper()

    def tearDown(self):
        # Delete test database
        os.remove(self.test_task_dbname)

        # Clear the my_task Task object
        self.my_task = None

def verbosity_helper():
    verbosity = 1
    try:
        if sys.argv[1] == '-v':
            verbosity = 2
    except:
        pass

    return verbosity

def print_helper():
    try:
        if verbosity_helper() == 2:
            sys.stderr.write()   # So output from tests is on a new linex
    except:
        pass

if __name__ == '__main__':
    verbosity = verbosity_helper()

    suite = unittest.TestLoader().loadTestsFromTestCase(TestSQLiteStorage)
    unittest.TextTestRunner(verbosity=verbosity).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestKeyGenerator)
    unittest.TextTestRunner(verbosity=verbosity).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFileStorage)
    unittest.TextTestRunner(verbosity=verbosity).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGTaskStorage)
    unittest.TextTestRunner(verbosity=verbosity).run(suite)
