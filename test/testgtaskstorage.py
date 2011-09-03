import unittest
import gtaskstorage
import task
import logging
import teststorage

#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference
class TestGTaskStorage(teststorage.TestStorage):
    def setUp(self):
        # Initialize task object with attributes
        self.my_task = task.Task(title='title', notes='note')

        # Initialize file storage object using test-specific file names
        self.storage = gtaskstorage.GTaskStorage()

        logging.basicConfig(
            level=logging.WARNING,
            format='[%(asctime)s] %(levelname)s:%(name)s:'
            '%(module)s.%(funcName)s(): %(message)s'
        )

        #print   # So output from tests is on a new linex

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


if __name__ == '__main__':
#    unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGTaskStorage)
    unittest.TextTestRunner(verbosity=2).run(suite)
