"""Task controller library

Classes:
    TaskController

The docstring for a module should generally list the classes, exceptions and functions (and any other objects) that are exported by the module, with a one-line summary of each. (These summaries generally give less detail than the summary line in the object's docstring.) The docstring for a package (i.e., the docstring of the package's __init__.py module) should also list the modules and subpackages exported by the package.
"""
import task
import taskstorage
import logging

# XXX: I believe this needs error handling.
class TaskController():
    """
    """
    def __init__(self,
            storage_type, 
            task_dbname='taskdb',
            task_filename='taskfile',
            key_filename='keyfile'):
        self._storage = taskstorage.StorageFactory.get(
                storage_type,
                task_dbname=task_dbname,
                task_filename=task_filename,
                key_filename=key_filename)


    def add(self, task_item):
        # pylint: disable=E1103
        """Return a Task given an argument dictionary.

        Arguments:
        action_info -- dictionary created from command line arguments

        Using the given dictionary, a Task object is created and added to
        storage.

        """
        logging.info('attempting to add arguments as Task')

        logging.info('storing and returning task')
        self._storage.add(task_item)
        return task_item

    def find(self, task_item):
        # pylint: disable=E1103
        """Return all Tasks or one with matching key.

        Arguments:
        action_info -- dictionary created from command line arguments

        Using the given dictionary, return a list of all Tasks if the given key
        is None. Return a single Task if a key is found to match the given key.

        """
        logging.info('attempting to find Task(s) using arguments')

        if task_item.key == None:
            logging.info('no key specified; returning list of all tasks')
            return self._storage.get_all()
        else:
            logging.info('finding task with key and returning Task')
            return self._storage.find(task_item.key)

    def edit(self, task_item):
        # pylint: disable=E1103
        """Edit an existing Task.

        Arguments:
        action_info -- dictionary created from command line arguments

        Using the given dictionary, create a Task object. If any attributes
        are None, replace those values with the values of the current values
        of the Task being updated then update the Task in storage.

        """
        logging.info('attempting to edit Task using arguments')

        logging.debug('using old task attributes if new ones are\'t given')
        old_task = self._storage.find(task_item.key)
        if old_task != None:
            if task_item.title == None:
                task_item.title = old_task.title
            if task_item.notes == None:
                task_item.notes = old_task.notes

        logging.info('replacing task with newly created task')
        self._storage.update(task_item)

        return old_task

    def delete(self, task_item):
        # pylint: disable=E1103
        """Delete an existing Task.

        Arguments:
        action_info -- dictionary created from command line arguments

        Using the given dictionary's key, attempt to delete the Task if a
        matching key is found.

        """
        logging.info('attempting to delete Task(s) using arguments')

        deleted_task = self._storage.find(task_item.key)
        self._storage.delete(task_item.key)

        logging.info('success! task deleted')
        return deleted_task
