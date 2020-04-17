import ktl
import argparse
import wftel

parser = argparse.ArgumentParser(description="Move the telescope in the az-el directions",
                         usage="azel.py az el")

parser.add_argument("az", type = float, help="az offset")

parser.add_argument("el", type=float, help="el offset")


args = parser.parse_args()

dcs = ktl.Service('dcs')
az = dcs['az']
el = dcs['el']
azoff.write(args.az, rel2curr = t)
eloff.write(ars.el, rel2curr = t)
time.sleep(3)
elapsedTime = wftel()
#TODO add logging
print("[azel] wftel completed in %f sec" % elapsedTime)
