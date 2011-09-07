#!/usr/bin/python2
import cliparser

# TODO: Add piping functionality (not directly in ctask):
            # i.e. do a search for a bunch of tasks then pipe that to a delete
    # Make symbol tables (would help standardize even debugging output)
    # Allow find and del to accept a list of keys
    # Rename the subcommand 'find' to 'list'?
def main():
#    task_filename = 'task_file'
#    key_filename = 'key_file'

    my_parser = cliparser.CLIParser()

    parsed_args = my_parser.parse_cl_args()

    something = parsed_args['func'](parsed_args)

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
