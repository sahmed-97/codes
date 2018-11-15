#PYTHON METHOD DEFINITION
'''
  title::
    Map GCP

  author::
    Sheela Ahmed

  description::
    This function will map one image onto another image of different size through a mapping function and linear least squares regression. The function will take in both x and y values of the source and map image and create a matrix to produce a second order polynomial mapping function.

  attributes::
    src: The source image.

    map: The final image on which the soure image will be mapped.

    srcX: The x values from the source image.

    srcY: The y values from the source image.

    mapX: The x values from the map image.

    mapY: The y values from the map image.

    order: The order of the polynomial. It is set to a default 1 (first order polynomial) and is changed to 2 (second order) in the test harness.

  copyright::
    Copyright(C), Rochester Institute of Technology, 2017
'''

import numpy as np
import ipcv
import math

def map_gcp(src, map, srcX, srcY, mapX, mapY, order=1):

#define Yxbar matrix
    Yxbar = np.matrix([mapX]).T

#define Yybar matrix
    Yybar = np.matrix([mapY]).T

#set x and y to arrays of mapX and mapY
    X = np.array(mapX)
#    X = X.flatten()
    print('X shape', X.shape)
    Y = np.array(mapY)
#    Y = Y.flatten()
    print('Y shape', Y.shape)

#Xbar matrix
    Xbar = np.matrix([np.ones(len(mapX)), X, Y, X * Y, X**2, Y**2]).T
#transpose Xbar matrix
    X_T = Xbar.T

#define a and b 
    a = (((X_T * Xbar)) * (X_T * Yxbar))

    b = (((X_T * Xbar)) * (X_T * Yybar))

#get x and y values from the map image
    coord = np.indices([map.shape[0], map.shape[1]])

#separate the x values ad y values
    xval = np.array(coord[1])
    xvalf = xval.flatten().T
    print('xval', xvalf)
    print(xvalf.shape)
    yval = np.array(coord[0])
    yvalf = yval.flatten().T
    print('yval', yvalf)
    print(yvalf.shape)

#define the x matrix again, this time with the otehr x and y values
    X_ = np.matrix([np.ones(len(srcX)), xvalf, yvalf, xvalf*yvalf, xvalf**2, yvalf**2])
    print('X_', X_)
    print(X_.shape)

#define xprime and yprime as final x and y values to fit in image
    xprime = a * X_
#    xprime = a[0] + (a[1]*X_[0:1]) + (a[2]*X_[0:2]) + (a[3]*X_[0:3]) + (a[4]*X_[0:4]) + (a[5]*X_[0:5])
    print('xprime', xprime)
    print(xprime.shape)
#    print(xprime.type)

    yprime = b * X_
#    yprime = b[0] + (b[1]*X_[0:1]) + (b[2]*X_[0:2])  + (b[3]*X_[0:3]) + (b[4]*X_[0:4]) + (b[5]*X_[0:5])
    print('yprime', yprime)
    print(yprime.shape)

    map1 = xprime.reshape(map.shape[0])
    map2 = yprime.reshape(map.shape[1])
#    print(yprime.type)


#    map = np.zeros(map.shape)
#    if order == 1:
        
#    elif order == 2:
#    else:
#        msg = "polynomial must be first or second order"
#        raise RuntimeError(msg)

#return the two as float32
    return map1.astype(np.float32), map2.astype(np.float32)
 

#PYTHON TEST HARNESS
if __name__ == '__main__':
    
    import cv2
    import ipcv
    import os.path
    import time

    home = os.path.expanduser('~')
    imgFilename = home + os.path.sep + \
                       'src/python/examples/data/registration/image.tif'
    mapFilename = home + os.path.sep + \
                       'src/python/examples/data/registration/map.tif'
    gcpFilename = home + os.path.sep + \
                       'src/python/examples/data/registration/gcp.dat'
    src = cv2.imread(imgFilename)
    map = cv2.imread(mapFilename)

    srcX = []
    srcY = []
    mapX = []
    mapY = []
    linesRead = 0
    f = open(gcpFilename, 'r')
    for line in f:
        linesRead += 1
        if linesRead > 2:
            data = line.rstrip().split()
            srcX.append(float(data[0]))
            srcY.append(float(data[1]))
            mapX.append(float(data[2]))
            mapY.append(float(data[3]))
    f.close()

    startTime = time.clock()
    map1, map2 = ipcv.map_gcp(src, map, srcX, srcY, mapX, mapY, order=2)
    elapsedTime = time.clock() - startTime
    print('Elapsed time (map creation) = {0} [s]'.format(elapsedTime)) 

    startTime = time.clock()
    dst = cv2.remap(src, map1, map2, cv2.INTER_NEAREST)
      #   dst = ipcv.remap(src, map1, map2, ipcv.INTER_NEAREST)
    elapsedTime = time.clock() - startTime
    print('Elapsed time (remap) = {0} [s]'.format(elapsedTime)) 

    srcName = 'Source (' + imgFilename + ')'
    cv2.namedWindow(srcName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(srcName, src)

    mapName = 'Map (' + mapFilename + ')'
    cv2.namedWindow(mapName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(mapName, map)

    dstName = 'Warped (' + mapFilename + ')'
    cv2.namedWindow(dstName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(dstName, dst)

    ipcv.flush()

