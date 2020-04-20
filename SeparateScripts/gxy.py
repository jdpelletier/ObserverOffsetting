import ktl
import argparse
import wftel
import KeckLogger

parser = argparse.ArgumentParser(description="Move the telescope guider coordinates",
                         usage="gxy.py tvxoff tvyoff")

parser.add_argument("tvxoff", type = float, help="guider x offset")

parser.add_argument("tvyoff", type=float, help="guider y offset")

args = parser.parse_args()

def gxy(x, Y):
    dcs = ktl.Service('dcs')
    tvxoff = self.dcs['tvxoff']
    tvyoff = self.dcs['tvyoff']
    tvxoff.write(x, rel2curr = 't')
    tvyoff.write(y, rel2curr = 't')
    elapsedTime = wftel()
    log = KeckLogger.getLogger()
    log.info("[gxy] offset %f, %f in guider coordinates" % (x, y))
    print("[gxy] wftel completed in %f sec" % elapsedTime)
    return True

if name == __main__:
    gxy(args.tvxoff, args.tvyoff)
