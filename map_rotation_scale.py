# PYTHON METHOD DEFINITION
'''
  title::
    Map Rotation Scale

  author::
    Sheela Ahmed

  description::
    This function will rotate and scale an image using a transformation matrix. 

  attributes::
    src: The source image

    rotation: The rotation of the final image in relation to the first. It is set to a value in degrees.

    scale: The x and y values at which the image will be scaled.

  copyright::
    Copyright(C), Rochester Institute of Technology, 2017
'''


import numpy as np
import math
import ipcv

def map_rotation_scale(src, rotation=0, scale=[1, 1]):
    

#define theta
    theta = np.radians(rotation)
#define the rotation matrix
    rotationMatrix = np.matrix([[-math.cos(theta),math.sin(theta)],[-math.sin(theta),-math.cos(theta)]])
#define scale matrix
    scaleMatrix = np.matrix([[scale[0], 0],[0, scale[1]]])
#multiply rotation matrix and scale matrix to get transformation matrix
    transformMatrix = rotationMatrix * scaleMatrix

#get x and y values from src image
    yval, xval = np.indices(src.shape[0:2])

#flatten x values
    xvalues = xval.flatten()

#define mapX
    mapX = xvalues - (src.shape[0]/2)

#flatten y values
    yvalues = yval.flatten()

#define mapY
    mapY = (src.shape[1]/2) - yvalues

#make matrix of x and y values from map image
    coordinates = np.matrix([mapX, mapY])
    

    #map = coordinates * transformMatrix 

#get map
    map = transformMatrix * coordinates

#define xphat and yphat to get final maps
    xp = map[0]
    xphat = xp + (src.shape[0]/2)

    yp = map[1]
    yphat = (src.shape[1]/2) - yp

#define final maps, mapA and mapB
    mapA = np.reshape(xphat, [src.shape[0], src.shape[1]])
    mapB = np.reshape(yphat, [src.shape[0], src.shape[1]])

#transpose both maps
    mapA = mapA.transpose()
    mapB = mapB.transpose()
   

#return both as float32
    return mapA.astype('float32'), mapB.astype('float32')


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

    startTime = time.clock()
    map1, map2 = ipcv.map_rotation_scale(src, rotation=30, scale=[1.3, 0.8])
    elapsedTime = time.clock() - startTime
    print('Elapsed time (map creation) = {0} [s]'.format(elapsedTime))

    startTime = time.clock()
    dst = cv2.remap(src, map1, map2, cv2.INTER_NEAREST)
      #   dst = ipcv.remap(src, map1, map2, ipcv.INTER_NEAREST)
    elapsedTime = time.clock() - startTime
    print('Elapsed time (remapping) = {0} [s]'.format(elapsedTime)) 

    srcName = 'Source (' + filename + ')'
    cv2.namedWindow(srcName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(srcName, src)

    dstName = 'Destination (' + filename + ')'
    cv2.namedWindow(dstName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(dstName, dst)

    ipcv.flush()

