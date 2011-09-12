import argparse
import uicontrollerfactory
import logging
from copy import copy

class CLIParser():
    def __init__(self):
        self._user_interface = uicontrollerfactory.UIControllerFactory.get(
                'cli',
                'file')

        self._arg_parser = argparse.ArgumentParser(
            description='Task organizer.',
            epilog='Goodbye.'
        )
        self._arg_parser.add_argument(
            '--version',
            action = 'version',
            version = '%(prog)s alpha'
        )
        self._arg_subparsers = self._arg_parser.add_subparsers(
            title='Sub-commands',
            description='Specify exactly one sub-command.',
            help='valid sub-commands'
        )

        self._parent_parser_key = argparse.ArgumentParser(add_help=False)
        self._parent_parser_key.add_argument(
                '--key',
                '-k',
                action='store',
                nargs=1,
                required=True,
                help='the key of the task'
        )
        self._parent_parser_title = argparse.ArgumentParser(add_help=False)
        self._parent_parser_title.add_argument(
                '--title',
                '-t',
                action='store',
                nargs=1,
                type=str,
                help='title of the task'
        )
        self._parent_parser_notes = argparse.ArgumentParser(add_help=False)
        self._parent_parser_notes.add_argument(
                '--notes',
                '-n',
                action='store',
                nargs=1,
                type=str,
                help='notes about the task'
        )

        self._init_add_subparser()
        self._init_find_subparser()
        self._init_edit_subparser()
        self._init_delete_subparser()


    def _init_add_subparser(self):
        # pylint: disable=E1103
        """Initialize the sub-parser for the add sub-command"""
        arg_parser_add = self._arg_subparsers.add_parser(
            'add',
            parents=[self._parent_parser_title, self._parent_parser_notes],
            epilog = 'Goodbye.',
            help='add a task'
        )

        arg_parser_add.set_defaults(func=self._user_interface.add)

        arg_parser_add.add_argument(
            'sub_cmd',
            action='store_const',
            const='add'
        )

    def _init_find_subparser(self):
        # pylint: disable=E1103
        """Initialize the sub-parser for the find sub-command"""
        arg_parser_find = self._arg_subparsers.add_parser(
            'find',
            epilog = 'Goodbye.',
            help='find tasks'
        )

        arg_parser_find.set_defaults(func=self._user_interface.find)

        arg_parser_find.add_argument(
            'sub_cmd',
            action='store_const',
            const='find'
        )
        arg_parser_find.add_argument(
            '--key',
            '-k',
            action='store',
            nargs=1,
            help='the key of the task')

    def _init_edit_subparser(self):
        # pylint: disable=E1103
        """Initialize the sub-parser for the edit sub-command"""
        arg_parser_edit = self._arg_subparsers.add_parser(
            'edit',
            parents=[
                self._parent_parser_key, 
                self._parent_parser_title, 
                self._parent_parser_notes],
            epilog = 'Goodbye.',
            help='edit a task'
        )

        arg_parser_edit.set_defaults(func=self._user_interface.edit)

        arg_parser_edit.add_argument(
            'sub_cmd',
            action='store_const',
            const='edit'
        )

    def _init_delete_subparser(self):
        # pylint: disable=E1103
        """Initialize the sub-parser for the del sub-command"""
        arg_parser_delete = self._arg_subparsers.add_parser(
            'del',
            parents=[self._parent_parser_key],
            epilog = 'Goodbye.',
            help='delete a task'
        )

        arg_parser_delete.set_defaults(func=self._user_interface.delete)

        arg_parser_delete.add_argument(
            'sub_cmd',
            action='store_const',
            const='del'
        )


    def parse_cl_args(self):
        """Return a dictionary of arguments

        Calls the argument parser to parse the command line arguments by
        using sys.argv. Then calls a sanitizer to get an argument dictionary
        which is returned.

        """

        logging.info('attempting to parse arguments')
        raw_parsed_args = self._arg_parser.parse_args()
        args_dict = self._sanitize(raw_parsed_args)
        logging.info('success! returning argument dictionary')
        return args_dict

    @staticmethod
    def _sanitize(raw_parsed_args):
        """Creates and sanitizes an arg dict given the raw parsed args"""
        logging.info('attepting to sanitize arguments')
        args_dict = copy(vars(raw_parsed_args))
        for key, value in args_dict.iteritems():
            if value != None:
                if key == 'key':
                    args_dict[key] = ''.join(map(str, value))
                elif key == 'title' or key == 'notes':
                    args_dict[key] = ''.join(value)

        logging.info('success! returning sanitized argument dictionary')
        return args_dict
