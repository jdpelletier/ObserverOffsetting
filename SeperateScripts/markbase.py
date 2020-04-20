import ktl

def markbase():
    #set the base telescope coordinates to the current coordinates
    dcs = ktl.Service('dcs')
    self.dcs['mark'].write('true')
    #TODO logging
    return True

if name == __main__:
    markbase()
