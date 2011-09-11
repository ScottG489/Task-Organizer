import unittest
import sys
import cliparser
import logger
import logging

logger.LOG.setLevel(logging.CRITICAL)

class TestCLIParser(unittest.TestCase):
    def setUp(self):
        self.parser = cliparser.CLIParser()

        self.title = 'title'
        self.notes = 'notes'
        self.key = '0'

        print_helper()

    def tearDown(self):
        pass

    def test_add_subparser(self):
        """Tests the parser when the add sub-command is specified"""
        sub_cmd = 'add'
        sys.argv = [
                'prog_name', 
                sub_cmd, 
                '--title', self.title, 
                '-n', self.notes]
        parsed_args = self.parser.parse_cl_args()
        self.assertEqual(
                [sub_cmd, self.title, self.notes],
                [parsed_args['sub_cmd'], 
                    parsed_args['title'], 
                    parsed_args['notes']])

    def test_find_subparser(self):
        """Tests the parser when the find sub-command is specified"""
        sub_cmd = 'find'
        sys.argv = [
                'prog_name', 
                sub_cmd, 
                '--key', self.key]
        parsed_args = self.parser.parse_cl_args()
        self.assertEqual(
                [sub_cmd, self.key],
                [parsed_args['sub_cmd'], 
                    parsed_args['key']])

    def test_edit_subparser(self):
        """Tests the parser when the edit sub-command is specified"""
        sub_cmd = 'edit'
        sys.argv = [
                'prog_name', 
                sub_cmd, 
                '--key', self.key,
                '-n', self.notes]
        parsed_args = self.parser.parse_cl_args()
        self.assertEqual(
                [sub_cmd, self.key, self.notes],
                [parsed_args['sub_cmd'], 
                    parsed_args['key'],
                    parsed_args['notes']])

    def test_delete_subparser(self):
        """Tests the parser when the del sub-command is specified"""
        sub_cmd = 'del'
        sys.argv = [
                'prog_name', 
                sub_cmd, 
                '--key', self.key]
        parsed_args = self.parser.parse_cl_args()
        self.assertEqual(
                [sub_cmd, self.key],
                [parsed_args['sub_cmd'], 
                    parsed_args['key']])

    def test_parse_cl_args(self):
        """Tests that options are correctly transformed into a dict"""
        sub_cmd = 'edit'
        sys.argv = [
                'prog_name', 
                sub_cmd, 
                '--key', self.key,
                '--title', self.title,
                '-n', self.notes]
        parsed_args = self.parser.parse_cl_args()

        self.assertEqual(
                [sub_cmd, self.key, self.title, self.notes],
                [parsed_args['sub_cmd'],
                    parsed_args['key'],
                    parsed_args['title'],
                    parsed_args['notes']])

    def test_sanitize(self):
        """Tests that raw parsed args are correctly sanitized"""
        sub_cmd = 'edit'
        sys.argv = [
                'prog_name', 
                sub_cmd, 
                '--key', self.key,
                '--title', self.title,
                '-n', self.notes]

        raw_parsed_args = self.parser.arg_parser.parse_args()

        args_dict = self.parser.sanitize(raw_parsed_args)

        self.assertEqual(
                [sub_cmd, self.key, self.title, self.notes],
                [args_dict['sub_cmd'],
                    args_dict['key'],
                    args_dict['title'],
                    args_dict['notes']])


def verbosity_helper():
    verbosity = 1
    try:
        if sys.argv[1] == '-v':
            verbosity = 2
            logger.LOG.setLevel(logging.DEBUG)
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

    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestCLIParser)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
