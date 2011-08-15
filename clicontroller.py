import task
import taskstoragefactory
import uicontroller
import logging

class CLIController(uicontroller.UIController):
    def __init__(self):
        self.storage = taskstoragefactory.TaskStorageFactory()
        self.storage = self.storage.getStorage('file')

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARNING)


    def add(self, cl_args):
        self.logger.info('attempting to add arguments as Task')

        self.logger.debug('creating task from arguments')
        task_item = task.Task(title=cl_args['title'], notes=cl_args['notes'])

        self.logger.info('storing and returning task')
        self.storage.add(task_item)
        return task_item

    def find(self, cl_args):
        self.logger.info('attempting to find Task(s) using arguments')

        if cl_args['key'] == None:
            self.logger.info('no key specified; returning list of all tasks')
            return self.storage.get_all()
        else:
            self.logger.info('finding task with key and returning Task')
            return self.storage.find(cl_args['key'])

    # TODO: Values not specified are overwritten with None. Change this behavior
                # so that (either here or in TaskFileStorage) attributes with a
                # value of None are ignored.
    def edit(self, cl_args):
        self.logger.info('attempting to edit Task using arguments')

        self.logger.debug('creating task from arguments')
        new_task = task.Task(
                key=cl_args['key'],
                title=cl_args['title'],
                notes=cl_args['notes']
        )

        old_task = self.storage.find(cl_args['key'])
        if old_task != None:
            if new_task.title == None:
                new_task.title = old_task.title
            if new_task.notes == None:
                new_task.notes = old_task.notes

        self.logger.info('replacing task with newly created task')
        self.storage.update(new_task)

        return old_task

    def delete(self, cl_args):
        self.logger.info('attempting to delete Task(s) using arguments')

        self.logger.info('deleting task with specified key')
        # TODO: If nothing is specified for del then this returns
                    # all tasks. Create filestorage.find_all()
        deleted_task = self.storage.find(cl_args['key'])
        self.storage.delete(cl_args['key'])

        return deleted_task
