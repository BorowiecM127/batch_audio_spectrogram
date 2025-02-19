"""
# main.py

This script processes an audio file to generate and display its spectrogram.
It utilizes the `librosa` library to load the audio file and compute its spectrogram.
The spectrogram is then converted to decibel units and visualized using `matplotlib`.
The x-axis of the spectrogram is formatted to display time in minutes and seconds.
"""

import librosa
import numpy as np
import matplotlib.pyplot as plt

TRACK_NAME = "voice.flac"

# Load the m4a file
audio, sampling_rate = librosa.load("voice.flac", sr=None)

# Compute the spectrogram
spectrogram = librosa.stft(audio)

# Display the spectrogram
db_spectrogram = librosa.amplitude_to_db(abs(spectrogram), ref=np.max)
plt.figure(figsize=(14, 7))
plt.imshow(
    db_spectrogram,
    origin="lower",
    cmap="inferno",
    aspect="auto",
    extent=(0, len(audio) / sampling_rate, 0, sampling_rate / 2),
)

# Format the x-axis to show time in minutes and seconds
plt.xlabel("Time")
plt.xticks(
    np.arange(0, len(audio) / sampling_rate, 60).tolist()
    + [len(audio) / sampling_rate],
    [
        f"{int(t/60):02d}:{int(t%60):02d}"
        for t in np.arange(0, len(audio) / sampling_rate, 60).tolist()
        + [len(audio) / sampling_rate]
    ],
)

# Format the y-axis to show frequency and limit it to the Nyquist frequency
plt.ylabel("Frequency (kHz)")
plt.yticks(
    np.arange(0, sampling_rate / 2, 5000).tolist() + [sampling_rate / 2],
    [f"{f:.0f}" for f in np.arange(0, sampling_rate / 2000, 5)]
    + [str(int(sampling_rate / 2000))],
)
plt.ylim(0, sampling_rate / 2)

plt.colorbar(format="%+2.0f dB")
plt.suptitle(f"{TRACK_NAME} spectrogram")
plt.title(
    f"Encoding: {1}, Bitrate: {2}, Sampling Rate: {3}, Channels: {4}", fontsize=10
)
plt.savefig("spectrogram.png")
