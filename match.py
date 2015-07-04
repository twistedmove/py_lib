"""
Match-related utility functions.

History
  create  -  Feng Zhou (zhfe99@gmail.com), 03-19-2015
  modify  -  Feng Zhou (zhfe99@gmail.com), 03-19-2015
"""
import os
import re
import shutil

# subx
subxs0 = ['m', 'h', 'cpp']

def isEndSub(filename, subxs):
    """
    Checking whether filename ends with any in the specified subfix list.

    Input
      filename  -  file name
      subxs     -  subfix list, 1 x m (list)

    Output
      res       -  result, True | False
    """
    for subx in subxs:
        pat = ".*\." + subx + "$"

        if re.match(pat, filename):
            return True

    return False

def listFiles(dirNm, isRec, subxs):
    """
    Return the list of all files that have the specified subfix in a folder.

    Input
      dirNm    -  dir fold, string
      isRec    -  flag of being recursive, True | False
      subxs    -  subfix list, 1 x m (list)

    Output
      relDirs  -  directory list
      fileNms  -  file names
    """
    relDirs = []
    fileNms = []

    # recursively
    if isRec:
        for root, dirs, files in os.walk(dirNm):
            for file in files:
                # skip non-matched file
                if not isEndSub(file, subxs):
                    continue

                # relative fold
                relDir = root[len(dirNm):]
                if relDir and relDir[0] == '/':
                    relDir = relDir[1:]

                # store
                relDirs.append(relDir)
                fileNms.append(file)

    # not recursively
    else:
        for file in os.listdir(dirNm):
            # file absolute path
            filePath = os.path.join(dirNm, file)

            # skip fold on non-matched file
            if os.path.isdir(filePath) or not isEndSub(file, subxs):
                continue

            # store
            relDirs.append('')
            fileNms.append(file)

    return (relDirs, fileNms)

def checkFoldMatch(srcDir, dstDir, logFile1, logFile2, isRec, subxs):
# check subfold match

    # open file
    fio1 = open(logFile1, 'w')
    fio2 = open(logFile2, 'w')

    # file list
    relDirs, fileNms = listFiles(dstDir, isRec, subxs)

    # each file
    for i in range(len(relDirs)):
        relDir = relDirs[i]
        fileNm = fileNms[i]

        # pdb.set_trace()

        # file path
        srcFile = os.path.join(srcDir, relDir, fileNm)
        dstFile = os.path.join(dstDir, relDir, fileNm)

        # matched
        if os.path.isfile(srcFile):
            fio1.write(srcFile + "\n")
            fio1.write(dstFile + "\n")

        # not matched
        else:
            fio2.write(dstFile + "\n");

    # close file
    fio1.close()
    fio2.close()

def updateFile(logFile):
    """
    Update file.

    Input
      logFile  -  log file
    """

    # open file
    fio = open(logFile, 'r')
    lines = fio.read().splitlines()
    fio.close()

    for i1 in range(0, len(lines), 2):
        line1 = lines[i1]
        line2 = lines[i1 + 1]

        # copy
        print line1
        print line2
        shutil.copy(line1, line2)
