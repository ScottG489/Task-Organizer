import task
import pickle
import keygenerator
import os
import logging

class TaskFileStorage():
    def __init__(self, task_filename='taskfile', key_file_name='keyfile'):
        self.task_file_name = task_filename
        self.key_file_name = key_file_name

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    #TODO:Make private?
    def read(self):
        self.logger.info('attempting to read task list')
        task_list = []
        try:
            self.logger.debug("try: open file for reading: %s" % self.task_file_name)
            task_file = open(self.task_file_name, 'r')

            self.logger.debug("try: load pickled task list")
            task_list = pickle.load(task_file)
            task_file.close()

        except:
            if os.stat(self.task_file_name).st_size == 0:
                self.logger.info('success! file is empty; returning empty task list')
                return task_list
            self.logger.exception("unable to successfully read task file")
            raise

        self.logger.info('success! returning task list')
        return task_list

    #TODO:Make private?
    def write(self, task_list):
        self.logger.info('attempting to write task list')
        try:
            self.logger.debug("try: open file for writing: %s" % self.task_file_name)
            task_file = open(self.task_file_name, 'w')

            self.logger.debug("try: dump pickled task list to file")
            pickle.dump(task_list, task_file, 0)
            task_file.close()
        except:
            self.logger.exception("unable to successfully write task file")
            raise


    def validate(self, task_list):
        self.logger.info('attempting to validate task list')
        for item in task_list:
            if not isinstance(item, task.Task):
                self.logger.exception('invalid or corrupt task list')
                raise TypeError('invalid or corrupt task list')
        self.logger.info('success! task list validated')
        return True

    def add(self, task_item):
        self.logger.info('attempting to add task item:\n%s' % task_item)
        try:
            task_list = self.read()
            self.validate(task_list)
        except:
            self.logger.exception('failed to access file for reading')
            raise

        key_gen = keygenerator.KeyGenerator(self.key_file_name)
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
        if key == None:
            try:
                task_list = self.read()
                self.validate(task_list)
                self.logger.debug('no key specified; returning task list')
                return task_list
            except:
                self.logger.exception('failed to access file for reading')
                raise

        try:
            task_list = self.read()
        except:
            self.logger.exception('failed to access file for reading')
            raise

        self.logger.debug('searching task list for item with matching key: %s' % key)
        task_item = None
        for task_item in task_list:
            if key == task_item.key:
                self.logger.info('success! task item found matching key')
                return task_item

        self.logger.info('no matching key found in task list')
        return task_item

    def update(self, task_item):
        task_list = self.find()
        #TODO: Call find() again except with an arg instead of below loop?
        for i, item in enumerate(task_list):
            if task_item.key == item.key:
                key_match = item.key
                task_list[i] = task_item
                self.write(task_list)
                break

        return key_match

    def delete(self, key):
        self.logger.info('attempting to delete task: %s' % key)
        task_list = self.find()
        key_match = None
        #TODO: Call find() again except with an arg instead of below loop?
        for i, item in enumerate(task_list):
            if key == item.key:
                self.logger.debug('matching task found; deleting task')
                key_match = item.key
                del task_list[i]
                self.write(task_list)
                self.logger.info('success! task item deleted')
                return key_match


        return key_match
