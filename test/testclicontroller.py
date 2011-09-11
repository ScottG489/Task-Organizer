import unittest
import testuicontroller
import uicontrollerfactory
import taskstorage
import os
import sys
import logger
import logging

logger.LOG.setLevel(logging.CRITICAL)

class TestCLIControllerFileStorage(testuicontroller.TestUIController):
    def setUp(self):
        self.test_task_filename = 'test_taskfile'
        self.test_key_filename = 'test_keyfile'

        self.user_interface = uicontrollerfactory.UIControllerFactory()
        self.user_interface = self.user_interface.get(
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

        self.added_task = self.add_task()

    def tearDown(self):
        os.remove(self.test_task_filename)
        os.remove(self.test_key_filename)


class TestCLIControllerSQLiteStorage(testuicontroller.TestUIController):
    def setUp(self):
        self.user_interface = uicontrollerfactory.UIControllerFactory()
        self.user_interface = self.user_interface.get(
                'cli',
                'sqlite',
                task_dbname='testtaskdb')

        self.title = 'tasks title'
        self.notes = 'notes text'
        self.key = None

        print_helper()

        self.added_task = self.add_task()

    def tearDown(self):
        storage = taskstorage.StorageFactory()
        storage = storage.get('sqlite')
        storage.delete(self.added_task.key)


class TestCLIControllerGTaskStorage(testuicontroller.TestUIController):
    def setUp(self):
        self.user_interface = uicontrollerfactory.UIControllerFactory()
        self.user_interface = self.user_interface.get(
                'cli',
                'gtasks')


        self.title = 'tasks title'
        self.notes = 'notes text'
        self.key = None

        print_helper()

        self.added_task = self.add_task()

    def tearDown(self):
        storage = taskstorage.StorageFactory()
        storage = storage.get('gtasks')
        storage.delete(self.added_task.key)

def verbosity_helper():
    verbosity = 1
    try:
        if sys.argv[1] == '-v':
            verbosity = 2
            logger.LOG.setLevel(logging.DEBUG)
    except IndexError:
        pass

    return verbosity

def print_helper():
    try:
        if verbosity_helper() == 2:
            sys.stderr.write('\n')   # So output from tests is on a new linex
    except IndexError:
        pass

if __name__ == '__main__':
    VERBOSITY = verbosity_helper()

    SUITE = unittest.TestLoader().loadTestsFromTestCase(
            TestCLIControllerFileStorage)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
    SUITE = unittest.TestLoader().loadTestsFromTestCase(
            TestCLIControllerSQLiteStorage)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
#    SUITE = unittest.TestLoader().loadTestsFromTestCase(
#            TestCLIControllerGTaskStorage)
#    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
