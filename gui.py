import tkinter as tk

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f'1500x1000')


def create_instructions_window():
    window = tk.Toplevel()
    instructions = tk.Label(window, text='Instructions')
    instructions.pack()

    close_button = tk.Button(window, text='Close', command=window.destroy)
    close_button.pack()

    window.mainloop()


webcam_frame = tk.Label(root, text='Webcam frame')
webcam_frame.pack()

next_button = tk.Button(root, text='Next')
next_button.pack()

back_button = tk.Button(root, text='Back')
back_button.pack()

close_button = tk.Button(root, text='Close', command=root.destroy)
close_button.pack()

reset_button = tk.Button(root, text='Reset')
reset_button.pack()

instructions_button = tk.Button(root, text='Instructions', command=create_instructions_window)
instructions_button.pack()

canvas = tk.Canvas(root)
canvas.pack()

square1 = canvas.create_rectangle(20, 20, 100, 100)
square2 = canvas.create_rectangle(100, 20, 180, 100)
square3 = canvas.create_rectangle(180, 20, 260, 100)
square4 = canvas.create_rectangle(20, 100, 100, 180)
square5 = canvas.create_rectangle(100, 100, 180, 180)
square6 = canvas.create_rectangle(180, 100, 260, 180)
square7 = canvas.create_rectangle(20, 180, 100, 260)
square8 = canvas.create_rectangle(100, 180, 180, 260)
square9 = canvas.create_rectangle(180, 180, 260, 260)

root.mainloop()
