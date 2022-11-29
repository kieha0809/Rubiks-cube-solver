import cv2 as cv
import numpy as np
import math

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


def morphological_operations(frame):
    gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  # Converts the image to grayscale
    blurred_frame = cv.GaussianBlur(gray_img, (3, 3), 0)  # Blurs the image
    canny_frame = cv.Canny(blurred_frame, 20, 40, 3)  # Canny edge detection
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
    dilated_frame = cv.dilate(canny_frame, kernel)  # Dilates the image using the kernel defined above
    return dilated_frame


def detect_square(dilated_frame):  # Takes in dilated frame as parameter
    coordinates = []  # Coordintes of the squares
    thresh = cv.adaptiveThreshold(dilated_frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 21,
                                  4)  # Thresholds the image
    cv.imshow('thresh', thresh)  # Shows the result of thresholding
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


def bgr_to_colour(b, g, r):  # Function for converting bgr values to a colour
    colours = {'r': [0, 0, 255],
               'o': [0, 128, 255],
               'g': [0, 255, 0],
               'b': [255, 0, 0],
               'w': [255, 255, 255],
               'y': [0, 255, 255]}  # Defines bgr values for each colour
    min_distance = 1000
    colour_output = 'white'
    for colour in colours:  # Loops through the colours
        red_part = colours[colour][0]
        green_part = colours[colour][1]
        blue_part = colours[colour][2]
        distance = (r - red_part)^2 + (g - green_part)^2 + (b - blue_part)^2
        if distance < min_distance:
            min_distance = distance
            colour_output = colour
    # if colours[colour][0][0] <= b <= colours[colour][1][0] and colours[colour][0][1] <= g <= colours[colour][1][
    # 1] and colours[colour][0][2] <= r <= colours[colour][1][
    # 2]:  # If each of the b,g and r values are within the prescribed range
    # return colour
    # else:
    # continue
    return colour_output


'''vid = cv.VideoCapture(0)  # Captures video through webcam
while True:
    ret, frame = vid.read()  # Gets frame from webcam feed
    face = morphological_operations(frame)  # Applies morphological operations to frame
    coordiates = detect_square(face)  # Gets the coordinates of the squares
    if len(coordiates) == 9:  # When 9 squares are detected, the while loop is broken and the current frame is shown
        cv.waitKey(0)
        break'''

img = cv.imread('blue.png')
bgr = img[10, 10]
b = bgr[0]
g = bgr[1]
r = bgr[2]
colour = bgr_to_colour(b, g, r)
print(b,g,r)
print(colour)

# a=get_square_coordinates(10,10,2,2)
# print(a)
