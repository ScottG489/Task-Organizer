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
        try:
            # Try to open file for reading
            self.logger.debug('try: open file for reading: \'%s\'' % self.task_file_name)
            task_file = open(self.task_file_name, 'r')
            # Try to load task_list
            try:
                self.logger.debug('try: load pickled task list')
                task_list = pickle.load(task_file)
                task_file.close()
                # Try to validate file contents.
                try:
                    self.logger.debug('try: validate task list')
                    self.validate(task_list)
                    self.logger.debug('success! returning task list')
                # If file is not valid; raise
                except TypeError:
                    self.logger.exception('file failed to validate')
                    raise
            # If task list won't load, check if it's empty
            except:
                self.logger.debug('checking if file is empty')
                # If the file is empty there are no tasks; return empty list
                if os.stat(self.task_file_name).st_size == 0:
                    task_list = []
                    self.logger.debug('success! file is empty; returning empty list')
                # If also not empty, file is in an unreadable format; raise
                else:
                    self.logger.exception('file is corrupt or in an unreadable format')
                    raise
        # If file won't open for reading, check that it exists as a file
        except:
            self.logger.debug('checking if file path exists')
            # If path doesn't exist as a file, create it and return empty list
            if not os.path.exists(self.task_file_name):
                open(self.task_file_name, 'w').close()
                task_list = []
                self.logger.debug('success! file was created; returning empty list')
            # If it also exists then we can't use it; raise.
            else:
                self.logger.exception('file can\'t be read')
                raise

        return task_list

    #TODO:Make private?
    def write(self, task_list):
        self.logger.info('attempting to write task list')
        try:
            # Try to open file for    writing 
            self.logger.debug('try: open file for writing: \'%s\'' % self.task_file_name)
            task_file = open(self.task_file_name, 'w')
            # Try to load task_list
            try:
                self.logger.debug('try: load pickled task list')
                temp_task_list = pickle.load(task_file)
                task_file.close()
                # Try to validate file contents.
                try:
                    self.logger.debug('try: validate task list')
                    self.validate(temp_task_list)
                # If file is not valid; raise
                except TypeError:
                    self.logger.exception('file failed to validate')
                    raise
                # If the file is valid, write to it
                pickle.dump(task_list, task_file, 0)
            # If task list won't load, check if it's empty
            except:
                self.logger.warning('failed to open file for writing')
                self.logger.debug('checking if file is empty')
                # If the file is empty there are no tasks to validate
                if os.stat(self.task_file_name).st_size == 0:
                    pickle.dump(task_list, task_file, 0)
                    self.logger.debug('success! file is empty; dumping pickled object')
                # If also not empty, file is in an unreadable format; raise
                else:
                    self.logger.exception('file is corrupt or in an unreadable format')
                    raise
        # If file won't open for writing, we can't do anything; raise
        except:
            self.logger.exception('file can\'t be read')
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
        self.logger.info('attempting to add task item: %s' % task_item)
        try:
            task_list = self.read()
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

        self.logger.debug('success! task item successfully added')
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
