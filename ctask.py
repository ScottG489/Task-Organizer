##TODO:
#	Make it so the 'find' subparser requires at least one argument and displays
#		error otherwise.
import task
import uicontroller
import taskfilestorage

def main():
	
	myCtrl = uicontroller.UIController()
	foo = myCtrl.parse_command_line()
	
	print foo
#	args = arg_parser.parse_args()
#	print args

	my_task = task.Task(''.join(foo.title), ''.join(foo.notes))
	print my_task
	
	my_storage = taskfilestorage.TaskFileStorage()
	my_storage.add(my_task)
	
	for item in my_storage.find('.*'):
		print item
		print

main()
