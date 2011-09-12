import unittest
import task
import sys
import logger
import logging

logger.LOG.setLevel(logging.CRITICAL)

class TestTask(unittest.TestCase):
    # pylint: disable=R0904
    def setUp(self):    # pylint: disable=C0103
        # Initialize task object with attributes
        self.my_task = task.Task(title='title', notes='note')

        print_helper()

    def tearDown(self):    # pylint: disable=C0103
        # Clear the my_task Task object
        self.my_task = None

    def test_equal(self):
        """Tests a Task's handling when compared to an equivalent Task"""
        new_task = task.Task(title='title', notes='note')

        self.assertEqual(self.my_task, new_task)

    def test_equal_false(self):
        """Tests a Task's handling when == returns False"""
        new_task = task.Task(title='title1', notes='note')

        bool_value = self.my_task == new_task

        self.assertFalse(bool_value)

    def test_not_equal(self):
        """Tests a Task's handling when != returns True"""
        new_task = task.Task(title='title1', notes='note')

        self.assertNotEqual(self.my_task, new_task)
        new_task = task.Task(title='title', notes='note')

        bool_value = self.my_task != new_task

        self.assertFalse(bool_value)

    def test_equal_false_instance(self):
        """Tests a Task's handling when == compares to a Task instance"""
        not_task = 'Not a Task'

        bool_value = self.my_task == not_task

        self.assertFalse(bool_value)

    def test_not_equal_instance(self):
        """Tests a Task's handling when != compares to a non-Task instance"""
        not_task = 'Not a Task'

        self.assertNotEqual(self.my_task, not_task)

def verbosity_helper():
    verbosity = 1
    try:
        if sys.argv[1] == '-v':
            verbosity = 2
            logger.LOG.setLevel(logging.CRITICAL)
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

    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestTask)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
