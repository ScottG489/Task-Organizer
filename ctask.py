##TODO:
#	Make it so the 'find' subparser requires at least one argument and displays
#		error otherwise.
import argparse
import task
import uicontroller

def main():
	
	myCtrl = uicontroller.UIController()
	foo = myCtrl.parse_command_line()
	
	print foo
#	args = arg_parser.parse_args()
#	print args
#	myTask = task.Task(''.join(args.title), ''.join(args.notes))

#	print myTask

main()
