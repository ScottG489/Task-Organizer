import task
import storagefactory
import uicontroller
import logging

class CLIController(uicontroller.UIController):
    def __init__(self, storage_type, task_filename='taskfile', key_filename='keyfile'):
        self.storage = storagefactory.StorageFactory()
        self.storage = self.storage.getStorage(
                storage_type,
                task_filename=task_filename,
                key_filename=key_filename)



    def add(self, action_info):
        logging.info('attempting to add arguments as Task')

        logging.debug('creating task from arguments')
        task_item = task.Task(
                title=action_info['title'],
                notes=action_info['notes'])

        logging.info('storing and returning task')
        self.storage.add(task_item)
        return task_item

    def find(self, action_info):
        logging.info('attempting to find Task(s) using arguments')

        if action_info['key'] == None:
            logging.info('no key specified; returning list of all tasks')
            return self.storage.get_all()
        else:
            logging.info('finding task with key and returning Task')
            return self.storage.find(action_info['key'])

    # TODO: Values not specified are overwritten with None. Change this behavior
                # so that (either here or in TaskFileStorage) attributes with a
                # value of None are ignored.
    def edit(self, action_info):
        logging.info('attempting to edit Task using arguments')

        logging.debug('creating task from arguments')
        new_task = task.Task(
                key=action_info['key'],
                title=action_info['title'],
                notes=action_info['notes']
        )

        old_task = self.storage.find(action_info['key'])
        if old_task != None:
            if new_task.title == None:
                new_task.title = old_task.title
            if new_task.notes == None:
                new_task.notes = old_task.notes

        logging.info('replacing task with newly created task')
        self.storage.update(new_task)

        return old_task

    def delete(self, action_info):
        logging.info('attempting to delete Task(s) using arguments')

        logging.info('deleting task with specified key')
        deleted_task = self.storage.find(action_info['key'])
        self.storage.delete(action_info['key'])

        return deleted_task
