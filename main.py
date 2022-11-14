import cv2 as cv
import numpy as np

squares = []


def hsv_to_colourTRIAL(hsv):  # Function for converting HSV values to colour
    colours = {  # HSV colour ranges
        'white': ([0, 0, 179], [179, 16, 255]),
        'yellow': ([15, 51, 0], [27, 183, 215]),
        'blue': ([79, 135, 104], [112, 255, 255]),
        'green': ([24, 53, 93], [158, 255, 255]),
        'red': ([0, 119, 135], [179, 255, 181]),
        'orange': ([0, 118, 157], [179, 255, 255]),
    }


def detect_square(frame):
    # img = cv.imread(frame)  # Reads in an image of the cube face
    gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  # Converts the image to grayscale

    blurred_frame = cv.medianBlur(gray_img, 3)  # Performs morphological operations: blurring,kernelling and dilation
    #sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    #sharpen = cv.filter2D(blurred_frame, -1, sharpen_kernel)
    canny_frame = cv.Canny(blurred_frame, 30, 60, 3)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
    dilated_frame = cv.dilate(canny_frame, kernel)
    close = cv.morphologyEx(dilated_frame, cv.MORPH_CLOSE, kernel, iterations = 2)

    thresh = cv.adaptiveThreshold(close, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,21,4)  # Thresholds the image
    cv.imshow('thresh', thresh)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)  # Finds contours
    min_area = 1000  # Defines the minimum area for a contour to be valid
    max_area = 2000
    for contour in contours:  # Loops through all contours detected
        approx = cv.approxPolyDP(contour, 0.1 * cv.arcLength(contour, True),
                                 True)  # Gets the number of sides in each contour
        area = cv.contourArea(contour)  # Gets the area of each contour
        if min_area < area < max_area and len(approx) == 4:  # Checks if number of sides and area are reasonable
            x, y, w, h = cv.boundingRect(contour)  # Gets coordinates of the corners of the square
            aspect_ratio = w / h  # Aspect ratio for a square should be one
            if 0.9 < aspect_ratio < 1.1:  # Checks if aspect ratio is close enough to 1 to be classified as a square
                cv.rectangle(frame, (x, y), (x + w, y + h), (36, 255, 12), 2)  # Draws the square onto the image
                # squares.append([x+w,y+h]) #Appends coordinates of centre of square to array

    # cv.drawContours(img, contours, -1, (0, 255, 0), 3)  # Draws on the contours
    # print(squares)
    # print(squares.sort())
    cv.imshow('img', frame)
    cv.waitKey(1)
    # return x, y, w, h


def get_square_coordinates(x, y, w, h):
    coordinates = []  # Coordinates of the centres of each square
    increment = w / 3  # The increment that is added to the x coordinate to get between squares at the same height
    for i in range(3):  # Loops through all squares on the top row and gets their coordinates
        x_cor = x + x / 6 + i * increment
        y_cor = y + y / 6
        coordinates.append((x_cor, y_cor))
    for i in range(3):  # Repeats the above procedure for the second row
        x_cor = x + x / 6 + i * increment
        y_cor = y + y / 2
        coordinates.append((x_cor, y_cor))
    for i in range(3):  # Repeats for the third row
        x_cor = x + x / 6 + i * increment
        y_cor = y + 5 * y / 6
        coordinates.append((x_cor, y_cor))

    return coordinates


def hsv_to_colour(h, s, v):
    if h < 5 and s > 5:
        return 'r'
    elif h < 10 and h >= 3:
        return 'o'
    elif h <= 25 and h > 10:
        return 'y'
    elif h >= 70 and h <= 85 and s > 100 and v < 180:
        return 'g'
    elif h <= 130 and s > 70:
        return 'b'
    elif h <= 100 and s < 10 and v < 200:
        return 'w'
    else:
        return 'w'


vid = cv.VideoCapture(0)
while True:
    ret, frame = vid.read()
    detect_square(frame)

# def get_hsv([x,y]):
# rgb =
detect_square('cube2.jpg')

# a=get_square_coordinates(10,10,2,2)
# print(a)
