import pickle
import keygenerator
import os
import logging
import taskstorage

class TaskFileStorage(taskstorage.TaskStorage):
    def __init__(self, task_filename='taskfile', key_filename='keyfile'):
        self.task_file_name = task_filename
        self.key_filename = key_filename

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARNING)

    #TODO:Make private?
    def read(self):
        self.logger.info('attempting to read task list')
        task_list = []
        try:
            self.logger.debug("try: open file for reading: %s"
                    % self.task_file_name)
            task_file = open(self.task_file_name, 'r')

            self.logger.debug("try: load pickled task list")
            task_list = pickle.load(task_file)
            task_file.close()

        except:
            if os.stat(self.task_file_name).st_size == 0:
                self.logger.info('success! file is empty; '
                        'returning empty task list')
                return task_list
            self.logger.exception("unable to successfully read task file")
            raise

        self.logger.info('success! returning task list')
        return task_list

    #TODO:Make private?
    def write(self, task_list):
        self.logger.info('attempting to write task list')
        try:
            self.logger.debug('try: open file for writing: %s'
                    % self.task_file_name)
            task_file = open(self.task_file_name, 'w')

            self.logger.debug("try: dump pickled task list to file")
            pickle.dump(task_list, task_file, 0)
            task_file.close()
        except:
            self.logger.exception("unable to successfully write task file")
            raise


    def add(self, task_item):
        self.logger.info('attempting to add task item:\n%s' % task_item)
        try:
            task_list = self.read()
        except:
            self.logger.exception('failed to access file for reading')
            raise

        key_gen = keygenerator.KeyGenerator(self.key_filename)
        task_item.key = key_gen.get()

        task_list.append(task_item)
        try:
            self.write(task_list)
        except:
            self.logger.exception('failed to access file for writing')
            raise

        self.logger.info('success! task item added:\n%s' % task_item)
        return task_item.key

    def find(self, key = None):
        self.logger.info('attempting to find item with key: %s' % key)
        try:
            task_list = self.read()
        except:
            self.logger.exception('failed to access file for reading')
            raise

        self.logger.debug('finding task list for item with matching key: %s'
                % key)
        for task_item in task_list:
            if key == task_item.key:
                self.logger.info('success! task item found matching key')
                return task_item

        self.logger.info('no matching key found in task list')
        task_item = None
        return task_item

    def get_all(self):
        self.logger.info('attempting to get all tasks')
        try:
            task_list = self.read()
        except:
            self.logger.exception('failed to access file for reading')
            raise

        self.logger.info('success! returning list of all tasks')
        return task_list

    def update(self, task_item):
        self.logger.info('attempting to update task: %s' % task_item)
        task_list = self.get_all()
        key_match = None
        #TODO: Call get_all() again except with an arg instead of below loop?
        for i, item in enumerate(task_list):
            if task_item.key == item.key:
                self.logger.debug('matching task found; updating task')
                key_match = item.key
                task_list[i] = task_item
                try:
                    self.write(task_list)
                except:
                    self.logger.exception('failed to access file for writing')
                    raise

                self.logger.info('success! task item updated')
                return key_match

        self.logger.info('no matching key found; nothing updated')
        return key_match

    def delete(self, key):
        self.logger.info('attempting to delete task: %s' % key)
        task_list = self.get_all()
        key_match = None
        #TODO: Call get_all() again except with an arg instead of below loop?
        for i, item in enumerate(task_list):
            if key == item.key:
                self.logger.debug('matching task found; deleting task')
                key_match = item.key
                del task_list[i]
                try:
                    self.write(task_list)
                except:
                    self.logger.exception('failed to access file for writing')
                    raise
                self.logger.info('success! task item deleted')
                return key_match

        self.logger.info('no matching key found; nothing deleted')
        return key_match

    def search(self, search_task):
        self.logger.info('attempting to search for task:\n%s' % search_task)
        task_list = self.get_all()
        task_search_list = []
        for task_item in task_list:
            if search_task.title == task_item.title\
                    and search_task.notes == task_item.notes:
                self.logger.debug('matching task found:\n%s' % task_item)
                task_search_list.append(task_item)

        if not task_search_list:
            self.logger.info('no matches found')
        else:
            self.logger.info('success! returning matching tasks')
        return task_search_list
