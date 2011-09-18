#!/usr/bin/python2
"""
usage: ctask.py [-h] [--version] {add,find,edit,del} ...

Task organizer.

optional arguments:
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
import cliparser
import taskcreator

# TODO: Add piping functionality (not directly in ctask):
            # i.e. do a search for a bunch of tasks then pipe that to a delete
    # Make symbol tables (would help standardize even debugging output)
    # Allow find and del to accept a list of keys
    # Rename the subcommand 'find' to 'list'?
def main():
    """Command line implementation of task library"""
#    task_filename = 'task_file'
#    key_filename = 'key_file'
    import logger 
    import logging
    logger.LOG.setLevel(logging.ERROR)

    my_parser = cliparser.CLIParser()

    parsed_args = my_parser.parse_cl_args()
    task_item = taskcreator.TaskCreator.build(parsed_args)

    something = parsed_args['func'](task_item)

    if parsed_args['sub_cmd'] == 'find':
        if parsed_args['key'] == None:
            for item in something:
                print item
        else:
            print something
    elif something:
        pass
        #print something
    else:
        print 'Task not found'

main()
