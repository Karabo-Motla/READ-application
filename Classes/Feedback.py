import tkinter as tk
from tkinter import Canvas, Button, PhotoImage, Toplevel, messagebox,Text
from pathlib import Path
from SharedData import SharedData
from StoryDatabaseManager import StoryDatabaseManager
from PIL import Image, ImageTk
import pyttsx3
from audio import Audio
from SharedData import SharedData

class Feedback:
    """
    A class representing the feedback window for a reading session.

    This class manages the user interface and functionality for providing
    feedback on the user's reading performance, including word accuracy
    and phoneme display.

    Class Attributes:
        accuracy (float): The overall accuracy of the reading session.
        total_correct_words (int): The total number of correctly read words.
        total_expected_words (int): The total number of words expected to be read.
    """

    accuracy = 0
    total_correct_words = 0
    total_expected_words = 0

    def __init__(self, transcription, expected_text,reading_session,master=None):
        """
        Initialize the Feedback instance.

        Args:
            transcription (str): The transcribed text from the user's reading.
            expected_text (str): The expected text that should have been read.
            reading_session (ReadingSession): The associated reading session.
            master (tk.Tk, optional): The master window. Defaults to None.
        """
        self.master = master if master else tk.Tk()
        self.window = Toplevel()
        self.expected_words = ""
        self.master.protocol("WM_DELETE_WINDOW", self.hide_window)  # Handle window close event
        self.master.geometry("934x575")
        self.master.configure(bg="#FFFFFF")
        self.reading_session = reading_session
        self.text_speech = pyttsx3.init()
        self.audio = Audio()
        self.setup_ui()
        self.create_buttons()
        self.update_content(transcription, expected_text)
        self.populate_highlighted_text()
        self.show_feedback()
    
    def setup_ui(self):
        """Set up the user interface elements."""
        self.canvas = Canvas(
            self.master,
            bg="#CFDBF7",
            height=575,
            width=934,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.create_main_section()
        self.master.resizable(False, False)

    def create_main_section(self):
        """Create the main section of the feedback window."""
        self.canvas.create_text(467.0, 80.0, anchor="center", text="Feedback", fill="#000000", font=("Kadwa Regular", 48 * -1))
        self.highlighted_text = Text(self.master, bg="#CFDBF7", font=("Inter Bold", 20), wrap="word", height=5, width=55)
        self.highlighted_text.place(x=61.0, y=120.0)
        self.highlighted_text.config(state=tk.DISABLED)
        self.phoneme_text = Text(self.master, bg="#CFDBF7", font=("Inter Bold", 20), wrap="word", height=5, width=55)
        self.phoneme_text.place(x=61.0, y=300.0)
 
    def create_buttons(self):
        """Create and place buttons on the interface.""" 
        self.play_audio_button= tk.Button(
            self.master,
            text="play audio",
            font="Kadwa 12 bold",
            fg="black",
            command =self.read_phonemes,
            relief="raised",
            borderwidth=0,
            bd=3,
            highlightthickness=0
        )
        self.play_audio_button.place(x=411, y=501, width=120, height=40)

        self.next_word_button = tk.Button(
            self.master,
            text="Next word",
            font="Kadwa 12 bold",
            fg="black",
            command=self.show_next_phoneme,
            borderwidth=0,
            bd=3,
            highlightthickness=0,
            relief="raised"
        )
        self.next_word_button.place(x=100, y=501, width=120, height=40)
      
        self.continue_button = tk.Button(
            self.master,
            text="Continue reading",
            font="Kadwa 12 bold",
            fg="black",
            command=self.back_to_reading,
            borderwidth=0,
            bd=3,
            highlightthickness=0,
            relief="raised",
        )
        self.continue_button.place(x=705, y=501, width=150, height=40)
   
    
    def relative_to_assets(self, path: str) -> Path:
        """
        Get the relative path to asset files.

        Args:
            path (str): The file name.

        Returns:
            Path: The full path to the asset file.
        """
        return Path(__file__).parent / "assets" / "frame8" / path 
    
    def hide_window(self):
        """Hide the feedback window."""
        self.master.withdraw()
        
    def read_phonemes(self):
        """Read the current word's phonemes using text-to-speech."""
        if self.current_word:
            phonemes = self.current_word
            self.text_speech.say(phonemes)
            self.text_speech.runAndWait()
        else:
            print("No current word to show phonemes for.")  

    def show_feedback(self):
        """Display feedback by highlighting words based on their accuracy scores."""
        self.highlighted_text.config(state="normal")
        self.highlighted_text.delete(1.0, "end")
        self.word_tags = []  # Reset word tags

        for i, (word, score) in enumerate(self.word_scores):
            self.highlighted_text.insert("end", word + " ")
            start_idx = self.highlighted_text.index(f"insert - {len(word) + 1}c")
            end_idx = self.highlighted_text.index("insert")

            tag_name = f"word_{i}"
            self.highlighted_text.tag_add(tag_name, start_idx, end_idx)
            self.word_tags.append(tag_name)

            if score < 0.6 or i >= len(self.word_scores) - 1:  # Treat last word as incorrect if it was cut off
                self.highlighted_text.tag_configure(tag_name, foreground="red")
            else:
                self.highlighted_text.tag_configure(tag_name, foreground="black")
                self.total_correct_words += 1

        self.highlighted_text.config(state="disabled")

    def show_next_phoneme(self):
        """Display the next incorrect word's phonemes."""
        self.highlighted_text.config(state="normal")
        self.phoneme_text.config(state="normal")

        if hasattr(self, 'current_tag'):
            self.highlighted_text.tag_configure(self.current_tag, background="")

        self.current_phoneme_index += 1

        while self.current_phoneme_index < len(self.word_scores): 
            self.current_word, score = self.word_scores[self.current_phoneme_index]
            
            
            if score < 0.6 or self.current_phoneme_index == len(self.word_scores) - 1:
                current_phonemes = self.audio.expected_phonemes(self.current_word)
                self.phoneme_text.delete(1.0, "end")
                self.phoneme_text.insert("end", f"{current_phonemes}")
                
                # Highlight phoneme text in green
                self.phoneme_text.tag_add("phoneme", "1.0", "end")
                self.phoneme_text.tag_configure("phoneme", foreground="green")

                # Highlight the current word in highlighted_text
                self.current_tag = self.word_tags[self.current_phoneme_index]
                self.highlighted_text.tag_configure(self.current_tag, background="lightgreen")
                
                # Scroll to make the highlighted word visible
                self.highlighted_text.see(self.current_tag + ".first")
                
                break
            self.current_phoneme_index += 1

        if self.current_phoneme_index >= len(self.word_scores):
            self.next_word_button.config(state="disabled")
            self.phoneme_text.delete(1.0, "end")
            self.phoneme_text.insert("end", "No more words to display.")

        self.highlighted_text.config(state="disabled")
        self.phoneme_text.config(state="disabled")

    def populate_highlighted_text(self):
        """Populate the highlighted text area with words colored based on their scores."""
        self.highlighted_text.config(state="normal")
        self.highlighted_text.delete(1.0, "end")
        for word, score in self.word_scores:
            self.highlighted_text.insert("end", word + " ")
            if score < 0.8:
                start = self.highlighted_text.index(f"end-{len(word)+1}c")
                end = self.highlighted_text.index("end-1c")
                self.highlighted_text.tag_add("incorrect", start, end)
        self.highlighted_text.tag_configure("incorrect", foreground="red")
        self.highlighted_text.config(state="disabled")

    def update_content(self, transcription, expected_text):
        """
        Update the feedback content with new transcription and expected text.

        Args:
            transcription (str): The transcribed text from the user's reading.
            expected_text (str): The expected text that should have been read.
        """
        self.transcription = transcription
        self.expected_text = expected_text
        self.expected_phonemes_list = self.audio.expected_phonemes(self.expected_text)
        self.word_scores = self.audio.improved_compare_phonemes(self.expected_text, self.transcription)
        
        expected_words = self.expected_text.split()
        if len(self.word_scores) < len(expected_words):
            for i in range(len(self.word_scores), len(expected_words)):
                self.word_scores.append((expected_words[i], 0.0))  # Treat cut-off words as incorrect
        
        for word, score in self.word_scores:
            if score >= 0.6:  
                Feedback.total_correct_words += 1
        Feedback.total_expected_words += len(expected_words)

        self.current_phoneme_index = -1
        self.current_word = None
        self.word_tags = []
        if hasattr(self, 'next_word_button'):
            self.next_word_button.config(state="normal")
        if hasattr(self, 'highlighted_text'):
            self.populate_highlighted_text()
            self.show_feedback()
            self.show_next_phoneme()
        
    @classmethod
    def calculate_accuracy(cls):
        """Calculate the overall accuracy of the reading session."""
        print("total_correct_words:",cls.total_correct_words)
        print("total_expected_words:",cls.total_expected_words)
        
        if cls.total_expected_words > 0:
            cls.accuracy = (cls.total_correct_words / cls.total_expected_words) * 100
        else:
            cls.accuracy = 0
        return cls.accuracy  
    
    @classmethod
    def get_accuracy(cls):
        """Get the calculated accuracy of the reading session."""
        if SharedData.get_session_status() == False:  
            cls.calculate_accuracy()
        return cls.accuracy
    
    def show(self):
        """Show the feedback window."""
        self.master.deiconify() 

    def hide_window(self):
        """Hide the feedback window and show the reading session window."""
        self.master.withdraw()  
        self.reading_session.show()  

    def back_to_reading(self):
        """Return to the reading session."""
        self.hide_window()
    
    def is_alive(self):
        """Check if the feedback window still exists."""
        try:
            return self.window.winfo_exists()
        except tk.TclError:
            return False

def main():
    """Main function to run the Feedback application."""
    root = tk.Tk()
    app = Feedback(root)
    root.mainloop()
    

# If this script is the main module, start the application
if __name__ == "__main__":
    main()
