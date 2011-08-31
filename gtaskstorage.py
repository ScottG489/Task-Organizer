import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage as gStorage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

import task
import storage
import logging

FLAGS = gflags.FLAGS

# XXX: Add try/except blocks around GTask API calls
#      Should I be including a key visibly in the program this way?
class GTaskStorage(storage.Storage):
    def __init__(self):
        FLOW = OAuth2WebServerFlow(
                client_id='651705833552.apps.googleusercontent.com',
                client_secret='Znu3bxWRp8Iii1GwLdBBolde',
                scope='https://www.googleapis.com/auth/tasks',
                user_agent='Task-Organizer/pre-alpha')

        gstorage = gStorage('tasks.dat')
        credentials = gstorage.get()
        if credentials is None or credentials.invalid == True:
            credentials = run(FLOW, gstorage)

        http = httplib2.Http()
        http = credentials.authorize(http)

        self.service = build(serviceName='tasks', version='v1', http=http,
                       developerKey='AIzaSyBcJBx1IHvzX7Kp7rcGuIzP01tzYY_pX9Y')

    def add(self, task_item):
        """Add a Task to the GTask storage.

        Arguments:
        task_item -- the Task object to be added to Storage

        The Task object is added to storage and given a key.

        """
        logging.info('attempting to add task item:\n%s' % task_item)
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
        task_item.notes = result['notes']
        logging.info('success! task item added\n%s' % task_item)
        return task_item.key

    def find(self, key = None):
        """Return a Task given it's key.

        Arguments:
        key -- the key for the desired Task object

        Using the given key, return the Task with the matching key. If none
        is found return None.
        """
        logging.info('attempting to find item with key: %s' % key)
        gtask_item = self.service.tasks().get(
                tasklist='@default',
                task=key
        ).execute()

        try:
            logging.debug('try: check if task is marked as deleted')
            if gtask_item['deleted'] == True:
                logging.debug('task marked as deleted; returning None')
                return None
        except:
            pass

        task_item = task.Task(
                key = gtask_item['id'],
                title = gtask_item['title'])
        try:
            task_item.notes = gtask_item['notes']
        except:
            pass

        return task_item

    def get_all(self):
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
            except:
                pass

            task_list.append(task_item)

        logging.info('success! returning list of all tasks')
        return task_list

    def update(self, task_item):
        """Update an existing Task in the GTask storage.

        Arguments:
        task_item -- the Task object to be updated

        Using the given Task's key, find the Task with a matching key and
        replace it with the given Task. Then return the old Task. If none
        is found, updating nothing and return None.

        """
        logging.info('attempting to update task:\n%s' % task_item)
        updating_task = self.service.tasks().get(
                tasklist='@default',
                task=task_item.key
        ).execute()

        try:
            logging.debug('try: check if task is marked as deleted')
            if updating_task['deleted'] == True:
                logging.debug('task marked as deleted; returning None')
                return None
        except:
            pass

        logging.debug('updating gtask attributes using supplied task')
        updating_task['title'] = task_item.title
        try:
            updating_task['notes'] = task_item.notes
        except:
            pass

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
        """Delete an existing Task in the GTask storage.

        Arguments:
        key -- the key for the desired Task object to delete

        Using the given key, delete the matching Task. If none is found,
        nothing is deleted and return None.

        """
        logging.info('attempting to delete task: %s' % key)
        deleting_task = self.service.tasks().get(
                tasklist='@default',
                task=key
        ).execute()

        try:
            logging.debug('try: check if task is marked as deleted')
            if deleting_task['deleted'] == True:
                logging.debug('task marked as deleted; returning None')
                return None
        except:
            pass

        self.service.tasks().delete(tasklist='@default', task=key).execute()
        logging.info('success! returning deleted task\'s key')
        return key

    def search(self, search_task):
        pass
