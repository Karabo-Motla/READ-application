import pyaudio
import wave
from threading import Thread
import os

class Audio:
    def __init__(self, output_filename="Recorded.wav", format=pyaudio.paInt16, channels=2, rate=44100, chunk=1024):
        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate
        # Save the file in the same directory as the script
        self.output_filename = os.path.join(os.path.dirname(__file__), output_filename)
        #self.output_filename = output_filename
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False

    def start_recording(self):
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

    def __del__(self):
        self.p.terminate()
