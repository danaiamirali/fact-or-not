import soundcard as sc

# List all available audio devices
devices = sc.all_speakers()
print("Available audio devices:")
for i, device in enumerate(devices):
    print(device)
