import pickle
import os
import logging

import gflags
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage as gStorage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

import task
import sqlite3

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
        """This functions is to be overridden by a specific storage method."""
        raise NotImplementedError


class FileStorage(Storage):
    def __init__(self, task_filename='taskfile', key_filename='keyfile'):
        Storage.__init__(self)
        self.task_filename = task_filename
        self.key_filename = key_filename

        if not os.path.exists(task_filename):
            logging.info('creating task storage file as it doesn\'t exist: %s'
                    , task_filename)
            open(self.task_filename, 'w').close()
        if not os.path.exists(key_filename):
            logging.info('creating key storage file as it doesn\'t exist: %s'
                    , key_filename)
            open(self.key_filename, 'w').close()


    def _read(self):
        """Read Task list from file"""
        logging.info('attempting to read task list')
        task_list = []
        try:
            logging.debug("try: open file for reading: %s"
                    , self.task_filename)
            task_file = open(self.task_filename, 'r')

            logging.debug("try: load pickled task list")
            task_list = pickle.load(task_file)
            task_file.close()

        except:
            logging.debug('unable to open file for reading')
            if os.stat(self.task_filename).st_size == 0:
                logging.info('success! file is empty; '
                        'returning empty task list')
                return task_list
            logging.exception("unable to successfully read task file")
            raise

        logging.info('success! returning task list')
        return task_list

    def _write(self, task_list):
        """Write Task list to file"""
        logging.info('attempting to write task list')
        try:
            logging.debug('try: open file for writing: %s'
                    , self.task_filename)
            task_file = open(self.task_filename, 'w')

            logging.debug("try: dump pickled task list to file")
            pickle.dump(task_list, task_file, 0)
            task_file.close()
        except:
            logging.exception("unable to successfully write task file")
            raise


    def add(self, task_item):
        """Add a Task to the file storage.

        Arguments:
        task_item -- the Task object to be added to storage

        The Task object is given a key and appended to the list of Tasks in the file.

        """
        logging.info('attempting to add task item:\n%s', task_item)
        try:
            task_list = self._read()
        except:
            logging.exception('failed to access file for reading')
            raise

        key_gen = _KeyGenerator(self.key_filename)
        task_item.key = key_gen.get()

        task_list.append(task_item)
        try:
            self._write(task_list)
        except:
            logging.exception('failed to access file for writing')
            raise

        logging.info('success! task item added:\n%s', task_item)
        return task_item.key

    def find(self, key = None):
        """Return a Task given it's key.

        Arguments:
        key -- the key for the desired Task object

        Using the given key, iterate through the Task list and return the Task
        with matching key. If none is found return None.

        """
        logging.info('attempting to find item with key: %s', key)
        try:
            task_list = self._read()
        except:
            logging.exception('failed to access file for reading')
            raise

        for task_item in task_list:
            if task_item.key == key:
                logging.info('success! task item found with matching key')
                return task_item

        logging.info('no matching key found in task list')
        task_item = None
        return task_item

    def get_all(self):
        """Return a list of all Tasks."""
        logging.info('attempting to get all tasks')
        try:
            task_list = self._read()
        except:
            logging.exception('failed to access file for reading')
            raise

        logging.info('success! returning list of all tasks')
        return task_list

    def update(self, task_item):
        """Update an existing Task in the file storage.

        Arguments:
        task_item -- the Task object to be updated

        Using the given Task's key, iterate through the Task list to find a
        matching key, replace the matching Task with the given Task, and
        return the old Task. If none is found, update nothing and return None.

        """
        logging.info('attempting to update task:\n%s', task_item)
        task_list = self.get_all()
        key_match = None
        #TODO: Call get_all() again except with an arg instead of below loop?
        for i, item in enumerate(task_list):
            if task_item.key == item.key:
                logging.debug('matching task found; updating task')
                key_match = item.key
                task_list[i] = task_item
                try:
                    self._write(task_list)
                except:
                    logging.exception('failed to access file for writing')
                    raise

                logging.info('success! task item updated; returning key')
                return key_match

        logging.info('no matching key found; nothing updated')
        return key_match

    def delete(self, key):
        """Delete an existing Task in the file storage.

        Arguments:
        key -- the key for the desired Task object to delete

        Using the given key, iterate through the Task list and delete the 
        matching Task. If none is found, nothing is deleted and return None.

        """
        logging.info('attempting to delete task: %s', key)
        task_list = self.get_all()
        key_match = None
        #TODO: Call get_all() again except with an arg instead of below loop?
        for i, item in enumerate(task_list):
            if key == item.key:
                logging.debug('matching task found; deleting task')
                key_match = item.key
                del task_list[i]
                try:
                    self._write(task_list)
                except:
                    logging.exception('failed to access file for writing')
                    raise
                logging.info('success! task item deleted')
                return key_match

        logging.info('no matching key found; nothing deleted')
        return key_match

    def search(self, search_task):
        """Return a Task given a search Task

        Arguments:
        search_task -- the Task to be used for searching

        Using the given search Task, iterate through the Task list and append
        matching Tasks to a Task list then return this list. If none matches,
        return None.

        """
        logging.info('attempting to search for task:\n%s', search_task)
        task_list = self.get_all()
        task_search_list = []
        for task_item in task_list:
            if search_task.title == task_item.title\
                    and search_task.notes == task_item.notes:
                logging.debug('matching task found:\n%s', task_item)
                task_search_list.append(task_item)

        if not task_search_list:
            logging.info('no matches found')
            task_search_list = None
        else:
            logging.info('success! returning matching tasks')
        return task_search_list


