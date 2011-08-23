class Storage():
    def __init__(self):
        pass

    def add(self, task_item):
        """This functions is to be overridden by a specific storage method."""
        pass

    def find(self, key = None):
        """This functions is to be overridden by a specific storage method."""
        pass

    def get_all(self):
        """This functions is to be overridden by a specific storage method."""
        pass

    def update(self, task_item):
        """This functions is to be overridden by a specific storage method."""
        pass

    def delete(self, key):
        """This functions is to be overridden by a specific storage method."""
        pass

    def search(self, search_task):
        """This functions is to be overridden by a specific storage method."""
        pass
