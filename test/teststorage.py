import unittest
import task
import logger


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

#if __name__ == '__main__':
#    unittest.main()
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestStorage)
#    unittest.TextTestRunner(verbosity=2).run(suite)
