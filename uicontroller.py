##TODO:
#	Make it so the 'find' subparser requires at least one argument and displays
#		error otherwise.
import argparse

class UIController():
	def parse_command_line(self):
		arg_parser = argparse.ArgumentParser(
			description='Task organizer.',
			epilog='Goodbye.'
		)
		arg_subparsers = arg_parser.add_subparsers(
			help='valid sub-commands'
		)
	##Add sub-command arguments
		arg_parser_add = arg_subparsers.add_parser(
			'add',
			help='add a task'
		)
		arg_parser_add.add_argument(
			'--title',
			action='store',
			nargs=1,
			type=str,
			required=True,
			help='the title of the task'
		)
		arg_parser_add.add_argument('--notes',
			action='store',
			nargs=1,
			type=str,
			help='notes	about the task'
		)
	#	arg_parser_add.add_argument('--priority',
	#		action='store',
	#		nargs=1,
	#		type=int,
	#		help='the priority of the task'
	#	)
#		arg_parser_add.add_argument('--tags',
#			action='store',
#			nargs=1,
#			type=str,
#			help='the tags for the task'
#		)
	##Find sub-command arguments
		arg_parser_find = arg_subparsers.add_parser(
			'find',
			help='find and get information on tasks'
		)
		arg_parser_find.add_argument('--key',
			action='store',
			nargs=1,
			type=int,
			help='the key of the task')
		arg_parser_find.add_argument('--title',
			action='store',
			nargs=1,
			type=str,
			help='a regular expression of the title of the task'
		)
	##Edit sub-command arguments
		arg_parser_edit = arg_subparsers.add_parser(
			'edit',
			help='edit tasks'
		)
		arg_parser_edit.add_argument('--key',
			action='store',
			nargs=1,
			type=int,
			help='the key of the task'
		)
		arg_parser_edit.add_argument('--title',
			action='store',
			nargs=1,
			type=str,
			help='a regular expression of the title of the task'
		)
		arg_parser_edit.add_argument('--notes',
			action='store',
			nargs=1,
			type=str,
			help='notes about the task'
		)
	#	arg_parser_edit.add_argument('--priority',
	#		action='store',
	#		nargs=1,
	#		type=int,
	#		help='the priority of the task'
	#	)
#		arg_parser_edit.add_argument('--tags',
#			action='store',
#			nargs=1,
#			type=str,
#			help='the tags for the task'
#		)
	##Delete sub-command arguments
		arg_parser_delete = arg_subparsers.add_parser(
			'del',
			help='delete tasks'
		)
		arg_parser_delete.add_argument('--key',
			action='store',
			nargs=1,
			type=int,
			help='the key of the task'
		)
		arg_parser_delete.add_argument('--title',
			action='store',
			nargs=1,
			type=str,
			help='a regular expression of the title of the task'
		)

		return arg_parser.parse_args()
