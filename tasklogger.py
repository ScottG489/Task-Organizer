import logging

class TaskLogger():
    def __init__(self, log_level=logging.DEBUG):
        logging.basicConfig(level=log_level)
