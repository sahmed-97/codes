 #PYTHON METHOD DEFINITION

'''
  title::
    High Speed Corner Detection through FAST

  author::
    Sheela Ahmed

  description::
    This code will detect corners in an image using high speed corner detection compared to the Harris method. It centers around creating a circle with a center pixel and comparing the intensities of the circle pixels to the center pixel. It also includes a method for non-maximal suppression, which removes corners in the image that have an adjacent corner with a higher score value. 

  attributes::
    src: The source image.

    differenceThreshold: The threshold set to determine if two pixels are drastically different to detect where there is a corner in the image.

    contiguousThreshold: The threshold set to determine if pixels with similar intensities are adjacent to one another. 

    nonMaximalSuppression: Set by default to "True" and determines whether or not non-maximal suppression will be executed in the code.

  copyright::
    Copyright(C), Rochester Institute of Technology, 2017
'''

import numpy
import ipcv
import cv2

#separate function to create the circle
def circle(row, col):


    #after refining the center row and column, the points were made by moving around the radius of 3

     point1 = (row+3, col) #add 3 to the rows; so 3 up
     point3 = (row+3, col-1) #3 up and 1 to the left
     #point2 = (row+3, col-2) #3 up and 2 to the left
     point5 = (row+1, col+3) #1 up and 3 to the right
     #point6 = (row, col+3) #3 to the right
     point7 = (row-1, col+3) # 1 down and 3 to the right
     #point8 = (row-3, col+1)
     point9 = (row-3, col) #3 down 
     #point10 = (row-3, col-2)
     point11 = (row-3, col-1) #3 down and 1 to the left
     #point12 = (row-2, col-3) 
     point13 = (row+1, col-3) #1 up and 3 to the left
     #point14 = (row, col-3) #3 to the left
     point15 = (row-1, col-3) #1 down and 3 to the left

     #return the points
     return [point1, point3, point5, point7, point9, point11, point13, point15]


#separate function to find the corners using the circle function
def corner(src, row, col, ROI, differenceThreshold):
     #get points rom circle fn
     ROI = circle(row,col)

     #get intensity of the row and col of the image that loops through int he fast fn
     intensity = int(src[row][col])

     #pick outer points using the circle fn and use the current row,col as center pixel
     row1, col1 = ROI[0]
     row9, col9 = ROI[4]
     row5, col5 = ROI[2]
     row13, col13 = ROI[6]

     #get intensities of each of those outer pixels
     intensity1 = int(src[row1][col1])
     intensity9 = int(src[row9][col9])
     intensity5 = int(src[row5][col5])
     intensity13 = int(src[row13][col13])


     #check if intensities are greater than difference threshold
     count = 0
     corners = []
     if abs(intensity1 - intensity) > differenceThreshold:
         count +=1
     if abs(intensity9 - intensity) > differenceThreshold:
         count += 1
     if abs(intensity5 - intensity) > differenceThreshold:
         count += 1
     if abs(intensity13 - intensity) > differenceThreshold:
         count += 1
     

     #return count if it is greater than 3
     if count >= 3:
         return count
             #get the corners from the counts greater than or equal to 3
#     return count 


#separate fn to check if pixels are adjacent to one another
def adjacent(point1, point2):

     #define two points
     row1, col1 = point1
     row2, col2 = point2

     #get the x and y distances
     x_dist = row1 - row2
     y_dist = col1 - col2
             
     #return the distances that are less than the Eucildean distance of 4
     return numpy.sqrt(x_dist**2 + y_dist**2) <= 4


#separate fn to find the score for non-maximal suppression
def score(src, point, ROI):
         
    #index
    i = 1

    #get a row and column and use the circle rn to get outer pixels
    row, col = point
    ROI = circle(row,col)

    #get intensity of the center pixel
    intensity = int(src[row][col])

    #define the row and column of the outer pixels
    row1, col1 = ROI[0]
    row3, col3 = ROI[1]
    row5, col5 = ROI[2]
    row7, col7 = ROI[3]
    row9, col9 = ROI[4]
    row11, col11 = ROI[5]
    row13, col13 = ROI[6]
    row15, col15 = ROI[7]

#    coord = numpy.matrix([ROI[0], ROI[1], ROI[2], ROI[3], ROI[4], ROI[5], ROI[6], ROI[7]])

