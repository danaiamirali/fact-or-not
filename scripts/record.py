import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import sys

chunks = []
output_path = "output.wav"
sample_rate = 44100
chunk_duration = 1

def write_to_file(output_path, recording):
    # Concatenate the chunks
    recording = np.concatenate(chunks, axis=0)

    # Save the recording to the .wav file at the specified path
    write(output_path, sample_rate, recording)

    print(f"Recording saved to {output_path}.")

def main():
    global output_path
    global chunks

    # Check if command line argument was provided
    if len(sys.argv) < 2:
        print("Usage: python record.py <output_path>")
        sys.exit(1)

    # Get the output path from the command line arguments
    output_path = sys.argv[1]

    print("Recording started. Press Enter to stop the recording.")

    # Start recording in chunks
    with sd.InputStream(samplerate=sample_rate, channels=2) as stream:
        while True:
            # Record a chunk
            chunk = stream.read(int(sample_rate * chunk_duration))
            # Append the chunk to the list
            chunks.append(chunk[0])


try:
    main()
except KeyboardInterrupt:
    write_to_file(output_path, chunks)