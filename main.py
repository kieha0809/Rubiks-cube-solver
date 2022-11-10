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
    img = cv.imread(img_location) #Reads in an image of the cube face
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY) #Converts the image to grayscale

    blurred_frame = cv.blur(gray_img, (3, 3)) #Performs morphological operations: blurring,kernelling and dilation
    canny_frame = cv.Canny(blurred_frame, 30, 60, 3)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (9, 9))
    dilated_frame = cv.dilate(canny_frame, kernel)

    ret, thresh = cv.threshold(dilated_frame, 200, 255, 0) #Thresholds the image
    cv.imshow('thresh', thresh)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) #Finds contours
    cv.drawContours(img, contours, -1, (0, 255, 0), 3) #Draws on the contours

    cv.imshow('img', img)
    cv.waitKey(0)


detect_square('cube.jpg')
'''img = cv.imread('cube.jpg')
cv.imshow('img',img)
cv.waitKey(0)'''