#    intensities = int(coord)

    #find the intensities of those outer pixels
    intensity1 = int(src[row1][col1])
    intensity3 = int(src[row3][col3])
    intensity5 = int(src[row5][col5])
    intensity7 = int(src[row7][col7])
    intensity9 = int(src[row9][col9])
    intensity11 = int(src[row11][col11])
    intensity13 = int(src[row13][col13])
    intensity15 = int(src[row15][col15])


    #find the score of the differences between each of the outer pixel intensities and the center pixel intensity. 
    score = abs(intensity - intensity1) + abs(intensity - intensity3) + \
            abs(intensity - intensity5) + abs(intensity - intensity7) + \
            abs(intensity - intensity9) + abs(intensity - intensity11) + \
            abs(intensity - intensity13) + abs(intensity - intensity15)

    #return the score value as it loops through each pixel
    return score

#start the final fast fn
def fast(src, differenceThreshold=50, contiguousThreshold=12, nonMaximalSuppression=True):
    
     #get the dimensions of the original src image
     numberRows, numberColumns, numberBands, dataType = ipcv.dimensions(src)

     #set the final dst image to numpy.zeros that is the same size as src
     dst = numpy.zeros(src.shape)
     #set corners to an empty list
     corners = []

     #to make sure not to go onto the edge of the image, loop through the image starting from a quarter of it to three quarters of it.
     startRow = int(.25*numberRows) #where to start the loop in rows
     endRow = int(.75*numberRows) #where to end the loop in rows
     startCol = int(.25*numberColumns) #start the loop in col
     endCol = int(.75*numberColumns)   #end the loop in col
     #run filter2d thru image

     #go thru all pixels and get intensities
     for row in range(startRow, endRow): #go through the rows and columns defined above
         for col in range(startCol, endCol):
             ROI = circle(row,col) #get the circle with each row,col in the loop as the center pixel
             if corner(src, row, col, ROI, differenceThreshold) == True: #if the count from the corner fn is greater than or equal to 3:
                 corners.append((row,col)) #add to the corners list
                 dst[row,col] = 1 #set the value at that row,col in the dst image to 1
#     print(corners)

     #execute the non-maximal suppression
     if nonMaximalSuppression == True:
         #index
         i = 1

         #go through the list of the corners
         while i < len(corners):
             currPt = corners[i] #set the current point
             prevPt = corners[i-1] #get the previous point
             if adjacent(prevPt, currPt): #check if they are adjacent to one another
                 #get the scores at the two points using the score fn
                 currScore = score(src, currPt, ROI) 
                 prevScore = score(src, prevPt, ROI)
                 #compare the score values  
                 if currScore > prevScore:
                     del(corners[i-1]) #if current score is greater, delete the previous corner point
                 else:
                     del(corners[i]) #if current is less, delete that corer point
             else:
                 i +=1
                 continue
         return
     
     #return the final dst image
     return dst

#   PYTHON TEST HARNESS
if __name__ == '__main__':

    import os.path
    import time
    import cv2

    home = os.path.expanduser('~')
    filename = home + os.path.sep + 'src/python/examples/data/checkerboard.tif'
#    filename = home + os.path.sep + \
#                'src/python/examples/data/sparse_checkerboard.tif'

    src = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

    startTime = time.time()
    dst = ipcv.fast(src, differenceThreshold=50,
                              contiguousThreshold=9,
                              nonMaximalSuppression=True)
    print('Elapsed time = {0} [s]'.format(time.time() - startTime))

    cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename, src)

    if len(src.shape) == 2:
        annotatedImage = cv2.merge((src, src, src))
    else:
        annotatedImage = src
    annotatedImage[dst == 1] = [0,0,255]

    cv2.namedWindow(filename + ' (FAST Corners)', cv2.WINDOW_AUTOSIZE)
    cv2.imshow(filename + ' (FAST Corners)', annotatedImage)

    print('Corner coordinates ...')
    indices = numpy.where(dst == 1)
    numberCorners = len(indices[0])
    if numberCorners > 0:
        for corner in range(numberCorners):
            print('({0},{1})'.format(indices[0][corner], indices[1][corner]))

    action = ipcv.flush()
