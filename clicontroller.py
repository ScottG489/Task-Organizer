import task
import taskstoragefactory
import uicontroller

class CLIController(uicontroller.UIController):
    def __init__(self):
        self.storage = taskstoragefactory.TaskStorageFactory()
        self.storage = self.storage.getStorage()

    def add(self, args):
        if args.title:
            args.title = ''.join(args.title)
        if args.notes:
            args.notes = ''.join(args.notes)
        task_item = task.Task(title=args.title, notes=args.notes)

        self.storage.add(task_item)

    def find(self, args):
        if args.key:
            args.key = int(''.join(map(str, args.key)))

        for task_item in self.storage.find(args.key):
            print task_item
        #print self.file_storage.find(args.key)

    def edit(self, args):
        if args.key:
            args.key = int(''.join(map(str, args.key)))
        if args.title:
            args.title = ''.join(args.title)
        if args.notes:
            args.notes = ''.join(args.notes)

        task_item = task.Task(args.key, args.title, args.notes)

        self.storage.update(task_item)

    def delete(self, args):
        if args.key:
            args.key = int(''.join(map(str, args.key)))

        print self.storage.delete(args.key)
