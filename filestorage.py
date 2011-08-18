import pickle
import keygenerator
import os
import logging
import storage

class FileStorage(storage.Storage):
    # TODO: Make this and calling funcs take *args instead of using defaults
    def __init__(self, task_filename='taskfile', key_filename='keyfile'):
        self.task_filename = task_filename
        self.key_filename = key_filename

        if not os.path.exists(task_filename):
            open(self.task_filename, 'w').close()
        if not os.path.exists(key_filename):
            open(self.key_filename, 'w').close()


    #TODO:Make private?
    def read(self):
        logging.info('attempting to read task list')
        task_list = []
        try:
            logging.debug("try: open file for reading: %s"
                    % self.task_filename)
            task_file = open(self.task_filename, 'r')

            logging.debug("try: load pickled task list")
            task_list = pickle.load(task_file)
            task_file.close()

        except:
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
                    % self.task_filename)
            task_file = open(self.task_filename, 'w')

            logging.debug("try: dump pickled task list to file")
            pickle.dump(task_list, task_file, 0)
            task_file.close()
        except:
            logging.exception("unable to successfully write task file")
            raise


    def add(self, task_item):
        logging.info('attempting to add task item:\n%s' % task_item)
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

        logging.info('success! task item added:\n%s' % task_item)
        return task_item.key

    def find(self, key = None):
        logging.info('attempting to find item with key: %s' % key)
        try:
            task_list = self.read()
        except:
            logging.exception('failed to access file for reading')
            raise

        logging.debug('finding task list for item with matching key: %s'
                % key)
        for task_item in task_list:
            if key == task_item.key:
                logging.info('success! task item found matching key')
                return task_item

        logging.info('no matching key found in task list')
        task_item = None
        return task_item

    def get_all(self):
        logging.info('attempting to get all tasks')
        try:
            task_list = self.read()
        except:
            logging.exception('failed to access file for reading')
            raise

        logging.info('success! returning list of all tasks')
        return task_list

    def update(self, task_item):
        logging.info('attempting to update task: %s' % task_item)
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

                logging.info('success! task item updated')
                return key_match

        logging.info('no matching key found; nothing updated')
        return key_match

    def delete(self, key):
        logging.info('attempting to delete task: %s' % key)
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
        logging.info('attempting to search for task:\n%s' % search_task)
        task_list = self.get_all()
        task_search_list = []
        for task_item in task_list:
            if search_task.title == task_item.title\
                    and search_task.notes == task_item.notes:
                logging.debug('matching task found:\n%s' % task_item)
                task_search_list.append(task_item)

        if not task_search_list:
            logging.info('no matches found')
        else:
            logging.info('success! returning matching tasks')
        return task_search_list
