'''
  title::
    Spatial Filtering

  author::
    Sheela Ahmed

  description::
    This method will apply a convolution filter to an image and produce the output final image to the screen. The function utilizes numpy.roll for a faster output. It takes in the source image, dstDepth, kernel, delta and maxCount as its parameters and returns the final output image.

  attributes::
    src: The src image that is being convoluted.

    dstDepth: The final data type of the destination/convoluted image.

    kernel: The kernel being used for the convolution.

    delta: the change 

    maxCount: The maximum digital count in the image, set to 255 as default

  copyright::
    Copyright(C), Rochester Institute of Technology, 2017
'''

#PYTHON METHOD DEFINITION
import numpy
import ipcv
def filter2D(src, dstDepth, kernel, delta=0, maxCount=255):

    #determine the rows, columns, bands and dtype of the src image
    numberRows, numberColumns, numberBands, dataType = ipcv.dimensions(src)
    
    #reshape image if grayscale to have only one band
    if numberBands == 1:
        src = src.reshape([numberRows, numberColumns, 1])

    #set kernel to an array of dtype float64
    kernel = numpy.asarray(kernel, dtype = numpy.float64)

    #set an output matrix of all zeros that is same size as src image and dtype exact same as kernel
    output = numpy.zeros([numberRows, numberColumns, numberBands], dtype = numpy.float64)

    #for loops to go through each pixel in rows and columns
    kRows, kCols = kernel.shape
    for kRow in range(kRows):
        for kCol in range(kCols):
            w = kernel[kRow, kCol] #set the weight of each individual element in the kernel
            offR = kRow - kRows//2 #offset in the rows
            offC = kCol - kCols//2 #offset in the columns
            Xroll = numpy.roll(src, offR, axis=0) #roll the rows
            Yroll = numpy.roll(Xroll, offC, axis=1) #roll the columns with each row
            output += Yroll * w  #multiply each roll by the weight of that given kernel element and add to the output matrix
          
    #return the output
    return output

#PYTHON TEST HARNESS
if __name__ == '__main__':

    import cv2
    import os.path
    import time

    home = os.path.expanduser('~')
#    filename = home + os.path.sep + 'src/python/examples/data/redhat.ppm'
    filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
#    filename = home + os.path.sep + 'src/python/examples/data/checkerboard.tif'
#    filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'

    src = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

    dstDepth = ipcv.IPCV_8U
#    kernel = numpy.asarray([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
#    offset = 0
    kernel = numpy.asarray([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
    offset = 128
#    kernel = numpy.ones((15,15))
#    offset = 0
#    kernel = numpy.asarray([[1,1,1],[1,1,1],[1,1,1]])
#    offset = 0


    startTime = time.time()
    dst = ipcv.filter2D(src, dstDepth, kernel, delta=offset)
    print('Elapsed time = {0} [s]'.format(time.time() - startTime))

    cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename, src)

    cv2.namedWindow(filename + ' (Filtered)', cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename + ' (Filtered)', dst)

    action = ipcv.flush()

