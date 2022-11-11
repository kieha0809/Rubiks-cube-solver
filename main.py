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
    img = cv.imread(img_location)  # Reads in an image of the cube face
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Converts the image to grayscale

    blurred_frame = cv.blur(gray_img, (3, 3))  # Performs morphological operations: blurring,kernelling and dilation
    canny_frame = cv.Canny(blurred_frame, 30, 60, 3)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (9, 9))
    dilated_frame = cv.dilate(canny_frame, kernel)

    ret, thresh = cv.threshold(dilated_frame, 200, 255, 0)  # Thresholds the image
    cv.imshow('thresh', thresh)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # Finds contours
    min_area = 10000  # Defines the minimum area for a contour to be valid
    for contour in contours:  # Loops through all contours detected
        approx = cv.approxPolyDP(contour, 0.1 * cv.arcLength(contour, True),
                                 True)  # Gets the number of sides in each contour
        area = cv.contourArea(contour)  # Gets the area of each contour
        if area > min_area and len(
                approx) == 4:  # Checks if the contour is large enough to be the square and if it has 4 sides
            x, y, w, h = cv.boundingRect(contour)  # Gets coordinates of the corners of the square
            cv.rectangle(img, (x, y), (x + w, y + h), (36, 255, 12), 2)  # Draws the square onto the image

    # cv.drawContours(img, contours, -1, (0, 255, 0), 3)  # Draws on the contours

    cv.imshow('img', img)
    cv.waitKey(0)
    return x, y, w, h


def get_square_coordinates(x, y, w, h):
    coordinates = [] #Coordinates of the centres of each square
    increment = w / 3 # The increment that is added to the x coordinate to get between squares at the same height
    for i in range(3): #Loops through all squares on the top row and gets their coordinates
        x_cor = x + x / 6 + i * increment
        y_cor = y + y / 6
        coordinates.append((x_cor, y_cor))
    for i in range(3): #Repeats the above procedure for the second row
        x_cor = x + x / 6 + i * increment
        y_cor = y + y / 2
        coordinates.append((x_cor, y_cor))
    for i in range(3): #Repeats for the third row
        x_cor = x + x / 6 + i * increment
        y_cor = y + 5 * y / 6
        coordinates.append((x_cor, y_cor))

    return coordinates


#detect_square('cube.jpg')
'''img = cv.imread('cube.jpg')
cv.imshow('img',img)
cv.waitKey(0)'''

a=get_square_coordinates(10,10,2,2)
print(a)