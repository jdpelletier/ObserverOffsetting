import ktl
import argparse
import wftel
import KeckLogger

parser = argparse.ArgumentParser(description="Move the telescope in the RA-DEC directions",
                         usage="en.py raoff decoff")

parser.add_argument("raoff", type = float, help="ra offset")

parser.add_argument("decoff", type=float, help="dec offset")


args = parser.parse_args()


def en(x, Y):
    if(x == 0.0 and yf == 0.0):
        print("WARNING: x and y moves are both zero -- exiting\n"")
        quit()
    dcs = ktl.Service('dcs')
    raoff = dcs['raoff']
    decoff = dcs['decoff']
    raoff.write(x, rel2curr = t)
    decoff.write(y, rel2curr = t)
    time.sleep(3)
    elapsedTime = wftel()
    log = KeckLogger.getLogger()
    log.info("[en] offset %f arcsec in RA, %f arcsec in DEC" % (x, y))
    print("[en] wftel completed in %f sec" % elapsedTime)
    return True

if name == __main__:
    en(args.raoff, args.decoff)
