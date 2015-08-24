"""
Image utility functions.

History
  create  -  Feng Zhou (zhfe99@gmail.com), 03-19-2015
  modify  -  Feng Zhou (zhfe99@gmail.com), 08-24-2015
"""
from pri import pr
from cell import cells
import skimage.io
import PIL
import numpy as np

def imgCrop(img0, box, isOkOut=False):
    """
    Crop an image patch within a bounding box.

    Input
      img0     -  image, h0 x w0 x 3
      box      -  bounding box, 2 x 2
                    box[0, 0]: top y
                    box[0, 1]: bottom y
                    box[1, 0]: left x
                    box[1, 1]: right x
      isOkOut  -  flag of whether out boundary is OK, True | {False}

    Output
      img      -  cropped image, h x w x 3
    """
    # original image dimension
    h0 = img0.shape[0]
    w0 = img0.shape[1]

    # bounding box
    xHd = box[1, 0]
    xEd = box[1, 1]
    yHd = box[0, 0]
    yEd = box[0, 1]

    # out of images
    if isOkOut:
        xHd = max(0, xHd)
        xEd = min(w0, xEd)
        yHd = max(0, yHd)
        yEd = min(h0, yEd)
    else:
        if xHd < 0 or xHd >= w0 or yHd < 0 or yEd >= h0:
            return None

    img = img0[yHd : yEd, xHd : xEd, :]
    return img

def imgIplCrop(imgPath0, imgPath, target_h=120, target_w=90):
    img = PIL.Image.open(imgPath0)
    [w, h] = (img.size[0], img.size[1])
    xmin = 0
    ymin = 0
    xmax = w
    ymax = h
    if w / target_w > h / target_h:
        new_w = 90 * h / 120
        xmin = (w - new_w) / 2
        xmax = xmin + new_w
    else:
        new_h = 120 * w / 90
        ymin = (h - new_h) / 2
        ymax = ymin + new_h
    size = target_w, target_h
    bbox = (xmin, ymin, xmax, ymax)
    img = img.crop(bbox)
    img.thumbnail(size, PIL.Image.ANTIALIAS)
    img.convert('RGB').save(imgPath, "JPEG")

def imgCropSca(img0, h=120, w=90):
    """
    Crop an image patch within a bounding box.

    Input
      img0  -  image, h0 x w0 x 3
      h     -  height, {120} | ...
      w     -  width, {90} | ...

    Output
      img   -  cropped image, h x w x 3
    """
    # dimension
    h0, w0, nChan = img0.shape

    # get the bounding box
    if 1.0 * w0 / h0 > 1.0 * w / h:
        # crop w
        h1 = h0
        w1 = int(1.0 * w * h1 / h)
        xMi = (w0 - w1) / 2
        xMa = xMi + w1 - 1
        yMi = 0
        yMa = h0 - 1
    else:
        # crop h
        w1 = w0
        h1 = int(1.0 * h * w1 / w)
        yMi = (h0 - h1) / 2
        yMa = yMi + h1 - 1
        xMi = 0
        xMa = w0 - 1

    # crop
    box = [[yMi, yMa], [xMi, xMa]]
    img = imgCrop(img0, np.array(box), isOkOut=True)

    # scale
    img = imgSizNew(img, [h, w])

    return img

def imgMeans(Img):
    """
    Compute the mean image.

    Input
      Img   -  a list of images, n x m, h x w x 3

    Output
      imgs  -  mean image, m (cell), h x w x 3
    """
    # dimension
    n, m = Img.shape

    imgs = cells(n)
    for i in range(n):
        imgs[i] = imgMean(Img[i])

    return imgs

def imgMean(imgs):
    """
    Compute the mean image.

    Input
      imgs  -  a list of images, n x, h x w x 3

    Output
      img   -  mean image, h x w x 3
    """
    # dimension
    n = len(imgs)

    # check the image size
    Siz = np.zeros((n, 3), dtype=np.uint8)
    for i in range(n):
        Siz[i] = np.array(imgs[i].shape, dtype=np.uint8)
    siz = Siz.max(axis=0)

    img = np.zeros(tuple(siz))
    for imgi in imgs:
        sizi = imgi.shape
        # pad
        imgi = np.lib.pad(imgi, ((0, siz[0] - sizi[0]), (0, siz[1] - sizi[1]), (0, siz[2] - sizi[2])), 'constant')

        # resize
        img += imgi

    # average
    img /= n
    return img

