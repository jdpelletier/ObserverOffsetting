import ktl
import math
import argparse

parser = argparse.ArgumentParser(description="Stores current ra and dec offsets",
                         usage="markbase.py")
def mark():
    dcs = ktl.Service('dcs')
    instrument = dcs.read('INSTRUMENT')
    instService = ktl.Service(instrument)
    raoff = dcs['raoff']
    decoff = dcs['decoff']
    raoff = raoff * 180 * 3600 / math.pi
    decoff = decoff * 180 * 3600 / math.pi
    dec = dcs.read('dec')
    raoff = raoff * math.cos(dec)
    instService['RAOFFSET'].write(raoff)
    instService['DECOFFSET'].write(decoff)
    #TODO logging
    return True

if name == __main__:
    mark()
