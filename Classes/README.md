# READ Project

## Overview

READ is an open-source platform designed to improve reading proficiency for young learners with low literacy skills. The system provides feedback on pronunciation accuracy, identifies mispronounced words, and tracks reading progress for each learner.

## Main Features

- **Speech Processing:** The system listens to the user's speech and compares it to the correct pronunciation of words.
- **Phoneme Matching:** It breaks down words into phonemes and analyzes speech for accuracy.
- **Reading Progress Tracking:** User reading speed and accuracy are stored in a database for continuous monitoring and improvement.

## Getting Started

### 1. System Requirements

- A computer with Python
- Windows 10 or 11
- Visual Studio Code

### 2. Setup

Install the following libraries using these commands in a terminal:

```
pip install Pillow
pip install transformers
pip install transformers phonemizer librosa torch
pip install pyaudio
pip install wave
pip install fastdtw
pip install Levenshtein
pip install pathlib
pip install pyttsx3
```

### 3. Install eSpeak

- Download and install eSpeak, a text-to-speech engine required for phoneme analysis.
- Ensure that eSpeak is added to your system's PATH environment variable so that it can be accessed globally.

### 4. Configuring System Variables (Windows)

1. Open **Control Panel** > **System and Security** > **System** > **Advanced System Settings**.
2. Under **Environment Variables**, locate **Path** under System Variables.
3. Click **Edit**, then **New**, and add the path to the eSpeak installation directory (e.g., C:\Program Files\eSpeak\).
4. Click **OK** to save the changes.

### 5. Configure Audio Input

- Use a microphone for recording speech.
- Ensure that the audio quality is clear, with minimal background noise.

## How to Use READ

1. **Start the Program:**
   - Go to the classes folder and run the sign-up class of the READ project to initialize the system.

2. **Sign Up and Sign In:**
   - Enter your sign-up details, then sign in.

3. **Choosing a Story:**
   - The user is prompted to select a story from the available list or is recommended a story.
   - The system displays one sentence at a time for the user to read aloud.

4. **Reading & Feedback:**
   - **Pronunciation Feedback:**
     - After reading, the system analyzes speech.
     - Mispronounced words will be highlighted and feedback will be shown.
     - Please note the system will take a few seconds to calculate and provide feedback.
   - **Phoneme Comparison:**
     - The system uses phoneme analysis to detect mispronunciations.
     - The phonemes of the mispronounced words will be displayed at the bottom and highlighted in green.
     - Press audio for correct word pronunciation.

5. **Tracking Progress:**
   - Each session is recorded with details such as:
     - Reading speed (in words per minute).
     - Accuracy (percentage of correctly pronounced words).
   - Users can review their accuracy after each reading session.

GitLab Link https://gitlab.cs.uct.ac.za/csc3003s/read.git
