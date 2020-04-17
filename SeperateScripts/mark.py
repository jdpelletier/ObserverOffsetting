def mark(self):
    #stores current ra and dec offsets
    #TODO syncheck
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
