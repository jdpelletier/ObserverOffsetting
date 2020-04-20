import ktl
import argparse
import wftel
import KeckLogger

parser = argparse.ArgumentParser(description="Move the telescope in the az-el directions",
                         usage="azel.py azoff eloff")

parser.add_argument("azoff", type = float, help="az offset")

parser.add_argument("eloff", type=float, help="el offset")


args = parser.parse_args()


def azel(x, Y):
    dcs = ktl.Service('dcs')
    azoff = dcs['azoff']
    eloff = dcs['eloff']
    azoff.write(x, rel2curr = t)
    eloff.write(y, rel2curr = t)
    time.sleep(3)
    elapsedTime = wftel()
    log = KeckLogger.getLogger()
    log.info("[azel] offset %f arcsec in AZ, %f arcsec in EL" % (x, y))
    print("[azel] wftel completed in %f sec" % elapsedTime)
    return True

if name == __main__:
    azel(args.azoff, args.eloff)
