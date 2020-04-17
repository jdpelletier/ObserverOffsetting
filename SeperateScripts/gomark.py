def gomark(self):
    #restore telescope position to saved offsets
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
    self.dcs['raoff'].write(raoff, rel2base = 't')
    self.dcs['decoff'].write(decoff, rel2base = 't')
    elapsedTime = self.wftel(self.autresum)
    log.info("[gomark] offset %f in RA, %f in DEC" % (raoff, decoff))
    print("[gomark] wftel completed in %f sec" % elapsedTime)
    return
