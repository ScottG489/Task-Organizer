import unittest
import task
import controller
import storage
import os
import util


class TestTaskController(unittest.TestCase):
    """Abstract tests for child tests using specific storage types

    Generic tests used by all TaskController tests undependent on what
    storage type they are using. These tests should never be called directly.
    """
    # pylint: disable=R0904
    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)
        self.interface_controller = None
        self.title = None
        self.notes = None
        self.added_task = None

    def add_task(self):
        """Helper function to add Task to storage as given dict"""
        action_dict = {
                'sub_cmd': 'add',
                'title': self.title,
                'notes': self.notes}

        task_item = task.TaskCreator.build(action_dict)

        return self.interface_controller.add(task_item)

    def find_task(self, task_key):
        """Helper function to find Task in storage when given key"""
        action_dict = {
                'sub_cmd':  'find',
                'key':      task_key}

        task_item = task.TaskCreator.build(action_dict)

        return self.interface_controller.find(task_item)


    def test_add(self):
        """Tests that add() correctly adds the arg dict as a Task to storage"""
        self.assertEqual(
                [self.added_task.title, self.added_task.notes],
                [self.title, self.notes])

    def test_find(self):
        """Tests that find() correctly returns a Task given an arg dict"""
        found_task = self.find_task(self.added_task.key)

        self.assertEqual(
                [found_task.title, found_task.notes],
                [self.title, self.notes])

    def test_find_all(self):
        """Tests that find() correctly returns all Tasks when given no key"""
        action_dict = {
                'sub_cmd':  'find',
                'key':      None}

        task_item = task.TaskCreator.build(action_dict)

        task_list = self.interface_controller.find(task_item)

        self.assertEqual(
                [task_list[0].title, task_list[0].notes],
                [self.added_task.title, self.added_task.notes])


    def test_edit(self):
        """Tests that edit() correctly modifies a Task given an arg dict"""
        action_dict = {
                'sub_cmd': 'edit',
                'title': self.title,
                'notes': 'new note',
                'key': self.added_task.key}

        task_item = task.TaskCreator.build(action_dict)

        old_task = self.interface_controller.edit(task_item)
        new_task = self.find_task(self.added_task.key)

        self.assertEqual(new_task.title, old_task.title)
        self.assertNotEqual(new_task.notes, old_task.notes)

    def test_edit_none(self):
        """Tests edit()'s handling of arg dicts with empty attributes"""
        action_dict = {
                'sub_cmd': 'edit',
                'title': None,
                'notes': None,
                'key': self.added_task.key}

        task_item = task.TaskCreator.build(action_dict)

        old_task = self.interface_controller.edit(task_item)
        new_task = self.find_task(self.added_task.key)

        self.assertEqual(
                [old_task.title, old_task.notes],
                [new_task.title, new_task.notes])

    def test_delete(self):
        """Tests that delete() correctly deletes a Task given an arg dict"""
        action_dict = {
                'sub_cmd': 'del',
                'key': self.added_task.key}

        task_item = task.TaskCreator.build(action_dict)

        self.interface_controller.delete(task_item)
        found_task = self.find_task(self.added_task.key)
        self.assertIsNone(found_task)




class TestTaskControllerFileStorage(TestTaskController):
    """Tests the TaskController while using file storage"""
    # pylint: disable=R0904
    def __init__(self, method_name):
        TestTaskController.__init__(self, method_name)

    def setUp(self):    # pylint: disable=C0103
        self.test_task_filename = 'test_taskfile'
        self.test_key_filename = 'test_keyfile'

        self.interface_controller = controller.TaskController(
                'file',
                task_filename=self.test_task_filename,
                key_filename=self.test_key_filename)


        self.title = 'tasks title'
        self.notes = 'notes text'
        self.key = None

        open(self.test_task_filename, 'w').close()
        open(self.test_key_filename, 'w').close()

        util.print_helper()

        # TODO: This isn't a good way to do this.
        self.added_task = self.add_task()

    def tearDown(self):    # pylint: disable=C0103
        os.remove(self.test_task_filename)
        os.remove(self.test_key_filename)


class TestTaskControllerSQLiteStorage(TestTaskController):
    """Tests the TaskController while using sqlite storage"""
    # pylint: disable=R0904
    def __init__(self, method_name):
        TestTaskController.__init__(self, method_name)

    def setUp(self):    # pylint: disable=C0103
        self.test_task_dbname = 'testtaskdb'
        self.interface_controller = controller.TaskController(
                'sqlite',
                task_dbname=self.test_task_dbname)

        self.title = 'tasks title'
        self.notes = 'notes text'
        self.key = None

        util.print_helper()

        # TODO: This isn't a good way to do this.
        self.added_task = self.add_task()

    def tearDown(self):    # pylint: disable=C0103
        os.remove(self.test_task_dbname)


class TestTaskControllerGTaskStorage(TestTaskController):
    """Tests the TaskController while using GTask storage"""
    # pylint: disable=R0904
    def __init__(self, method_name):
        TestTaskController.__init__(self, method_name)

    def setUp(self):    # pylint: disable=C0103
        self.interface_controller = controller.TaskController(
                'gtasks')


        self.title = 'tasks title'
        self.notes = 'notes text'
        self.key = None

        util.print_helper()
        # TODO: This isn't a good way to do this.
        self.added_task = self.add_task()

    def tearDown(self):    # pylint: disable=C0103
        task_storage = storage.StorageFactory.get('gtasks')
        task_storage.delete(self.added_task.key)


if __name__ == '__main__':
    VERBOSITY = util.verbosity_helper()

    SUITE = unittest.TestLoader().loadTestsFromTestCase(
            TestTaskControllerFileStorage)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
    SUITE = unittest.TestLoader().loadTestsFromTestCase(
            TestTaskControllerSQLiteStorage)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
    SUITE = unittest.TestLoader().loadTestsFromTestCase(
            TestTaskControllerGTaskStorage)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
