
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path
import os

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Radiobutton, StringVar , messagebox


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_Login():
    window.destroy()  # Close the login window
    os.system("python Login.py")

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
    575.0,
    fill="#D9D9D9",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    470.0,
    289.0,
    image=image_image_1
)

#header rectangle
canvas.create_rectangle(
    165.0,
    33.0,
    769.0,
    96.0,
    fill="#AAC0F6",
    outline="")

#header text
canvas.create_text(
    #edited size/position here
    467.0,
    65.0,
    anchor="center", #to center the text
    text="WELCOME TO THE READ APP",
    fill="#000000",
    font=("Kadwa Regular", 24 * -1)
)

#main sign up reactangle
canvas.create_rectangle(
    196.0,
    118.0,
    736.0,
    530.0,
    fill="#AAC0F6",
    outline="")

#sign up header line
canvas.create_rectangle(
    220.0,
    186.0,
    703.0,
    187.0,
    fill="#000000",
    outline="")

canvas.create_text(
    #edited here
    467.0,
    160.0,
    anchor="center",
    text="Sign up",
    fill="#000000",
    font=("Kadwa Regular", 24 * -1)
)

#labels 
canvas.create_text(
    219.0,
    250.0,
    anchor="nw",
    text="Name ",
    fill="#000000",
    font=("Kadwa Regular", 24 * -1)
)

canvas.create_text(
    219.0,
    301.0,
    anchor="nw",
    text="Email",
    fill="#000000",
    font=("Kadwa Regular", 24 * -1)
)

canvas.create_text(
    219.0,
    349.0,
    anchor="nw",
    text="Role",
    fill="#000000",
    font=("Kadwa Regular", 24 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=check_entries,
    relief="flat"
)
button_1.place(
    x=371.0,
    y=418.0,
    width=171.0,
    height=46.0
)

login_button = Button(
    text = "login",
    fg="blue",
    borderwidth=0,
    highlightthickness=0,
    command=open_Login,
    relief="flat"
)
login_button.place(
    x=431.9814758300781,
    y=493.0,
    width=52.01852035522461,
    height=20.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    484.5,
    323.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#F5F5F5",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=375.0,
    y=310.0,
    width=219.0,
    height=25.0
)

#admin and student radiobutton
selected_role = StringVar(value="Student") #default value
radio_admin = Radiobutton(
    window,
    text = "Admin",
    variable = selected_role, #links radio button to variable
    value = "Admin", #value the radio button represents
    indicatoron = True
)

radio_student = Radiobutton(
    window,
    text = "Student",
    variable = selected_role,
    value = "Student",
    indicatoron = True
)

radio_admin.place(
    x=342.0,
    y=365.0,
    width=85.0,
    height=17.0
)

radio_student.place(
    x=485.0,
    y=365.0,
    width=85.0,
    height=18.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    358.0,
    323.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    356.0,
    266.0,
    image=image_image_3
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    484.5,
    265.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#F5F5F5",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=375.0,
    y=252.0,
    width=219.0,
    height=25.0
)
window.resizable(False, False)
window.mainloop()