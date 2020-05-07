import argparse

import ktl

parser = argparse.ArgumentParser(description="Return specified instrument pscale or gscale",
                         usage="getScales.py instrument scale")

parser.add_argument("instrument", help="instrument you want to check")

parser.add_argument("scale", choices = ['pscale', 'gscale'], help="pscale or gscale")

args = parser.parse_args()

def getScales(instrument, scale):
    scale_dict = {'mosfire': {'pscale': 0.1799, 'gscale': 0.164},
                  'lris': {'pscaler': 0.134, 'pscaleb': 0.135, 'gscale': 0.239},
                  'hires': {'pscale': 0.0, 'gscale': 0.1},
                  'osiris': {'pscale': 0.01, 'sscale': ktl.read('instrument', 'sscale'), 'gscale': 0.1338},
                  'kcwi': {'pscale': 0.0076, 'gscale': 0.184},
                  'nirc2': {'pscale': 0.009942, 'gscale': 0.1},
                  'nirspec': {'pscale': 0.1185, 'gscale': 0.207},
                  'esi': {'pscale': 0.153, 'gscale': 0.233},
                  'deimos': {'pscale': 0.1185, 'gscale': 0.207},
                  'nires': {'pscale': 0.123, 'gscale': 0.244}
                  }
    return scale_dict[instrument][scale]

if __name__=='__main__':
    getScales(args.instrument, args.scale)
