import unittest
import logging
import testuicontroller
import uicontrollerfactory
import os

# TODO: Get logging working in tests.
class TestCLIController(testuicontroller.TestUIController):
    def setUp(self):
        self.test_task_filename = 'test_taskfile'
        self.test_key_filename = 'test_keyfile'

        self.ui = uicontrollerfactory.UIControllerFactory()
        self.ui = self.ui.getUI(
                'cli',
                'file',
                task_filename=self.test_task_filename,
                key_filename=self.test_key_filename)

        # Initialize file storage object using test-specific file names
        logging.basicConfig(
            level=logging.WARNING,
            format='[%(asctime)s] %(levelname)s:%(name)s:'
            '%(module)s.%(funcName)s(): %(message)s'
        )

        self.title = 'tasks title'
        self.notes = 'notes text'
        self.key = None

        open(self.test_task_filename, 'w').close()
        open(self.test_key_filename, 'w').close()

        #print   # So output from tests is on a new linex

    def tearDown(self):
        os.remove(self.test_task_filename)
        os.remove(self.test_key_filename)



if __name__ == '__main__':
    unittest.main()
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestCLIController)
#    unittest.TextTestRunner(verbosity=2).run(suite)
