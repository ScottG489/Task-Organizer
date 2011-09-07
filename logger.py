import logging
import sys


log = logging.getLogger()
# Set the default logging level to WARNING
log.setLevel(logging.WARNING)
formatter = logging.Formatter(
    fmt='[%(asctime)s] %(levelname)s:%(name)s:'
    '%(module)s.%(funcName)s(): %(message)s')

handler = logging.StreamHandler(sys.stderr)
# Set the lowest possible logging level to DEBUG
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
log.addHandler(handler)
