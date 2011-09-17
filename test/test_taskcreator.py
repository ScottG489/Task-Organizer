import unittest
import util
import taskcreator

class TestTaskCreator(unittest.TestCase):
    # pylint: disable=R0904
    def setUp(self):    # pylint: disable=C0103
        self.title = 'task title'
        self.notes = 'task notes'

    def tearDown(self):    # pylint: disable=C0103
        self.title = None
        self.notes = None


    def test_build(self):
        action_dict = {
                'sub_cmd': 'add',
                'title': self.title,
                'notes': self.notes}

        task_item = taskcreator.TaskCreator.build(action_dict)

        self.assertEqual(
                [task_item.title, task_item.notes],
                [action_dict['title'], action_dict['notes']])


if __name__ == '__main__':
    VERBOSITY = util.verbosity_helper()

    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestTaskCreator)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
