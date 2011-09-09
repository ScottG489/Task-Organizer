import unittest
import testuicontroller
import uicontrollerfactory
import taskstorage
import os
import sys
import logger
import logging

logger.LOG.setLevel(logging.CRITICAL)

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

        print_helper()

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

        print_helper()

    def tearDown(self):
        storage = taskstorage.StorageFactory()
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

        print_helper()

    def tearDown(self):
        storage = taskstorage.StorageFactory()
        storage = storage.get('gtasks')
        storage.delete(self.key)

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

    suite = unittest.TestLoader().loadTestsFromTestCase(TestCLIControllerFileStorage)
    unittest.TextTestRunner(verbosity=verbosity).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCLIControllerSQLiteStorage)
    unittest.TextTestRunner(verbosity=verbosity).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCLIControllerGTaskStorage)
    unittest.TextTestRunner(verbosity=verbosity).run(suite)
