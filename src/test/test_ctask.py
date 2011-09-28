import unittest
import sys
import os
import ctask
import util


class TestCTask(unittest.TestCase):
    """Tests parsing of the command line for the ctask script."""
    # pylint: disable=R0904
    def setUp(self):    # pylint: disable=C0103
        self.test_task_filename = 'testtaskfile'
        self.test_key_filename = 'testkeyfile'
        self.parser = ctask.CLIParser(
                'file',
                task_filename=self.test_task_filename,
                key_filename=self.test_key_filename)

        self.title = 'title'
        self.notes = 'notes'
        self.key = 0

        util.print_helper()

    def tearDown(self):    # pylint: disable=C0103
        os.remove(self.test_task_filename)
        os.remove(self.test_key_filename)

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


if __name__ == '__main__':
    VERBOSITY = util.verbosity_helper()

    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestCTask)
    unittest.TextTestRunner(verbosity=VERBOSITY).run(SUITE)
