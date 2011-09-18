import unittest
import task
import util


class TestTask(unittest.TestCase):
    """Tests Task objects"""
    # pylint: disable=R0904
    def setUp(self):    # pylint: disable=C0103
        # Initialize task object with attributes
        self.my_task = task.Task(title='title', notes='note')

        util.print_helper()

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


class TestTaskCreator(unittest.TestCase):
    """Tests that TaskCreator correctly creates Task objects"""
    # pylint: disable=R0904
    def setUp(self):    # pylint: disable=C0103
        self.title = 'task title'
        self.notes = 'task notes'

    def tearDown(self):    # pylint: disable=C0103
        self.title = None
        self.notes = None


    def test_build(self):
        """Tests the creation of Task objects from dictionaries"""
        action_dict = {
                'sub_cmd': 'add',
                'title': self.title,
                'notes': self.notes}

        task_item = task.TaskCreator.build(action_dict)

        self.assertEqual(
                [task_item.title, task_item.notes],
                [action_dict['title'], action_dict['notes']])


if __name__ == '__main__':
    VERBOSITY = util.verbosity_helper()

    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestTask)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestTaskCreator)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
