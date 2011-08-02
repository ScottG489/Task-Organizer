import taskfilestorage

class TaskStorageFactory():
    def __init__(self):
        pass

    def getStorage(self):
        return taskfilestorage.TaskFileStorage()
