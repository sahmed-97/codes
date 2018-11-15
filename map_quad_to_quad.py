'''
  title::
    Perspective Transformation

  author::
    Sheela Ahmed

  description::
    This method will map one image onto another using quad-to-quad mapping and perspective transformation. It will take in the coordinates chosen for the size of the image and, through matrix multiplication, map the image onto another image. The function takes in both images and four coordinate points from both images to perform the multiplication

  attributes::
    img: The initial image; the image being mapped onto the other image.

    map: the seocnd image; the image that the img will be mapped on.

    imgX: The x values from img.

    imgY: The y values from img.

    mapX: The x vales from the points chosen for the map image.

    mapY: The y values from the points chosen for the map image.

  copyright::
    Copyright(C), Rochester Institute of Technology, 2017
'''

#PYTHON METHOD DEFINITION
import numpy
def map_quad_to_quad(img, map, imgX, imgY, mapX, mapY):

    #define a transformation matrix to multiply by img coordinates 
    u = mapX
    v = mapY
    x = imgX
    y = imgY
    row1 = u[0], v[0],1, 0, 0, 0, -u[0]*x[0], -v[0]*x[0]
    row2 = u[1], v[1], 1, 0, 0, 0, -u[1]*x[1], -v[1]*x[1]
    row3 = u[2], v[2], 1, 0, 0, 0, -u[2]*x[2], -v[2]*x[2]
    row4 = u[3], v[3], 1, 0, 0, 0, -u[3]*x[3], -v[3]*x[3]
    row5 = 0, 0, 0, u[0], v[0], 1, -u[0]*y[0], -v[0]*y[0]
    row6 = 0, 0, 0, u[1], v[1], 1, -u[1]*y[1], -v[1]*y[1]
    row7 = 0, 0, 0, u[2], v[2], 1, -u[2]*y[2], -v[2]*y[2]
    row8 = 0, 0, 0, u[3], v[3], 1, -u[3]*y[3], -v[3]*y[3]

    #create the matrix
    Matr = numpy.matrix([row1, row2, row3, row4, row5, row6, row7, row8])
   
    #create matrix of all the image x and y values
    img_val = numpy.matrix([x[0], x[1], x[2], x[3], y[0], y[1], y[2], y[3]])
    img_val = img_val.transpose()


    #multiply together to get the P map_to_image
    P = Matr.I * img_val
    
    #append a 1 to the end to make a 3x3 matrix
    one = numpy.matrix([1])
    P_M = numpy.vstack([P, one])
    P_M = numpy.reshape(P_M, (3,3))

    #get all x and y values from map image to put in matrix
    map_values = numpy.indices(map.shape[0:2])
    map_x = map_values[1]
    map_x = map_x.flatten()
    map_y = map_values[0]
    map_y = map_y.flatten()

    #create matrix of all ones
    uv = numpy.ones([3, map_x.size])
    
    #set first and second row to the x adn y values
    uv[0,:] = map_x
    uv[1,:] = map_y

    #multply by the P matrix to get x and y values in image with DC
    img_val = P_M * uv

    #convert to array
    img_val = numpy.array(img_val)

    #separate the rows to normalize
    xih = img_val[0]
    yih = img_val[1]
    h = img_val[2]

    #divide the first and second rows by the third to normalize the homogenous coordinate
    xval = xih/h
    yval = yih/h

    #extract x and y values into maps
    mapA = xval
    mapA = mapA.transpose()
    mapB = yval
    mapB = mapB.transpose()

    #reshape maps to fit the map shape
    map1 = numpy.reshape(mapA, map.shape[0:2])
    map2 = numpy.reshape(mapB, map.shape[0:2])

    #return as float32
    return map1.astype(numpy.float32), map2.astype(numpy.float32)

#   PYTHON TEST HARNESS
if __name__ == '__main__':
    
    import cv2
    import ipcv
    import os.path
    import time
    
    home = os.path.expanduser('~')
    imgFilename = home + os.path.sep + 'src/python/examples/data/lenna.tif'
    mapFilename = home + os.path.sep + 'src/python/examples/data/gecko.jpg'
    img = cv2.imread(imgFilename)
    map = cv2.imread(mapFilename)

    mapName = 'Select corners for the target area (CW)'
    cv2.namedWindow(mapName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(mapName, map)

    print('')
    print('--------------------------------------------------------------')
    print('  Select the corners for the target area of the source image')
    print('  in clockwise order beginning in the upper left hand corner')
    print('--------------------------------------------------------------')
    p = ipcv.PointsSelected(mapName, verbose=True)
    while p.number() < 4:
        cv2.waitKey(100)
    cv2.destroyWindow(mapName)

    imgX = [0, img.shape[1]-1, img.shape[1]-1, 0]
    imgY = [0, 0, img.shape[0]-1, img.shape[0]-1]
    mapX = p.x()
    mapY = p.y()

    print('')
    print('Image coordinates ...')
    print('   x -> {0}'.format(imgX))
    print('   y -> {0}'.format(imgY))
    print('Target (map) coordinates ...')
    print('   u -> {0}'.format(mapX))
    print('   v -> {0}'.format(mapY))
    print('')

    startTime = time.clock()
    map1, map2 = ipcv.map_quad_to_quad(img, map, imgX, imgY, mapX, mapY)
    elapsedTime = time.clock() - startTime
    print('Elapsed time (map creation) = {0} [s]'.format(elapsedTime)) 

    startTime = time.clock()
    dst = cv2.remap(img, map1, map2, cv2.INTER_NEAREST)
    elapsedTime = time.clock() - startTime
    print('Elapsed time (remap) = {0} [s]'.format(elapsedTime)) 
    print('')

    compositedImage = map
    mask = numpy.where(dst != 0)
    if len(mask) > 0:
        compositedImage[mask] = dst[mask]

    compositedName = 'Composited Image'
    cv2.namedWindow(compositedName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(compositedName, compositedImage)

    ipcv.flush()


