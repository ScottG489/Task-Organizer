import unittest
import testtaskcontroller
import taskcontroller
import taskstorage
import os
import sys
import logger
import logging

logger.LOG.setLevel(logging.CRITICAL)

class TestTaskControllerFileStorage(testtaskcontroller.TestTaskController):
    # pylint: disable=R0904
    def __init__(self, method_name):
        testtaskcontroller.TestTaskController.__init__(self, method_name)

    def setUp(self):    # pylint: disable=C0103
        self.test_task_filename = 'test_taskfile'
        self.test_key_filename = 'test_keyfile'

        self.interface_controller = taskcontroller.TaskController(
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

    def tearDown(self):    # pylint: disable=C0103
        os.remove(self.test_task_filename)
        os.remove(self.test_key_filename)


class TestTaskControllerSQLiteStorage(testtaskcontroller.TestTaskController):
    # pylint: disable=R0904
    def __init__(self, method_name):
        testtaskcontroller.TestTaskController.__init__(self, method_name)

    def setUp(self):    # pylint: disable=C0103
        self.interface_controller = taskcontroller.TaskController(
                'sqlite',
                task_dbname='testtaskdb')

        self.title = 'tasks title'
        self.notes = 'notes text'
        self.key = None

        print_helper()

        self.added_task = self.add_task()

    def tearDown(self):    # pylint: disable=C0103
        storage = taskstorage.StorageFactory()
        storage = storage.get('sqlite')
        storage.delete(self.added_task.key)


class TestTaskControllerGTaskStorage(testtaskcontroller.TestTaskController):
    # pylint: disable=R0904
    def __init__(self, method_name):
        testtaskcontroller.TestTaskController.__init__(self, method_name)

    def setUp(self):    # pylint: disable=C0103
        self.interface_controller = taskcontroller.TaskController(
                'gtasks')


        self.title = 'tasks title'
        self.notes = 'notes text'
        self.key = None

        print_helper()

        self.added_task = self.add_task()

    def tearDown(self):    # pylint: disable=C0103
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
            TestTaskControllerFileStorage)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
    SUITE = unittest.TestLoader().loadTestsFromTestCase(
            TestTaskControllerSQLiteStorage)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
    SUITE = unittest.TestLoader().loadTestsFromTestCase(
            TestTaskControllerGTaskStorage)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
