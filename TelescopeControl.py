import ktl
import time
import math


class TelescopeControl:

    def __init__(self):
        self.dcs = ktl.Service('dcs')
        self.instrument = self.dcs.read('INSTRUMENT')
        self.instService = ktl.Service(self.instrument)
        self.autresum = self.dcs.monitor('autresum')

    def azel(self, x, y):
        azoff = self.dcs['azoff']
        eloff = self.dcs['eloff']
        azoff.write(x, rel2curr = t)
        eloff.write(y, rel2curr = t)
        time.sleep(3)
        elapsedTime = self.wftel(self.autresum)
        print("[azel] wftel completed in %f sec" % elapsedTime)
        return

    def en(self, x, y):
        if(x == 0.0 and y == 0.0):
            print("WARNING: x and y moves are both zero -- exiting\n"")
            return
        raoff = self.dcs['raoff']
        decoff = self.dcs['decoff']
        raoff.write(x, rel2curr = t)
        decoff.write(y, rel2curr = t)
        elapsedTime = self.wftel(self.autresum)
        #TODO log move
        print("[en] wftel completed in %f sec" % elapsedTime)
        return

    def gmov(self, n, x1, y1, x2, y2):
        gscale = self.instService.read('gscale') #TODO figure out how to read this
        dx = gscale * (x1-x2)
        dy = gscale * (y2-y1)
        if n == True: #TODO figure this out
            print("Required %f in x and %f in y" % (dx, dy))
        else:
            print("Moving %f in x and %f in y" % (dx, dy))
            gxy(dx, dy)
        return

    def gomark(self):
        #TODO syncheck
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
        #TODO logging
        self.dcs['raoff'].write(raoff, rel2base = 't')
        self.dcs['decoff'].write(decoff, rel2base = 't')
        elapsedTime = self.wftel(self.autresum)
        print("[gomark] wftel completed in %f sec" % elapsedTime)
        return

    def gxy(self, x, Y):
        tvxoff = self.dcs['tvxoff']
        tvyoff = self.dcs['tvyff']
        tvxoff.write(x, rel2curr = 't')
        tvyoff.write(y, rel2curr = 't')
        elapsedTime = self.wftel(self.autresum)
        #TODO log move
        print("[gxy] wftel completed in %f sec" % elapsedTime)
        return

    def mark(self):
        #TODO syncheck
        raoff = self.dcs['raoff']
        decoff = self.dcs['decoff']
        raoff = raoff * 180 * 3600 / math.pi
        decoff = decoff * 180 * 3600 / math.pi
        dec = self.dcs.read('dec')
        raoff = raoff * math.cos(dec)
        instService['RAOFFSET'].write(raoff)
        instService['DECOFFSET'].write(decoff)
        return

    def markbase(self):
        return self.dcs['mark'].write('true')

    def mov(self, n, x1, y1, x2, y2):
        pscale = self.instService.read('pscale') #TODO figure out how to read this
        dx = pscale * (x1-x2)
        dy = pscale * (y2-y1)
        if n == True: #figure this out
            print("Required %f in x and %f in y" % (dx, dy))
        else:
            print("Moving %f in x and %f in y" % (dx, dy))
            self.gxy(dx, dy)
        return

    def mxy(self, n, abs, x, y):
        instxoff = self.dcs['tvxoff']
        instyoff = self.dcs['tvyff']
        if abs == True:
            instxoff.write(x, rel2base = 't')
            instyoff.write(y, rel2base = 't')
        else:
            instxoff.write(x, rel2curr = 't')
            instyoff.write(y, rel2curr = 't')
        elapsedTime = self.wftel(self.autresum)
        #TODO no move?
        #TODO log move
        print("[mxy] wftel completed in %f sec" % elapsedTime)
        return

    def wftel(self, autresum):
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
