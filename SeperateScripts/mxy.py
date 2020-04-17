def mxy(self, n, abs, x, y):
    #move telescope in instrument (detector) coordinates
    instxoff = self.dcs['tvxoff']
    instyoff = self.dcs['tvyff']
    if abs == True:
        instxoff.write(x, rel2base = 't')
        instyoff.write(y, rel2base = 't')
    else:
        instxoff.write(x, rel2curr = 't')
        instyoff.write(y, rel2curr = 't')
    elapsedTime = self.wftel(self.autresum)
    if n == True:
        print("[mxy] move command (NOT SENT) is: instoffx.write(%f) instyoff.write(%f)" % (x, y))
        return
    log.info("[mxy] offest %f, %f, abs = %s in detector coordinates" % (x, y, abs))
    print("[mxy] wftel completed in %f sec" % elapsedTime)
    return
