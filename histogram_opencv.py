import cv2
import numpy
import matplotlib

'''
  title:
   Histogram_OpenCV
  author:
   Sheela Ahmed
  description:
   This method will compute the histogram of a given image, both grayscale and RGB, using the OpenCV method. It will also compute the Probability Density Function and Cumulative Density Function.
  attributes:
   The method taken in the image and returns the histogram, PDF, and CDF.
  copyright:
   Copyright(C), Rochester Institute of Technology, 2015
'''
def histogram(im, composite = "FALSE"):

   #define the number of bands - whether grayscale or RGB
    if len(im.shape) == 2:
       row, column = im.shape
       im = numpy.reshape(im, (row, column,1))

    row, column, band = im.shape

   #calculate histogram
    hist = []
    for i in range(band):   
       h = cv2.calcHist([im], [i], None, [256], [0,256])
       hist.append(h)  
    hist = numpy.asarray(hist) 

   #calculate PDF and CDF
    pixels = row*column
    pdf = hist/pixels
    cdf = numpy.cumsum(pdf, axis=1)

    return hist, pdf, cdf


if __name__ == '__main__':

   import cv2
   import ipcv
   import time
   import matplotlib.pyplot
   import matplotlib.backends.backend_agg

   # A greyscale test image
#   filename = 'crowd.jpg'
   # A 3-channel color test image
   filename = 'lenna.tif'

   im = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
   print('Data type = {0}'.format(type(im)))
#   print('Image shape = {0}'.format(im.shape))
#   print('Image size = {0}'.format(im.size))

   startTime = time.time()
   h, pdf, cdf = ipcv.histogram(im)
   print('Elapsed time = {0} [s]'.format(time.time() - startTime))

# The following will produce a figure containing color-coded plots of the 
# computed histogram, probabilty density function (PDF), and cumulative density 
# function (CDF) 


   if len(im.shape) == 3:
    color = ['blue', 'green', 'red']

    figure = matplotlib.pyplot.figure()
    for s in range(im.shape[2]):
     axes = figure.add_subplot(3,1,1)
     axes.set_xlim([0, 255])
     axes.set_xlabel('Digital Count')
     axes.set_ylabel('Number of Pixels')
     axes.plot(h[s,:], color = color[s])

     axes = figure.add_subplot(3,1,2)
     axes.set_xlim([0,255])
     axes.set_xlabel('Digital Count')
     axes.set_ylabel('PDF')
     axes.plot(pdf[s,:], color = color[s])
     

     axes = figure.add_subplot(3,1,3)
     axes.set_xlim([0,255])
     axes.set_xlabel('Digital Count')
     axes.set_ylabel('CDF')
     axes.plot(cdf[s,:], color = color[s])

    matplotlib.pyplot.show()

   else:
      figure = matplotlib.pyplot.figure()

      axes = figure.add_subplot(3,1,1)
      axes.set_xlim([0,255])
      axes.set_xlabel('Digital Count')
      axes.set_ylabel('Number of Pixels')
      axes.plot(h[0], color = "black")

      axes = figure.add_subplot(3,1,2)
      axes.set_xlim([0,255])
      axes.set_xlabel('Digital Count')
      axes.set_ylabel('PDF')
      axes.plot(pdf[0], color = "black")

      axes = figure.add_subplot(3,1,3)
      axes.set_xlim([0,255])
      axes.set_xlabel('Digital Count')
      axes.set_ylabel('CDF')
      axes.plot(cdf[0], color = "black")
      matplotlib.pyplot.show()


