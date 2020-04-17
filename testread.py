import ktl
import argparse

parser = argparse.ArgumentParser(description="Move the telescope in the az-el directions",
                         usage="azel.py az el")

parser.add_argument("az", type = float,
                    help="az offset")

parser.add_argument("el", type=float,
                    help="el offset")


args = parser.parse_args()
print("az offset = %f, al offset = %f" % (args.az, args.el))
dcs = ktl.Service('dcs')
az = dcs['az']
el = dcs['el']
print(az.read())
print(el.read())
