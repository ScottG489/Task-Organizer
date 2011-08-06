import task
import taskstoragefactory
import uicontroller
import logging

class CLIController(uicontroller.UIController):
    def __init__(self):
        self.storage = taskstoragefactory.TaskStorageFactory()
        self.storage = self.storage.getStorage()

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def add(self, cli_args):
        self.logger.info('attempting to add arguments as Task')
        if cli_args.title:
            cli_args.title = ''.join(cli_args.title)
        if cli_args.notes:
            cli_args.notes = ''.join(cli_args.notes)

        self.logger.debug('creating task from arguments')
        task_item = task.Task(title=cli_args.title, notes=cli_args.notes)

        self.logger.info('storing task and returning its key')
        return self.storage.add(task_item)

    def find(self, cli_args):
        self.logger.info('attempting to find Task(s) using arguments')
        if cli_args.key:
            cli_args.key = int(''.join(map(str, cli_args.key)))

        if not cli_args.key:
            self.logger.info('no key specified; returning list of all tasks')
            return self.storage.find(cli_args.key)
        else:
            self.logger.info('finding task with key and returning Task')
            return self.storage.find(cli_args.key)

    # TODO: Values not specified are overwritten with None. Change this behavior
                # so that (either here or in TaskFileStorage) attributes with a
                # value of None are ignored.
    def edit(self, cli_args):
        self.logger.info('attempting to edit Task using arguments')
        if cli_args.key:
            cli_args.key = int(''.join(map(str, cli_args.key)))
        if cli_args.title:
            cli_args.title = ''.join(cli_args.title)
        if cli_args.notes:
            cli_args.notes = ''.join(cli_args.notes)

        self.logger.debug('creating task from arguments')
        task_item = task.Task(key=cli_args.key, title=cli_args.title, notes=cli_args.notes)

        self.logger.info('replacing task with newly created task')
        return self.storage.update(task_item)

    def delete(self, cli_args):
        self.logger.info('attempting to delete Task(s) using arguments')
        if cli_args.key:
            cli_args.key = int(''.join(map(str, cli_args.key)))

        self.logger.info('deleting task with specified key')
        return self.storage.delete(cli_args.key)
