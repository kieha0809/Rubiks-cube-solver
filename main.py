import cv2 as cv
import numpy as np
import math

squares = []


def morphological_operations(frame):
    gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  # Converts the image to grayscale
    blurred_frame = cv.GaussianBlur(gray_img, (3, 3), 0)  # Blurs the image
    canny_frame = cv.Canny(blurred_frame, 20, 40, 3)  # Canny edge detection
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
    dilated_frame = cv.dilate(canny_frame, kernel)  # Dilates the image using the kernel defined above
    return dilated_frame


def detect_square(dilated_frame):  # Takes in dilated frame as parameter
    coordinates = []  # Coordinates of the squares
    thresh = cv.adaptiveThreshold(dilated_frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 21,
                                  4)  # Thresholds the image
    # cv.imshow('thresh', thresh)  # Shows the result of thresholding
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)  # Finds contours
    min_area = 1000  # Defines the minimum area for a contour to be valid
    max_area = 2000  # Maximum area for which the contour is valid
    for contour in contours:  # Loops through all contours detected
        approx = cv.approxPolyDP(contour, 0.1 * cv.arcLength(contour, True),
                                 True)  # Gets the number of sides in each contour
        area = cv.contourArea(contour)  # Gets the area of each contour
        if min_area < area < max_area and len(approx) == 4:  # Checks if number of sides and area are reasonable
            x, y, w, h = cv.boundingRect(contour)  # Gets coordinates of the corners of the square
            aspect_ratio = w / h  # Aspect ratio for a square should be one
            if 0.9 < aspect_ratio < 1.1:  # Checks if aspect ratio is close enough to 1 to be classified as a square
                cv.rectangle(frame, (x, y), (x + w, y + h), (36, 255, 12), 2)  # Draws the square onto the image
                coordinates.append((x, y, w, h))
    cv.imshow('img', frame)
    cv.waitKey(1)
    return coordinates


def bgr_to_colour(bgr):  # Function for converting an array of bgr values to a colour
    colours = {'r': [0, 0, 200],
               'o': [0, 125, 200],
               'g': [0, 150, 0],
               'b': [160, 0, 0],
               'w': [255, 255, 255],
               'y': [70, 200, 200]}  # Defines bgr values for each colour
    min_distance = 1000  # Variable for the smallest distance between colours
    colour_output = 'w'  # Variable which stores the colour it is determined to be
    for colour in colours:  # Loops through the colours
        blue_part = colours[colour][0]  # Gets the red part from BGR values for each colour
        green_part = colours[colour][1]  # Same as above for green part
        red_part = colours[colour][2]  # Same as above for red part
        distance = math.sqrt((bgr[0] - blue_part) ** 2 + (bgr[1] - green_part) ** 2 + (
                    bgr[2] - red_part) ** 2)  # Works out 'distance' between colours
        if distance < min_distance:  # If distance calculated above is smaller than current minimum
            min_distance = distance  # Replace minimum distance with the distance calculated above
            colour_output = colour  # Replace the colour output with the colour we have been working with
    return colour_output  # Returns the first letter of the colour with the smallest distance


vid = cv.VideoCapture(0)  # Captures video through webcam
while True:
    ret, frame = vid.read()  # Gets frame from webcam feed
    face = morphological_operations(frame)  # Applies morphological operations to frame
    coordinates = detect_square(face)  # Gets the coordinates of the squares
    if len(coordinates) == 9:  # When 9 squares are detected, the while loop is broken and the current frame is shown
        for coordinate in coordinates:
            x = coordinate[0]
            y = coordinate[1]
            w = coordinate[2]
            h = coordinate[3]
            square_midpoint_x = int(x + w / 2)
            square_midpoint_y = int(y + h / 2)
            bgr = frame[square_midpoint_y, square_midpoint_x]
            colour = bgr_to_colour(bgr)
            print(coordinate,colour)
        cv.waitKey(0)
        break

'''img = cv.imread('red.png')
bgr = img[10,10]
print(bgr)
colour = bgr_to_colour(bgr)
print(colour)'''
