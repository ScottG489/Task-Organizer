import argparse
import uicontrollerfactory
import logging
from copy import copy

# TODO: Figure out how to make this more testable then create tests.
class CLIParser():
    def __init__(self):
        self.user_interface = uicontrollerfactory.UIControllerFactory()
        self.user_interface = self.user_interface.get(
                'cli',
                'file')

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

        self.parent_parser_key = argparse.ArgumentParser(add_help=False)
        self.parent_parser_key.add_argument(
                '--key',
                '-k',
                action='store',
                nargs=1,
                required=True,
                help='the key of the task'
        )
        self.parent_parser_title = argparse.ArgumentParser(add_help=False)
        self.parent_parser_title.add_argument(
                '--title',
                '-t',
                action='store',
                nargs=1,
                type=str,
                help='a regular expression of the title of the task'
        )
        self.parent_parser_notes = argparse.ArgumentParser(add_help=False)
        self.parent_parser_notes.add_argument(
                '--notes',
                '-n',
                action='store',
                nargs=1,
                type=str,
                help='notes about the task'
        )

        self.init_add_subparser()
        self.init_find_subparser()
        self.init_edit_subparser()
        self.init_delete_subparser()


    def init_add_subparser(self):
        arg_parser_add = self.arg_subparsers.add_parser(
            'add',
            parents=[self.parent_parser_title, self.parent_parser_notes],
            epilog = 'Goodbye.',
            help='add a task'
        )

        arg_parser_add.set_defaults(func=self.user_interface.add)

        arg_parser_add.add_argument(
            'sub_cmd',
            action='store_const',
            const='add'
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

    def init_edit_subparser(self):
        arg_parser_edit = self.arg_subparsers.add_parser(
            'edit',
            parents=[
                self.parent_parser_key, 
                self.parent_parser_title, 
                self.parent_parser_notes],
            epilog = 'Goodbye.',
            help='edit a task'
        )

        arg_parser_edit.set_defaults(func=self.user_interface.edit)

        arg_parser_edit.add_argument(
            'sub_cmd',
            action='store_const',
            const='edit'
        )

    def init_delete_subparser(self):
        arg_parser_delete = self.arg_subparsers.add_parser(
            'del',
            parents=[self.parent_parser_key],
            epilog = 'Goodbye.',
            help='delete a task'
        )

        arg_parser_delete.set_defaults(func=self.user_interface.delete)

        arg_parser_delete.add_argument(
            'sub_cmd',
            action='store_const',
            const='del'
        )


    def parse_cl_args(self):
        logging.info('attempting to parse arguments')
        raw_parsed_args = self.arg_parser.parse_args()
        args_dict = self.sanitize(raw_parsed_args)
        logging.info('success! returning argument dictionary')
        return args_dict

    def sanitize(self, raw_parsed_args):
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
