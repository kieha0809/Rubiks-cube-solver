import tkinter as tk  # Imports Tkinter library
import cv2 as cv  # Imports OpenCv-python library
import PIL.Image, PIL.ImageTk  # Imports two modules from PIL


class MainWindow:  # Class for the main window
    def __init__(self, root, reset_callback):  # Uses callback function to detect when Reset button is pressed
        self.root = root
        self.reset_callback = reset_callback

        self.next_button = tk.Button(root, text='Next', font=30,
                                     command=self.set_colours_to_correct)  # Creates a button to press when current scan is correct
        self.next_button.pack()

        self.reset_button = tk.Button(root, text='Reset', font=30,
                                      command=self.reset_cube)  # Creates a button to reset the cube
        self.reset_button.pack()

        self.instructions_button = tk.Button(root, text='Instructions',
                                             font=30,
                                             command=self.open_instructions_window)  # Creates a button which will open the instructions in a new window
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

        self.instructions_window = None  # Attribute for the instructions window

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

    def open_instructions_window(self):  # Method for opening the instructions window
        if self.instructions_window is not None:  # Checks if there is already one open
            self.instructions_window.window.lift()  # If there is then lift the current instructions window
        else:  # If there is no instructions window
            # Create new window with a callback
            self.instructions_window = InstructionsWindow(self.root, self.close_instructions_window)

    def close_instructions_window(self):  # Close callback function
        self.instructions_window = None  # Resets attribute which stores instruction window

    def reset_cube(self):  # Method for resetting the cube
        self.reset_callback()  # Calls the callback function


class InstructionsWindow:  # Class for the instructions window
    def __init__(self, root, close_callback):  # Takes root window and callback function as parameters
        self.root = root
        self.close_callback = close_callback

        self.window = tk.Toplevel(self.root)  # Creates new window
        self.window.title("Instructions")  # Gives the window a title
        self.window.geometry('1000x500')  # Sets the dimensions of the window

        scrollbar = tk.Scrollbar(self.window)  # Creates a scrollbar
        scrollbar.pack(side="right")  # Places scrollbar on the right

        # Create a label for the heading
        self.heading = tk.Label(self.window, text='How to scan the cube', font=("Arial", 20))
        self.heading.pack()

        self.text = tk.Text(self.window)  # Creates text widget
        self.text.pack()

        # Creates a list of instructions
        self.instructions = [
            "1. Scan the yellow face first by having the yellow side facing the camera, the white side facing you and the green side to your left.",
            "2. Turn the cube once towards you, then turn it once to the left. Now the green side should be facing the camera, the blue side should be facing you and the orange side is on your left.",
            "3. Turn the cube once to the right. Now the red side should be facing the camera.",
            "4. Turn the cube once towards you. Now the white side should be facing the camera.",
            "5. Turn the cube once away from you (i.e. to the opposite of the previous instruction). Then turn the cube once to the right. Now the blue face should be facing the camera.",
            "6. Turn the cube once to the right. Now the orange face should be facing the camera.",
            "7. All the colours have now been scanned. Leave the cube in its current position where the red side is facing you, the top side is yellow and the left side is blue. Execute the instructions shown from this position."
        ]

        for instruction in self.instructions:  # Loops through all the instructions
            self.text.insert("end", instruction + "\n")  # Adds each instruction to the text widget

        self.text.config(wrap="word", state="disabled")  # Wraps text and prevents editing

        self.close_button = tk.Button(self.window, text='Close',
                                      command=self.close_window)  # Creates a close button
        self.close_button.pack()

        # Binds the callback function to the closing of the window
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):  # Method called when the 'Close' button is pressed
        self.window.destroy()  # Destroys the window
        self.close_callback()  # Calls the callback function
