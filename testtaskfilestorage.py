import unittest
import testtaskstorage

#TODO:  add() returns a key but it isn't necessary to assign it since it's
#           pass by reference
class TestTaskFileStorage(testtaskstorage.TestTaskStorage):
    def test_read(self):
        self.my_task.key = self.file_storage.add(self.my_task)
        task_list = self.file_storage.read()

        self.assertEqual(self.my_task, task_list[0])

    def test_write(self):
        self.file_storage.write([self.my_task])
        task_list = self.file_storage.read()

        self.assertEqual(self.my_task, task_list[0])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTaskFileStorage)
    unittest.TextTestRunner(verbosity=2).run(suite)
