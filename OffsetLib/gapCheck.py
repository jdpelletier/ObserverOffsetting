import argparse

parser = argparse.ArgumentParser(description="Check move over LRIS chip gap",
                         usage="gapCheck.py x1 y1 x2 y2 detector")

parser.add_argument("x1", type=float, help="initial x pixel postion")

parser.add_argument("y1", type=float, help="initial y pixel postion")

parser.add_argument("x2", type=float, help="final x pixel postion")

parser.add_argument("y2", type=float, help="final y pixel postion")

parser.add_argument("detector", choices=['red', 'blue'], help='red/blue')

args = parser.parse_args()

if args.detector == 'red':
    scalestring = 'pscaler'
else:
    scalestring = 'pscaleb'


#TODO Check all of this function
def gapCheck(x1, y1, x2, y2, scalestring):
    if scalestring == 'pscaler':
        # The calculation below is used to determine how to shift across the gap.
        # The linear relationship below is completely unknown and needs to
        # be updated following commissioning. Currently, we should not trust
        # moves across the gap.
        if x1 > 2048:
            x1 = x1 + 250.0
        if x2 > 2048:
            x2 = x2 + 250.0
    else:
        # The calculation below is used to determine how to shift across the gap.
        if x1 > 2048:
            x1 = x1 + 96.627 + 0.00162*x2
            y1 = y1 + 2.982
        if x2 > 2048:
            x2 = x2 + 96.627 + 0.00162*y2
            y2 = y2 + 2.982
    return x1, x2, y1, y2

if __name__ == '__main__':
    gapCheck(args.x1, args.x2, args.y1, args.y2, scalestring)
