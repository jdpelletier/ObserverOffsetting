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
