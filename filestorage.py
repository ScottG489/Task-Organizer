import pickle
import keygenerator
import os
import logging
import storage

class FileStorage(storage.Storage):
    def __init__(self, task_filename='taskfile', key_filename='keyfile'):
        self.task_filename = task_filename
        self.key_filename = key_filename

        if not os.path.exists(task_filename):
            logging.info('creating task storage file as it doesn\'t exist: %s'
                    , task_filename)
            open(self.task_filename, 'w').close()
        if not os.path.exists(key_filename):
            logging.info('creating key storage file as it doesn\'t exist: %s'
                    , key_filename)
            open(self.key_filename, 'w').close()


    #TODO:Make private?
    def read(self):
        logging.info('attempting to read task list')
        task_list = []
        try:
            logging.debug("try: open file for reading: %s"
                    , self.task_filename)
            task_file = open(self.task_filename, 'r')

            logging.debug("try: load pickled task list")
            task_list = pickle.load(task_file)
            task_file.close()

        except:
            logging.debug('unable to open file for reading')
            if os.stat(self.task_filename).st_size == 0:
                logging.info('success! file is empty; '
                        'returning empty task list')
                return task_list
            logging.exception("unable to successfully read task file")
            raise

        logging.info('success! returning task list')
        return task_list

    #TODO:Make private?
    def write(self, task_list):
        logging.info('attempting to write task list')
        try:
            logging.debug('try: open file for writing: %s'
                    , self.task_filename)
            task_file = open(self.task_filename, 'w')

            logging.debug("try: dump pickled task list to file")
            pickle.dump(task_list, task_file, 0)
            task_file.close()
        except:
            logging.exception("unable to successfully write task file")
            raise


    def add(self, task_item):
        """Add a Task to the file storage.

        Arguments:
        task_item -- the Task object to be added to storage

        The Task object is given a key and appended to the list of Tasks in the file.

        """
        logging.info('attempting to add task item:\n%s', task_item)
        try:
            task_list = self.read()
        except:
            logging.exception('failed to access file for reading')
            raise

        key_gen = keygenerator.KeyGenerator(self.key_filename)
        task_item.key = key_gen.get()

        task_list.append(task_item)
        try:
            self.write(task_list)
        except:
            logging.exception('failed to access file for writing')
            raise

        logging.info('success! task item added:\n%s', task_item)
        return task_item.key

    def find(self, key = None):
        """Return a Task given it's key.

        Arguments:
        key -- the key for the desired Task object

        Using the given key, iterate through the Task list and return the Task
        with matching key. If none is found return None.

        """
        logging.info('attempting to find item with key: %s', key)
        try:
            task_list = self.read()
        except:
            logging.exception('failed to access file for reading')
            raise

        for task_item in task_list:
            if task_item.key == key:
                logging.info('success! task item found with matching key')
                return task_item

        logging.info('no matching key found in task list')
        task_item = None
        return task_item

    def get_all(self):
        """Return a list of all Tasks."""
        logging.info('attempting to get all tasks')
        try:
            task_list = self.read()
        except:
            logging.exception('failed to access file for reading')
            raise

        logging.info('success! returning list of all tasks')
        return task_list

    def update(self, task_item):
        """Update an existing Task in the file storage.

        Arguments:
        task_item -- the Task object to be updated

        Using the given Task's key, iterate through the Task list to find a
        matching key, replace the matching Task with the given Task, and
        return the old Task. If none is found, update nothing and return None.

        """
        logging.info('attempting to update task:\n%s', task_item)
        task_list = self.get_all()
        key_match = None
        #TODO: Call get_all() again except with an arg instead of below loop?
        for i, item in enumerate(task_list):
            if task_item.key == item.key:
                logging.debug('matching task found; updating task')
                key_match = item.key
                task_list[i] = task_item
                try:
                    self.write(task_list)
                except:
                    logging.exception('failed to access file for writing')
                    raise

                logging.info('success! task item updated; returning key')
                return key_match

        logging.info('no matching key found; nothing updated')
        return key_match

    def delete(self, key):
        """Delete an existing Task in the file storage.

        Arguments:
        key -- the key for the desired Task object to delete

        Using the given key, iterate through the Task list and delete the 
        matching Task. If none is found, nothing is deleted and return None.

        """
        logging.info('attempting to delete task: %s', key)
        task_list = self.get_all()
        key_match = None
        #TODO: Call get_all() again except with an arg instead of below loop?
        for i, item in enumerate(task_list):
            if key == item.key:
                logging.debug('matching task found; deleting task')
                key_match = item.key
                del task_list[i]
                try:
                    self.write(task_list)
                except:
                    logging.exception('failed to access file for writing')
                    raise
                logging.info('success! task item deleted')
                return key_match

        logging.info('no matching key found; nothing deleted')
        return key_match

    def search(self, search_task):
        """Return a Task given a search Task

        Arguments:
        search_task -- the Task to be used for searching

        Using the given search Task, iterate through the Task list and append
        matching Tasks to a Task list then return this list. If none matches,
        return None.

        """
        logging.info('attempting to search for task:\n%s', search_task)
        task_list = self.get_all()
        task_search_list = []
        for task_item in task_list:
            if search_task.title == task_item.title\
                    and search_task.notes == task_item.notes:
                logging.debug('matching task found:\n%s', task_item)
                task_search_list.append(task_item)

        if not task_search_list:
            logging.info('no matches found')
            task_search_list = None
        else:
            logging.info('success! returning matching tasks')
        return task_search_list
