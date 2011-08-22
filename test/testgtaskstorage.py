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
            level=logging.DEBUG,
            format='[%(asctime)s] %(levelname)s:%(name)s:'
            '%(module)s.%(funcName)s(): %(message)s'
        )

        #print   # So output from tests is on a new linex

    def tearDown(self):
        self.storage.delete(self.my_task.key)

        # Clear the my_task Task object
        self.my_task = None


if __name__ == '__main__':
    unittest.main()
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestTaskFileStorage)
#    unittest.TextTestRunner(verbosity=2).run(suite)
