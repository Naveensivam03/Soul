from vosk import Model, KaldiRecognizer
import pyaudio

# Load the Vosk speech recognition model
model = Model(r"./vosk-model-small-en-us-0.15")

# Create a recognizer with the model and sample rate
recognizer = KaldiRecognizer(model, 16000)

# Set up PyAudio to capture live microphone input
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16,      # 16-bit audio
                  channels=1,                  # mono
                  rate=16000,                  # 16kHz
                  input=True,                  # input stream
                  frames_per_buffer=8192)      # chunk size

# Start the audio stream
stream.start_stream()

# Continuous listening loop
while True:
    data = stream.read(4096)
    
    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        print(text[14:-3])  # Extract only the recognized text from the JSON string

