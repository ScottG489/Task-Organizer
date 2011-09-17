import task


class TaskCreator():
    def __init__(self):
        pass

    @staticmethod
    def build(arg_dict):
        task_item = task.Task()

        try:
            task_item.key = arg_dict['key']
        except KeyError:
            task_item.key = None

        try:
            task_item.title = arg_dict['title']
        except KeyError:
            task_item.title = None

        try:
            task_item.notes = arg_dict['notes']
        except KeyError:
            task_item.notes = None

        return task_item
