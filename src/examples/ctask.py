#!/usr/bin/python2
"""
usage: ctask.py [-h] [--version] {add,find,edit,del} ...

Task organizer.

Optional arguments:
  -h, --help           show this help message and exit
  --version            show program's version number and exit

Sub-commands:
  Specify exactly one sub-command.

  {add,find,edit,del}  valid sub-commands
    add                add a task
    find               find tasks
    edit               edit a task
    del                delete a task
"""
import task
import logger 
import logging

import argparse
import controller
from copy import copy

# TODO: Add piping functionality (not directly in ctask):
            # i.e. do a search for a bunch of tasks then pipe that to a delete
    # Make symbol tables (would help standardize even debugging output)
    # Allow find and del to accept a list of keys
    # Rename the subcommand 'find' to 'list'?
def main():
    """Command line implementation of task library."""
#    task_filename = 'task_file'
#    key_filename = 'key_file'
    logger.LOG.setLevel(logging.ERROR)

    my_parser = CLIParser('file')

    parsed_args = my_parser.parse_cl_args()
    task_item = task.TaskCreator.build(parsed_args)

    result = parsed_args['func'](task_item)

    if parsed_args['sub_cmd'] == 'find':
        if parsed_args['key'] == None:
            for item in result:
                print item
        else:
            print result
    elif result:
        pass
        #print result
    else:
        print 'Task not found'


class CLIParser():
    """Parser for a cli program using the task package.

    Public Classes:
        CLIParser

    Configures a command line parser and provides a means to invoke it on
    command line arguments.
    """
    def __init__(self,
            storage_type, 
            task_dbname='taskdb',
            task_filename='taskfile',
            key_filename='keyfile'):
        self._storage_type = storage_type
        self._interface_controller = controller.Controller(
                storage_type,
                task_dbname=task_dbname,
                task_filename=task_filename,
                key_filename=key_filename)

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
        """Initialize the sub-parser for the add sub-command."""
        arg_parser_add = self._arg_subparsers.add_parser(
            'add',
            parents=[self._parent_parser_title, self._parent_parser_notes],
            epilog = 'Goodbye.',
            help='add a task'
        )

        arg_parser_add.set_defaults(func=self._interface_controller.add)

        arg_parser_add.add_argument(
            'sub_cmd',
            action='store_const',
            const='add'
        )

    def _init_find_subparser(self):
        # pylint: disable=E1103
        """Initialize the sub-parser for the find sub-command."""
        arg_parser_find = self._arg_subparsers.add_parser(
            'find',
            epilog = 'Goodbye.',
            help='find tasks'
        )

        arg_parser_find.set_defaults(func=self._interface_controller.find)

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
        """Initialize the sub-parser for the edit sub-command."""
        arg_parser_edit = self._arg_subparsers.add_parser(
            'edit',
            parents=[
                self._parent_parser_key, 
                self._parent_parser_title, 
                self._parent_parser_notes],
            epilog = 'Goodbye.',
            help='edit a task'
        )

        arg_parser_edit.set_defaults(func=self._interface_controller.edit)

        arg_parser_edit.add_argument(
            'sub_cmd',
            action='store_const',
            const='edit'
        )

    def _init_delete_subparser(self):
        # pylint: disable=E1103
        """Initialize the sub-parser for the del sub-command."""
        arg_parser_delete = self._arg_subparsers.add_parser(
            'del',
            parents=[self._parent_parser_key],
            epilog = 'Goodbye.',
            help='delete a task'
        )

        arg_parser_delete.set_defaults(func=self._interface_controller.delete)

        arg_parser_delete.add_argument(
            'sub_cmd',
            action='store_const',
            const='del'
        )


    def parse_cl_args(self):
        """Return a dictionary of arguments.

        Calls the argument parser to parse the command line arguments by
        using sys.argv. Then calls a sanitizer to get an argument dictionary
        which is returned.

        """
        logging.info('attempting to parse arguments')
        raw_parsed_args = self._arg_parser.parse_args()
        args_dict = self._sanitize(raw_parsed_args)
        logging.info('success! returning argument dictionary')
        return args_dict

    def _sanitize(self, raw_parsed_args):
        """Creates and sanitizes an arg dict given the raw parsed args."""
        logging.info('attempting to sanitize arguments')
        args_dict = copy(vars(raw_parsed_args))
        for key, value in args_dict.iteritems():
            if value != None:
                if key == 'key':
                    if self._storage_type in ['file', 'sqlite']:
                        args_dict[key] = int(''.join(map(str, value)))
                    else:
                        args_dict[key] = ''.join(map(str, value))
                elif key == 'title' or key == 'notes':
                    args_dict[key] = ''.join(value)

        logging.info('success! returning sanitized argument dictionary')
        return args_dict


if __name__ == '__main__':
    main()
