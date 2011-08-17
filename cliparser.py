##TODO: Create parent parsers to reduce code duplication.
import argparse
import uicontrollerfactory
import logging
from copy import copy

class CLIParser():
    def __init__(self):
        self.user_interface = uicontrollerfactory.UIControllerFactory()
        self.user_interface = self.user_interface.getUI(
                'cli',
                'file')

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARNING)

        self.arg_parser = argparse.ArgumentParser(
            description='Task organizer.',
            epilog='Goodbye.'
        )
        self.arg_parser.add_argument(
            '--version',
            action = 'version',
            version = '%(prog)s alpha'
        )
        self.arg_subparsers = self.arg_parser.add_subparsers(
            title='Sub-commands',
            description='Specify exactly one sub-command.',
            help='valid sub-commands'
        )

        self.init_add_subparser()
        self.init_find_subparser()
        self.init_edit_subparser()
        self.init_delete_subparser()


    def init_add_subparser(self):
        arg_parser_add = self.arg_subparsers.add_parser(
            'add',
            epilog = 'Goodbye.',
            help='add a task'
        )

        arg_parser_add.set_defaults(func=self.user_interface.add)

        arg_parser_add.add_argument(
            'sub_cmd',
            action='store_const',
            const='add'
        )
        arg_parser_add.add_argument(
            '--title',
            '-t',
            action='store',
            nargs=1,
            type=str,
            help='the title of the task'
        )
        arg_parser_add.add_argument(
            '--notes',
            '-n',
            action='store',
            nargs=1,
            type=str,
            help='notes about the task'
        )

    def init_find_subparser(self):
        arg_parser_find = self.arg_subparsers.add_parser(
            'find',
            epilog = 'Goodbye.',
            help='find tasks'
        )

        arg_parser_find.set_defaults(func=self.user_interface.find)

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
#        arg_parser_find.add_argument(
#            '--title',
#            action='store',
#            nargs=1,
#            type=str,
#            help='a regular expression of the title of the task'
#        )

    def init_edit_subparser(self):
        arg_parser_edit = self.arg_subparsers.add_parser(
            'edit',
            epilog = 'Goodbye.',
            help='edit a task'
        )

        arg_parser_edit.set_defaults(func=self.user_interface.edit)

        arg_parser_edit.add_argument(
            'sub_cmd',
            action='store_const',
            const='edit'
        )
        arg_parser_edit.add_argument(
            '--key',
            '-k',
            action='store',
            nargs=1,
            required=True,
            help='the key of the task'
        )
        arg_parser_edit.add_argument(
            '--title',
            '-t',
            action='store',
            nargs=1,
            type=str,
            help='a regular expression of the title of the task'
        )
        arg_parser_edit.add_argument(
            '--notes',
            '-n',
            action='store',
            nargs=1,
            type=str,
            help='notes about the task'
        )

    def init_delete_subparser(self):
        arg_parser_delete = self.arg_subparsers.add_parser(
            'del',
            epilog = 'Goodbye.',
            help='delete a task'
        )

        arg_parser_delete.set_defaults(func=self.user_interface.delete)

        arg_parser_delete.add_argument(
            'sub_cmd',
            action='store_const',
            const='del'
        )
        arg_parser_delete.add_argument(
            '--key',
            '-k',
            action='store',
            nargs=1,
            required=True,
            help='the key of the task'
        )
    # TODO: Is there a way to tell the main() program what sub-commands and
                # arguments are being called so it can handle them correctly?
    def parse_cl_args(self):
        raw_parsed_args = self.arg_parser.parse_args()
        args_dict = self.sanitize(raw_parsed_args)
        return args_dict

    def sanitize(self, raw_parsed_args):
        args_dict = copy(vars(raw_parsed_args))
        # TODO: Instead of deleting it, convert it into a sub_com key?
              # This would be a possible fix for the cli arg attribute problem
        for key, value in args_dict.iteritems():
            if value != None:
                if key == 'key':
                    args_dict[key] = ''.join(map(str, value))
                elif key == 'title' or key == 'notes':
                    args_dict[key] = ''.join(value)

        return args_dict