class SQLiteStorage(Storage):
    def __init__(self, task_dbname='taskdb'):
        Storage.__init__(self)
        self.task_dbname = task_dbname
        self.task_tablename = 'tasks'

        self.db_connection = sqlite3.connect(task_dbname)
        self.db_connection.row_factory = sqlite3.Row
        conn_cursor = self.db_connection.cursor()

        conn_cursor.execute('select name from sqlite_master where name=?'
                , (self.task_tablename,))

        try:
            conn_cursor.fetchone()[0]
        except TypeError:
            logging.info('creating table as it doesn\'t exist: %s'
                   , self.task_tablename)
            conn_cursor.execute(
                    '''create table tasks
                    (id integer primary key,
                    title text,
                    notes text)''')


    def add(self, task_item):
        """Add a Task to the database storage.

        Arguments:
        task_item -- the Task object to be added to storage

        The Task object is given a key and appended to the list of Tasks in
        the database.

        """
        logging.info('attempting to add task item:\n%s', task_item)
        conn_cursor = self.db_connection.cursor()
        result = conn_cursor.execute(
                '''insert into %s (title, notes) values (?, ?)'''
               % self.task_tablename, (task_item.title, task_item.notes))
        task_item.key = result.lastrowid

        self.db_connection.commit()
        conn_cursor.close()
        return task_item.key


    def find(self, key = None):
        """Return a Task given it's key.

        Arguments:
        key -- the key for the desired Task object

        Using the given key, get the Task with the matching key from the
        database and return the Task. If none is found return None.

        """
        logging.info('attempting to find item with key: %s', key)
        conn_cursor = self.db_connection.cursor()
        result = conn_cursor.execute(
                '''select * from %s where id=?'''
               % self.task_tablename, (key,))
        result = result.fetchall()

        if result == []:
            logging.info('no matching key found; nothing updated')
            self.db_connection.commit()
            conn_cursor.close()
            return None

        result = result[0]
        logging.debug('creating Task from retrieved row')
        task_item = task.Task(
                key=result['id'], 
                title=result['title'], 
                notes=result['notes'])

        self.db_connection.commit()
        conn_cursor.close()
        return task_item


    def get_all(self):
        """Return a list of all Task's"""
        logging.info('attempting to get all tasks')
        conn_cursor = self.db_connection.cursor()
        sqltask_list = conn_cursor.execute(
                '''select * from %s ''' % self.task_tablename)

        task_list = []
        for sqltask_item in sqltask_list.fetchmany():
            task_item = task.Task(
                    key=sqltask_item['id'], 
                    title=sqltask_item['title'], 
                    notes=sqltask_item['notes'])
            task_list.append(task_item)

        self.db_connection.commit()
        conn_cursor.close()
        return task_list

    def update(self, task_item):
        """Update an existing Task in the database storage.

        Arguments:
        task_item -- the Task object to be updated

        Using the given Task's key, find the matching Task in the database and
        replace it with the given Task then return the old Task. If none is
        found, update nothing and return None.

        """
        logging.info('attempting to update task:\n%s', task_item)
        conn_cursor = self.db_connection.cursor()
        result = conn_cursor.execute(
                '''update %s set title=?, notes=? where id=?'''
               % self.task_tablename,
                (task_item.title, task_item.notes, task_item.key))

        if result.rowcount == 0:
            logging.info('no matching key found; nothing updated')
            self.db_connection.commit()
            conn_cursor.close()
            return None

        logging.info('success! task item updated; returning key')
        self.db_connection.commit()
        conn_cursor.close()
        return task_item.key

    def delete(self, key):
        """Delete an existing Task in the database storage.

        Arguments:
        key -- the key for the desired Task object to delete

        Using the given key, find the matching Task in the database and
        delete it. If none is found, nothing is deleted and return None.

        """
        logging.info('attempting to delete task: %s', key)
        conn_cursor = self.db_connection.cursor()
        result = conn_cursor.execute(
                '''delete from %s where id=?'''
               % self.task_tablename, (key,))
        if result.rowcount == 0:
            logging.info('no matching key found; nothing updated')
            self.db_connection.commit()
            conn_cursor.close()
            return None

        logging.info('success! task item updated; returning key')
        self.db_connection.commit()
        conn_cursor.close()
        return key

    def search(self, search_task):
        """Return a Task given a search Task

        Arguments:
        search_task -- the Task to be used for searching

        Using the given search Task,

        """
        logging.info('attempting to search for task:\n%s', search_task)
        #pass


