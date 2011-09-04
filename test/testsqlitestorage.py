import unittest
import teststorage
import sqlitestorage
import task
import os
import logging

#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference
class TestSQLiteStorage(teststorage.TestStorage):
    def setUp(self):
        # Initialize task object with attributes
        self.my_task = task.Task(title='title', notes='note')

        # Initialize test database name
        self.test_task_dbname = 'testtaskdb'

        # Initialize file storage object using test-specific file names
        self.storage = sqlitestorage.SQLiteStorage(
            self.test_task_dbname)

        logging.basicConfig(
            level=logging.WARNING
            ,
            format='[%(asctime)s] %(levelname)s:%(name)s:'
            '%(module)s.%(funcName)s(): %(message)s'
        )

        print   # So output from tests is on a new linex

    def tearDown(self):
        # Delete test database
        os.remove(self.test_task_dbname)

        # Clear the my_task Task object
        self.my_task = None


if __name__ == '__main__':
#    unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSQLiteStorage)
    unittest.TextTestRunner(verbosity=2).run(suite)
