"""
IO utility functions.

History
  create  -  Feng Zhou (zhfe99@gmail.com), 03-19-2015
  modify  -  Feng Zhou (zhfe99@gmail.com), 08-09-2015
"""
import os
import csv

def loadLns(inpath):
    """
    Read a file and return its content as list of lines.

    Input
      inpath  -  input path, string

    Output
      lines   -  lines, 1 x n (list)
    """
    fio = open(inpath, 'r')
    lines = fio.read().splitlines()
    fio.close()

    return lines

def saveLns(lines, outpath, subx=None):
    """
    Write a list of line into a file.

    Input
      lines    -  lines, 1 x n (list)
      outpath  -  output path, string
      subx     -  subfix of each line, {None} | '\n' | ...
    """
    fio = open(outpath, 'w')
    for line in lines:
        try:
            fio.write(line)
        except UnicodeEncodeError:
            fio.write(line.encode('utf8'))

        if subx is not None:
            fio.write(subx)
    fio.close()

def mkDir(dirPath, mkL=0):
    """
    Make a fold if not existed.

    Input
      dirPath  -  directory path
      mkL      -  operation level if fold already exists, {0} | 1
                    0: do nothing
                    1: del the fold
    """
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    else:
        if mkL == 1:
            import shutil
            shutil.rmtree(dirPath, ignore_errors=True)
            os.makedirs(dirPath)

def cpFile(pathSrc, pathDst):
    """
    Copy file.

    Input
      pathSrc  -  src path
      pathDst  -  dst path
    """
    import shutil
    shutil.copyfile(pathSrc, pathDst)

def rmFile(path):
    """
    Delete file if exist.

    Input
      path  -  src path
    """
    if os.path.exists(path):
        os.remove(path)

def save(filepath, data, svL=1):
    """
    Save data as a pickle format.

    Input
      filepath  -  file name
      data      -  data
      svL       -  save level
    """
    import cPickle

    if svL == 0 or filepath is None:
        return

    with open(filepath, "w") as fo:
        cPickle.dump(data, fo, protocol=cPickle.HIGHEST_PROTOCOL)

def load(filename):
    """
    Load data from a pickle-format file.

    Input
      filename  -  filename

    Output
      data      -  data
    """
    import cPickle

    fo = open(filename, 'r')
    data = cPickle.load(fo)
    fo.close()
    return data

def loadH5(filename, varNm, dtype=None):
    """
    Load data from a hdf5 file.

    Input
      filename  -  filename
      varNm     -  variable name
      dtype     -  type, {None} | np.double | ...

    Output
      data      -  data
    """
    import h5py
    import numpy as np

    file = h5py.File(filename, 'r')
    data0 = file[varNm]
    if dtype is None:
        data = np.asarray(data0)
    else:
        data = np.asarray(data0, dtype=dtype)
    file.close()
    return data

def saveH5(filename, data, varNm):
    """
    Save data in hdf5 file.

    Input
      filename  -  filename
      data      -  data
      varNm     -  variable name
    """
    import h5py
    file = h5py.File(filename, "w")
    file.create_dataset(varNm, data=data)
    file.close()

def savePath(fold, prex, subx=None, type=None):
    """
    Get the save path.

    Input
      fold  -  fold
      prex  -  path prefix
      subx  -  subfix, {None}
      type  -  type, None

    Output
      path  -  file path
    """
    saveFold = os.path.expanduser('~/work/save')
    saveFold = os.path.join(saveFold, fold)

    # create fold if necessary
    mkDir(saveFold)

    # subfix
    if subx is not None:
        prex = prex + '_' + subx

    if type == None:
        path = os.path.join(saveFold, prex)
    elif type == 'txt':
        path = os.path.join(saveFold, prex + '.txt')
    else:
        raise Exception('unknown type: {}'.format(type))
    return path

def exist(nm, type='file'):
    """
    Check whether the name eixst.

    Input
      nm    -  name
      type  -  type, {'file'}

    Output
      res   -  status, 'True' | 'False'
    """

    if nm is None:
        return False

    if type == 'file':
        return os.path.isfile(nm)

    else:
        raise Exception('unknown type: {}'.format(type))

