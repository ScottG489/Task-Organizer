#!/usr/bin/python2
import clicontroller
import taskfilestorage
import logging
import sys

# TODO: Add piping functionality (not directly in ctask):
            # i.e. do a search for a bunch of tasks then pipe that to a delete
def main():
    task_filename = 'task_file'
    key_filename = 'key_file'
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s:%(name)s:'
        '%(module)s.%(funcName)s(): %(message)s'
    )

    my_ui = clicontroller.CLIController()
    # TODO: How do we tell main() which subcommand was used?

    print my_ui.exec_ui()
    # TODO: This doesn't work because when exec_ui() is caled it calls
                # cliparser which creates a clicontroller object itself which
                # is separate from this one. Fix?
    #print my_ui.command_line_arguments

    #my_storage.add(my_task)

main()
