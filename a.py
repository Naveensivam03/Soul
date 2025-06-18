import whisper
import pyaudio
import numpy as np
import wave
import tempfile
import os
import time

# Load Whisper model
model = whisper.load_model("tiny")

# Audio config
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
SILENCE_THRESHOLD = 500  # Adjust based on your mic
MAX_SILENCE_SECONDS = 5

# Setup audio stream
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Listening... (Ctrl+C to stop)")

# For storing transcriptions
transcriptions = []

try:
    while True:
        frames = []
        silent_chunks = 0
        speaking = False
        start_time = time.time()

        print("Waiting for speech...")

        while True:
            data = stream.read(CHUNK)
            frames.append(data)

            # Convert to numpy array to check volume
            audio_data = np.frombuffer(data, dtype=np.int16)
            volume = np.abs(audio_data).mean()

            if volume > SILENCE_THRESHOLD:
                speaking = True
                silent_chunks = 0
            elif speaking:
                silent_chunks += 1

            # Stop after 5 seconds of silence
            if speaking and silent_chunks > (RATE / CHUNK * MAX_SILENCE_SECONDS):
                break

        # Save to temp WAV
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            wf = wave.open(tmpfile.name, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            # Transcribe
            result = model.transcribe(tmpfile.name)
            print("You said:", result["text"])
            transcriptions.append(result["text"])

            os.unlink(tmpfile.name)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("\nFull Transcript:")
    for i, t in enumerate(transcriptions):
        print(f"{i+1}: {t}")
