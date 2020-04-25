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
    abs = False
    coordString = input('Enter offset numbers as x y (no comma): ')
    coords = coordString.split()
    while len(coords) != 2 or ',' in coordString:
        startString = input('Error: Enter offset numbers as x y (no comma): ')
        coords = coordString.split()
    x = start[0]
    y = start[1]
    if command == 3:
        argTuple = (False, x, y)
    elif command == 4:
        absString = input(
            '''
            Move relative to:
            1: Current position
            2: Base
            '''
            )
        while absString != '1' or '2'
            absString = input("Error: Enter 1 (current) or 2 (base): ")
        if absString = '2':
            abs = True
        argTuple = (False, abs, x, y)
    else:
        argTuple = (x, y)
    moveFrame(command)(*argTuple)
    return True
##


##Function for moving object to spot on guider or detector
def getSpecMove(command):
    frame = 'guider'
    nomove = False
    if command == 6:
        frame = 'detector'
    startString = input('Enter the %s pixel coordinates of the object (no comma): ' % frame)
    start = startString.split()
    while len(start) != 2 or ',' in startString:
        startString = input('Error: Enter input as x y (no comma): ')
        start = startString.split()
    endString = input('Enter the destination guider pixel coordinates (no comma): ')
    end = endString.split()
    while len(end) != 2 or ',' in endString:
        endString = input('Error: Enter input as x y (no comma): ')
        end = endString.split()
    moveString = input(
        '''
        Do you want to:
        1: Send moves
        2: Check offset
        '''
        )
    while moveString != '1' or '2'
        moveString = input("Error: Enter 1 (send move) or 2 (no move): ")
    if moveString == '2':
        nomove = True
    if command == 5:
        gscale = getGscale()
        dx = gscale * (start[0]-end[0])
        dy = gscale * (end[1]-start[1])
        argTuple = (nomove, dx, dy)
    else:
        pscale = getPscale()
        dx = pscale * (start[0]-end[0])
        dy = pscale * (end[1]-start[1])
        argTuple = (nomove, False, dx, dy)
    moveFrame(command)(*argTuple)
    return True
##

##Quitting program
def endprogram():
    print('Ending Telescope Controller...')
    sys.exit()
##

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
