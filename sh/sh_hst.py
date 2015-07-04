"""
Histogram-related utility functions.

History
  create  -  Feng Zhou (zhfe99@gmail.com), 03-19-2015
  modify  -  Feng Zhou (zhfe99@gmail.com), 04-17-2015
"""
import numpy as np
import matplotlib.pyplot as plt
from lib.cell import cells
from sh_com import genMkCl

def shHst(mes, devs=[], ax=None, xs=[], barWid=0.8, devWid=0.8, bdWid=0, ori='ver', clG=None):
    """
    Plot histogram.

    Input
      mes       -  histogram, 1 x n
      devs      -  deviation, {[]} | 1 x n
      ax        -  axis, {None}
      xs        -  x position, {[]} | n x
      barWid    -  width of histogram bar, {.8} <= 1
      devWid    -  width of deviation line in terms of the 'barWid', {1} <= 1
      bdWid     -  width of boundary of bar, {1}
      ori       -  orientation, {'ver'} | 'hor'
      clG       -  global color, {'None'} | 'red' | ...
        lnWid   -  width of deviation line, {2}
        dev     -  dev flag, {'y'} | 'n'
        val     -  value flag, 'y' | {'n'}
        form    -  value form, {'%d'}
        yLim    -  threshold in y axis, {[]}
        leg     -  legend, {[]}

    Output
      haBars
    """
    if ax is not None:
        fig = plt.gcf()
        fig.sca(ax)

    # mk & cl
    mks, cls = genMkCl()

    # dimension
    n = len(mes)

    # label position
    if len(xs) == 0:
        xs = np.arange(1, n + 1)
    gap = xs[1] - xs[0] if n > 1 else .5

    # width
    barWid2 = 1.0 * barWid / 2 * gap
    devWid2 = 1.0 * devWid / 2 * gap

    # import pdb; pdb.set_trace()
    # plot mean
    haBars = cells(n)
    for i in range(n):
        x = xs[i]
        y = mes[i]
        xL = x - barWid2
        xR = x + barWid2

        if y == 0:
            continue

        # color
        if clG is None:
            cl = cls[i % len(cls)]
        else:
            cl = clG

        # draw
        if bdWid == 0:
            if ori == 'ver':
                ha = plt.fill([xL, xR, xR, xL], [0, 0, y, y], color=cl, edgecolor=cl)
            else:
                ha = plt.fill([0, 0, y, y], [xL, xR, xR, xL], color=cl, edgecolor=cl)
        else:
            if ori == 'ver':
                ha = plt.fill([xL, xR, xR, xL], [0, 0, y, y], color=cl, LineWidth=bdWid)
            else:
                ha = plt.fill([0, 0, y, y], [xL, xR, xR, xL], color=cl, LineWidth=bdWid)
        haBars[i] = ha

    # plot dev
    if len(devs) > 0:
        ys = mes + devs

        for i in range(n):
            x = xs(i)
            y = mes(i)
            dev = devs(i)
            xL = x - devWid2
            xR = x + devWid2

            if y == 0:
                continue

            # color
            cl = cls[i % len(cls)]
            cl = 'k'
            lnWid = 1

            # vertical line
            plt.plot([x, x], [-dev, dev] + y, 'Color', cl, 'LineWidth', lnWid)

            # horizontal line
            plt.plot([xL, xR], [dev, dev] + y, 'Color', cl, 'LineWidth', lnWid)
            plt.plot([xL, xR], [-dev, -dev] + y, 'Color', cl, 'LineWidth', lnWid)

    return haBars
    # maximum value
    # may = max(ys)

