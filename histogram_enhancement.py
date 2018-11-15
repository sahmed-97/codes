#PYTHON METHOD DEFINITION

import numpy
import ipcv
import cv2

'''
  title::
    Histogram Enhancement

  author::
    Sheela Ahmed

  description::
    This method will use the histogram and CDF of an image to enhance it and return the enhanced image. The various enhancement types are equalize, match, linear2 and linear2. In equalize, the histogram is equalized to fir the entire domain. The match enhancement type matches the histogram of one image to the histogram of another. For linear1 and linear2, the CDF of an image is calculated as well as the slope. Linear enhancement linearly expands data into a new distribution. At certain thresholds at the low and high parts of the distribution determine clipping and crushing of the image. For equalization, the histogram of an image is equalized to fit the entire range of pixels and pixel values. This code will compute all these forms of enhancements to the images provided.
  attributes::
    etype: The enhancement type specified. It can be equalize, match, linear1 or linear2. If no etype is specified, then linear2 is performed.

    target: the image whose histogram is matched to the first image; the second image

    maxCount:The maximum count in the image.

  copyright::
    Copyright(C), Rochester Institute of Technology, 2017
'''
#thiss code does not work and I was having trouble finding the right syntax. I feel I know what I had to accomplish logically and algorithmically, but I struggled to correctly itnerpret it in my code.

def histogram_enhancement(im, etype='linear2', target=None, maxCount=255):

    histogram = ipcv.histogram(im) #call histogram openCV code from freshman class

    row, column = im.shape #determine shape of image, row by column
    im = numpy.reshape(im, (row, column, 1)) #reshape image to be 2d
    row, column, band = im.shape #shape of image
    pixels = row*column #total pixels in the image

#    pdf = histogram // pixels #calculate pdf
    cdf = numpy.cumsum(histogram) #calculate cdf
    cdf_normalized = cdf * maxCount/cdf[-1] #normalize the cdf

    target = 'matchFilename' #assign target image to matchFilename; image whose histogram I want to match

    #hist equalization/matching
    if etype == 'match' or 'equalize':
        #if image is RGB
#        for c in xrange(0,2):
#            im[:,:,c] = cv2.equalizeHist(im[:,:,c])
        #if image is grayscale
        equ = cv2.equalizeHist(im) #equalize the histogram
        enhancedImage = cv2.imwrite('matchFilename', equ) #rewrite histogram of first image to second image 
        histogram = ipcv.histogram(target) #set histogram of second image to histogram of first after equalizing it
        
    #linear 1
    elif etype == 'linear1' or 'linear2':
#        if etype == 'linear1':
            
        low = (x[cdf.argmin()], 0) #find min x and y values
        high = (x[cdf.argmax()], maxCount) #find max x and y values
        y = (m*x) + b #slope eq
        m = maxCount / (high - low) #find slope
        b = maxCount - (m*low) #find intercept

        for pixel in range(im): #go through each pixel
            if pixel < 0: #check values less than 0
                pixel = 0 #truncate them to 0
            elif pixel > maxCount: #check values greater than maxCount, 255
                pixel = maxCount #set them equal to maxCount
    else:
        msg = 'The enhancement type must be equalize, match, linear1 or linear2'
        raise RuntimeError(msg)

#        cdf_s = cdf[] #find new cdf after truncating outer value
        
    
    return enhancedImage #return parameters
 


#PYTHON TEST HARNESS
if __name__ == '__main__':

    import cv2
    import ipcv
    import os.path
    import time

    home = os.path.expanduser('~')
    filename = home + os.path.sep + 'src/python/examples/data/redhat.ppm'
    filename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'
    filename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
    filename = home + os.path.sep + 'src/python/examples/data/giza.jpg'

    matchFilename = home + os.path.sep + 'src/python/examples/data/giza.jpg'
    matchFilename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
    matchFilename = home + os.path.sep + 'src/python/examples/data/redhat.ppm'
    matchFilename = home + os.path.sep + 'src/python/examples/data/crowd.jpg'

    im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    print('Filename = {0}'.format(filename))
    print('Data type = {0}'.format(type(im)))
    print('Image shape = {0}'.format(im.shape))
    print('Image size = {0}'.format(im.size))

    cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename, im)

    print('Linear 2% ...')
    startTime = time.time()
    enhancedImage = ipcv.histogram_enhancement(im, etype='linear2')
    print('Elapsed time = {0} [s]'.format(time.time() - startTime))
    cv2.namedWindow(filename + ' (Linear 2%)', cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename + ' (Linear 2%)', enhancedImage)

    print('Linear 1% ...')
    startTime = time.time()
    enhancedImage = ipcv.histogram_enhancement(im, etype='linear1')
    print('Elapsed time = {0} [s]'.format(time.time() - startTime))
    cv2.namedWindow(filename + ' (Linear 1%)', cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename + ' (Linear 1%)', enhancedImage)

    print('Equalized ...')
    startTime = time.time()
    enhancedImage = ipcv.histogram_enhancement(im, etype='equalize')
    print('Elapsed time = {0} [s]'.format(time.time() - startTime))
    cv2.namedWindow(filename + ' (Equalized)', cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename + ' (Equalized)', enhancedImage)

    tgtIm = cv2.imread(matchFilename, cv2.IMREAD_UNCHANGED)
    print('Matched (Image) ...')
    startTime = time.time()
    enhancedImage = ipcv.histogram_enhancement(im, etype='match', target=tgtIm)
    print('Elapsed time = {0} [s]'.format(time.time() - startTime))
    cv2.namedWindow(filename + ' (Matched - Image)', cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename + ' (Matched - Image)', enhancedImage)

    tgtPDF = numpy.ones(256) / 256
    print('Matched (Distribution) ...')
    startTime = time.time()
    enhancedImage = ipcv.histogram_enhancement(im, etype='match', target=tgtPDF)
    
    print('Elapsed time = {0} [s]'.format(time.time() - startTime))
    cv2.namedWindow(filename + ' (Matched - Distribution)', cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename + ' (Matched - Distribution)', enhancedImage)

    action = ipcv.flush()


