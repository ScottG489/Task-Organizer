import filestorage
import gtaskstorage

class StorageFactory():
    def __init__(self):
        pass

    def getStorage(
            self, 
            storage_type, 
            task_filename='taskfile', 
            key_filename='keyfile'):
        if storage_type == 'file':
            return filestorage.FileStorage(task_filename, key_filename)
        if storage_type == 'gtasks':
            return gtaskstorage.GTaskStorage()
