##TODO:
#    Make it so the 'find' subparser requires at least one argument and displays
#        error otherwise.
import argparse
import uicontrollerfactory

class CLIParser():
    def __init__(self):
        self.user_interface = uicontrollerfactory.UIControllerFactory()
        self.user_interface = self.user_interface.getUI()

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
    ##Add sub-command arguments
        arg_parser_add = self.arg_subparsers.add_parser(
            'add',
            epilog = 'Goodbye.',
            help='add a task'
        )

        arg_parser_add.set_defaults(func=self.user_interface.add)

        arg_parser_add.add_argument(
            '--title',
            action='store',
            nargs=1,
            type=str,
            help='the title of the task'
        )
        arg_parser_add.add_argument(
            '--notes',
            action='store',
            nargs=1,
            type=str,
            help='notes about the task'
        )

    def init_find_subparser(self):
    ##Find sub-command arguments
        arg_parser_find = self.arg_subparsers.add_parser(
            'find',
            epilog = 'Goodbye.',
            help='find tasks'
        )

        arg_parser_find.set_defaults(func=self.user_interface.find)

        arg_parser_find.add_argument(
            '--key',
            action='store',
            nargs=1,
            type=int,
            help='the key of the task')
#        arg_parser_find.add_argument(
#            '--title',
#            action='store',
#            nargs=1,
#            type=str,
#            help='a regular expression of the title of the task'
#        )

    def init_edit_subparser(self):
    ##Edit sub-command arguments
        arg_parser_edit = self.arg_subparsers.add_parser(
            'edit',
            epilog = 'Goodbye.',
            help='edit a task'
        )

        arg_parser_edit.set_defaults(func=self.user_interface.edit)

        arg_parser_edit.add_argument(
            '--key',
            action='store',
            nargs=1,
            type=int,
            help='the key of the task'
        )
        arg_parser_edit.add_argument(
            '--title',
            action='store',
            nargs=1,
            type=str,
            help='a regular expression of the title of the task'
        )
        arg_parser_edit.add_argument(
            '--notes',
            action='store',
            nargs=1,
            type=str,
            help='notes about the task'
        )

    def init_delete_subparser(self):
    ##Delete sub-command arguments
        arg_parser_delete = self.arg_subparsers.add_parser(
            'del',
            epilog = 'Goodbye.',
            help='delete a task'
        )

        arg_parser_delete.set_defaults(func=self.user_interface.delete)

        arg_parser_delete.add_argument(
            '--key',
            action='store',
            nargs=1,
            type=int,
            help='the key of the task'
        )


    def parse_cl_args(self):
        args = self.arg_parser.parse_args()
        
        args.func(args)

        #return new_task
