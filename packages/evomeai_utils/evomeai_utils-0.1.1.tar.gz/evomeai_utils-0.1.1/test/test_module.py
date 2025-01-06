from evomeai_utils import LogTimer
import logging


logging.basicConfig(level=logging.DEBUG)
with LogTimer('test'):
    print('hello, world')

LogTimer.output()