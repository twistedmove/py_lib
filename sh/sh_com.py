"""
Common show functions.

History
  create  -  Feng Zhou (zhfe99@gmail.com), 03-19-2015
  modify  -  Feng Zhou (zhfe99@gmail.com), 07-04-2015
"""
import numpy as np
import matplotlib.pyplot as plt

def shIni(isOut=False):
    """
    Init figure setting.

    Input
      isOut  -  output mode, True | {False}
    """
    plt.close('all')
    plt.rcParams['figure.figsize'] = (10, 10)
    plt.rcParams['figure.facecolor'] = 'w'
    plt.rcParams['image.interpolation'] = 'nearest'
    plt.rcParams['image.cmap'] = 'gray'

    if isOut:
        plt.rcParams['text.usetex'] = True
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = 'Arial'
    else:
        plt.rcParams['text.usetex'] = False

    # import matplotlib as mpl
    # mpl.rcParams['toolbar'] = 'None'

def iniAx(fig, rows, cols, siz=None, wGap=.2, hGap=.2,
          pos=[0, 0, 1, 1], flat=True, sizMa=[20, 20], hs=None, ws=None, dpi=None):
    """
    Create axes.

    Input
      fig    -  figure id
      rows   -  #rows
      cols   -  #cols
      siz    -  figure size, {None} | 2 x |
                  siz == None: siz = [rows * 5, cols * 5]
      wGap   -  gap in width, {.2}
      hGap   -  gap in height, {.2}
      pos    -  position of the axes in the figure, {[0 0 1 1]}
      flat   -  flatten or not, {True} | False
      sizMa  -  maximum image size, {[8, 8]} | 2 x
      ws     -  size in width, {None} | 2 x
      hs     -  size in height, {None} | 2 x
      dpi    -  dpi, {None} | 200 | ...

    Output
      Ax     -  axes, rows cols x 1 (if flat == True) | rows x cols (if flat == False)
    """
    # default size
    if siz is None:
        siz = [rows * 5, cols * 5]

    # maximum size
    if sizMa is not None:
        from tool.py_lib.img import imgSizFit
        siz, _ = imgSizFit(siz, sizMa);

    # figure
    plt.close(fig)
    if dpi is None:
        plt.figure(num=fig, figsize=[siz[1], siz[0]])
    else:
        plt.figure(num=fig, figsize=[siz[1], siz[0]], dpi=dpi)

    # axes size
    wMar = pos[2] * wGap / (cols + 1)
    if ws is None:
        wBodys = np.zeros((cols + 1)) + pos[2] * (1 - wGap) / cols
    else:
        ws.insert(0, 0)
        wBodys = np.asarray(ws) / sum(ws) * (1 - wGap) / pos[2]
    wBodys[0] = 0
    wws = np.cumsum(wBodys)

    hMar = pos[3] * hGap / (rows + 1)
    if hs is None:
        hBodys = np.zeros((rows + 1)) + pos[3] * (1 - hGap) / rows
    else:
        hs.append(0)
        hBodys = 1.0 * np.asarray(hs) / sum(hs) * (1 - hGap) * pos[3];
    hBodys[-1] = 0
    hhs = np.cumsum(hBodys[-1 : 0 : -1])

    Ax = np.empty((rows, cols), dtype=object)
    for row in range(rows):
        for col in range(cols):
            rect = [wMar * (col + 1) + wws[col] + pos[0],
                    hMar * (rows - row) + hhs[rows - row - 1] + pos[1],
                    wBodys[col + 1], hBodys[row]]
            # print rect
            Ax[row, col] = plt.axes(rect)

    if flat:
        return Ax.flatten()
    else:
        return Ax

def setAx(ax):
    """
    Set current axes of current figure.

    Input
      ax  -  axes
    """
    if ax is not None:
        fig = plt.gcf()
        fig.sca(ax)

def show():
    """
    A wrapper of plt.show()
    """
    plt.show()

def setTick(xy, labs, ori='hor', siz=0):
    """
    Set x or y tick labels.

    Input
      xy    -  x or y, 'x' | 'y'
      labs  -  label names, k
      ori   -  orientation, {'hor'} | 'ver'
      siz   -  font size, {0} | 1 | ...
    """
    # dimension
    k = len(labs)
    ran = np.arange(1, k + 1)

    if xy == 'x':
        locs, labels = plt.xticks(ran, labs)
    elif xy == 'y':
        locs, labels = plt.yticks(ran, labs)
    else:
        raise Exception('unknown xy: {}'.format(xy))

    # text orientation
    if xy == 'x' and ori == 'ver':
        plt.setp(labels, rotation=90)

    # font size
    if siz > 0:
        plt.setp(labels, fontsize=siz)

def shBox(box, cl='r'):
    """
    Plot box.

    Input
      box  -  box, 2 x 2
      cl   -  color, {'r'} | 'b'
    """

    xHd = box[1, 0]
    xEd = box[1, 1] - 1
    yHd = box[0, 0]
    yEd = box[0, 1] - 1

    plt.plot([xHd, xEd, xEd, xHd, xHd], [yHd, yHd, yEd, yEd, yHd], '-', color=cl)

def genMkCl(c=-1):
    """
    Return with markers and colors.

    Input
      c    -  index, {-1} | 0 | 1 | ...

    Output
      mks  -  string | 1 x 12 (cell) (if c == -1)
      cls  -  string | 1 x 12 (cell) (if c == -1)
    """
    mks = ['o', 's', '^', 'd', '+', '*', 'x', 'p', 'v', 'o', 's', '^', 'd'];
    cls = [[ 1,  0,  0], # 'r'
           [ 0,  0,  1], # 'b'
           [ 0,  1,  0], # 'g'
           [ 1,  0,  1], # 'm'
           [ 0,  0,  0], # 'k'
           [ 0,  1,  1], # 'c'
           [.3, .3, .3],
           [.5, .5, .5],
           [.7, .7, .7],
           [.1, .1, .1],
           [ 1, .8,  0],
           [ 1, .4, .6]]

    if not c == -1:
        cc = c % len(cls)
        mks = mks[cc]
        cls = cls[cc]

    return mks, cls
