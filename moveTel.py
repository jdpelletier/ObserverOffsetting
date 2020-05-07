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
from OffsetLib import getScales
from OffsetLib import gapCheck

if platform.system() == "Windows":
    os.system('cls')
else:
    os.system('clear')

##cache instrument
instrument = ktl.cache('dcs', 'INSTRUME')

##Welcome print

print('''
-----------------------------------------
------Telescope controller started!------
-----------------------------------------
''')


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


##Get arguments and execute requested command:
# Each of the functions in OffsetLib returns
# true. completion flag in main() checks that
# to see if the move was executed. Will add
# more error handling when we can start testing
# moves.
def executeCommand(command, instrument):
    if command in range(1, 5):
        return moveFrame(command)(*getXY(command))
    elif command in range(5, 7):
        argTuple = getSpecMove(command, instrument)
        command = command - 2
        return moveFrame(command)(*argTuple)
    elif command in range(7 ,11):
        command = command - 2
        return moveFrame(command)()
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
    return argTuple
##


##Function for moving object to spot on guider or detector
def getSpecMove(command, instrument):
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
        gscale = getScales.getScales(instrument, 'gscale')
        dx = gscale * (int(start[0])-int(end[0]))
        dy = gscale * (int(end[1])-int(start[1]))
        command = 3
        argTuple = (nomove, dx, dy)
    else:
        scalestring = 'pscale'
        if instrument == 'lris':
            response = input('Red or blue side? > ')
            while scalestring = 'pscale':
                if response in ['red', 'Red', 'RED', 'r']:
                    scalestring = 'pscaler'
                elif response in ['blue', 'Blue', 'BLUE']:
                    scalestring = 'pscaleb'
                else:
                    response = input('Respond with red or blue > ')
            start[0], start[1], end[0], end[1] = gapCheck.gapCheck(start[0], start[1], end[0], end[1])
        elif instrument == 'osiris':
            response = input('osimg or ospec? > ')
            if response in ['OSPEC', 'ospec', 'Ospec']:
                scalestring = 'sscale'
        pscale = getScales.getScales(instrument, scalestring)
        #TODO this is probably differnt for each detector, need to update
        dx = pscale * (int(start[0])-int(end[0])
        dy = pscale * (int(end[1])-int(start[1]))
        command = 4
        argTuple = (nomove, False, dx, dy)
    return argTuple
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

def main(instrument):
    '''
    Script works by first setting completion flag to "False", then
    asking the user for the move they'd like to execute. After getting
    the command, get the arguments then executes the move.  If everything
    works, the move should return "True" which sets the completetion
    flag to "True". Script runs until KeyboardInterrupt or user shutdown.
    '''
    completion = False
    command = getCommand()
    completion = executeCommand(command, instrument.read())
    if completion == True:
        print('Action successfully completed!')
    else:
        print('Improper input, please try again.')


##Execute program until endprogram called or KeyboardInterrupt
if __name__=='__main__':
    try:
        while True:
            '''
            NOTE this looks ugly, but easy way to make sure user isn't
            entering in letters.
            '''
            try:
                main(instrument)
            except ValueError:
                print("\nWARNING: only enter numbers.\n")
                continue
    except KeyboardInterrupt:
            endprogram()
