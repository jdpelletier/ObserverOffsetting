def gmov(self, n, x1, y1, x2, y2):
    #move an object to a given position on the KCWI guider
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
