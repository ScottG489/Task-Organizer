##TODO:
#	Make it so the 'find' subparser requires at least one argument and displays
#		error otherwise.
import task
import uicontroller
import taskfilestorage

def main():
	
	myCtrl = uicontroller.UIController()
	foo = myCtrl.parse_command_line()
	
#	args = arg_parser.parse_args()
#	print args

	my_task = task.Task(''.join(foo.title), ''.join(foo.notes))
	new_task = my_task
	
	print new_task
	
	my_storage = taskfilestorage.TaskFileStorage()
	my_storage.add(new_task)
	print new_task
#	new_task.key = my_storage.add(new_task)
#	
#	print my_task
#	for item in my_storage.read():
##	item = my_storage.find(9)
#		print item

main()