FLAGS = gflags.FLAGS
# XXX: Add try/except blocks around GTask API calls
#      Should I be including a key visibly in the program this way?
class GTaskStorage(Storage):
    def __init__(self):
        Storage.__init__(self)
        flow = OAuth2WebServerFlow(
                client_id='651705833552.apps.googleusercontent.com',
                client_secret='Znu3bxWRp8Iii1GwLdBBolde',
                scope='https://www.googleapis.com/auth/tasks',
                user_agent='Task-Organizer/pre-alpha')

        gstorage = gStorage('tasks.dat')
        credentials = gstorage.get()
        if credentials is None or credentials.invalid == True:
            credentials = run(flow, gstorage)

        http = httplib2.Http()
        http = credentials.authorize(http)

        self.service = build(serviceName='tasks', version='v1', http=http,
                       developerKey='AIzaSyBcJBx1IHvzX7Kp7rcGuIzP01tzYY_pX9Y')

    def add(self, task_item):
        # pylint: disable=E1101
        """Add a Task to the GTask storage.

        Arguments:
        task_item -- the Task object to be added to Storage

        The Task object is added to storage and given a key.

        """
        logging.info('attempting to add task item:\n%s', task_item)
        new_task = {
                'title': task_item.title,
                'notes': task_item.notes,
        }

        result = self.service.tasks().insert(
                tasklist='@default',
                body=new_task
        ).execute()
        task_item.key = result['id']
        task_item.title = result['title']
        try:
            task_item.notes = result['notes']
        except KeyError:
            pass
        logging.info('success! task item added\n%s', task_item)
        return task_item.key

    def find(self, key = None):
        # pylint: disable=E1101
        """Return a Task given it's key.

        Arguments:
        key -- the key for the desired Task object

        Using the given key, return the Task with the matching key. If none
        is found return None.
        """
        logging.info('attempting to find item with key: %s', key)
        gtask_item = self.service.tasks().get(
                tasklist='@default',
                task=key
        ).execute()

        try:
            logging.debug('try: check if task is marked as deleted')
            if gtask_item['deleted'] == True:
                logging.debug('task marked as deleted; returning None')
                return None
        except KeyError:
            pass

        task_item = task.Task(
                key = gtask_item['id'],
                title = gtask_item['title'])
        try:
            task_item.notes = gtask_item['notes']
        except KeyError:
            pass

        return task_item

    def get_all(self):
        # pylint: disable=E1101
        """Return a list of all Tasks."""
        logging.info('attempting to get all tasks')
        gtask_list = self.service.tasks().list(tasklist='@default').execute()

        task_list = []
        logging.debug('creating task list from all gtasks')
        for gtask_item in gtask_list['items']:
            task_item = task.Task(
                    key = gtask_item['id'],
                    title = gtask_item['title'])
            try:
                task_item.notes = gtask_item['notes']
            except KeyError:
                pass

            task_list.append(task_item)

        logging.info('success! returning list of all tasks')
        return task_list

    def update(self, task_item):
        # pylint: disable=E1101
        """Update an existing Task in the GTask storage.

        Arguments:
        task_item -- the Task object to be updated

        Using the given Task's key, find the Task with a matching key and
        replace it with the given Task. Then return the old Task. If none
        is found, updating nothing and return None.

        """
        logging.info('attempting to update task:\n%s', task_item)
        updating_task = self.service.tasks().get(
                tasklist='@default',
                task=task_item.key
        ).execute()

        try:
            logging.debug('try: check if task is marked as deleted')
            if updating_task['deleted'] == True:
                logging.debug('task marked as deleted; returning None')
                return None
        except KeyError:
            pass

        logging.debug('updating gtask attributes using supplied task')
        updating_task['title'] = task_item.title
        updating_task['notes'] = task_item.notes

        logging.debug('sending updated gtask')
        result = self.service.tasks().update(
                tasklist='@default',
                task=updating_task['id'],
                body=updating_task
        ).execute()
        task_item.key = result['id']

        logging.info('success! returning updated task key')
        return task_item.key

    def delete(self, key):
        # pylint: disable=E1101
        """Delete an existing Task in the GTask storage.

        Arguments:
        key -- the key for the desired Task object to delete

        Using the given key, delete the matching Task. If none is found,
        nothing is deleted and return None.

        """
        logging.info('attempting to delete task: %s', key)
        deleting_task = self.service.tasks().get(
                tasklist='@default',
                task=key
        ).execute()

        try:
            logging.debug('try: check if task is marked as deleted')
            if deleting_task['deleted'] == True:
                logging.debug('task marked as deleted; returning None')
                return None
        except KeyError:
            pass

        self.service.tasks().delete(tasklist='@default', task=key).execute()
        logging.info('success! returning deleted task\'s key')
        return key

    def search(self, search_task):
        pass


