def wftel():
    #wait for telescope move to complete
    autresum = ktl.read('dcs', 'autresum')
    startTime = time.time()
    axestat = self.dcs.monitor('AXESTAT')
    ktl.waitfor(axestat == "tracking")
    active = self.dcs.read("AUTACTIV")
    if (active == 'no'):
        print("WARNING: guider not currently active.\n")
        return
    count = 0
    while(True):
        if autresum != ktl.read('dcs', 'autresum'):
            break
        count += 1
        if count >= 20:
            print("[wftel] WARNING: timeoutwaiting for AUTRESUM to increment\n\a")
            break
        time.sleep(1)
    count = 0
    while(true):
        autgo = self.dcs.read('autgo')
        if autgo.upper() == "RESUMEACK" or augo.upper() == "GUIDE":
            break
        count += 1
        if count >= 20:
            print("[wftel]WARNING: timeout waiting for AUTGO to be RESUMEACK or GUIDE\n\a")
            break
        time.sleep(1)
    elapsedTime = time.time() - startTime
    return elapsedTime