def shHstG(Me, Dev=[], ax=None, xs=[], barWid=0.8, barWidG=.8, devWid=0.8, bdWid=0, ori='ver', clG=None):
    """
    Plot histogram groups.

    Input
      Me        -  histogram, k x n
                     k: #bin in each group
                     n: #group
      Dev       -  deviation, {[]} | 1 x n
      ax        -  axis, {None}
      xs        -  x position, {[]} | n x
      barWid    -  width of histogram bar, {.8} <= 1
      devWid    -  width of deviation line in terms of the 'barWid', {1} <= 1
      bdWid     -  width of boundary of bar, {1}
      ori       -  orientation, {'ver'} | 'hor'
      clG       -  global color, {'None'} | 'red' | ...
        lnWid   -  width of deviation line, {2}
        dev     -  dev flag, {'y'} | 'n'
        val     -  value flag, 'y' | {'n'}
        form    -  value form, {'%d'}
        yLim    -  threshold in y axis, {[]}
        leg     -  legend, {[]}

    Output
      haBars
    """
    # axis
    if ax is not None:
        fig = plt.gcf()
        fig.sca(ax)

    # mk & cl
    mks, cls = genMkCl()

    # dimension
    k, n = Me.shape

    # label position
    if len(xs) == 0:
        xs = np.arange(1, n + 1)
    gap = xs[1] - xs[0] if n > 1 else .5

    # width
    barWidG2 = barWidG / 2
    barWid = barWid * (barWidG / k)
    gapWid = (barWidG - barWid * k) / (k - 1)
    devWid2 = barWid * devWid / 2

    # plot mean
    HaBar = cells((k, n))
    for i in range(n):
        x = xs[i] - barWidG2
        for c in range(k):
            xL = x + (gapWid + barWid) * c
            xR = xL + barWid
            y = Me[c, i]

            # color
            if clG is None:
                cl = cls[c % len(cls)]
            else:
                cl = clG

            # draw
            if bdWid == 0:
                if ori == 'ver':
                    ha = plt.fill([xL, xR, xR, xL], [0, 0, y, y], color=cl, edgecolor=cl)
                else:
                    ha = plt.fill([0, 0, y, y], [xL, xR, xR, xL], color=cl, edgecolor=cl)
            else:
                if ori == 'ver':
                    ha = plt.fill([xL, xR, xR, xL], [0, 0, y, y], color=cl, LineWidth=bdWid)
                else:
                    ha = plt.fill([0, 0, y, y], [xL, xR, xR, xL], color=cl, LineWidth=bdWid)
            HaBar[c, i] = ha

    # plot dev
    if Dev is not None:
        ys = mes + devs

        for i in range(n):
            x = xs(i)
            y = mes(i)
            dev = devs(i)
            xL = x - devWid2
            xR = x + devWid2

            if y == 0:
                continue

            # color
            cl = cls[i % len(cls)]
            cl = 'k'
            lnWid = 1

            # vertical line
            plt.plot([x, x], [-dev, dev] + y, 'Color', cl, 'LineWidth', lnWid)

            # horizontal line
            plt.plot([xL, xR], [dev, dev] + y, 'Color', cl, 'LineWidth', lnWid)
            plt.plot([xL, xR], [-dev, -dev] + y, 'Color', cl, 'LineWidth', lnWid)

    return HaBar
    # maximum value
    # may = max(ys)

def shCur(Me, Dev, ax=None, xs=[], labs=None, mkSiz=5, edWid=1):
    """
    Plot curve group.

    Input
      Me        -  mean matrix, k x n
                      k : #curves (algorithms)
                      n : #points (bins) per curve
      Dev       -  standard variation matrix, k x n
      ax        -  axis, {None}
      xs        -  x position, {[]} | n x
        parMk    -  marker parameter, {[]}
        barWidG  -  width of group of histgram bar, {.8} <= 1
        barWid   -  width of histgram bar in terms of 'barWidG / k', {.8} <= 1
        devWid   -  width of deviation line in terms of the 'barWid', {1} <= 1
        bdWid    -  width of boundary of bar, {1}
        dev      -  dev flag, {'y'} | 'n'
        yLim     -  threshold in y axis, {[]}
        algs     -  algorithm names as legends, {[]} | 1 x nAlg (cell)

    Output
      ha         -  handle
    """
    if ax is not None:
        fig = plt.gcf()
        fig.sca(ax)

    # mk & cl
    mks, cls = genMkCl()

    # devWid = ps(varargin, 'devWid', .1);
    # bdWid = ps(varargin, 'bdWid', 1);
    # parMk = ps(varargin, 'parMk', []);
    # isDev = psY(varargin, 'dev', 'y');
    # yLim = ps(varargin, 'yLim', []);
    # algs = ps(varargin, 'algs', []);
    # xs = ps(varargin, 'xs', []);

    # dimension
    k, n = Me.shape

    # devWid = devWid * 1;

    # x position
    if len(xs) == 0:
        xs = np.arange(1, n + 1)

    # range
    may = Me.max()
    miy = Me.min()
    # import pdb; pdb.set_trace()

    # plot mean
    haLns = []
    for c in range(k):
        cl = cls[c % len(cls)]
        if labs is None:
            ha, = plt.plot(xs, Me[c], '-' + mks[c], color=cl, markersize=mkSiz, markeredgewidth=edWid)
        else:
            ha, = plt.plot(xs, Me[c], '-' + mks[c], label=labs[c], color=cl, markersize=mkSiz, markeredgewidth=edWid)
        haLns.append(ha)
    return haLns
