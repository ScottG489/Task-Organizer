import unittest
import gtaskstorage
import task
import logging
import testtaskstorage

#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference
class TestGTaskStorage(testtaskstorage.TestTaskStorage):
    def setUp(self):
        # Initialize task object with attributes
        self.my_task = task.Task(title='title', notes='note')

        # Initialize file storage object using test-specific file names
        self.storage = gtaskstorage.GTaskStorage()

        self.logger = logging.getLogger()
        self.stderr = logging.StreamHandler()
        self.stderr.setLevel(logging.WARNING)
        self.formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s:%(name)s.'
                '%(funcName)s(): %(message)s'
        )
        self.stderr.setFormatter(self.formatter)
        self.logger.addHandler(self.stderr)

        #print   # So output from tests is on a new linex

    def tearDown(self):
        # Clear the my_task Task object
        self.my_task = None

        # Remove handler so loggers aren't continuously created
        self.logger.removeHandler(self.stderr)


if __name__ == '__main__':
    unittest.main()
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestTaskFileStorage)
#    unittest.TextTestRunner(verbosity=2).run(suite)
