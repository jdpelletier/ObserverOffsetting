import time
import math
import logger
from subprocess import Popen, PIPE

import ktl



##Logger setup
log = logging.getLogger('MyLogger')
log.setLevel(logging.INFO)
p = Popen('nightly', stdin=PIPE, stdout=PIPE, stderr=PIPE)
ouput, err = p.communicate()
nightpath = output.strip() + 'instrumentOffsets'
LogFileHandler = logging.FileHandler(nightpath)
LogFormat = logging.Formatter('%(asctime)s:%(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
LogFileHandler.setFormatter(LogFormat)
log.addHandler(LogFileHandler)
##End logger setup


class TelescopeControl:

    def __init__(self):
        self.dcs = ktl.Service('dcs')
        self.instrument = self.dcs.read('INSTRUME')
        self.instService = ktl.Service(self.instrument)
        self.autresum = self.dcs.monitor('autresum')

    def azel(self, x, y):
        #move the telescope x arcsec in azimuth and y arcsec in elevation
        azoff = self.dcs['azoff']
        eloff = self.dcs['eloff']
        azoff.write(x, rel2curr = t)
        eloff.write(y, rel2curr = t)
        time.sleep(3)
        elapsedTime = self.wftel(self.autresum)
        log.info("[azel] offset %f arcsec in AZ, %f arcsec in EL" % (x, y))
        print("[azel] wftel completed in %f sec" % elapsedTime)
        return

    def en(self, x, y):
        #	Move the telescope the given number of arcsec EAST & NORTH
        #       relative to its current position
        if(x == 0.0 and y == 0.0):
            print("WARNING: x and y moves are both zero -- exiting\n"")
            return
        raoff = self.dcs['raoff']
        decoff = self.dcs['decoff']
        raoff.write(x, rel2curr = t)
        decoff.write(y, rel2curr = t)
        elapsedTime = self.wftel(self.autresum)
        log.info("[en] offset %f arcsec in RA, %f arcsec in DEC" % (x, y))
        print("[en] wftel completed in %f sec" % elapsedTime)
        return

    def gmov(self, n, x1, y1, x2, y2):
        #move an object to a given position on the guider
        gscale = self.instService.read('gscale') #TODO figure out how to read this
        dx = gscale * (x1-x2)
        dy = gscale * (y2-y1)
        if n == True:
            print("Required %f in x and %f in y" % (dx, dy))
        else:
            print("Moving %f in x and %f in y" % (dx, dy))
            gxy(dx, dy)
            log.info('[gmov] executed')
        return

    def gomark(self):
        #restore telescope position to saved offsets
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
        self.dcs['raoff'].write(raoff, rel2base = 't')
        self.dcs['decoff'].write(decoff, rel2base = 't')
        elapsedTime = self.wftel(self.autresum)
        log.info("[gomark] offset %f in RA, %f in DEC" % (raoff, decoff))
        print("[gomark] wftel completed in %f sec" % elapsedTime)
        return

    def gxy(self, x, Y):
        #move the telescope in GUIDER coordinates
        tvxoff = self.dcs['tvxoff']
        tvyoff = self.dcs['tvyoff']
        tvxoff.write(x, rel2curr = 't')
        tvyoff.write(y, rel2curr = 't')
        elapsedTime = self.wftel(self.autresum)
        log.info("[gxy] offset %f, %f in guider coordinates" % (x, y))
        print("[gxy] wftel completed in %f sec" % elapsedTime)
        return

    def mark(self):
        #stores current ra and dec offsets
        raoff = self.dcs['raoff']
        decoff = self.dcs['decoff']
        raoff = raoff * 180 * 3600 / math.pi
        decoff = decoff * 180 * 3600 / math.pi
        dec = self.dcs.read('dec')
        raoff = raoff * math.cos(dec)
        instService['RAOFFSET'].write(raoff)
        instService['DECOFFSET'].write(decoff)
        log.info("[mark] stored offsets RA %f, DEC %f" % (x, y))
        return

    def markbase(self):
        #set the base telescope coordinates to the current coordinates
        self.dcs['mark'].write('true')
        log.info("[markbase] executed")
        return

    def mov(self, n, x1, y1, x2, y2):
        #move an object to a given position on the detector
        pscale = self.instService.read('pscale') #TODO figure out how to read this
        dx = pscale * (x1-x2)
        dy = pscale * (y2-y1)
        if n == True: #figure this out
            print("Required %f in x and %f in y" % (dx, dy))
        else:
            print("Moving %f in x and %f in y" % (dx, dy))
            self.mxy(dx, dy)
            log.info('[mov] executed')
        return

    def mxy(self, n, abs, x, y):
        #move telescope in instrument (detector) coordinates
        instxoff = self.dcs['instxoff']
        instyoff = self.dcs['instyoff']
        if n == True:
            print("[mxy] move command (NOT SENT) is: instxoff.write(%f) instyoff.write(%f)" % (x, y))
            return
        if abs == True:
            instxoff.write(x, rel2base = 't')
            instyoff.write(y, rel2base = 't')
        else:
            instxoff.write(x, rel2curr = 't')
            instyoff.write(y, rel2curr = 't')
        elapsedTime = self.wftel(self.autresum)
        log.info("[mxy] offest %f, %f, abs = %s in detector coordinates" % (x, y, abs))
        print("[mxy] wftel completed in %f sec" % elapsedTime)
        return

    def wftel(self, autresum):
        #wait for telescope move to complete
        startTime = time.time()
        axestat = self.dcs.monitor('AXESTAT')
        ktl.waitfor(axestat == "tracking")
        active = self.dcs.read("AUTACTIV")
        if (active == 'no'):
            print("WARNING: guider not currently active.\n")
            return
        count = 0
        while(True):
            if autresum != self.autresum:
                break
            count += 1
            if count >= 20:
                print("[wftel] WARNING: timeoutwaiting for AUTRESUM to increment\n\a")
                break
            time.sleep(1)
        count = 0
        while(true):
            autgo = self.dcs.read('autgo')
            if autgo.upper() == "RESUMEACK" or augo.upper() == "GUIDE":
                break
            count += 1
            if count >= 20:
                print("[wftel]WARNING: timeout waiting for AUTGO to be RESUMEACK or GUIDE\n\a")
                break
            time.sleep(1)
        elapsedTime = time.time() - startTime
        return elapsedTime