def listFold(fold):
    """
    Return the list of all folders under a folder.

    Input
      fold       -  root fold

    Output
      foldNms    -  directory name list, 1 x n (list)
      foldPaths  -  directory path list, 1 x n (list)
    """
    foldNms = []
    foldPaths = []

    for foldNm in os.listdir(fold):
        # fold absolute path
        foldPath = os.path.join(fold, foldNm)

        # skip non fold
        if not os.path.isdir(foldPath):
            continue

        # store
        foldNms.append(foldNm)
        foldPaths.append(foldPath)

    return foldNms, foldPaths

def listFoldR(fold):
    """
    Return the list of all folders recursively under a folder.

    Input
      fold       -  root fold

    Output
      foldNms    -  directory name list, 1 x n (list)
      foldPaths  -  directory path list, 1 x n (list)
    """
    foldNms = []
    foldPaths = []

    # each sub file
    for dirname, dirNms, fileNms in os.walk(fold):
        for dirNm in dirNms:
            # file and cmd path
            foldPath = os.path.join(dirname, dirNm)

            # store
            foldNms.append(dirNm)
            foldPaths.append(foldPath)

    return foldNms, foldPaths

def listFile(fold, subx=None):
    """
    Return the list of all files matched with the subfix under a folder.

    Input
      fold       -  root fold
      subx       -  subfix, {None} | 'txt' | ...

    Output
      fileNms    -  directory name list, n x
      filePaths  -  directory path list, n x
    """
    fileNms = []
    filePaths = []

    for foldNm in os.listdir(fold):
        # fold absolute path
        filePath = os.path.join(fold, foldNm)

        # skip non fold
        if os.path.isdir(filePath):
            continue

        # skip filepath
        if subx is not None and not filePath.endswith(subx):
            continue

        # store
        fileNms.append(foldNm)
        filePaths.append(filePath)

    return fileNms, filePaths

def listFileR(fold, subx=None):
    """
    Return the list of all files matched with the subfix recursively under a folder.

    Input
      fold      -  root fold
      subx      -  subfix, {None} | 'txt' | ...

    Output
      fileNms    -  directory name list, n x
      filePaths  -  directory path list, n x
    """
    fileNms = []
    filePaths = []

    # each sub file
    for dirname, dirnames, fileNms in os.walk(fold):
        for fileNm in fileNms:
            # skip filepath
            if subx is not None and not fileNm.endswith(subx):
                continue

            # file and cmd path
            filePath = os.path.join(dirname, fileNm)

            # store
            fileNms.append(dirname)
            filePaths.append(filePath)

    return fileNms, filePaths

def getch():
    """
    Get one char from input.

    Output
      c  -  character
    """
    import termios
    import sys, tty

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        c = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return c

def loadCsv(csvPath, nLnSkip=0, delimiter=',', quotechar=None):
    """
    Load from csv.

    Input
      csvPath    -  csv path
      nLnSkip    -  #line to skip in the header, {0} | ...
      delimiter  -  delimiter, {','} | ...
      quotechar  -  quotechar, {None} | ...

    Output
      dcts       -  symbol list, n x
      keys       -  key list, nKey x
    """
    dcts = []
    with open(csvPath, 'rb') as csvfile:
        csvHa = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        for i, row in enumerate(csvHa):
            # skip line
            if i < nLnSkip:
                continue

            # field name
            if i == nLnSkip:
                keys = row
                nKey = len(row)
                continue

            # symbol
            assert(len(row) == nKey)
            dct = {}
            for iKey, key in enumerate(keys):
                dct[key] = row[iKey]
            dcts.append(dct)
    return dcts, keys

def lmdbRIn(lmdbPath):
    """
    Get the lmdb handle of a given sequence.

    Input
      lmdbPath  -  path of the lmdb file

    Output
      ha        -  handles
    """
    import lmdb

    # path file
    env = lmdb.open(lmdbPath)
    txn = env.begin()
    cur = txn.cursor()

    # store
    ha = {'env': env,
          'cur': cur,
          'co': 0,
          'lmdb': lmdbPath}
    return ha

def lmdbR(ha):
    """
    Read one item from lmdb handle.

    Input
      ha   -  handles

    Output
      key  -  key
      val  -  value
    """
    # move cursor
    if ha['co'] == 0:
        ha['cur'].first()
    else:
        if not ha['cur'].next():
            return None, None, None
    ha['co'] += 1

    # get key & value
    key = ha['cur'].key()
    val = ha['cur'].value()

    return key, val

def lmdbROut(ha):
    """
    Close the handler.

    Input
      ha  -  handle
    """
    ha['env'].close()
