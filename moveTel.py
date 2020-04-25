import sys
import os
import platform

import ktl

from OffsetLib import azel
from OffsetLib import en
from OffsetLib import gxy
from OffsetLib import mxy
from OffsetLib import mark
from OffsetLib import gomark
from OffsetLib import markbase

if platform.system() == "Windows":
    os.system('cls')
else:
    os.system('clear')


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
    print(
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
        10: Quit (crtl-c) \n
        '''
        )
    response = input('>>> ')
    return int(response)
##


##get arguments, based on response
def executeCommand(command):
    if command in range(1, 5):
        return getXY(command)
    elif command in range(5, 7):
        return getSpecMove(command)
    elif command in range(7 ,11):
        command = command - 2
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
        coordString = input('Error: Enter offset numbers as x y (no comma): ')
        coords = coordString.split()
    x = int(coords[0])
    y = int(coords[1])
    if command == 3:
        argTuple = (False, x, y)
    elif command == 4:
        abs = False
        print(
            '''
            Move relative to:
            1: Current position
            2: Base
            '''
            )
        absString = int(input('>>> '))
        while absString not in [1, 2]:
            absString = input("Error: Enter 1 (current) or 2 (base): ")
        if absString == 2:
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
    print(
        '''
        Do you want to:
        1: Send moves
        2: Check offset
        '''
        )
    moveString = int(input('>>> '))
    while moveString not in [1, 2]:
        moveString = input("Error: Enter 1 (send move) or 2 (no move): ")
    if moveString == 2:
        nomove = True
    if command == 5:
        gscale = getGscale()
        dx = gscale * (int(start[0])-int(end[0]))
        dy = gscale * (int(end[1])-int(start[1]))
        command = 3
        argTuple = (nomove, dx, dy)
    else:
        pscale = getPscale()
        dx = pscale * (int(start[0])-int(end[0])
        dy = pscale * (int(end[1])-int(start[1]))
        command = 4
        argTuple = (nomove, False, dx, dy)
    moveFrame(command)(*argTuple)
    return True
##

##Quitting program
def endprogram():
    print('\nEnding Telescope Controller...\n')
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
        7:markbase.markbase,
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
            endprogram()
