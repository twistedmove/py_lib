"""
Cell-related functions.

History
  create  -  Feng Zhou (zhfe99@gmail.com), 02-16-2015
  modify  -  Feng Zhou (zhfe99@gmail.com), 06-06-2015
"""
import numpy as np

def cells(shape, n=1):
    """
    Create a cell matrix.

    Input
      shape  -  shape tuple
      n      -  #output, {1} | 2 | ...

    Output
      A      -  cell matrix, 1 x n (tuple)
    """
    if n == 0:
        return

    res = tuple(np.empty(shape, dtype=np.object) for i in range(n))

    if n == 1:
        return res[0]

    else:
        return res

def zeros(shape, n=1):
    """
    Create zero numpy matrices.

    Input
      shape  -  shape tuple
      n      -  #output, {1} | 2 | ...

    Output
      A      -  zero matrix
    """
    if n == 0:
        return

    # res = tuple(np.zeros(shape, dtype=np.object) for i in range(n))
    res = tuple(np.zeros(shape) for i in range(n))

    if n == 1:
        return res[0]

    else:
        return res

def rands(shape, n=1):
    """
    Create random numpy matrices.

    Input
      shape  -  shape tuple
      n      -  #output, {1} | 2 | ...

    Output
      A      -  rand matrix
    """
    if n == 0:
        return

    res = tuple(np.random.rand(*shape) for i in range(n))

    if n == 1:
        return res[0]
    else:
        return res

def ods(n=1):
    """
    Create a set of OrderedDict.

    Input
      n      -  #output, {1} | 2 | ...

    Output
      o      -  OrderedDict
    """
    if n == 0:
        return

    import collections as col
    res = tuple(col.OrderedDict() for i in range(n))

    if n == 1:
        return res[0]
    else:
        return res
