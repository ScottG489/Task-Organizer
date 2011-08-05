import os
import logging

class KeyGenerator():
    def __init__(self, key_filename='keyfile'):
    # File will hold the ID of the NEXT task
        self.key_filename = key_filename

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    #TODO:Make private?
    def read(self):
        self.logger.info('attempting to read key')
        key = 0
        try:
            self.logger.debug("try: open file for reading: %s"
                    % self.key_filename)
            key_file = open(self.key_filename, 'r')

            self.logger.debug("try: read key")
            key = int(key_file.read())
            key_file.close()
        except:
            if os.stat(self.key_filename).st_size == 0:
                self.logger.debug('success! file is empty; returning key')
                return key
            self.logger.exception("unable to successfully read key file")
            raise

        self.logger.debug('success! returning key')
        return key

    #TODO:Make private?
    def write(self, key):
        self.logger.info('attempting to write key')
        try:
            self.logger.debug("try: open file for writing: %s"
                    % self.key_filename)
            key_file = open(self.key_filename, 'w')

            self.logger.debug("try: write key to file")
            key_file.write(str(key))
        except:
            self.logger.exception("unable to successfully write task file")
            raise

        key_file.close()

    def validate(self, key):
        self.logger.info('attempting to validate key')
        if key < 0:
            raise TypeError('invalid or corrupt key file')
        self.logger.debug('success! key validated')
        return True

    def get(self):
        self.logger.info("attempting to retrieve key")
        try:
            key = self.read()
        except:
            self.logger.exception("failed to access file for reading")
            raise

        try:
            self.write(key)
        except:
            self.logger.exception("failed to access file for writing")
            raise

        self.update(key)

        self.logger.debug('success! key retrieved and updated: %s'
                % key)
        return key

    def update(self, key):
        self.logger.info("attempting to update key")
        key += 1
        try:
            self.write(key)
        except:
            self.logger.exception("failed to access file for writing")
            raise
        self.logger.debug('success! key updated')
        return key
