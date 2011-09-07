class Storage():
    def __init__(self):
        pass

    def add(self, task_item):
        """This functions is to be overridden by a specific storage method."""
        raise NotImplementedError

    def find(self, key = None):
        """This functions is to be overridden by a specific storage method."""
        raise NotImplementedError

    def get_all(self):
        """This functions is to be overridden by a specific storage method."""
        raise NotImplementedError

    def update(self, task_item):
        """This functions is to be overridden by a specific storage method."""
        raise NotImplementedError

    def delete(self, key):
        """This functions is to be overridden by a specific storage method."""
        raise NotImplementedError

    def search(self, search_task):
        raise NotImplementedError
        """This functions is to be overridden by a specific storage method."""
