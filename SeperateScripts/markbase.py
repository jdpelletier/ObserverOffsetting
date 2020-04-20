import ktl
import KeckLogger

parser = argparse.ArgumentParser(description="Set the base telescope coordinates to the current coordinates",
                         usage="markbase.py")


def markbase():
    dcs = ktl.Service('dcs')
    self.dcs['mark'].write('true')
    log = KeckLogger.getLogger()
    log.info("[mark] stored offsets RA %f, DEC %f" % (x, y))
    return True

if name == __main__:
    markbase()
