"""Logging configuration module

Set's up and configures the root logger which is used by all of the task
modules.

"""
import logging
import sys


LOG = logging.getLogger()
# Set the default logging level to WARNING
LOG.setLevel(logging.WARNING)
FORMATTER = logging.Formatter(
    fmt='[%(asctime)s] %(levelname)s:%(name)s:'
    '%(module)s.%(funcName)s(): %(message)s')

HANDLER = logging.StreamHandler(sys.stderr)
# Set the lowest possible logging level to DEBUG
HANDLER.setLevel(logging.DEBUG)
HANDLER.setFormatter(FORMATTER)
LOG.addHandler(HANDLER)
