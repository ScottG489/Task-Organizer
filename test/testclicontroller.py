import unittest
import testuicontroller
import uicontrollerfactory
import storagefactory
import os
import sys

# TODO: Get logger working in tests.
class TestCLIControllerFileStorage(testuicontroller.TestUIController):
    def setUp(self):
        self.test_task_filename = 'test_taskfile'
        self.test_key_filename = 'test_keyfile'

        self.ui = uicontrollerfactory.UIControllerFactory()
        self.ui = self.ui.get(
                'cli',
                'file',
                task_filename=self.test_task_filename,
                key_filename=self.test_key_filename)


        self.title = 'tasks title'
        self.notes = 'notes text'
        self.key = None

        open(self.test_task_filename, 'w').close()
        open(self.test_key_filename, 'w').close()

        try:
            if sys.argv[1] == '-v':
                sys.stderr.write()   # So output from tests is on a new linex
        except:
            pass

    def tearDown(self):
        os.remove(self.test_task_filename)
        os.remove(self.test_key_filename)


class TestCLIControllerSQLiteStorage(testuicontroller.TestUIController):
    def setUp(self):
        self.ui = uicontrollerfactory.UIControllerFactory()
        self.ui = self.ui.get(
                'cli',
                'sqlite',
                task_dbname='testtaskdb')


        self.title = 'tasks title'
        self.notes = 'notes text'
        self.key = None

        try:
            if sys.argv[1] == '-v':
                sys.stderr.write()   # So output from tests is on a new linex
        except:
            pass

    def tearDown(self):
        storage = storagefactory.StorageFactory()
        storage = storage.get('sqlite')
        storage.delete(self.key)


class TestCLIControllerGTaskStorage(testuicontroller.TestUIController):
    def setUp(self):
        self.ui = uicontrollerfactory.UIControllerFactory()
        self.ui = self.ui.get(
                'cli',
                'gtasks')


        self.title = 'tasks title'
        self.notes = 'notes text'
        self.key = None

        try:
            if sys.argv[1] == '-v':
                sys.stderr.write()   # So output from tests is on a new linex
        except:
            pass

    def tearDown(self):
        storage = storagefactory.StorageFactory()
        storage = storage.get('gtasks')
        storage.delete(self.key)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        unittest.main()
    elif sys.argv[1] == '-v':
        suite = unittest.TestLoader().loadTestsFromTestCase(TestCLIControllerFileStorage)
        unittest.TextTestRunner(verbosity=2).run(suite)
        suite = unittest.TestLoader().loadTestsFromTestCase(TestCLIControllerSQLiteStorage)
        unittest.TextTestRunner(verbosity=2).run(suite)
        suite = unittest.TestLoader().loadTestsFromTestCase(TestCLIControllerGTaskStorage)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else:
        unittest.main()
