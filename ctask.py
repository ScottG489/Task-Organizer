##TODO:
#    Make it so the 'find' subparser requires at least one argument and displays
#        error otherwise.
import uicontroller
import taskfilestorage
import logging

def main():
    task_filename = 'task_file'
    key_filename = 'key_file'
    logging.basicConfig(
        level=logging.WARNING,
        format='[%(asctime)s] %(levelname)s:%(name)s: %(message)s'
    )
#    open(task_filename, 'w').close()
#    open(key_filename, 'w').close()

    #my_storage = taskfilestorage.TaskFileStorage(task_filename, key_filename)
    my_ctrl = uicontroller.UIController()

    my_ctrl.parse_cl_args()

    #my_storage.add(my_task)

main()
