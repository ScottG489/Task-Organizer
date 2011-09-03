import filestorage
import gtaskstorage
import sqlitestorage

class StorageFactory():
    def __init__(self):
        pass
# TODO: Shouldn't have to delete keywords as incorrect keyword Arguments
        # shouldn't be passed in the first place. However, they are set as
        # defaults in clicontroller.
    def get(
            self, 
            storage_type, 
            **kwargs):
        """Return a Task storage instance.

        Arguments:
        storage_type -- name of the desired storage type
        kwargs -- keyword arguments specific to each storage type

        Using the given storage type, create an instance with the given
        optional keyword arguments and return the storage instance.

        """
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