def imgSizNew(img0, siz, order=1):
    """
    Resize an image.

    Input
      img0   -  original image, h0 x w0 x nChan
      siz    -  size, h x w
      order  -  interpolation order, {1} | ...

    Output
      img    -  new image, h x w x nChan
    """
    siz0 = img0.shape
    if siz0[-1] == 1 or siz0[-1] == 3:
        from skimage.transform import resize

        # skimage is fast but only understands {1,3} channel images in [0, 1].
        im_min, im_max = img0.min(), img0.max()
        im_std = (img0 - im_min) / (im_max - im_min)
        resized_std = resize(im_std, siz, order=order)
        resized_im = resized_std * (im_max - im_min) + im_min

    else:
        from scipy.ndimage import zoom

        # ndimage interpolates anything but more slowly.
        scale = tuple(np.array(siz) / np.array(img0.shape[:2]))
        resized_im = zoom(img0, scale + (1,), order=order)

    return resized_im.astype(np.float32)

def imgSizEqW(siz0, w):
    """
    Adjust the image size to fit with the width.

    Input
      siz0   -  original size, 2 x | 3 x
      w      -  width

    Output
      siz    -  new size, 2 x | 3 x
    """
    # original size
    h0 = siz0[0]
    w0 = siz0[1]

    # adjust height
    sca = 1.0 * h0 / w0
    w = w
    h = int(round(sca * w))

    # store
    if len(siz0) == 2:
        siz = [h, w]
    elif len(siz0) == 3:
        siz = [h, w, siz0[2]]
    else:
        raise Exception('unsupported dim: {}'.format(siz0.shape))

    return siz

def imgSizFit(siz0, sizMa):
    """
    Adjust the image size to fit with the maximum size constraint but keeping the ratio.

    Input
      siz0   -  original size, 2 x | 3 x
      sizMa  -  maximum size, 2 x

    Output
      siz    -  new size, 2 x | 3 x
      rat    -  ratio
    """
    # original size
    h0 = siz0[0]
    w0 = siz0[1]

    # maximum size
    hMa = sizMa[0]
    wMa = sizMa[1]

    # error
    if hMa == 0 and wMa == 0:
        siz = siz0
        rat = 1
        return siz, rat

    # fit already
    if h0 <= hMa and w0 <= wMa:
        siz = siz0
        rat = 1
        return siz, rat

    # adjust height
    if h0 > hMa:
        sca = 1.0 * w0 / h0
        h0 = hMa
        w0 = int(round(sca * h0))

    # adjust width
    if w0 > wMa:
        sca = 1.0 * h0 / w0
        w0 = wMa
        h0 = int(round(sca * w0))

    # ratio
    rat = np.mean(1.0 * np.array([h0, w0]) / np.array(siz0[:2]))

    # store
    if len(siz0) == 2:
        siz = [h0, w0]
    elif len(siz0) == 3:
        siz = [h0, w0, siz0[2]]
    else:
        raise Exception('unsupported dim: {}'.format(siz0.shape))

    return siz, rat

def imgSv(imgPath, img):
    """
    Save an image to the path.

    Input
      imgPath  -  image path
      img      -  an image with type np.float32 in range [0, 1], H x W x nChan
    """
    skimage.io.imsave(imgPath, img)

def imgLoad(imgPath, color=True):
    """
    Load an image converting from grayscale or alpha as needed.

    Input
      imgPath  -  image path
      color    -  flag for color format. True (default) loads as RGB while False
                  loads as intensity (if image is already grayscale).

    Output
      image    -  an image with type np.float32 in range [0, 1]
                    of size (H x W x 3) in RGB or
                    of size (H x W x 1) in grayscale.
    """
    # load
    try:
        img0 = skimage.io.imread(imgPath)
        import pdb; pdb.set_trace()

        img = skimage.img_as_float(img0).astype(np.float32)

    except:
        pr('unable to open img: {}'.format(imgPath))
        return None

    # color channel
    if img.ndim == 2:
        img = img[:, :, np.newaxis]
        if color:
            img = np.tile(img, (1, 1, 3))

    elif img.shape[2] == 4:
        img = img[:, :, :3]

    return img

