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
        self.key = 0

        self.my_parser = cliparser.CLIParser()

        print   # So output from tests is on a new linex

    def tearDown(self):
        # Remove handler so loggers aren't continuously created
        self.logger.removeHandler(self.stderr)

    def test_add(self):
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
        added_task = self.my_parser.parse_cl_args()
        self.assertEqual(
                [added_task['title'], added_task['notes']],
                [self.title, self.notes]
        )

    def test_find(self):
        #sys.argv = ['./ctask.py', 'find', '--key', '%i' % self.key]
        pass

    def test_find_all(self):
        pass

    def test_edit(self):
        pass

    def test_delete(self):
        pass


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUIController)
    unittest.TextTestRunner(verbosity=2).run(suite)
