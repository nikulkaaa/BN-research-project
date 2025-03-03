import cv2 as cv
import os
import numpy as np
import math

# So you only draw when clicking dragging
drawing = False 
center_x, center_y = -1, -1
# some lists for storage of numbers

coords = []
coords_x = []
coords_y = []
coords_x_object = []
coords_y_object = []
radiusss = []

def drawPoint(event, x, y, flags, param):
    # Make coords accessible across function calls
    global coords
    global coords_x
    global coords_y 
    img = param
    # double click to draw dot. 
    if event == cv.EVENT_LBUTTONDBLCLK:
        if len(coords) < 2:  # Allow only two points
            cv.circle(img, (x, y), 10, (0, 0, 255), -1)
            coords_x.append(x)
            coords_y.append(y)
            coords.append((x,y))


    # function for the dynamic circle drawing
def draw_circle_objects(event,x,y,flags,param):
    # Make coord lists accessible
    global coords_x_object
    global coords_y_object
    global radiusss
    global radiuss

    # cv event starting to draw.
    global drawing, center_x, center_y
    img = param
    # Allow only 2 circles. it resets on each image
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        # To remember the center
        center_x, center_y = x, y
        center = (center_x, center_y)
        # Store the values for the analysis calculations requiring the center
        coords_x_object.append(center_x)
        coords_y_object.append(center_y)

    # To keep drawing active while dragging
    elif event == cv.EVENT_MOUSEMOVE:
        drawing == True
    elif event == cv.EVENT_LBUTTONUP:
        # Calculate radius upen endpoint of 'line' drawn. And display the circle with the parameters
        radius = math.sqrt(((center_x-x)**2)+((center_y-y)**2))
        # store the radius
        radiuss.append(radius)
        cv.circle(img, (center_x, center_y), int(radius), (0, 0, 255), -1)
        # Stop drawing
        drawing = False
        
# For the backup circle drawing
def drag_and_draw_circle():
    global coords_x_object
    global coords_y_object
    global radiuss
    # reset the list so it can be seperate
    radiuss = []
    coords_x_object = []
    coords_y_object = []
            
    img = cv.imread("first_frame.jpg")
    # The amount of drawn circles or ROIs can be changed up in the function draw_circle_objects()
    # Change the max length of the list. 
    windowname = "Drag and draw the two objects, keep in mind the order (left, right or up, down for instance)"
    cv.namedWindow(windowname)
    cv.setMouseCallback(windowname, draw_circle_objects, img)

    while True:
        cv.imshow(windowname, img)
        k = cv.waitKey(30)
        if k == 27 or len(radiuss) == 2:
            break
    # Take down all windows and return the necessary values
    cv.destroyAllWindows()
    return coords_x_object, coords_y_object, radiuss
    # Take a screenshot of the first frame
def get_first_frame(videoname):
    vidcap = cv.VideoCapture(videoname)
    success, image = vidcap.read()
    if success:
        cv.imwrite("first_frame.jpg", image)  # save frame as JPEG file
    # Function that uses the drawpoint function, by double clicking and 
    # only allowing two dots per img
def double_click_draw():
    global coords
    global coords_x
    global coords_y

    coords = [] 
    img = cv.imread("first_frame.jpg")
    windowname = "Assign a length on the image"
    cv.namedWindow(windowname)
    cv.setMouseCallback(windowname, drawPoint, img)

    while True:
        cv.imshow(windowname, img)
        k = cv.waitKey(30)
        if k == 27 or len(coords) == 2: 
            break

    cv.destroyAllWindows()
    return coords_y, coords_x


def ratio_calc(actual_distance):
    global coords_x
    global coords_y
    n = len(coords_x)
    # ratio calculations
    difference_x = abs(coords_x[n-1] - coords_x[n-2])
    difference_y = abs(coords_y[n-1] - coords_y[n-2])
    
    distance_pixels = np.sqrt((difference_x)** 2 + (difference_y) ** 2)
    ratio = distance_pixels / actual_distance
    return ratio