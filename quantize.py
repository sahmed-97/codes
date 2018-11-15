import numpy

'''
  title::
    Quantize

  author::
    Sheela Ahmed

  description::
    This method will quantize the given images into the desired levels with equal bin sizes. The code will include two types of quantization: uniform and igs(Improved Grayscale Quantization).The method will return the image as the same data type it initially was read in as and perform both quantization forms. It will return three images: the original, uniform quantization, and igs quantization. 

  attributes::
    levels: The number of levels is the number of bins desired to bin the values. In this code it will be equal to 7

    qtype:This is the quantization type; either uniform or igs. The code includes the method taken to achieve both types.

    maxCount:The maximum count in the image.

    displayLevels:the number of levels to display the image back with similar brightness as it is initially.

  copyright::
    Copyright(C), Rochester Institute of Technology, 2017
'''

#   PYTHON METHOD DEFINITION
def quantize(im, levels, qtype='uniform', maxCount=255, displayLevels=None):

    dType = im.dtype #set image to uint8 because range from 0 to 255
#    dType = numpy.uint8 #hardcoding the data type of the image, commented out; used it before im.dtype

    if displayLevels == None:
        scale = 1.0
    else:
        scale = displayLevels // levels #do integer division if displayLevels is 255 so it divides evenly

    #error check for levels
    if levels <= 0: 
        msg = 'specified levels must be a positive integer'
        raise ValueError

    if len(im.shape) == 2: #defining shape and number of bands of the image, whether grayscale or RGB, taken from my histogram code
        row, column = im.shape 
        im =numpy.reshape(im, (row,column, 1)) #reshape to go through every value
    row, column, band = im.shape #shape of the image


    d = (maxCount + 1) / levels #define divisor as being the maxCount +1 (256) divided by levels

    #uniform quantization
    if qtype =='uniform':
        quantizedImage = numpy.floor(im / d)  #use integer division
    #igs quantization
    elif qtype == 'igs':
        quantizedImage = numpy.reshape(im, im.size) #describe fn and im.size
        r = 0 #set remainder initially to 0
        for pixel in range(im.size):
            v = quantizedImage[pixel] + r #add remainder to value
            if v > maxCount:#make sure the value doesn't exceed size of image, 255
                v = quantizedImage[pixel] #set it equal to maxCount if it does exceed
            r = v % d #find remainder
            quantizedImage[pixel] = v // d #integer division
        quantizedImage = numpy.reshape(quantizedImage, im.shape) #reshape image after including remainder
    else:
        raise RuntimeError #error check if it's neither uniform nor igs quantization

    quantizedImage *= scale

    return quantizedImage.astype(dType) #return image as same data type as it was in beginning


#   PYTHON TEST HARNESS
if __name__ == '__main__':

    import cv2
    import ipcv
    import os.path

    home = os.path.expanduser('~')
#    filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
#    filename = home + os.path.sep + 'src/python/examples/data/redhat.ppm'
    filename = home + os.path.sep + 'src/python/examples/data/linear.tif'
#    filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'

    im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    print('Filename = {0}'.format(filename))
    print('Data type = {0}'.format(type(im)))
    print('Image shape = {0}'.format(im.shape))
    print('Image size = {0}'.format(im.size))

    cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename, im)


    numberLevels = 7
    quantizedImage = ipcv.quantize(im,
                                   numberLevels,
                                   qtype='uniform',
                                   displayLevels=256)
    cv2.namedWindow(filename + ' (Uniform Quantization)', cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename + ' (Uniform Quantization)', quantizedImage)


    numberLevels = 7
    quantizedImage = ipcv.quantize(im,
                                   numberLevels,
                                   qtype='igs',
                                   displayLevels=256)
    cv2.namedWindow(filename + ' (IGS Quantization)', cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename + ' (IGS Quantization)', quantizedImage)
    

    action = ipcv.flush()


