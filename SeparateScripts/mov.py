import ktl
import argparse
import wftel
from mxy import mxy
import KeckLogger

parser = argparse.ArgumentParser(description="Move the object to a given position on the detector",
                         usage="mov.py [-n] x1 y1 x2 y2")

parser.add_argument("-n", "--nomove", action='store_true',
                         help="don't send moves")

parser.add_argument("x1", type=float, help="initial x pixel postion")

parser.add_argument("y1", type=float, help="initial y pixel postion")

parser.add_argument("x2", type=float, help="final x pixel postion")

parser.add_argument("y2", type=float, help="final y pixel postion")

args = parser.parse_args()

log = KeckLogger.getLogger()

dcs = ktl.Service('dcs')
instrument = dcs.read('INSTRUMENT')
instService = ktl.Service(instrument)
pscale = instService.read('pscale')
#NOTE pscale is not unified on instruments:
    #MOSFIRE: This keyword SHOULD work
    #KCWI: pscale is currently hardcoded

dx = pscale * (args.x1-args.x2)
dy = pscale * (args.y2-args.y1)

if argos.nomove:
    print("Required %f in x and %f in y" % (dx, dy))
else:
    print("Moving %f in x and %f in y" % (dx, dy))
    mxy(False, False, dx, dy)
    log.info('[mov] executed')
