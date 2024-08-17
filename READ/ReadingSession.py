# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

import tkinter as tk
import sys
from pathlib import Path
from tkinter import Canvas, Button, PhotoImage, Text
import re

#import audio recorder
from audio import Audio

# Paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\\frame2")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def display_story_line_by_line(story_text, line_number=0):
    # Split the story text into sentences
    sentences = re.split(r'(?<=[.!?]) +', story_text)  # Split at .!? followed by space

    if line_number >= len(sentences):
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, "end")
        text_widget.insert("end", "Well done. You have completed the story")
        text_widget.config(state=tk.DISABLED)
        return  # Stop if there are no more sentences to display

    current_sentence = sentences[line_number]

    # Temporarily enable the Text widget, clear it, insert the new sentence, then disable it again
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, "end")
    text_widget.insert("end", current_sentence)
    text_widget.config(state=tk.DISABLED)

    # Update the "Next" button to show the next sentence
    button_next.config(command=lambda: display_story_line_by_line(story_text, line_number + 1))

# Initialize the Tkinter window
window = tk.Tk()
window.geometry("934x575")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=575,
    width=934,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    0.0,
    0.0,
    934.0,
    575.0,
    fill="#F8BABA",
    outline=""
)

canvas.create_rectangle(
    167.0,
    41.0,
    775.0,
    109.0,
    fill="#C4D1EC",
    outline=""
)

canvas.create_text(
    455.0,
    75.0,
    anchor="center",
    text="Story Title",
    fill="#000000",
    font=("Inter Medium", 40 * -1)
)

canvas.create_rectangle(
    20.0,
    142.0,
    922.0,
    348.0,
    fill="#F8BABA",
    outline=""
)

# Create a Text widget to display the current sentence of the story
text_widget = Text(window, bg="#F8BABA", font=("Inter Bold", 20), wrap="word", height=4, width=55)
text_widget.place(x=61.0, y=185.0)
text_widget.config(state=tk.DISABLED)

# Load button images and create buttons
button_image_next = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_next = Button(
    image=button_image_next,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Next button clicked"),
    relief="flat"
)

button_next.place(
    x=350.0,
    y=370.0,
    width=211.0,
    height=39.0
)

recorder = Audio()

button_image_close = PhotoImage(
    file=relative_to_assets("button_2.png"))
start_button = Button(
    image=button_image_close,
    borderwidth=0,
    highlightthickness=0,
    command=recorder.start_recording,  #start recording
    relief="flat"
)
start_button.place(
    x=150.0,
    y=454.0,
    width=174.0,
    height=51.0
)

button_image_close_alt = PhotoImage(
    file=relative_to_assets("button_3.png"))
end_button = Button(
    image=button_image_close_alt,
    borderwidth=0,
    highlightthickness=0,
    command=recorder.stop_recording,  #stop recording
    relief="flat"
)
end_button.place(
    x=580.0,
    y=454.0,
    width=174.0,
    height=51.0
)

# Load the story text from command line arguments
story_text = sys.argv[1] if len(sys.argv) > 1 else "No story provided."


# Start displaying the story line by line
display_story_line_by_line(story_text)

window.resizable(False, False)
window.mainloop()