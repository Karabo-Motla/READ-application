
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path
import os

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\\frame3")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_readingSession_app():
    window.destroy()  # Close the login window
    os.system("python ReadingSession.py")

def open_readingList():
    window.destroy()
    os.system("python ChooseStory.py")


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
    467.0,
    320.0,
    image=image_image_1
)

canvas.create_rectangle(
    181.0,
    96.0,
    785.0,
    159.0,
    fill="#C4D1EC",
    outline="")

canvas.create_text(
    467.0,
    130.0,
    anchor="center",
    text="The number 1 Reading App",
    fill="#000000",
    font=("Kadwa Regular", 24 * -1)
)

canvas.create_text(
    467.0,
    300.0,
    anchor="center",
    text="You can choose from our selection of\n stories or you could have the system \n recommend you a story. ",
    fill="#000000",
    font=("Kadwa Regular", 20 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
recommend_button = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"), #add functionality
    relief="flat"
)
recommend_button.place(
    x=140.0,
    y=450.0,
    width=218.0,
    height=51.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
choose_button = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command= lambda: open_readingList(),
    relief="flat"
)
choose_button.place(
    x=600.0,
    y=450.0,
    width=218.0,
    height=51.0
)

canvas.create_rectangle(
    0.0,
    0.0,
    934.0,
    64.0,
    fill="#F8F7F2",
    outline="")

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    466.0,
    32.0,
    image=image_image_2
)

#view profile button
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=885.0,
    y=9.0,
    width=48.0,
    height=48.0
)

#menu options button
button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=0.0,
    y=5.0,
    width=48.0,
    height=48.0
)
window.resizable(False, False)
window.mainloop()