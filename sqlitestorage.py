import logging
import storage
import task
import sqlite3

class SQLiteStorage(storage.Storage):
    def __init__(self, task_dbname='taskdb'):
        self.task_dbname = task_dbname
        self.task_tablename = 'tasks'

        self.db_connection = sqlite3.connect(task_dbname)
        self.db_connection.row_factory = sqlite3.Row
        conn_cursor = self.db_connection.cursor()

        conn_cursor.execute('select name from sqlite_master where name=?'
                , (self.task_tablename,))

        try:
            conn_cursor.fetchone()[0]
        except:
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
        pass

#def main():
#    task_dbname = 'taskdb'
#    db_connection = sqlite3.connect(task_dbname)
#    db_connection.row_factory = sqlite3.Row
#    conn_cursor = db_connection.cursor()
#
#    conn_cursor.execute('drop table tasks')
#    conn_cursor.execute('''create table tasks
#            (id integer primary key,
#            title text,
#            notes text)''')
#
#    title = 'task title'
#    notes = 'task notes'
#
#
#    #result = conn_cursor.execute('select * from tasks where id=4')
#    #print result.fetchall()
#
#
#main()
