 #PYTHON METHOD DEFINITION

'''
  title::
    Corner Detection using the Harris Method

  author::
    Sheela Ahmed

  description::
    This code will detect corners in an image using the Harris corner detection method. It considers a local window in the image and find teh gradients and determinant and trace to find where there is a response for a corner. The code taken in the source image, the value sigma for the blurring filter and the constant value k for the threshold.

  attributes::
    src: The source image.

    sigma: The value for blurring the image. This code blurs the image while going through the pixels in the given window.

    k: The "Harris" constant value used for the response of a corner. It is set by default to 0.04.

  copyright::
    Copyright(C), Rochester Institute of Technology, 2017
'''

import numpy
import cv2
import ipcv

def harris(src, sigma=1, k=0.04):


#    img = cv2.GaussianBlur(src, 

    #create dst image that is same size as src image
    dst = numpy.zeros(src.shape)
    #get rows and columns of src image
    rows = src.shape[0]
    cols = src.shape[1]
    
    #get a gradient for x and y of src image
    dy, dx = numpy.gradient(src)

    #find the elements of the matrix, A, B and C in terms of xx, xy, and yy
    xx = dx**2
    xy = dy*dx
    yy = dy**2
 
    #set corners to an empty list
    corners = []
     
    #set the window size for blurring the image to 3
    window_size = 3

    #set an offset for blurring the image
    offset = window_size//2

    #go thru all the rows and columns
    for y in range(offset, rows-offset):
        for x in range(offset, cols-offset):
            #calculate the blurring with the window and offset going thru image
            window_xx = xx[y-offset:y+offset+1, x-offset:x+offset+1]
            window_xy = xy[y-offset:y+offset+1, x-offset:x+offset+1]
            window_yy = yy[y-offset:y+offset+1, x-offset:x+offset+1]

            #calculate the sums for each xx, xy and yy
            sum_xx = window_xx.sum()
            sum_xy = window_xy.sum()
            sum_yy = window_yy.sum()

            #find determinant and trace
            determinant = (sum_xx * sum_yy) - (sum_xy**2)
            trace = sum_xx + sum_yy

            #find the response with the determinant and trace
            response = determinant - k*(trace**2)

            #set the response values in the dst. image.
            dst[y,x] = response

    #return dst image
    return dst


#   PYTHON TEST HARNESS
if __name__ == '__main__':

    import os.path
    import time
    import cv2

    home = os.path.expanduser('~')
    filename = home + os.path.sep + 'src/python/examples/data/checkerboard.tif'
   # filename = home + os.path.sep + \
    #            'src/python/examples/data/sparse_checkerboard.tif'

    src = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

    sigma = 1
    k = 0.04
    startTime = time.time()
    dst = ipcv.harris(src, sigma, k)
    print('Elapsed time = {0} [s]'.format(time.time() - startTime))

    cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename, src)

    if len(src.shape) == 2:
        annotatedImage = cv2.merge((src, src, src))
    else:
        annotatedImage = src
    fractionMaxResponse = 0.25
    annotatedImage[dst > fractionMaxResponse*dst.max()] = [0,0,255]

    cv2.namedWindow(filename + ' (Harris Corners)', cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename + ' (Harris Corners)', annotatedImage)

    print('Corner coordinates ...')
    indices = numpy.where(dst > fractionMaxResponse*dst.max())
    numberCorners = len(indices[0])
    if numberCorners > 0:
        for corner in range(numberCorners):
            print('({0},{1})'.format(indices[0][corner], indices[1][corner]))

    action = ipcv.flush()
