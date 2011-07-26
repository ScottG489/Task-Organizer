import task
import pickle
import keygenerator
import os
import logging

class TaskFileStorage():
    def __init__(self, task_file_name='taskfile', key_file_name='keyfile'):
        self.task_file_name = task_file_name
        self.key_file_name = key_file_name

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    #TODO:Make private?
    #    * raise more informative messages? (ex. if path exists as a dir)
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
                self.logger.debug('success! file is empty; returning empty task list')
                return task_list
            self.logger.exception("unable to successfully read task file")
            raise

        self.logger.debug('success! returning task list')
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
        self.logger.debug('success! task list validated')
        return True

    #TODO:Auto create ID's (make KeyGenerator class)
    def add(self, task_item):
        self.logger.info('attempting to add task item:\n%s' % task_item)
        try:
            task_list = self.read()

            self.logger.debug("try: validate task list")
            self.validate(task_list)
            self.logger.debug("success! returning task list")
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

        self.logger.debug('success! task item successfully added:\n%s' % task_item)
        return task_item.key

    #TODO:Validate the input regular expression here or somewhere
    #    * Return a task instead of a list when key is specified?
    def find(self, key):
        self.logger.info('attempting to find item with key: %s' % key)
        try:
            task_list = self.read()
        except:
            self.logger.exception('failed to access file for reading')
            raise
        self.logger.debug('searching task list for item with matching key: %s' % key)
        task_item = None
        for task_item in task_list:
            if key == task_item.key:
                self.logger.debug('success! task item found matching key')
                return task_item

        self.logger.debug('no matching key found in task list')
        return task_item

    def update(self, task_item):
        pass
    #    return key

    def delete(self, key):
        pass
#        return key

logging.shutdown()
