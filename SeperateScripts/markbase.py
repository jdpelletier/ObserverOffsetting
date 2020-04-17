    def markbase(self):
        #set the base telescope coordinates to the current coordinates
        log.info("[markbase] executed")
        return self.dcs['mark'].write('true')
