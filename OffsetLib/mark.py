import math
import argparse

import ktl

import KeckLogger

parser = argparse.ArgumentParser(description="Stores current ra and dec offsets",
                         usage="markbase.py")

args = parser.parse_args()

def mark():
    dcs = ktl.Service('dcs')
    instrument = dcs.read('INSTRUME')
    instService = ktl.Service(instrument)
    raoff = dcs['raoff']
    decoff = dcs['decoff']
    raoff = raoff * 180 * 3600 / math.pi
    decoff = decoff * 180 * 3600 / math.pi
    dec = dcs.read('dec')
    raoff = raoff * math.cos(dec)
    instService['RAOFFSET'].write(raoff)
    instService['DECOFFSET'].write(decoff)
    log = KeckLogger.getLogger()
    log.info("[mark] stored offsets RA %f, DEC %f" % (x, y))
    return True

if __name__ =='__main__':
    mark()
