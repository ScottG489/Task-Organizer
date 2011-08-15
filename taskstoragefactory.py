import taskfilestorage
import gtaskstorage

class TaskStorageFactory():
    def __init__(self):
        pass

    def getStorage(self, storage_type):
        if storage_type == 'file':
            return taskfilestorage.TaskFileStorage()
        if storage_type == 'gtask':
            return gtaskstorage.GTaskStorage()
