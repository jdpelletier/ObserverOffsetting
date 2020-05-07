import argparse

import ktl

from mxy import mxy
from getScales import getScales
from gapCheck import gapCheck
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

x1, y1, x2, y2 = args.x1, args.y1, args.x2, args.y2

instrument = dcs.read('INSTRUME')
scalestring = 'pscale'

if instrument == 'lris':
    response = input('Red or blue side? (Where are you starting if both)> ')
    while scalestring = 'pscale':
        if response in ['red', 'Red', 'RED', 'r']:
            scalestring = 'pscaler'
        elif response in ['blue', 'Blue', 'BLUE']:
            scalestring = 'pscaleb'
        else:
            response = input('Respond with red or blue > ')
    x1, y1, x2, y2 = gapCheck(x1, y1, x2, y2, scalestring)

elif instrument == 'osiris':
    response = input('osimg or ospec? > ')
    if response in ['OSPEC', 'ospec', 'Ospec']:
        scalestring = 'sscale'

pscale = getScales(instrument, scalestring)


dx = pscale * (x1-x2)
dy = pscale * (y2-y1)

if argos.nomove:
    print("Required %f in x and %f in y" % (dx, dy))
else:
    print("Moving %f in x and %f in y" % (dx, dy))
    mxy(False, False, dx, dy)
    log.info('[mov] executed')
