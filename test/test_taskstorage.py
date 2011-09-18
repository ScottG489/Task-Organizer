import unittest
import taskstorage
import task
import os
import util


#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference
#       Delete added tasks in tearDown()
# TODO: self.my_task.key needs to be assiged so tearDown
#       can delete self.my_task.key
class TestStorage(unittest.TestCase):
    """Abstract tests for the child classes of the Storage class

    This abstract test case's functions should be called only through a
    child test case.

    """
    # pylint: disable=R0904
    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)
        self.storage = None
        self.my_task = None

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

    def test_search_not_found(self):
        """Tests search()'s behavior when no match is found"""
        self.storage.add(self.my_task)
        search_task = task.Task(title='title1', notes='note1')
        task_search_list = self.storage.search(search_task)

        self.assertEqual(task_search_list, None)

class TestGenericStorage(unittest.TestCase):
    """Tests the Storage abstract base class directly

    Tests that Storage abstract base class handles direct instantiations.

    """
    # pylint: disable=R0904
    def setUp(self):    # pylint: disable=C0103
        self.my_task = task.Task(title='title', notes='note')
        self.storage_instance = taskstorage.Storage()

    def tearDown(self):    # pylint: disable=C0103
        pass

    def test_not_implemented(self):
        """Tests error handling in storage's abstract functions"""
        self.assertRaises(
                NotImplementedError,
                self.storage_instance.add,
                self.my_task)
        self.assertRaises(
                NotImplementedError,
                self.storage_instance.find,
                self.my_task.key)
        self.assertRaises(
                NotImplementedError,
                self.storage_instance.get_all)
        self.assertRaises(
                NotImplementedError,
                self.storage_instance.update,
                self.my_task)
        self.assertRaises(
                NotImplementedError,
                self.storage_instance.delete,
                self.my_task.key)
        self.assertRaises(
                NotImplementedError,
                self.storage_instance.search,
                self.my_task)

#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference

class TestFileStorage(TestStorage):
    """Tests specific to the FileStorage class

    Tests that only apply to the implementation of the FileStorage class and
    not other storage types.

    """
    # pylint: disable=R0904
    def __init__(self, method_name):
        TestStorage.__init__(self, method_name)

    def setUp(self):    # pylint: disable=C0103
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

        util.print_helper()

    def tearDown(self):    # pylint: disable=C0103
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



#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference
class TestSQLiteStorage(TestStorage):
    """Tests specific to the SQLiteStorage class

    Tests that only apply to the implementation of the SQLiteStorage class and
    not other storage types.

    """
    # pylint: disable=R0904
    def __init__(self, method_name):
        TestStorage.__init__(self, method_name)

    def setUp(self):    # pylint: disable=C0103
        # Initialize task object with attributes
        self.my_task = task.Task(title='title', notes='note')

        # Initialize test database name
        self.test_task_dbname = 'testtaskdb'

        # Initialize file storage object using test-specific file names
        self.storage = taskstorage.SQLiteStorage(
            self.test_task_dbname)

        util.print_helper()

    def tearDown(self):    # pylint: disable=C0103
        # Delete test database
        os.remove(self.test_task_dbname)

        # Clear the my_task Task object
        self.my_task = None


#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference
class TestGTaskStorage(TestStorage):
    """Tests specific to the GTaskStorage class

    Tests that only apply to the implementation of the GTaskStorage class and
    not other storage types.

    """
    # pylint: disable=R0904
    def __init__(self, method_name):
        TestStorage.__init__(self, method_name)

    def setUp(self):    # pylint: disable=C0103
        # Initialize task object with attributes
        self.my_task = task.Task(title='title', notes='note')

        # Initialize file storage object using test-specific file names
        self.storage = taskstorage.GTaskStorage()

        util.print_helper()

    def tearDown(self):    # pylint: disable=C0103
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



# TODO: How to test _update()'s failed write?
#       _update will never fail because get() will never call it if it's
#       call to write() has failed. Maybe add an assert in _update?
class TestKeyGenerator(unittest.TestCase):
    """Tests for the KeyGenerator class

    Tests the public methods of the KeyGenerator class used by the FileStorage
    class.

    """
    # pylint: disable=R0904
    def setUp(self):    # pylint: disable=C0103
        # Initialize test file names
        self.test_key_filename = 'testkeyfile'

        # Initialize file storage object using test-specific file names
        self.key_gen = taskstorage._KeyGenerator(
            self.test_key_filename
        )


        # Clear/Create test files
        open(self.test_key_filename, 'w').close()

        util.print_helper()

    def tearDown(self):    # pylint: disable=C0103
        # Delete test files
        os.remove(self.test_key_filename)


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


if __name__ == '__main__':
    VERBOSITY = util.verbosity_helper()

    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestGenericStorage)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestKeyGenerator)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestFileStorage)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestSQLiteStorage)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestGTaskStorage)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
