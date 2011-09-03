import os
import logging

class KeyGenerator():
    def __init__(self, key_filename='keyfile'):
    # File will hold the ID of the NEXT task
        self.key_filename = key_filename


    #TODO:Make private?
    def read(self):
        logging.info('attempting to read key')
        key = 0
        try:
            logging.debug("try: open file for reading: %s"
                    , self.key_filename)
            key_file = open(self.key_filename, 'r')

            logging.debug("try: read key")
            key = int(key_file.read())
            key_file.close()
        except:
            if os.stat(self.key_filename).st_size == 0:
                logging.debug('success! file is empty; returning key')
                return key
            logging.exception("unable to successfully read key file")
            raise

        logging.debug('success! returning key')
        return key

    #TODO:Make private?
    def write(self, key):
        logging.info('attempting to write key')
        try:
            logging.debug("try: open file for writing: %s"
                    , self.key_filename)
            key_file = open(self.key_filename, 'w')

            logging.debug("try: write key to file")
            key_file.write(str(key))
        except:
            logging.exception("unable to successfully write task file")
            raise

        key_file.close()

    def get(self):
        """Return a unique Task key."""
        logging.info("attempting to retrieve key")
        try:
            key = self.read()
        except:
            logging.exception("failed to access file for reading")
            raise

        try:
            self.write(key)
        except:
            logging.exception("failed to access file for writing")
            raise

        self.update(key)

        logging.debug('success! key retrieved and updated: %s'
                , key)
        return key

    def update(self, key):
        logging.info("attempting to update key")
        key += 1
        try:
            self.write(key)
        except:
            logging.exception("failed to access file for writing")
            raise
        logging.debug('success! key updated')
        return key
