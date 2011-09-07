import unittest
import logger

class TestUIController(unittest.TestCase):
    def add_task(self):
        action_dict = {
                'sub_cmd': 'add',
                'title': self.title,
                'notes': self.notes}

        return self.ui.add(action_dict)

    def find_task(self):
        action_dict = {
                'sub_cmd':  'find',
                'key':      self.key}

        return self.ui.find(action_dict)


    def test_add(self):
        """Tests that add() correctly adds the arg dict as a Task to storage"""
        added_task = self.add_task()
        self.key = added_task.key

        self.assertEqual(
                [added_task.title, added_task.notes],
                [self.title, self.notes])

    def test_find(self):
        """Tests that find() correctly returns a Task given an arg dict"""
        added_task = self.add_task()
        self.key = added_task.key

        found_task = self.find_task()

        self.assertEqual(
                [found_task.title, found_task.notes],
                [self.title, self.notes])

    def test_find_all(self):
        """Tests that find() correctly returns all Tasks when given no key"""
        added_task = self.add_task()
        self.key = added_task.key

        action_dict = {
                'sub_cmd':  'find',
                'key':      None}

        task_list = self.ui.find(action_dict)

        self.assertEqual(
                [task_list[0].title, task_list[0].notes],
                [added_task.title, added_task.notes])


    def test_edit(self):
        """Tests that edit() correctly modifies a Task given an arg dict"""
        added_task = self.add_task()
        self.key = added_task.key

        action_dict = {
                'sub_cmd': 'edit',
                'title': self.title,
                'notes': 'new note',
                'key': self.key}

        old_task = self.ui.edit(action_dict)
        new_task = self.find_task()

        self.assertEqual(new_task.title, old_task.title)
        self.assertNotEqual(new_task.notes, old_task.notes)

    def test_edit_none(self):
        """Tests edit()'s handling of arg dicts with empty attributes"""
        added_task = self.add_task()
        self.key = added_task.key

        action_dict = {
                'sub_cmd': 'edit',
                'title': None,
                'notes': None,
                'key': self.key}

        old_task = self.ui.edit(action_dict)
        new_task = self.find_task()

        self.assertEqual(
                [old_task.title, old_task.notes],
                [new_task.title, new_task.notes])

    def test_delete(self):
        """Tests that delete() correctly deletes a Task given an arg dict"""
        added_task = self.add_task()
        self.key = added_task.key

        action_dict = {
                'sub_cmd': 'del',
                'key': self.key}

        self.ui.delete(action_dict)
        found_task = self.find_task()
        self.assertIsNone(found_task)

#if __name__ == '__main__':
#    unittest.main()
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestCLIController)
#    unittest.TextTestRunner(verbosity=2).run(suite)
