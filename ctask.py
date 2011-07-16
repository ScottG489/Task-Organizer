import argparse
import task

def main():
	arg_parser = argparse.ArgumentParser(description='Task organizer.', epilog='Goodbye.')
	arg_subparsers = arg_parser.add_subparsers(help='Sub command help')
	
	arg_parser_add = arg_subparsers.add_parser('add', help='add help')
	arg_parser_edit = arg_subparsers.add_parser('edit', help='edit help')
	arg_parser_list = arg_subparsers.add_parser('list', help='list help')
	
	arg_parser_add.add_argument('--title', action='store', nargs=1, type=str, required=True, help='The title of the task.')
	arg_parser_add.add_argument('--notes', action='store', nargs=1, type=str, help='Notes about the task.')
	arg_parser_add.add_argument('--priority', action='store', nargs=1, type=int, help='The priority of the task.')
	arg_parser_add.add_argument('--tags', action='store', nargs=1, type=str, help='The tags for the task.')

	#arg_parser_edit.add_argument('--tags', action='store', nargs=1, type=str, help='The tags for the task.')

	#arg_parser_list.add_argument('--title', action='store', nargs=1, type=str, help='The title of the task')

	args = arg_parser.parse_args()
	
	print ''.join(args.title)

	myTask = task.Task(''.join(args.title), ''.join(args.notes))

	print myTask

main()
