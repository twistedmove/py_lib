"""
Dictionary-related functions.

History
  create  -  Feng Zhou (zhfe99@gmail.com), 12-16-2014
  modify  -  Feng Zhou (zhfe99@gmail.com), 06-21-2015
"""

def dctSub(dct0, keys):
    """
    Return a sub-dictionary for the selected keys.

    Input
      dct0  -  original dictionary
      keys  -  key list, 1 x m

    Output
      dct   -  new dictionary
    """
    return dict((key, dct0[key]) for key in keys)

def dctItem(dct, idx):
    """
    Return a list of items for the corresponding index.

    Input
      dct   -  original dictionary
      idx   -  index, m x

    Output
      keys  -  keys, m x
      vals  -  values, m x
    """
    keys = []
    vals = []
    items = dct.items()
    for i in idx:
        key, val = items[i]
        keys.append(key)
        vals.append(val)
    return keys, vals

def lns2dct(lns, sep=':'):
    """
    Generate dictionary from lines.

    Input
      lns  -  line, n x
      sep  -  seperator, {':'} | ...

    Output
      dct  -  dictionary
    """
    dct = {}
    for ln in lns:
        parts = ln.split(sep)
        assert(len(parts) == 2)
        dct[parts[0]] = parts[1]

    return dct
