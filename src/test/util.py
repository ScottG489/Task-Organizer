import sys
import logger
import logging

logger.LOG.setLevel(logging.CRITICAL)

def verbosity_helper():
    verbosity = 1
    try:
        if sys.argv[1] == '-v':
            verbosity = 2
            logger.LOG.setLevel(logging.CRITICAL)
    except IndexError:
        pass

    return verbosity

def print_helper():
    try:
        if verbosity_helper() == 2:
            sys.stderr.write('\n')   # So output from tests is on a new line
    except IndexError:
        pass
