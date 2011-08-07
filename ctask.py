#!/usr/bin/python2
##TODO:
#    Make it so the 'find' subparser requires at least one argument and displays
#        error otherwise.
import clicontroller
import taskfilestorage
import logging
import sys

def main():
    task_filename = 'task_file'
    key_filename = 'key_file'
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s:%(name)s:'
        '%(module)s.%(funcName)s(): %(message)s'
    )
#    open(task_filename, 'w').close()
#    open(key_filename, 'w').close()

    #my_storage = taskfilestorage.TaskFileStorage(task_filename, key_filename)
    my_ctrl = clicontroller.CLIController()
    # TODO: How do we tell main() which subcommand was used?

    print my_ctrl.exec_ui()

    #my_storage.add(my_task)

main()
