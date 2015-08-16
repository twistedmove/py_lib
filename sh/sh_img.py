"""
Image-related utility functions.

History
  create  -  Feng Zhou (zhfe99@gmail.com), 03-19-2015
  modify  -  Feng Zhou (zhfe99@gmail.com), 08-16-2015
"""
import matplotlib.pyplot as plt

def shImg(img, isFilt=False, ax=None):
    """
    Show image.

    Input
      img     -  image, h x w x 3
      ax      -  axes to show, {None}
      isFilt  -  filt or not, {False}
    """
    if ax is not None:
        fig = plt.gcf()
        fig.sca(ax)

    if isFilt:
        img -= img.min()
        img /= img.max()
        img = img.transpose(1, 2, 0)

    if len(img.shape) == 2 or img.shape[2] > 1:
        plt.imshow(img)
    else:
        plt.imshow(img[:, :, 0])

    _ = plt.axis('off')

def shImgs(imgs, axs, labs=None):
    """
    Show multiple images.

    Input
      imgs  -  images, n x 1 (numpy array)
      axs   -  axes, n x 1 (numpy array)
    """

    for i, (img, ax) in enumerate(zip(imgs.flatten(), axs.flatten())):
        shImg(img, ax=ax)

        if labs is not None:
            plt.title(labs[i])

def shSv(fold, prex, type='pdf'):
    """
    Save image.

    Input
      fold  -  image fold
      prex  -  image prefix
      type  -  type, {'pdf'} | 'png' | 'jpg'
    """
    from lib.io import savePath
    imgPath = savePath(fold, prex)
    shSvPath(imgPath, type=type)

def shSvPath(imgPath, type='pdf', dpi=None):
    """
    Save image.

    Input
      imgPath  -  image path
      type     -  type, {'pdf'} | 'png' | 'jpg'
      dpi      -  dpi, {None} | ...
    """
    from py_lib.str import strDelSub
    imgNm = strDelSub(imgPath)

    if dpi is None:
        plt.savefig('{}.{}'.format(imgNm, type), format=type)
    else:
        plt.savefig('{}.{}'.format(imgNm, type), format=type, dpi=dpi)

def shBox(box):
    """
    Show box on image.

    Input
      box  -  bounding box, 2 x 2
                 box[0, 0]: top y
                 box[0, 1]: bottom y
                 box[1, 0]: left x
                 box[1, 1]: right x

    Output
      ha   -  box handle
    """
    # bounding box
    xHd = box[1, 0]
    xEd = box[1, 1]
    yHd = box[0, 0]
    yEd = box[0, 1]

    ha = plt.plot([xHd, xEd, xEd, xHd, xHd], [yHd, yHd, yEd, yEd, yHd], '-r')

    return ha
