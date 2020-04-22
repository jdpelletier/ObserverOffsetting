import time
import argparse

import ktl

import KeckLogger

parser = argparse.ArgumentParser(description="Wait for the telescope move to complete, stores time it took to complete",
                         usage="wftel.py")

args = parser.parse_args()

def wftel():
    dcs = ktl.Service('dcs')
    autresum = dcs.read('autresum')
    startTime = time.time()
    axestat = dcs.monitor('AXESTAT')
    ktl.waitfor(axestat == "tracking")
    active = dcs.read("AUTACTIV")
    if (active == 'no'):
        print("WARNING: guider not currently active.\n")
        return
    count = 0
    while(True):
        if autresum != dcs.read('autresum'):
            break
        count += 1
        if count >= 20:
            print("[wftel] WARNING: timeoutwaiting for AUTRESUM to increment\n\a")
            break
        time.sleep(1)
    count = 0
    while(true):
        autgo = dcs.read('autgo')
        if autgo.upper() == "RESUMEACK" or augo.upper() == "GUIDE":
            break
        count += 1
        if count >= 20:
            print("[wftel]WARNING: timeout waiting for AUTGO to be RESUMEACK or GUIDE\n\a")
            break
        time.sleep(1)
    elapsedTime = time.time() - startTime
    return elapsedTime

if __name__ =='__main__':
    print("wftel completed in %f sec" % wftel())
