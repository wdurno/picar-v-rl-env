## this is basically just ball_tracker.py (linked), reduced to an API 
## link: https://github.com/sunfounder/SunFounder_PiCar-V/blob/V3.0/ball_track/ball_tracker.py 
## 
## primary interface: 
## - img ## img.read(), img.release() 
## - find_blob() ## returns (x, y), radius 
## - fw ## front wheels, ie. fw.turn(90)  
## - bw ## back wheels, ie. bw.speed = 60, bw.stop(), bw.forward() 

from time import sleep
import cv2
import numpy as np
import os

SCREEN_WIDTH = 80 ## reduced by half for more-efficient AI processing 
SCREEN_HIGHT = 60 ## also reduced by half 
CENTER_X = SCREEN_WIDTH/2
CENTER_Y = SCREEN_HIGHT/2
BALL_SIZE_MIN = SCREEN_HIGHT/10
BALL_SIZE_MAX = SCREEN_HIGHT/3

def find_blob(bgr_image) :
    radius = 0
    # Load input image
    #_, bgr_image = img.read()
    ##ret, bgr_image = img.read()
    ##if ret == False:
    ##    print("Failed to read image")

    orig_image = bgr_image

    bgr_image = cv2.medianBlur(bgr_image, 3)

    # Convert input image to HSV
    hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image, keep only the red pixels
    lower_red_hue_range = cv2.inRange(hsv_image, (0, 100, 100), (10, 255, 255))
    upper_red_hue_range = cv2.inRange(hsv_image, (160, 100, 100), (179, 255, 255))
    # Combine the above two images
    red_hue_image = cv2.addWeighted(lower_red_hue_range, 1.0, upper_red_hue_range, 1.0, 0.0)

    red_hue_image = cv2.GaussianBlur(red_hue_image, (9, 9), 2, 2)

    # Use the Hough transform to detect circles in the combined threshold image
    circles = cv2.HoughCircles(red_hue_image, cv2.HOUGH_GRADIENT, 1, 120, 100, 20, 10, 0)

    if circles is not None:
        circles = np.uint16(np.around(circles))

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        return (0, 0), 0
    if radius > 3:
        return center, radius
    else:
        return (0, 0), 0 

