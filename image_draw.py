import cv2 as cv
import os
import numpy as np
# Global list to store coordinates
coords = []
coords_x = []
coords_y = []

def drawPoint(event, x, y, flags, param):
    global coords
    global coords_x
    global coords_y  # Make coords accessible across function calls
    img = param
    if event == cv.EVENT_LBUTTONDBLCLK:
        if len(coords) < 2:  # Allow only two points
            cv.circle(img, (x, y), 10, (0, 0, 255), -1)
            coords_x.append(x)
            coords_y.append(y)
            coords.append((x,y))

def get_first_frame(videoname):
    vidcap = cv.VideoCapture(videoname)
    success, image = vidcap.read()
    if success:
        cv.imwrite("first_frame.jpg", image)  # save frame as JPEG file

def double_click_draw():
    global coords
    global coords_x
    global coords_y   # Use the global list
    coords = []  # Reset at start
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
    difference_x = abs(coords_x[n-1] - coords_x[n-2])
    difference_y = abs(coords_y[n-1] - coords_y[n-2])
    
    distance_pixels = np.sqrt((difference_x)** 2 + (difference_y) ** 2)
    ratio = distance_pixels / actual_distance
    return ratio