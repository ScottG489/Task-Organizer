import unittest
import keygenerator
import os
import logging

## Is there a simple way to test non-returning functions?
class TestKeyGenerator(unittest.TestCase):
    def setUp(self):
        # Initialize test file names
        self.test_key_filename = 'testkeyfile'

        # Initialize file storage object using test-specific file names
        self.key_gen = keygenerator.KeyGenerator(
            self.test_key_filename
        )

        logging.basicConfig(
            level=logging.WARNING,
            format='[%(asctime)s] %(levelname)s:%(name)s:'
            '%(module)s.%(funcName)s(): %(message)s'
        )

        # Clear/Create test files
        open(self.test_key_filename, 'w').close()

        print   # So output from tests is on a new linex

    def tearDown(self):
        # Delete test files
        os.remove(self.test_key_filename)


    def test_read(self):
        key = self.key_gen.get()
        key2 = self.key_gen.read()

        self.assertEqual(key, key2 - 1)

    def test_read_corrupt(self):
        file_handler = open(self.test_key_filename, 'w')
        file_handler.write('Mock corrupt data')
        file_handler.close()

        self.assertRaises(ValueError, self.key_gen.read)

    def test_write(self):
        key = self.key_gen.get()
        self.key_gen.write(key)
        key2 = self.key_gen.read()

        self.assertEqual(key, key2)

    def test_write_permission_fail(self):
        os.chmod(self.test_key_filename, 000)

        self.assertRaises(IOError, self.key_gen.write, 0)

    def test_get(self):
        key = self.key_gen.get()
        key2 = self.key_gen.get()

        self.assertEqual(key, key2 - 1)

    def test_get_read_fail(self):
        file_handler = open(self.test_key_filename, 'w')
        file_handler.write('Mock corrupt data')
        file_handler.close()
        os.chmod(self.test_key_filename, 000)

        self.assertRaises(IOError, self.key_gen.get)

    def test_get_write_fail(self):
        os.chmod(self.test_key_filename, 0400)

        self.assertRaises(IOError, self.key_gen.get)

    def test_update(self):
        key = self.key_gen.get()
        key2 = self.key_gen.update(key)

        self.assertEqual(key, key2 - 1)

    def test_update_write_fail(self):
        os.chmod(self.test_key_filename, 0400)

        self.assertRaises(IOError, self.key_gen.update, 0)

if __name__ == '__main__':
#    unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestKeyGenerator)
    unittest.TextTestRunner(verbosity=2).run(suite)
