import os
import warnings
import logging
import transformers
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
from phonemizer import phonemize
import librosa
import pyaudio
import wave
from threading import Thread
import string
import difflib
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
from speechTest import improved_phoneme_comparison,provide_feedback

# Suppress unnecessary logs and warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
warnings.filterwarnings("ignore")
transformers.logging.set_verbosity_error()
logging.basicConfig(level=logging.CRITICAL)


class Audio:
    """
    A class for handling audio recording, transcription, and phoneme comparison.

    This class provides functionality to record audio, transcribe it using a pre-trained
    model, and compare the transcription with expected text using phoneme-based analysis.
    """
    def __init__(self, output_filename="Recorded.wav", format=pyaudio.paInt16, channels=2, rate=44100, chunk=1024, on_stop_callback=None):
        """
        Initialize the Audio class.

        Args:
            output_filename (str): Name of the output audio file.
            format (int): Audio format (default: pyaudio.paInt16).
            channels (int): Number of audio channels (default: 2).
            rate (int): Sample rate (default: 44100).
            chunk (int): Buffer size (default: 1024).
            on_stop_callback (function): Callback function when recording stops.
        """
        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate
        self.output_filename = os.path.join(os.path.dirname(__file__), output_filename)
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False
        self.on_stop_callback = on_stop_callback 

        # Load the pre-trained model and processor
        self.model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft")
        self.processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-xlsr-53-espeak-cv-ft")

    def start_recording(self):
        """Start audio recording."""
        self.frames = []
        self.is_recording = True

        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunk)

        def record():
            while self.is_recording:
                data = self.stream.read(self.chunk)
                self.frames.append(data)

        Thread(target=record).start()
        print("Recording started...")

    def stop_recording(self):
        """
        Stop audio recording and process the recorded audio.

        Returns:
            str: The transcription of the recorded audio.
        """
        self.is_recording = False
        self.stream.stop_stream()
        self.stream.close()

        wf = wave.open(self.output_filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print("Recording stopped and saved to", self.output_filename)

        transcription = self.process_recording()
        return transcription 

    def process_recording(self):
        """
        Process the recorded audio file and generate a transcription.

        Returns:
            str: The transcription of the audio.
        """
        audio, rate = librosa.load(self.output_filename, sr=16000)
        input_values = self.processor(audio, return_tensors="pt", sampling_rate=16000).input_values
        logits = self.model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.decode(predicted_ids[0])

        return transcription

    def expected_phonemes(self, expected_text):
        """
        Generate phonemes for the expected text.

        Args:
            expected_text (str): The expected text.

        Returns:
            str: The phoneme representation of the expected text.
        """
        expected_phonemes = phonemize(expected_text, language='en-us', backend='espeak', strip=True, preserve_punctuation=False, with_stress=False)
        return expected_phonemes

    def improved_compare_phonemes(self, expected_text, recorded_phonemes):
        """
        Compare the expected text with the recorded phonemes.

        Args:
            expected_text (str): The expected text.
            recorded_phonemes (str): The phonemes from the recorded audio.

        Returns:
            list: A list of tuples containing words and their similarity scores.
        """
        word_scores = improved_phoneme_comparison(expected_text, recorded_phonemes)
        feedback= provide_feedback(word_scores, expected_text, threshold=0.6)
        return word_scores

    def highlight_incorrect_words(self, expected_text, discrepancies):
        """
        Highlight incorrect words in the expected text.

        Args:
            expected_text (str): The expected text.
            discrepancies (list): A list of tuples containing indices of incorrect words.

        Returns:
            str: The expected text with incorrect words highlighted.
        """
        words = expected_text.split()
        highlighted_text = ""
        discrepancy_index = 0

        for i, word in enumerate(words):
            if discrepancy_index < len(discrepancies) and discrepancies[discrepancy_index][0] == i:
                # This word has a discrepancy
                highlighted_text += f"{{incorrect}}{word}{{/incorrect}} "
                discrepancy_index += 1
            else:
                # This word is correct
                highlighted_text += word + " "

        return highlighted_text.strip()

    def __del__(self):
        """Cleanup method to terminate PyAudio."""
        self.p.terminate()
