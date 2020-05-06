import argparse

import ktl

from wftel import wftel
import KeckLogger

parser = argparse.ArgumentParser(description="Move the telescope detctor coordinates",
                         usage="mxy.py [-n] [-a] instxoff instyoff")

parser.add_argument("-n", "--nomove", action='store_true',
                         help="don't send moves")

parser.add_argument("-a", "--absolute", action='store_true',
                         help="send moves relative to base")

parser.add_argument("instxoff", type = float, help="detector x offset")

parser.add_argument("instyoff", type=float, help="detector y offset")

args = parser.parse_args()

def mxy(n, abs, x, y):
    dcs = ktl.Service('dcs')
    instrument = dcs.read('INSTRUME')
    #TODO double check if math is right on CSU conversion
    if instrument == 'mosfire': #CSU conversion
        angle = 0.136 # offset between CSU and detector [deg]
        x = (x * math.cos(math.radians(angle))) + (y * math.sin(math.radians(angle)))
        y = (y * math.cos(math.radians(angle))) - (x * sin(math.radians(angle)))
    instxoff = dcs['instxoff']
    instyoff = dcs['instyoff']
    if n == True:
        print("[mxy] move command (NOT SENT) is: instxoff.write(%f) instyoff.write(%f)" % (x, y))
        return
    if abs == True:
        print('Sending moves rel2base')
        instxoff.write(x, rel2base = 't')
        instyoff.write(y, rel2base = 't')
    else:
        print('Sending moves rel2curr')
        instxoff.write(x, rel2curr = 't')
        instyoff.write(y, rel2curr = 't')
    elapsedTime = wftel()
    log = KeckLogger.getLogger()
    log.info("[mxy] offest %f, %f, abs = %s in detector coordinates" % (x, y, abs))
    print("[mxy] wftel completed in %f sec" % elapsedTime)
    return

if __name__ =='__main__':
    mxy(args.nomove, args.absolute, args.x, args.y)
