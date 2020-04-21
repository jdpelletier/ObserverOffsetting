import logging
import argparse
from subprocess import Popen, PIPE

from nightpath import nightpath

parser = argparse.ArgumentParser(description="Return the cutom logger",
                         usage="log = getlogger()")

args = parser.parse_args()

def getLogger():
    log = logging.getLogger('MyLogger')
    log.setLevel(logging.INFO)
    nightly = nightpath()
    nightly = nightly / 'instrumentOffsets'
    LogFileHandler = logging.FileHandler(nightly)
    LogFormat = logging.Formatter('%(asctime)s:%(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    LogFileHandler.setFormatter(LogFormat)
    log.addHandler(LogFileHandler)
    return log

if __name__ =='__main__':
    getLogger()
