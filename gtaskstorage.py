import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage as gStorage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

import task
import storage

FLAGS = gflags.FLAGS

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
        return task_item.key

    def find(self, key = None):
        gtask_item = self.service.tasks().get(
                tasklist='@default',
                task=key
        ).execute()

        try:
            if gtask_item['deleted'] == True:
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
        gtask_list = self.service.tasks().list(tasklist='@default').execute()
        task_list = []
        for gtask_item in gtask_list['items']:
            task_item = task.Task(
                    key = gtask_item['id'],
                    title = gtask_item['title'])
            try:
                task_item.notes = gtask_item['notes']
            except:
                pass

            task_list.append(task_item)

        return task_list

    def update(self, task_item):
        updating_task = self.service.tasks().get(
                tasklist='@default',
                task=task_item.key
        ).execute()
        updating_task['title'] = task_item.title
        try:
            updating_task['notes'] = task_item.notes
        except:
            pass

        result = self.service.tasks().update(
                tasklist='@default',
                task=updating_task['id'],
                body=updating_task
        ).execute()
        task_item.key = result['id']

        return task_item.key

    def delete(self, key):
        self.service.tasks().delete(tasklist='@default', task=key).execute()
        return key
