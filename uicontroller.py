class UIController():
    def __init__(self):
        pass

    def add(self, args):
        """This functions is to be overridden by a specific storage method."""
        raise NotImplementedError

    def find(self, args):
        """This functions is to be overridden by a specific storage method."""
        raise NotImplementedError

    def edit(self, args):
        """This functions is to be overridden by a specific storage method."""
        raise NotImplementedError

    def delete(self, args):
        """This functions is to be overridden by a specific storage method."""
        raise NotImplementedError
