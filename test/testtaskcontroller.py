import unittest
import logger
import logging

logger.LOG.setLevel(logging.CRITICAL)

class TestTaskController(unittest.TestCase):
    # pylint: disable=R0904
    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)
        self.interface_controller = None
        self.title = None
        self.notes = None
        self.added_task = None

    def add_task(self):
        action_dict = {
                'sub_cmd': 'add',
                'title': self.title,
                'notes': self.notes}

        return self.interface_controller.add(action_dict)

    def find_task(self, task_key):
        action_dict = {
                'sub_cmd':  'find',
                'key':      task_key}

        return self.interface_controller.find(action_dict)


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

        task_list = self.interface_controller.find(action_dict)

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

        old_task = self.interface_controller.edit(action_dict)
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

        old_task = self.interface_controller.edit(action_dict)
        new_task = self.find_task(self.added_task.key)

        self.assertEqual(
                [old_task.title, old_task.notes],
                [new_task.title, new_task.notes])

    def test_delete(self):
        """Tests that delete() correctly deletes a Task given an arg dict"""
        action_dict = {
                'sub_cmd': 'del',
                'key': self.added_task.key}

        self.interface_controller.delete(action_dict)
        found_task = self.find_task(self.added_task.key)
        self.assertIsNone(found_task)
