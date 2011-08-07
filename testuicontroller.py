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
        self.key = 'notes text'

        self.cli_parser = cliparser.CLIParser()

        print   # So output from tests is on a new linex

    def tearDown(self):
        # Remove handler so loggers aren't continuously created
        self.logger.removeHandler(self.stderr)

    def test_add(self):
        sys.argv = ['./ctask.py', 'add', '--title', '%s' % self.title, '--notes', '%s' % self.notes]
        cl_args = self.cli_parser.parse_cl_args()
        added_task = self.cli_parser.exec_ui()
        self.assertEqual([added_task.title, added_task.notes], [cl_args.title, cl_args.notes])

    def test_find(self):
        pass

    def test_edit(self):
        pass

    def test_delete(self):
        pass


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUIController)
    unittest.TextTestRunner(verbosity=2).run(suite)
