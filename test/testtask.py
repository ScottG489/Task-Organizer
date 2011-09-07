import unittest
import task
import sys
import logger

#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference
class TestTask(unittest.TestCase):
    def setUp(self):
        # Initialize task object with attributes
        self.my_task = task.Task(title='title', notes='note')

        try:
            if sys.argv[1] == '-v':
                sys.stderr.write()   # So output from tests is on a new linex
        except:
            pass

    def tearDown(self):
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


if __name__ == '__main__':
    if len(sys.argv) == 1:
        unittest.main()
    elif sys.argv[1] == '-v':
        suite = unittest.TestLoader().loadTestsFromTestCase(TestTask)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else:
        unittest.main()
