#!/usr/bin/python2
import cliparser
import logging

# TODO: Add piping functionality (not directly in ctask):
            # i.e. do a search for a bunch of tasks then pipe that to a delete
    # Make symbol tables (would help standardize even debugging output)
def main():
#    task_filename = 'task_file'
#    key_filename = 'key_file'
    logging.basicConfig(
        level=logging.WARNING,
        format='[%(asctime)s] %(levelname)s:%(name)s:'
        '%(module)s.%(funcName)s(): %(message)s'
    )

    my_parser = cliparser.CLIParser()
    # TODO: How do we tell main() which subcommand was used?

    parsed_args = my_parser.parse_cl_args()

    something = parsed_args['func'](parsed_args)

    if parsed_args['sub_cmd'] == 'find' and parsed_args['key'] == None:
        for item in something:
            print item
    elif something:
        print something
    else:
        print 'Task not found'
    # TODO: This doesn't work because when exec_ui() is caled it calls
                # cliparser which creates a clicontroller object itself which
                # is separate from this one. Fix? Try just calling the parser
    #print my_ui.command_line_arguments

    #my_storage.add(my_task)

main()