def imgLoadTxt(txtPaths):
    """
    Load image from txt file.

    Input
      txtPaths  -  txt path, 3 x

    Output
      img       -  image, h x w x 3
    """
    # dimension
    d = len(txtPaths)

    # load matrix
    As = []
    for i in range(d):
        A = np.loadtxt(txtPaths[i])
        if i == 0:
            h = A.shape[0]
            w = A.shape[1]
        else:
            assert(A.shape[0] == h and A.shape[1] == w)
        As.append(A)

    # merge
    img = np.zeros((h, w, d))
    for i in range(d):
        img[:, :, i] = As[i]
    img = img / 255

    # import pdb; pdb.set_trace()

    return img

def imgSaveTxt(img, txtPaths, fmt='%.2f'):
    """
    Save image to txt files.

    Input
      img       -  image, 3 x h x w
      txtPaths  -  txt path, 3 x
      fmt       -  format
    """
    # dimension
    d = len(txtPaths)

    # load matrix
    for i in range(d):
        np.savetxt(txtPaths[i], img[i], fmt)

def imgLoadPil(imgPath):
    """
    Load an image using PIL.

    Input
      imgPath  -  image path

    Output
      image    -  image in PIL format
    """
    # load
    from PIL import Image
    img = Image.open(imgPath)
    return img

def imgLoadCv(imgPath):
    """
    Load an image using OpenCV.

    Input
      imgPath  -  image path

    Output
      image    -  image, h x w x nChan
    """
    # load
    import cv2
    img = cv2.imread(imgPath)
    return img

def imgPil2Ski(im):
    """
    Convert image from PIL format to an Skimage one.

    Input
      img0   -  original PIL image

    Output
      image  -  new Ski image
    """
    img0 = np.array(im.getdata())
    if img0.shape[1] == 4:
        pix = img0[:, 0 : 3].reshape(im.size[1], im.size[0], 3) / 255.0
    elif img0.shape[1] == 3:
        pix = img0.reshape(im.size[1], im.size[0], 3) / 255.0
    im = skimage.img_as_float(pix).astype(np.float32)

    return im

def imgPil2Cv(img0):
    """
    Convert image from PIL format to an Skimage one.

    Input
      img0  -  original PIL image

    Output
      img   -  new OpenCV image
    """
    data = np.array(img0.getdata())
    img = data.reshape(img0.size[1], img0.size[0], 3)
    return img[:, :, [2, 1, 0]].astype(np.uint8)

def imgPil2Ipl(img0):
    """
    Convert image from PIL format to an OpenCV IPL one.

    Input
      img0     -  original PIL image

    Output
      image    -  image in PIL format
    """
    import cv2

    if not isinstance(img0, PIL.Image.Image):
        raise TypeError, 'must be called with PIL.Image.Image!'

    # dimension
    size = (img0.size[0], img0.size[1])

    # mode dictionary:
    # (pil_mode : (ipl_depth, ipl_channels, color model, channel Seq)
    mode_list = {
        "RGB" : (cv2.cv.IPL_DEPTH_8U, 3),
        "L"   : (cv2.cv.IPL_DEPTH_8U, 1),
        "F"   : (cv2.cv.IPL_DEPTH_32F, 1)}
    if not mode_list.has_key(img0.mode):
        raise ValueError, 'unknown or unsupported input mode'
    modes = mode_list[img0.mode]

    result = cv2.cv.CreateImageHeader(size, modes[0], modes[1])

    # set imageData
    step = size[0] * (result.depth / 8) * result.nChannels
    cv2.cv.SetData(result, img0.rotate(180).tostring()[::-1], step)

    return result
