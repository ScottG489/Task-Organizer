##TODO:
#    Make it so the 'find' subparser requires at least one argument and displays
#        error otherwise.
import argparse
import task
import taskfilestorage

class UIController():
    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(
            description='Task organizer.',
            epilog='Goodbye.'
        )
        self.arg_parser.add_argument(
            '--version',
            action = 'version',
            version = '%(prog)s alpha'
        )
        arg_subparsers = self.arg_parser.add_subparsers(
            title='Sub-commands',
            description='Specify exactly one sub-command.',
            help='valid sub-commands'
        )
    ##Add sub-command arguments
        self.arg_parser_add = arg_subparsers.add_parser(
            'add',
            epilog = 'Goodbye.',
            help='add a task'
        )

        self.arg_parser_add.set_defaults(func=self.add)

        self.arg_parser_add.add_argument(
            '--title',
            action='store',
            nargs=1,
            type=str,
            help='the title of the task'
        )
        self.arg_parser_add.add_argument(
            '--notes',
            action='store',
            nargs=1,
            type=str,
            help='notes about the task'
        )
    ##Find sub-command arguments
        self.arg_parser_find = arg_subparsers.add_parser(
            'find',
            epilog = 'Goodbye.',
            help='find tasks'
        )

        self.arg_parser_find.set_defaults(func=self.find)

        self.arg_parser_find.add_argument(
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
    ##Edit sub-command arguments
        self.arg_parser_edit = arg_subparsers.add_parser(
            'edit',
            epilog = 'Goodbye.',
            help='edit a task'
        )

        self.arg_parser_edit.set_defaults(func=self.edit)

        self.arg_parser_edit.add_argument(
            '--key',
            action='store',
            nargs=1,
            type=int,
            help='the key of the task'
        )
        self.arg_parser_edit.add_argument(
            '--title',
            action='store',
            nargs=1,
            type=str,
            help='a regular expression of the title of the task'
        )
        self.arg_parser_edit.add_argument(
            '--notes',
            action='store',
            nargs=1,
            type=str,
            help='notes about the task'
        )
    ##Delete sub-command arguments
        self.arg_parser_delete = arg_subparsers.add_parser(
            'del',
            epilog = 'Goodbye.',
            help='delete a task'
        )

        self.arg_parser_delete.set_defaults(func=self.delete)

        self.arg_parser_delete.add_argument(
            '--key',
            action='store',
            nargs=1,
            type=int,
            help='the key of the task'
        )

        self.file_storage = taskfilestorage.TaskFileStorage()


    def add(self, args):
        print 'add function'
        print args
        if args.title:
            args.title = ''.join(args.title)
        if args.notes:
            args.notes = ''.join(args.notes)
        task_item = task.Task(args.title, args.notes)
        print 'asdfasdfasdf', task_item

        self.file_storage.add(task_item)

    def find(self, args):
        print 'find function'
        print args
        if args.key:
            args.key = int(''.join(map(str, args.key)))

        for task_item in self.file_storage.find(args.key):
            print task_item
        #print self.file_storage.find(args.key)

    def edit(self, args):
        print 'edit function'
        print args
        if args.key:
            args.key = int(''.join(map(str, args.key)))
        if args.title:
            args.title = ''.join(args.title)
        if args.notes:
            args.notes = ''.join(args.notes)

        task_item = task.Task(args.key, args.title, args.notes)

        self.file_storage.update(task_item)

    def delete(self, args):
        print 'delete function'
        print args
        if args.key:
            args.key = int(''.join(map(str, args.key)))

        print self.file_storage.delete(args.key)

    def parse_cl_args(self):
        args = self.arg_parser.parse_args()
        
        args.func(args)

        #return new_task
