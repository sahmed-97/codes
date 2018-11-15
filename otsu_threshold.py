#PYTHON METHOD DEFINITION
'''
  title::
    Otsu Thresholding

  author::
    Sheela Ahmed

  description::
    This method will compute a threshold value for giza.jpg using Otsu's method. It will include the histogram, pdf and cdf of the image and compute a threshold value to return  a binary image at that threshold value. It will return the thresholded image and the threshold value.

  attributes::
    im: The image that is brought in. For this code, it is giza.jpg

    maxCount: The maximum digital count in the image

    verbose: The verbose flag indicates whether or not the pdf and threshold value of the image are plotted. If it is true, the code will return a graph depicting the PDF and threshold value of the image. If it is false, it will not return anything.

  copyright::
    Copyright(C), Rochester Institute of Technology, 2017
'''
from matplotlib import pyplot as plt
import cv2
import numpy as np
import ipcv

def otsu_threshold(im, maxCount=255, verbose=False):

    #create an empty array of zeroes to make the final image
    img = np.zeros(im.shape) 

    #calculate histogram, pdf and cdf from histogram_opencv file
    h, pdf, cdf = ipcv.histogram(im) 

    #flatten pdf and cdf
    pdf = pdf.flatten() 
    cdf = cdf.flatten() 

    #find the dimensions of the image using the dimensions file
    numberRows, numberColumns, numberBands, dataType = ipcv.dimensions(im)

    #error check to make sure image is in grayscale
    if len(im.shape) > 2:
        msg = 'Image must be in grayscale'
        raise RuntimeError(msg)

    #set an empty array for the threshold values
    kvalues = []
    for k in range(maxCount+1):
        
        #set omegak initally to 0, and sum up the pdf values at every x value in the range before the threshold, using the omegak equation given for Otsu's method
        omegak = 0
        for x in range(0, k-1):
            omegak += pdf[x] 

        #fix the divide by 0 issue
        if omegak == 0:
            omegak = 0.0001
        elif omegak == 1:
            omegak = .9999

        #set muk initially to 0, and sum up the values at every x value in the range before the threshold, using the muk equation given for Otsu's method.
        muk = 0
        for x in range(0, k-1):
            muk = muk + (pdf[x]*x) #multiple the pdf by every x value and add to total.

        #set muT to 0 and sum up values at every x value in the entire range.
        muT = 0
        for y in range(0, maxCount+1):
            muT = muT + (pdf[y]*y)

        #equation to find sigmaK
        sigmak = (((muT*omegak)-muk)**2)//(omegak*(1-omegak))
        
        #append all the values of k into the list kvalues
        kvalues.append(sigmak)

    #create an array of all the k values
    kvalues = np.asarray(kvalues)
    
    #find the threshold in the array
    threshold = np.argmax(kvalues)
    
        #determine if the pixel values in the image are greater or less than the threshold value. If they are greater, set value to 1, If they are less, set it to 0.
    for pixel in range(im.size):
        if im.flat[pixel] < threshold:
            img.flat[pixel] = 0
        if im.flat[pixel] > threshold:
            img.flat[pixel] = 1
         
    #set thresholded image to the final image.
    thresholdedImage = img
    
    #plotting the pdf with the threshold value
    if verbose == True:
        figure = plt.figure()
        axes = figure.add_subplot(1,1,1)
        axes.set_xlabel('Digital Count')
        axes.set_ylabel('PDF')
        axes.set_title('PDF and Threshold Value for giza.jpg')
        axes.set_xlim(0, maxCount)
        axes.axvline(threshold, color = 'r')
        plt.plot(pdf)
        plt.show()

    #return thresholded image and the threshold value
    return thresholdedImage.astype(np.uint8), threshold
    

#PYTHON TEST HARNESS
if __name__ == '__main__':
        import cv2
        import ipcv
        import os.path
        import time

        home = os.path.expanduser('~')
        filename = home + os.path.sep + 'src/python/examples/data/giza.jpg'

        im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        print('Filename = {0}'.format(filename))
        print('Data type = {0}'.format(type(im)))
        print('Image shape = {0}'.format(im.shape))
        print('Image size = {0}'.format(im.size))

        startTime = time.time()
        thresholdedImage, threshold = ipcv.otsu_threshold(im, verbose=True)
        print('Elapsed time = {0} [s]'.format(time.time() - startTime))

        print('Threshold = {0}'.format(threshold))

        cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(filename, im)
        cv2.namedWindow(filename + ' (Thresholded)', cv2.WINDOW_AUTOSIZE)
        cv2.imshow(filename + ' (Thresholded)', thresholdedImage * 255)

        action = ipcv.flush()


