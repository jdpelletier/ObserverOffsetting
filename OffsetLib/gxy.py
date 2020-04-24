import argparse

import ktl

from wftel import wftel
import KeckLogger

parser = argparse.ArgumentParser(description="Move the telescope guider coordinates",
                         usage="gxy.py [-n] tvxoff tvyoff")

parser.add_argument("-n", "--nomove", action='store_true',
                         help="don't send moves")

parser.add_argument("tvxoff", type = float, help="guider x offset")

parser.add_argument("tvyoff", type=float, help="guider y offset")

args = parser.parse_args()

def gxy(n, x, y):
    dcs = ktl.Service('dcs')
    tvxoff = self.dcs['tvxoff']
    tvyoff = self.dcs['tvyoff']
    if n == True:
        print("[gxy] move command (NOT SENT) is: tvxoff.write(%f) tvyoff.write(%f)" % (x, y))
        return
    tvxoff.write(x, rel2curr = 't')
    tvyoff.write(y, rel2curr = 't')
    elapsedTime = wftel()
    log = KeckLogger.getLogger()
    log.info("[gxy] offset %f, %f in guider coordinates" % (x, y))
    print("[gxy] wftel completed in %f sec" % elapsedTime)
    return True

if __name__ =='__main__':
    gxy(args.nomove, args.tvxoff, args.tvyoff)
