import logging
import argparse
from subprocess import Popen, PIPE

parser = argparse.ArgumentParser(description="Return the cutom logger",
                         usage="log = getlogger()")

args = parser.parse_args()

def getLogger():
    log = logging.getLogger('MyLogger')
    log.setLevel(logging.INFO)
    p = Popen('nightly', stdin=PIPE, stdout=PIPE, stderr=PIPE)
    ouput, err = p.communicate()
    nightpath = output.strip() + 'instrumentOffsets'
    LogFileHandler = logging.FileHandler(nightpath)
    LogConsoleHandler.setLevel(logging.INFO)
    LogFormat = logging.Formatter('%(asctime)s:%(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    LogFileHandler.setFormatter(LogFormat)
    log.addHandler(LogFileHandler)
    return log

if name == __main__:
    getLogger()
