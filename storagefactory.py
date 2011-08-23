import filestorage
import gtaskstorage

class StorageFactory():
    def __init__(self):
        pass

    def get(
            self, 
            storage_type, 
            **kwargs):
        if storage_type == 'file':
            return filestorage.FileStorage(**kwargs)
        if storage_type == 'gtasks':
            return gtaskstorage.GTaskStorage()