class StorageFactory():
    def __init__(self):
        pass
# TODO: Shouldn't have to delete keywords as incorrect keyword Arguments
        # shouldn't be passed in the first place. However, they are set as
        # defaults in clicontroller.
    @staticmethod
    def get(
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
            except KeyError:
                pass
            return FileStorage(**kwargs)
        if storage_type == 'gtasks':
            return GTaskStorage()
        if storage_type == 'sqlite':
            try:
                del kwargs['task_filename']
            except KeyError:
                pass
            try:
                del kwargs['key_filename']
            except KeyError:
                pass
            return SQLiteStorage(**kwargs)


class _KeyGenerator():
    def __init__(self, key_filename='keyfile'):
    # File will hold the ID of the NEXT task
        self.key_filename = key_filename


    def _read(self):
        """Read key from file"""
        logging.info('attempting to read key')
        key = 0
        try:
            logging.debug("try: open file for reading: %s"
                    , self.key_filename)
            key_file = open(self.key_filename, 'r')

            logging.debug("try: read key")
            key = int(key_file.read())
            key_file.close()
        except:
            if os.stat(self.key_filename).st_size == 0:
                logging.debug('success! file is empty; returning key')
                return key
            logging.exception("unable to successfully read key file")
            raise

        logging.debug('success! returning key')
        return key

    def _write(self, key):
        """Write key to file"""
        logging.info('attempting to write key')
        try:
            logging.debug("try: open file for writing: %s"
                    , self.key_filename)
            key_file = open(self.key_filename, 'w')

            logging.debug("try: write key to file")
            key_file.write(str(key))
        except:
            logging.exception("unable to successfully write task file")
            raise

        key_file.close()

    def get(self):
        """Return a unique Task key."""
        logging.info("attempting to retrieve key")
        try:
            key = self._read()
        except:
            logging.exception("failed to access file for reading")
            raise

        try:
            self._write(key)
        except:
            logging.exception("failed to access file for writing")
            raise

        self._update(key)

        logging.debug('success! key retrieved and updated: %s'
                , key)
        return key

    def _update(self, key):
        """Update key in file by incrementing by 1"""
        logging.info("attempting to update key")
        key += 1
        try:
            self._write(key)
        except:
            logging.exception("failed to access file for writing")
            raise
        logging.debug('success! key updated')
        return key
