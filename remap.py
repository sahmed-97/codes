#PYTHON METHOD DEFINITION
'''
  title::
    Remap

  author::
    Sheela Ahmed

  description::
    This function will remap the src image to fit properly in the destination image of a different size. It will take in the map1 and map2 calculated in ipcv.map_rotation_scale function.

  attributes::
    src: The source image

    map1, map2: the maps collected from the map_rotation_scale code.

    interpolation: The interpolation technique, set at defualt to INTER_NEAREST.

    borderMode = The method set for treating the borders of the image. It is set at deault to BORDER_REPLICATE which replicates the pixels outside the image to the pixel values at the edges of the image.

  copyright::
    Copyright(C), Rochester Institute of Technology, 2017
'''

import ipcv
import cv2
from scipy import interpolate
def remap(src, map1, map2, interpolation=ipcv.INTER_NEAREST, borderMode=ipcv.BORDER_CONSTANT, borderValue=0):

#define interpolation method
    if interpolation == ipcv.constants.INTER_NEAREST:
        dst = interpolate.NearestNDInterpolator(map1, map2)
#    elif interpolation = INTER.LINEAR:

#define border method REPLICATE
    if borderMode == ipcv.constants.BORDER_REPLICATE:
        r = max(map1) - min(src.shape[0]) #define right edge of image
        l = min(map1) - min(src.shape[0]) #define left edge of image
        t = max(map2) - max(src.shape[1]) #define top of image
        b = min(map2) - min(src.shape[1]) #define bottom of image
        dst = cv2.copyMakeBorder(src, t, b, l, r, cv2.BORDER_REPLICATE)

#return the destination image.
        return dst
#   PYTHON TEST HARNESS
if __name__ == '__main__':

    import cv2
    import ipcv
    import os.path
    import time

    home = os.path.expanduser('~')
    filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
    filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
    src = cv2.imread(filename)

    map1, map2 = ipcv.map_rotation_scale(src, rotation=30, scale=[1.3, 0.8])

    startTime = time.clock()
    dst = ipcv.remap(src, map1, map2, interpolation=ipcv.INTER_NEAREST, borderMode=ipcv.BORDER_CONSTANT, borderValue=0)
    elapsedTime = time.clock() - startTime
    print('Elapsed time (remap) = {0} [s]'.format(elapsedTime))

    srcName = 'Source (' + filename + ')'
    cv2.namedWindow(srcName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(srcName, src)

    dstName = 'Destination (' + filename + ')'
    cv2.namedWindow(dstName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(dstName, dst)

    ipcv.flush()

