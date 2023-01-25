rimport
cv2 as cv
# import numpy as np
import math
import keyboard
import kociemba


class Cube:  # Class for the representation of the cube
    def __init__(self):
        self.colours = ''  # Creates attribute for colours
        self.positions = ''  # Creates attribute for the positions of the colours

    def add_face(self, colours):  # Method for adding the colours of a face
        self.colours += colours

    def remove_current_face(self):  # Method for removing the most recently added face from colours
        self.colours = self.colours[:-6]

    def get_number_of_colours(self):  # Method for returning the number of colours added to the cube
        return len(self.colours)  # Returns the length of the colours attribute string

    def get_colours(self):  # Method for outputting the colours added
        return self.colours

    def get_positions(self):  # Method for outputting the string of positions
        return self.positions

    def set_positions(self, positions):
        self.positions = positions

    def convert_colours_to_positions(self, colours):  # Takes in a string of all colours and converts it to positions
        positions = ''
        for colour in self.colours:  # Loops through each letter in the string of colours
            if colour == 'y':
                positions += 'U'  # If the colour is yellow the position is U
            elif colour == 'b':
                positions += 'L'  # If the colour is blue the position is L
            elif colour == 'r':
                positions += 'F'  # If the colour is red the position is F
            elif colour == 'g':
                positions += 'R'  # If the colour is green the position is R
            elif colour == 'o':
                positions += 'B'  # If the colour is orange the position is B
            else:
                positions += 'D'  # If the colour is white the position is D
        self.set_positions(positions)  # Uses setter to change position attribute

    def solve_cube(self, cube_string):  # Takes in the string of positions as a parameter
        return kociemba.solve(str(cube_string))  # Uses the position attribute as argument in Kociemba function

    def reset_cube(self):  # Method for removing the all the colours from the 'colours' attribute
        self.colours = ''  # Resets colour attribute to empty string
        self.positions = ''  # Resets position attribute to empty string


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
                coordinates.append((x, y, w, h))  # Adds each (x,y,w,h) tuple to coordinates array
    cv.imshow('img', frame)  # Shows the frame with the squares drawn on
    cv.waitKey(1)  # Keeps the frame open
    return coordinates


def bgr_to_colour(bgr):  # Function for converting an array of bgr values to a colour
    colours = {'r': [30, 10, 200],
               'o': [50, 80, 170],
               'g': [0, 150, 0],
               'b': [160, 0, 0],
               'w': [200, 200, 200],
               'y': [80, 170, 180]}  # Defines bgr values for each colour
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


def sort_coordinates(coordinates):  # Function for arranging coordinates from left to right, row by row
    sorted_coordinates = sorted(coordinates, key=lambda k: [k[1], k[0]])  # Sorts coordinates based on y coordinates
    sorted_coordinates[0:3] = sorted(sorted_coordinates[0:3],
                                     key=lambda k: [k[0]])  # Sorts the first three coordinates by x coordinate
    sorted_coordinates[3:6] = sorted(sorted_coordinates[3:6],
                                     key=lambda k: [k[0]])  # Sorts the next three coordinates by x coordinate
    sorted_coordinates[6:9] = sorted(sorted_coordinates[6:9],
                                     key=lambda k: [k[0]])  # Sorts the final three coordinates by x coordinate
    return sorted_coordinates


def detect_colours():
    found_all_squares = False  # Variable for checking if colour detection is correct
    face_colours = ''  # String of colours in one face
    face = morphological_operations(frame)  # Applies morphological operations to frame
    coordinates = detect_square(face)  # Gets the coordinates of the squares
    if len(coordinates) == 9:  # When 9 squares are detected, the while loop is broken and the current frame is shown
        ordered_coordinates = sort_coordinates(coordinates)
        for coordinate in ordered_coordinates:  # Loops through the coordinates
            x = coordinate[0]  # Gets the x coordinate of the top left corner of the square
            y = coordinate[1]  # Gets the y coordinate of the top left corner of the square
            w = coordinate[2]  # Gets the width of the square
            h = coordinate[3]  # Gets the height of the square
            square_midpoint_x = int(x + w / 2)  # Calculates x coordinate of the midpoint of the square
            square_midpoint_y = int(y + h / 2)  # Calculates y coordinate of the midpoint of the square
            bgr = frame[square_midpoint_y, square_midpoint_x]  # Gets BGR value of pixel at midpoint of square
            colour = bgr_to_colour(bgr)  # Converts BGR value of pixel to a colour
            face_colours += colour  # Adds colour detected to the end of the string
        print(
            f'Are these colours correct: {face_colours}? Press space if yes, press any other key if no')  # Asks the user to check if the colours detected are correct
        cv.waitKey(0)  # Keeps the current frame open
    if keyboard.is_pressed('space'):  # If the user presses the space bar
        found_all_squares = True  # Colour detection is correct
    return (found_all_squares,
            face_colours)  # Returns a tuple with the success of the colour detection and the string of nine colours


cube = Cube()  # Creates an instance of the cube class
vid = cv.VideoCapture(0)  # Captures video through webcam
while cube.get_number_of_colours() != 54:  # Loop continues until all of the colours are detected
    ret, frame = vid.read()  # Gets frame from webcam feed
    colours_found = detect_colours()  # Sets the tuple output of detect_colours to a variable
    if colours_found[0] == True:  # If the nine colours were found successfully
        cube.add_face(colours_found[1])  # Add the colours to attribute in the cube class
print(cube.get_colours())  # For testing purposes
print(cube.get_positions())  # For testing purposes
all_colours = cube.get_colours()  # Assigns colour string to a variable
cube.convert_colours_to_positions(all_colours)  # Creates the position string from the colours
position_string = cube.get_positions()  # Assigns string of positions to a variable
solution = cube.solve_cube(position_string)  # Gets the solution using the class methods
print(solution)  # Displays solution
