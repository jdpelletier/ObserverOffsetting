import ktl
import argparse
import wftel
import KeckLogger

parser = argparse.ArgumentParser(description="Move the telescope detctor coordinates",
                         usage="mxy.py [-n] [-a] instxoff instyoff")

parser.add_argument("-n", "--nomove", action='store_true',
                         help="don't send moves")

parser.add_argument("-a", "--absolute", action='store_true',
                         help="send moves relative to base")

parser.add_argument("instxoff", type = float, help="detector x offset")

parser.add_argument("instyoff", type=float, help="detector y offset")

log = KeckLogger.getLogger()

def mxy(n, abs, x, y):
    dcs = ktl.Service('dcs')
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
        instxoff.write(x, rel2curr = 't')
        instyoff.write(y, rel2curr = 't')
    elapsedTime = wftel()
    log.info("[mxy] offest %f, %f, abs = %s in detector coordinates" % (x, y, abs))
    print("[mxy] wftel completed in %f sec" % elapsedTime)
    return

if name == __main__:
    mxy(args.nomove, args.absolute, args.x, args.y)
