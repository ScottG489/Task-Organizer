import unittest
import logging
import testuicontroller
import uicontrollerfactory
import os
# TODO: Move all of this to a testuicontroller and make it UI generic
class TestCLIController(testuicontroller.TestUIController):
    def setUp(self):
        self.test_task_filename = 'test_taskfile'
        self.test_key_filename = 'test_keyfile'

        self.ui = uicontrollerfactory.UIControllerFactory()
        self.ui = self.ui.getUI(
                'cli',
                'gtasks',
                task_filename=self.test_task_filename,
                key_filename=self.test_key_filename)

        # Initialize file storage object using test-specific file names
        self.logger = logging.getLogger()
        self.stderr = logging.StreamHandler()
        self.stderr.setLevel(logging.WARNING)
        self.formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s:%(name)s:'
                '%(module)s.%(funcName)s(): %(message)s'
        )
        self.stderr.setFormatter(self.formatter)
        self.logger.addHandler(self.stderr)

        self.title = 'tasks title'
        self.notes = 'notes text'
        self.key = None

        open(self.test_task_filename, 'w').close()
        open(self.test_key_filename, 'w').close()

        #print   # So output from tests is on a new linex

    def tearDown(self):
        # Remove handler so loggers aren't continuously created
        self.logger.removeHandler(self.stderr)
        os.remove(self.test_task_filename)
        os.remove(self.test_key_filename)


    def test_add(self):
        pass

    def test_find(self):
        pass

    def test_find_all(self):
        pass

    def test_edit(self):
        pass

    def test_delete(self):
        pass

if __name__ == '__main__':
    unittest.main()
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestCLIController)
#    unittest.TextTestRunner(verbosity=2).run(suite)
