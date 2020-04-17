import logger

log = logging.getLogger('MyLogger')
log.setLevel(logging.INFO)
p = Popen('nightly', stdin=PIPE, stdout=PIPE, stderr=PIPE)
ouput, err = p.communicate()
nightpath = output.strip() + 'instrumentOffsets'
LogFileHandler = logging.FileHandler(nightpath)
LogConsoleHandler.setLevel(logging.INFO)
LogFormat = logging.Formatter('%(asctime)s:%(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
LogFileHandler.setFormatter(LogFormat)
log.addHandler(LogFileHandler)
