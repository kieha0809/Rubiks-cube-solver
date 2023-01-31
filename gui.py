import tkinter as tk
import cv2 as cv
import PIL.Image, PIL.ImageTk


# import main


# import main

class MainWindow:
    def __init__(self, root):
        self.next_button = tk.Button(root, text='Next', font=30)
        self.next_button.pack()

        self.back_button = tk.Button(root, text='Back', font=30)
        self.back_button.pack()

        self.reset_button = tk.Button(root, text='Reset', font=30)
        self.reset_button.pack()

        self.instructions_button = tk.Button(root, text='Instructions', font=30)
        self.instructions_button.pack()

        self.command = tk.StringVar()
        self.command_label = tk.Label(root, textvariable=self.command, font=30)
        self.command_label.pack()

        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        self.square1 = self.canvas.create_rectangle(20, 20, 100, 100)
        self.square2 = self.canvas.create_rectangle(100, 20, 180, 100)
        self.square3 = self.canvas.create_rectangle(180, 20, 260, 100)
        self.square4 = self.canvas.create_rectangle(20, 100, 100, 180)
        self.square5 = self.canvas.create_rectangle(100, 100, 180, 180)
        self.square6 = self.canvas.create_rectangle(180, 100, 260, 180)
        self.square7 = self.canvas.create_rectangle(20, 180, 100, 260)
        self.square8 = self.canvas.create_rectangle(100, 180, 180, 260)
        self.square9 = self.canvas.create_rectangle(180, 180, 260, 260)

        self.webcam_frame = tk.Label(root)
        self.webcam_frame.pack()

        self.stop_updating_frame = False

    def show_frame(self, webcam_frame):
        # while True:
        # vid = cv.VideoCapture(0)
        # ret, frame = vid.read()
        if not self.stop_updating_frame:
            frame = cv.flip(webcam_frame, 1)
            cv2image = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
            img = PIL.Image.fromarray(cv2image)
            imgtk = PIL.ImageTk.PhotoImage(image=img)
            self.webcam_frame.imgtk = imgtk
            self.webcam_frame.configure(image=imgtk)
            self.webcam_frame.update()

    def freeze_frame(self):
        self.stop_updating_frame = True

    def unfreeze_fram(self):
        self.stop_updating_frame = False
