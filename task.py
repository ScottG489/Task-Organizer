"""Create task objects

Public classes:
    Task
    TaskCreator

Provides ways to intantiate a Task instance.

"""
from textwrap import dedent

# TODO: Should this be private if TaskCreator is to be the only
#       correct way to make a Task instance?
class Task():
    """Instantiate a Task object

    Provides attributes for tasks and methods to compare Task instaces.

    """
    def __init__(self, **kwargs):
        try:
            self.key = kwargs['key']
        except KeyError:
            self.key = None

        try:
            self.title = kwargs['title']
        except KeyError:
            self.title = None

        try:
            self.notes = kwargs['notes']
        except KeyError:
            self.notes = None

#        self.priority = priority
#        self.tags = tags


    def __str__(self):
        return dedent('''\
            ID: %(key)s
            Title: %(title)s
            Notes: %(notes)s''') % {
                'key': self.key,
                'title': self.title,
                'notes': self.notes
        }

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        if self.key == other.key\
                and self.title == other.title\
                and self.notes == other.notes:
            return True
        return False

    def __ne__(self, other):
        if not isinstance(other, Task):
            return True
        if self.key != other.key\
                or self.title != other.title\
                or self.notes != other.notes:
            return True

        return False


class TaskCreator():
    """Create a Task instance automatically

    Public methods:
        build(arg_dict)

    Create a Task instance in a automatic and safer manner."""
    def __init__(self):
        pass

    @staticmethod
    def build(arg_dict):
        """Creates a Task instance given a dictionary

        Args:
            arg_dict (dict): dictionary formatted to create a Task

        The given dictionary must have a correct naming scheme. However, it
        can be missing any field.
        """

        task_item = Task()

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
