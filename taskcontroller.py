"""Task controller library

Classes:
    TaskController

The docstring for a module should generally list the classes, exceptions and functions (and any other objects) that are exported by the module, with a one-line summary of each. (These summaries generally give less detail than the summary line in the object's docstring.) The docstring for a package (i.e., the docstring of the package's __init__.py module) should also list the modules and subpackages exported by the package.
"""
import taskstorage
import logging

# XXX: I believe this needs error handling.
class TaskController():
    """Interface to manipulate Tasks

    Args:
        storage_type (str): Type of storage in which to persist Tasks

    Kwargs:
        task_dbname (str): Name of the sqlite database file.
        task_filename (str): Name of the file when using file storage.
        key_filename (str): Name of the key file when using file storage.

    Methods:
        add(task_item)
        find(task_item)
        edit(task_item)
        delete(task_item)

    API for working with Task objects.

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

        Args:
            task_item (Task): Task object to add to storage

        Returns:
            task_item (Task): Newly added Task with key

        The given task is added to storage.

        """
        logging.info('attempting to add arguments as Task')

        logging.info('storing and returning task')
        self._storage.add(task_item)
        return task_item

    def find(self, task_item):
        # pylint: disable=E1103
        """Return all Tasks or one with matching key.

        Arguments:
            task_item (Task): Task object to find in storage.

        Returns:
            task_list (Task[]): Returned if task_item.key is None.
            task_match (Task): Returned if key has matching Task.
            None (None): Returned if key has no matching Task.

        Using the given Task, return a list of all Tasks if it's key is None.
        Return a single Task if a key is specified and there is a Task in
        storage with a matching key.

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
            task_item (Task): Task with matching key and updated attributes.

        Returns:
            old_task (Task): Task as it was in storage before being updated.

        Using the given Task's key, finds a Task instorage with a matching key
        and replaces it with the new Task's attributes that aren't None.

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
            task_item (Task): Task to use to delete a Task in storage.

        Returns:
            deleted_task (Task): Task that was in storage before being deleted.

        Using the given Task's key, if a Task with a matching key is found in
        storage, delete it.

        """
        logging.info('attempting to delete Task(s) using arguments')

        deleted_task = self._storage.find(task_item.key)
        self._storage.delete(task_item.key)

        logging.info('success! task deleted')
        return deleted_task

#    def search(self, task_item):
#        pass
