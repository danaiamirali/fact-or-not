import soundcard as sc
import soundfile as sf

# Get the specific audio input device
device = sc.get_microphone("BlackHole")

# Record audio for 5 seconds
duration = 5  # seconds
audio_data = device.record(samplerate=44100, numframes=duration * 44100)

# Save the recorded audio to a WAV file
output_file = "output.wav"
sf.write(output_file, audio_data, samplerate=44100)

print(f"Recording saved to {output_file}.")
