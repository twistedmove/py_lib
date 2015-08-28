"""
Print-related utility functions.

History
  create  -  Feng Zhou (zhfe99@gmail.com), 03-19-2015
  modify  -  Feng Zhou (zhfe99@gmail.com), 2015-08
"""
import os
import sys
import logging
from util import tic, toc

# global variable
logFile = None
lPr = None
lMaPr = None
nmPrs = None
ticPrs = None
ticPr0s = None
nRepPrs = None
scaPrs = None

def prSet(lMa, logPath=None):
    """
    Set the promption level.

    Input
      lMa      -  maximum level, 0 | 1 | 2 | ...
      logPath  -  log file path, {None} | ...
    """
    global lPr, lMaPr, nmPrs, ticPrs, ticPr0s, nRepPrs, scaPrs, logFile

    # level
    lPr = 0
    lMaPr = lMa

    # list
    nMa = 10
    nmPrs = range(nMa)
    ticPrs = range(nMa)
    ticPr0s = range(nMa)
    nRepPrs = range(nMa)
    scaPrs = range(nMa)

    # log
    if logPath is not None:
        logFile = logPath
        logSet(logPath, haNew=True)

def pr(form, *args):
    """
    Prompt the information specified in the parameters.

    Input
      form   -  format
      *args  -  object list
    """
    # variables
    global lPr, lMaPr

    if lPr < lMaPr:
        for l in range(lPr + 1):
            sys.stdout.write('-')
        if len(args) == 0:
            print form
            if logFile is not None:
                logging.info(form)
        else:
            print form % args
            if logFile is not None:
                logging.info(form % args)

def prIn(nm, form="", *args):
    """
    Start a propmter for displaying information.

    Input
      nm        -  name
      form      -  format
      varargin  -  object list
    """
    # variables set in "prSet()"
    global lPr

    # init
    if not 'lPr' in globals():
        prSet(3)

    # print
    if form == "":
        pr('%s', nm)
    else:
        pr('%s: ' + form, nm, *args)

    # self add
    lPr = lPr + 1

def prOut():
    """
    Stop a propmter for function.
    """
    # variables set in "prSet.m"
    global lPr

    # delete
    lPr = lPr - 1

def prInOut(nm, form="", *args):
    """
    Prompt the information specified in the parameters.

    Input
      form   -  format
      *args  -  object list
    """
    prIn(nm, form=form, *args)
    prOut()

def prCIn(nm, nRep, sca):
    """
    Start a propmter for displaying information about loop.

    Input
      nm    -  name
      nRep  -  #steps
      sca   -  scale of moving, (0, 1) | 1 | 2 | ...
    """
    # variables set in "prSet()"
    global lPr, nmPrs, ticPrs, ticPr0s, nRepPrs, scaPrs

    # insert
    nmPrs[lPr] = nm
    ticPrs[lPr] = tic()
    ticPr0s[lPr] = ticPrs[lPr]
    nRepPrs[lPr] = nRep

    # scaling
    if sca < 1:
        sca = round(nRep * sca)
    if sca == 0:
        sca = 1
    scaPrs[lPr] = sca

    # print
    pr('%s: %d %d' %(nm, nRep, sca))

    lPr = lPr + 1

def prCOut(nRep):
    """
    Stop a propmter for counting.

    Input
      nRep  -  #steps
    """
    # variables defined in "prSet.m"
    global lPr, nmPrs, ticPrs, ticPr0s, nRepPrs, scaPrs

    lPr = lPr - 1

    # time
    t = toc(ticPr0s[lPr])

    # print
    pr('%s: %d iters, %.2f secs' %(nmPrs[lPr], nRep, t))

def prC(iRep):
    """
    Prompt information of a counter.

    Input
      iRep  -  current step
    """
    # variables defined in "prSet()"
    global lPr, nmPrs, ticPrs, nRepPrs, scaPrs

    lPr = lPr - 1
    if (iRep != 0 and iRep % scaPrs[lPr] == 0) or (iRep == nRepPrs[lPr]):
        # time
        t = toc(ticPrs[lPr])

        # print
        pr('%s: %d/%d, %.2f secs' %(nmPrs[lPr], iRep, nRepPrs[lPr], t))

        # re-start a timer
        ticPrs[lPr] = tic()

    lPr = lPr + 1

def logSet(logPath, level='info', reNew=True, recDate=True, recLevel=True, haNew=False):
    """
    Set up logger.

    Input
      logPath   -  log path
      level     -  level, {'info'} |
      reNew     -  flag of creating a new log, {True} | False
      recDate   -  flag of recording time, {True} | False
      recLevel  -  flag of recording time, {True} | False
      haNew     -  flag of creating all new handler, True | {False}
    """
    import io

    # create the log folder if necessary
    logFold = os.path.dirname(logPath)
    io.mkDir(logFold)

    # delete old log
    if reNew:
        io.rmFile(logPath)

    # remove onld handler
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # level
    if level == 'info':
        level = logging.INFO
    else:
        raise Exception('unknown level: {}'.format(level))

    # format
    format = '%(message)s'
    if recLevel:
        format = '%(levelname)s; ' + format
    if recDate:
        format = '%(asctime)s; ' + format

    # set
    logging.basicConfig(level=level, filename=logPath,
                        format=format,
                        datefmt="%Y-%m-%d %H:%M:%S")

def log(form, level='info', *args):
    """
    Output to log file.

    Input
      form   -  format
      level  -  level, {'info'} |
      *args  -  object list
    """
    if level == 'info':
        if len(args) == 0:
            logging.info(form)
        else:
            logging.info(form % args)

    elif level == 'error':
        if len(args) == 0:
            logging.error(form)
        else:
            logging.error(form % args)

    else:
        raise Exception('unknown level: {}'.format(level))
