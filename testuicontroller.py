import unittest
import logging

class TestTaskFileStorage(unittest.TestCase):
    def setUp(self):
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

        print   # So output from tests is on a new linex

    def tearDown(self):
        # Remove handler so loggers aren't continuously created
        self.logger.removeHandler(self.stderr)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTaskFileStorage)
    unittest.TextTestRunner(verbosity=2).run(suite)
