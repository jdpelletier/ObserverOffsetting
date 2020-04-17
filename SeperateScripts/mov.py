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
