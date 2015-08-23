"""
String-related functions.

History
  create  -  Feng Zhou (zhfe99@gmail.com), 12-16-2014
  modify  -  Feng Zhou (zhfe99@gmail.com), 08-23-2015
"""
import re
from cell import zeros


def strLstPre(lst0, pre):
    """
    Return a sub-list of string that starts with the specified prefix.

    Input
      lst0  -  original string list, 1 x n0
      pre   -  prefix

    Output
      lst   -  new string list, 1 x n
    """
    lst = []
    for str0 in lst0:
        if str0[: len(pre)] == pre:
            lst.append(str0)

    return lst


def strLstPat(lst0, pats):
    """
    Return a sub-list of string that match with the specified pattern.

    Input
      lst0  -  original string list, 1 x n0
      pats  -  pattern list, m x

    Output
      lst   -  new string list, 1 x n
    """
    lst = []
    for str0 in lst0:
        for pat in pats:
            if re.match(pat, str0):
                lst.append(str0)
                break

    return lst


def strDelSub(name0):
    """
    Remove subfix from a file name.

    Input
      name0  -  original name

    Output
      name   -  new name
    """
    tail = name0.find('.')
    if tail == -1:
        name = name0
    else:
        name = name0[: tail]

    return name


def strGetSub(name):
    """
    Get subfix from a file name.

    Input
      name  -  file name

    Output
      subx  -  subfix
    """
    tail = name.find('.')
    if tail == -1:
        subx = ''
    else:
        subx = name[tail + 1:]

    return subx


def strRepSub(name0, subx):
    """
    Replace subfix to the given one.

    Input
      name0  -  original name
      subx   -  new subx

    Output
      name   -  new name
    """
    name = strDelSub(name0)

    return name + '.' + subx


def strNumCo(s):
    """
    Count the number character in a given string.

    Example
      in: s = 'a32b'
      call: co = strNumCo()
      out: co = 2

    Input
      s   -  string

    Output
      co  -  #number character
    """
    co = 0
    for c in s:
        if c >= '0' and c < '9':
            co += 1
    return co


def strLst2Float(arrS):
    """
    Convert a string list to a float list.

    Input
      arrS  -  string list, n x 1 (str)

    Output
      arrF  -  float list, n x 1 (float)
    """
    arrF = [float(s.strip()) for s in arrS]
    return arrF


def strLst1NotIn2(arr1, arr2):
    """
    Compare two string lists to find the strings in arr1 that
    are not contained in arr2.

    Input
      arr1  -  array 1, n1 x 1
      arr2  -  array 2, n2 x 1

    Output
      arrD  -  different elements in arr1, nD x 1
    """
    arrD = []
    m2 = len(arr2)
    vis = zeros(m2)
    for s1 in arr1:
        found = False
        for i2, s2 in enumerate(arr2):
            if vis[i2]:
                continue

            if s1 == s2:
                vis[i2] = 1
                found = True
                break
        if not found:
            arrD.append(s1)
    return arrD


def str2ran(s):
    """
    Convert a string range to an integer list.

    Example 1
      input: s = '1'
      call:  lst = str2range(s)
      output: lst = 1

    Example 2
      input: s = '2:10'
      call:  lst = str2range(s)
      output: lst = [2, 3, 4, 5, 6, 7, 8, 9]

    Input
      s    -  string

    Output
      lst  -  an integer list
    """
    parts = s.split(':')
    a = [int(part) for part in parts]

    if len(parts) == 1:
        lst = a
    elif len(parts) == 2:
        lst = range(a[0], a[1])
    else:
        raise Exception('unsupported')

    return lst
