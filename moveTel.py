import sys

import ktl

from OffsetLib import *


##cache instrument
instrument = ktl.cache('dcs', 'INSTRUME')

###Welcome print

print('''
-----------------------------------------
------Telescope controller started!------
-----------------------------------------
\n\n
''')


##Get Pscale and Gscale function for Gmov and Dmov
##NOTE: this is not unified over all instruments yet,
##      works for MOSFIRE but not KCWI, trying to fix
##      that but may need to adjust this.
def getPscale(instrument):
    inst = ktl.read(instrument)
    return ktl.read(inst, 'pscale')

def getGscale(instrument):
    inst = ktl.read(instrument)
    return ktl.read(inst, 'gscale')
##


##Function to print instructions and get command from user.
def getCommand():
    response = input(
        '''
        Choose a command from the list below:
        1: Move in the AZ-EL direction
        2: Move in the RA-DEC direction
        3: Move in guider coordinates
        4: Move in detector coordinates
        5: Move object to position on guider
        6: Move object to position on detector
        7: Mark current position
        8: Go to previously marked position
        9: Mark base
        10: Quit (crtl-c) \n >
        '''
        )
    return input
##


##get arguments, based on response
def executeCommand(command):
    if command in range(1:4):
        return getXY(command)
    elif command in range(5:6):
        return getSpecMove(command)
    elif command in range(7-10):
        moveFrame(command)()
        return True
    else:
        return False
##


##If the command only needs x and y coords, run this function.
def getXY(command):
    coordString = input('Enter offset numbers as x y (no comma): ')
    coords = coordString.split()
    while len(coords) != 2 or ',' in coordString:
        startString = input('Error: Enter offset numbers as x y (no comma): ')
        coords = coordString.split()
    x = start[0]
    y = start[1]
    moveFrame(command)(x, y)
    return True
##


##Function for moving object to spot on guider or detector
#TODO add nomove
def getSpecMove(command):
    abs = False
    frame = 'guider'
    moveString = input(
        '''
        Do you want to:
        1: Send moves
        2: Check offset
        '''
        )
    
    if command == 6:
        frame = 'detector'
    startString = input('Enter the %s pixel coordinates of the object (no comma): ' % frame)
    start = startString.split()
    while len(start) != 2 or ',' in startString:
        startString = input('Error: Enter input as x y (no comma): ')
        start = startString.split()
    endString = input('Enter the destination guider pixel coordinates (no comma): ')
    end = endString.split()
    while len(end) != 2 or ',' in startString:
        endString = input('Error: Enter input as x y (no comma): ')
        end = endString.split()
    if command == 6:
        pscale = getPscale()
        dx = pscale * (start[0]-end[0])
        dy = pscale * (end[1]-start[1])
        absString = input(
            '''
            Send move reletive to:
            1: Current
            2: Base
            '''
            )
        if absString == '2':
            abs = True

    gscale = getGscale()
    dx = gscale * (start[0]-end[0])
    dy = gscale * (end[1]-start[1])
    print("Sending star at %s to %s..." % (startString, endString))
    moveFrame(3)(dx, dy)
    return True
##

##Function for moving object to spot on detector
#TODO add nomove and abs
def getDmov():
    startString = input('Enter the detector pixel coordinates of the object (no comma): ')
    start = startString.split()
    while len(start) != 2 or ',' in startString:
        startString = input('Error: Enter input as x y (no comma): ')
        start = startString.split()
    endString = input('Enter the destination detector pixel coordinates (no comma): ')
    end = endString.split()
    while len(end) != 2 or ',' in startString:
        endString = input('Error: Enter input as x y (no comma): ')
        end = endString.split()
    print("Sending star at %s to %s..." % (startString, endString))
    pscale = getPscale()
    dx = pscale * (start[0]-end[0])
    dy = pscale * (end[1]-start[1])
    moveFrame(4)(nomove, dx, dy)
    return true

##

##Quitting program
def endprogram():
    print('Ending Telescope Controller...')
    sys.exit()


#Command "switch case"
def moveFrame(i):
    switcher={
        1:azel.azel,
        2:en.en,
        3:gxy.gxy,
        4:mxy.mxy,
        5:mark.mark,
        6:gomark.gomark,
        7:markbase.markbase
        8:endprogram
        }
    return switcher.get(i,"Invalid choice")
##

def main():
    completion = False
    command = getCommand()
    completion = executeCommand(command)
    if completion == True:
        print('Action successfully completed!')
    else:
        print('Improper input, please try again.')


##Execute program until endprogram called or KeyboardInterrupt
if __name__=='__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
            endprogram
