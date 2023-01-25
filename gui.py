import tkinter as tk
import cv2 as cv
import PIL.Image, PIL.ImageTk


# import main


class MainWindow:
    def __init__(self, root):
        self.next_button = tk.Button(root, text='Next', font=30, command=self.show_webcam)
        self.next_button.pack()

        self.back_button = tk.Button(root, text='Back', font=30)
        self.back_button.pack()

        self.close_button = tk.Button(root, text='Close', font=30, command=root.destroy)
        self.close_button.pack()

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

    def show_webcam(self):
        vid = cv.VideoCapture(0)
        ret, frame = vid.read()
        # rgb_frame =  cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        captured_frame = PIL.Image.fromarray(frame)
        photo_image = PIL.ImageTk.PhotoImage(image=captured_frame)
        self.webcam_frame.photo = photo_image
        self.webcam_frame.configure(image=photo_image)
        self.webcam_frame.after(20, self.show_webcam)


class InstructionsWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.instructions = tk.Label(self.window, text='Instructions')
        self.instructions.pack()

        self.close_button = tk.Button(self.window, text='Close', command=self.window.destroy)
        self.close_button.pack()


root = tk.Tk()  # Creates a window
root.geometry('1500x1000')  # Sets the dimensions of the window
root.title("Rubik's cube solver")  # Gives the window a title
gui = MainWindow(root)
# gui.show_webcam()
root.mainloop()
