import tkinter as tk  # Imports Tkinter library
import cv2 as cv  # Imports OpenCv-python library
import PIL.Image, PIL.ImageTk  # Imports two modules from PIL


class MainWindow:  # Class for the main window
    def __init__(self, root):
        self.next_button = tk.Button(root, text='Next', font=30,
                                     command=self.set_colours_to_correct)  # Creates a button to press when current scan is correct
        self.next_button.pack()

        self.reset_button = tk.Button(root, text='Reset', font=30)  # Creates a button to reset the cube
        self.reset_button.pack()

        self.instructions_button = tk.Button(root, text='Instructions',
                                             font=30)  # Creates a button which will open the instructions in a new window
        self.instructions_button.pack()

        self.command = tk.StringVar()  # Creates a StringVar to show the user commands
        self.command_label = tk.Label(root, textvariable=self.command,
                                      font=30)  # Creates a label which will show the user commands
        self.command_label.pack()

        self.canvas = tk.Canvas(root)  # Creates a canvas for drawing squares onto the window
        self.canvas.pack()

        self.square1 = self.canvas.create_rectangle(20, 20, 100, 100)  # Draws 9 squares to resemble a cube face
        self.square2 = self.canvas.create_rectangle(100, 20, 180, 100)
        self.square3 = self.canvas.create_rectangle(180, 20, 260, 100)
        self.square4 = self.canvas.create_rectangle(20, 100, 100, 180)
        self.square5 = self.canvas.create_rectangle(100, 100, 180, 180)
        self.square6 = self.canvas.create_rectangle(180, 100, 260, 180)
        self.square7 = self.canvas.create_rectangle(20, 180, 100, 260)
        self.square8 = self.canvas.create_rectangle(100, 180, 180, 260)
        self.square9 = self.canvas.create_rectangle(180, 180, 260, 260)

        self.webcam_frame = tk.Label(root)  # Label for showing the webcam frame
        self.webcam_frame.pack()

        self.colours_correct = False  # Attribute for checking if the user has confirmed the colours on screen

    def show_frame(self, webcam_frame):  # Method for updating the webcam frame label
        frame = cv.cvtColor(webcam_frame, cv.COLOR_BGR2RGB)  # Converts frame to RGB colour space
        img = PIL.Image.fromarray(frame)  # Converts frame from NumPy array to image
        imgtk = PIL.ImageTk.PhotoImage(image=img)  # Converts image into Tkinter PhotoImage object
        self.webcam_frame.configure(image=imgtk)  # Assigns frame to webcam frame label
        self.webcam_frame.update()  # Applies change to label

    def set_colours_to_correct(self):  # Method to show that the user confirms that the colours detected are correct
        self.colours_correct = True  # Sets colours_correct attribute to True

    def reset_colours_correct(self):  # Method to rest the colours_correct attribute
        self.colours_correct = False  # Sets colours_correct attribute to False

    def check_if_colours_correct(self):  # Method to check if the user has confirmed the colours
        return self.colours_correct  # Returns the colours_correct attribute
