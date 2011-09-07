import logging
import sys


log = logging.getLogger()

formatter = logging.Formatter(
    fmt='[%(asctime)s] %(levelname)s:%(name)s:'
    '%(module)s.%(funcName)s(): %(message)s')

handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.CRITICAL)
handler.setFormatter(formatter)
log.addHandler(handler)
