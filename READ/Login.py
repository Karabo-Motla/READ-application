
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path
from tkinter import messagebox
import os

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_selectStory_app():
    window.destroy()  
    os.system("python SelectStory.py")

def is_entry_empty(entry):
    return not entry.get().strip()  # Check if the text is empty after removing any leading or trailing whitespaces

def check_entries():
    if is_entry_empty(entry_1) or is_entry_empty(entry_2):
        messagebox.showwarning("Warning", "One or both fields are empty")
    else:
        open_selectStory_app()  # Open the next window if both fields are filled

  # Open the main application window


window = Tk()

window.geometry("934x575")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 575,
    width = 934,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    934.0,
    582.0,
    fill="#D9D9D9",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    468.0,
    289.0,
    image=image_image_1
)

canvas.create_rectangle(
    165.0,
    33.0,
    769.0,
    96.0,
    fill="#AAC0F6",
    outline="")

canvas.create_text(
    467.0,
    65.0,
    anchor="center",
    text="WELCOME TO THE READ APP",
    fill="#000000",
    font=("Kadwa Regular", 24 * -1)
)

canvas.create_rectangle(
    196.0,
    118.0,
    736.0,
    530.0,
    fill="#AAC0F6",
    outline="")

canvas.create_rectangle(
    220.0,
    186.0,
    703.0,
    187.0,
    fill="#000000",
    outline="")

canvas.create_text(
    467.0,
    160.0,
    anchor="center",
    text="Login",
    fill="#000000",
    font=("Kadwa Regular", 24 * -1)
)

canvas.create_text(
    250.0,
    251.0,
    anchor="nw",
    text="Email",
    fill="#000000",
    font=("Kadwa Regular", 24 * -1)
)

forgot_password_button = Button(
    text = "forgot password",
    fg = "blue",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"), #add functionality here
    relief="flat"
)

forgot_password_button.place(
    x=394.0,
    y=473.0,
    width=126.0,
    height=22.0
)

canvas.create_text(
    215.0,
    318.0,
    anchor="nw",
    text="Password",
    fill="#000000",
    font=("Kadwa Regular", 24 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    499.0,
    271.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#F5F5F5",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=388.0,
    y=258.0,
    width=222.0,
    height=25.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    373.0,
    271.0,
    image=image_image_2
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    498.5,
    329.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#F5F5F5",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=387.0,
    y=316.0,
    width=223.0,
    height=25.0
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    373.0,
    330.0,
    image=image_image_3
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command= check_entries,
    relief="flat"
)
button_2.place(
    x=371.0,
    y=396.0,
    width=171.0,
    height=46.0
)
window.resizable(False, False)
window.mainloop()
