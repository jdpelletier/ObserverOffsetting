from OffsetLib import *

##print options

##get response

##get arguments, based on response

##execute funtion from dictionary

##continue while loop until exiting

def moveFrame(i):
    switcher={
        1:azel.azel,
        2:en.en,
        3:gxy.gxy,
    return switcher.get(i,"Invalid choice")

moveframe(i)(arguments)
