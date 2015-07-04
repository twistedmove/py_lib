"""
Distance-related functions.

History
  create  -  Feng Zhou (zhfe99@gmail.com), 02-18-2015
  modify  -  Feng Zhou (zhfe99@gmail.com), 06-11-2015
"""
import numpy as np

def conDst(X1, X2, dst='e'):
    """
    Compute distance matrix.

    Remark
      Dij is the squared Euclidean distance between the i-th point in X1 and j-th point in X2.
      i.e., D[i, j] = || X1[i] - X2[j] ||_2^2

    Usage
      input  -  X1 = lib.rands((5, 3))
                X2 = lib.rands((6, 3))
      call   -  D = conDst(X1, X2)
                D.shape = (5, 6)

    Input
      X1     -  1st sample matrix, n1 x dim | dim x
      X2     -  2nd sample matrix, n2 x dim | dim x
      dst    -  distance type, {'e'} | 'b'
                  'e': Euclidean distance
                  'b': binary distance
    Output
      D      -  squared distance matrix, n1 x n2
    """
    # dimension
    n1, dim = X1.shape
    n2 = X2.shape[0]

    if dim == 1:
        X1 = np.concatenate((X1, np.zeros((n1, 1))), axis=1)
        X2 = np.concatenate((X2, np.zeros((n2, 1))), axis=1)

    XX1 = np.expand_dims((X1 * X1).sum(axis=1), axis=1)
    XX2 = np.expand_dims((X2 * X2).sum(axis=1), axis=0)

    # compute
    X12 = np.dot(X1, X2.T)
    D = np.tile(XX1, (1, n2)) + np.tile(XX2, (n1, 1)) - 2 * X12

    # Euclidean distance
    if dst == 'e':
        pass
    else:
        raise Exception('unknown distance: {}'.format(dst));

    return D

def conDstB(X1, X2):
    """
    Compute binary distance matrix.

    Remark
      Dij is the squared Euclidean distance between the i-th point in X1 and j-th point in X2.
      i.e., D[i, j] = || X1[i] - X2[j] ||_2^2

    Usage
      input  -  X1 = lib.rands((5, 3))
                X2 = lib.rands((6, 3))
      call   -  D = conDst(X1, X2)
                D.shape = (5, 6)

    Input
      X1     -  1st sample matrix, n1 x dim | dim x
      X2     -  2nd sample matrix, n2 x dim | dim x
      dst    -  distance type, {'e'} | 'b'
                  'e': Euclidean distance
                  'b': binary distance
    Output
      D      -  squared distance matrix, n1 x n2
    """
    # dimension
    n1, dim = X1.shape
    n2 = X2.shape[0]

    D = np.zeros((n1, n2))
    for i1 in range(n1):
        x1 = X1[i1]
        for i2 in range(n2):
            x2 = X2[i2]
            idx = np.nonzero(x1 == x2)
            if len(idx) > 0:
                D[i1, i2] = 1

    return D
