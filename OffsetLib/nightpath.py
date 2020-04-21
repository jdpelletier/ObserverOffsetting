import datetime
from pathlib import Path
import argparse

import ktl

parser = argparse.ArgumentParser(description="Returns path to nightly directory and if it exists",
                         usage="nightpath.py")

args = parser.parse_args()

def nightpath():
    nightly = Path('/s')
    tel = ktl.read('dcs', 'TELESCOP')
    if tel == 'Keck I':
        nightly = nightly / 'nightly1'
    else:
        nightly = nightly / 'nightly2'
    date = datetime.datetime.now()
    year, month, day = str(date.strftime("%y")), str(date.strftime("%m")), str(date.strftime("%d"))
    nightly = nightly / year / month / day
    return nightly

def checkNightpath():
    nightly = nightpath()
    return nightly.exists()

if __name__ =='__main__':
    print(nightpath())
    print('Path exists: %s' % checkNightpath())
