import unittest
import keygenerator
import os
import logging

## Is there a simple way to test non-returning functions?
class TestKeyGenerator(unittest.TestCase):
    def setUp(self):
        # Initialize test file names
        self.test_key_file_name = 'testkeyfile'

        # Initialize file storage object using test-specific file names
        self.key_gen = keygenerator.KeyGenerator(
            self.test_key_file_name
        )

        self.logger = logging.getLogger()
        self.stderr = logging.StreamHandler()
        self.stderr.setLevel(logging.WARNING)
        self.formatter = logging.Formatter(
                '[%(asctime)s] %(levelname)s:%(name)s:'
                '%(module)s.%(funcName)s(): %(message)s'
        )
        self.stderr.setFormatter(self.formatter)
        self.logger.addHandler(self.stderr)

        # Clear/Create test files
        open(self.test_key_file_name, 'w').close()
        
#        print   # So output from tests is on a new linex

    def tearDown(self):
        # Delete test files
        os.remove(self.test_key_file_name)

        # Remove handler so loggers aren't continuously created
        self.logger.removeHandler(self.stderr)

    def test_read(self):
        key = self.key_gen.get()
        key2 = self.key_gen.read()

        self.assertEqual(key, key2 - 1)


    def test_write(self):
        key = self.key_gen.get()
        self.key_gen.write(key)
        key2 = self.key_gen.read()

        self.assertEqual(key, key2)

#    def test_validate(self):
#        key = self.key_gen.get()
#
#        self.assertTrue(self.key_gen.validate(key))

    def test_get(self):
        key = self.key_gen.get()
        key2 = self.key_gen.get()

        self.assertEqual(key, key2 - 1)
    
    def test_update(self):
        key = self.key_gen.get()
        key2 = self.key_gen.update(key)

        self.assertEqual(key, key2 - 1)

if __name__ == '__main__':
    unittest.main()
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestKeyGenerator)
#    unittest.TextTestRunner(verbosity=2).run(suite)
