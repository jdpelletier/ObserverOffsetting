import ktl
import wftel
import argparse
import KeckLogger

parser = argparse.ArgumentParser(description="Restore telescope position to saved offsets",
                         usage="gomark.py")

log = KeckLogger.getLogger()

def gomark():
    dcs = ktl.Service('dcs')
    instrument = dcs.read('INSTRUMENT')
    instService = ktl.Service(instrument)
    raoff = instService['raoffset']
    decoff = instService['decoffset']
    pattern = instService['pattern']
    if pattern == "Stare":
        print("NOTE: Dither mode is set to Stare, so skipping \n")
        print("       move to base in gomark script -- exiting\n")
        return
    if raoff == 0 and decoff == 0:
        print("[gomark] NOTE: RA and DEC moves are both zero -- exiting\n")
        return
    dcs['raoff'].write(raoff, rel2base = 't')
    dcs['decoff'].write(decoff, rel2base = 't')
    elapsedTime = wftel()
    log.info("[gomark] offset %f in RA, %f in DEC" % (raoff, decoff))
    print("[gomark] wftel completed in %f sec" % elapsedTime)
    return True

if name == __main__:
    gomark()
