##TODO:
#    Make it so the 'find' subparser requires at least one argument and displays
#        error otherwise.
import task
import uicontroller
import taskfilestorage
import logging

def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s:%(name)s: %(message)s'
    )

    my_ctrl = uicontroller.UIController()
    temp = my_ctrl.parse_command_line()

#    args = arg_parser.parse_args()
#    print args

    my_task = task.Task(''.join(temp.title), ''.join(temp.notes))

    my_storage = taskfilestorage.TaskFileStorage()
    my_storage.add(my_task)
    print my_task

    logging.warning('this is a warning')
    logging.info('this is some info')
#    new_task.key = my_storage.add(new_task)
#
#    print my_task
#    for item in my_storage.read():
##    item = my_storage.find(9)
#        print item

main()
