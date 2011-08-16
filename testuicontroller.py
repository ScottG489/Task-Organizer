import unittest
import logging
import cliparser
import sys

class TestUIController(unittest.TestCase):
    def setUp(self):
        # Initialize file storage object using test-specific file names
        self.logger = logging.getLogger()
        self.stderr = logging.StreamHandler()
        self.stderr.setLevel(logging.WARNING)
        self.formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s:%(name)s:'
                '%(module)s.%(funcName)s(): %(message)s'
        )
        self.stderr.setFormatter(self.formatter)
        self.logger.addHandler(self.stderr)

        self.title = 'tasks title'
        self.notes = 'notes text'
        # TODO: Don't set key here. Needs to be set by doing a find()
                # because 0 isn't storage-generic
        self.key = 0

        self.my_parser = cliparser.CLIParser()

        #print   # So output from tests is on a new linex

    def tearDown(self):
        # Remove handler so loggers aren't continuously created
        self.logger.removeHandler(self.stderr)

    def add_task(self):
        sys.argv = [
                './ctask.py',
                'add',
                '--title',
                '%s'
                % self.title,
                '--notes', 
                '%s'
                % self.notes
        ]
        args_dict = self.my_parser.parse_cl_args()
        return args_dict['func'](args_dict)

    def find_task(self):
        sys.argv = ['./ctask.py', 
                'find', 
                '--key', 
                '%i' 
                % self.key
        ]
        args_dict = self.my_parser.parse_cl_args()
        return args_dict['func'](args_dict)


    def test_add(self):
        task_value = self.add_task()
        self.assertEqual(
                [task_value.title, task_value.notes],
                [self.title, self.notes]
        )

    def test_find(self):
        task_value = self.add_task()

        task_value = self.find_task()
        self.assertEqual([task_value.title, task_value.notes],
                [self.title, self.notes])

    def test_find_all(self):
        self.add_task()

        sys.argv = [
                './ctask.py', 
                'find'
        ]
        args_dict = self.my_parser.parse_cl_args()
        task_value = args_dict['func'](args_dict)
        self.assertEqual([task_value[0].title, task_value[0].notes],
                [self.title, self.notes])

    def test_edit(self):
        self.add_task()

        new_title = 'new title'
        new_notes = 'new notes'
        sys.argv = [
                './ctask.py',
                'edit',
                '--key', 
                '%i' 
                % self.key,
                '--title',
                '%s'
                % new_title,
                '--notes', 
                '%s'
                % new_notes
        ]
        args_dict = self.my_parser.parse_cl_args()
        args_dict['func'](args_dict)

        task_value = self.find_task()

        self.assertEqual([task_value.title, task_value.notes],
                [new_title, new_notes])

    def test_delete(self):
        self.add_task()

        sys.argv = ['./ctask.py', 
                'del', 
                '--key', 
                '%i' 
                % self.key
        ]
        args_dict = self.my_parser.parse_cl_args()
        print args_dict
        args_dict['func'](args_dict)

        task_value = self.find_task()

        self.assertIsNone(task_value)

if __name__ == '__main__':
    unittest.main()
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestCLIController)
#    unittest.TextTestRunner(verbosity=2).run(suite)
