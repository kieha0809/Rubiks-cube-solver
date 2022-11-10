import cv2 as cv
import numpy as np


def hsv_to_colour(hsv):  # Function for converting HSV values to colour
    colours = {  # HSV colour ranges
        'white': ([0, 0, 179], [179, 16, 255]),
        'yellow': ([15, 51, 0], [27, 183, 215]),
        'blue': ([79, 135, 104], [112, 255, 255]),
        'green': ([24, 53, 93], [158, 255, 255]),
        'red': ([0, 119, 135], [179, 255, 181]),
        'orange': ([0, 118, 157], [179, 255, 255]),
    }


def detect_square(img_location):
    img = cv.imread(img_location)
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray_img, 200, 255, 0)
    cv.imshow('dfgf',thresh)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    print(contours, hierarchy)

    cv.drawContours(img, contours, -1, (0, 255, 0), 3)

    '''min_area = 1000
    max_area = 2000
    for contour in contours:
        area = cv.contourArea(contour)'''

    cv.imshow('img', img)
    cv.waitKey(0)


detect_square('cube2.jpg')
'''img = cv.imread('cube.jpg')
cv.imshow('img',img)
cv.waitKey(0)'''
