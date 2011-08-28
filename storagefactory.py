import filestorage
import gtaskstorage
import sqlitestorage

class StorageFactory():
    def __init__(self):
        pass

    def get(
            self, 
            storage_type, 
            **kwargs):
        if storage_type == 'file':
            try:
                del kwargs['task_dbname']
            except:
                pass
            return filestorage.FileStorage(**kwargs)
        if storage_type == 'gtasks':
            return gtaskstorage.GTaskStorage()
        if storage_type == 'sqlite':
            try:
                del kwargs['task_filename']
            except:
                pass
            try:
                del kwargs['key_filename']
            except:
                pass
            return sqlitestorage.SQLiteStorage(**kwargs)
