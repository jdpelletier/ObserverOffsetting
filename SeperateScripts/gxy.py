def gxy(self, x, Y):
    #move the telescope in GUIDER coordinates
    tvxoff = self.dcs['tvxoff']
    tvyoff = self.dcs['tvyff']
    tvxoff.write(x, rel2curr = 't')
    tvyoff.write(y, rel2curr = 't')
    elapsedTime = self.wftel(self.autresum)
    log.info("[gxy] offset %f, %f in guider coordinates" % (x, y))
    print("[gxy] wftel completed in %f sec" % elapsedTime)
    return
