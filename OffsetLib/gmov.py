import ktl
import argparse

from gxy import gxy
from getScales import getScales
import KeckLogger

parser = argparse.ArgumentParser(description="Move the object to a given position on the guider",
                         usage="gmov.py [-n] x1 y1 x2 y2")

parser.add_argument("-n", "--nomove", action='store_true',
                         help="don't send moves")

parser.add_argument("x1", type=float, help="initial x pixel postion")

parser.add_argument("y1", type=float, help="initial y pixel postion")

parser.add_argument("x2", type=float, help="final x pixel postion")

parser.add_argument("y2", type=float, help="final y pixel postion")

args = parser.parse_args()

log = KeckLogger.getLogger()

dcs = ktl.Service('dcs')
instrument = dcs.read('INSTRUME')
gscale = getScales(instrument, 'gscale')

dx = gscale * (args.x1-args.x2)
dy = gscale * (args.y2-args.y1)

if argos.nomove:
    print("Required %f in x and %f in y" % (dx, dy))
else:
    print("Moving %f in x and %f in y" % (dx, dy))
    gxy(False, dx, dy)
    log.info('[gmov] executed')
