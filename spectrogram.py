"""
# spectrogram.py

This script processes an audio file to generate and display its spectrogram.
It utilizes the `librosa` library to load the audio file and compute its spectrogram.
The spectrogram is then converted to decibel units and visualized using `matplotlib`.
The x-axis of the spectrogram is formatted to display time in minutes and seconds.
"""

import pathlib
import warnings
import librosa
import numpy as np
import matplotlib.pyplot as plt
from metadata_parser import MetadataParser

warnings.filterwarnings("ignore", category=RuntimeWarning)


class Spectrogram:
    """
    A class representing a spectrogram of an audio file.

    The Spectrogram class provides methods for loading an audio file, computing its spectrogram,
    and saving the spectrogram as a PNG image. The class also provides private helper methods
    for customizing the spectrogram plot.

    Attributes:
        audio_file (pathlib.Path): The path to the audio file.
        audio (np.ndarray): The audio data.
        sampling_rate (int): The sampling rate of the audio data.
        spectrogram (np.ndarray): The spectrogram of the audio data.
        db_spectrogram (np.ndarray): The spectrogram in decibel units.

    Methods:
        create(audio_file): Loads an audio file and computes its spectrogram.
        save_png(filename): Saves the spectrogram plot as a PNG image.
    """

    def __init__(self) -> None:
        """
        Initialize the Spectrogram object with empty data.

        This method initializes the Spectrogram object with empty data. It sets
        the audio file path to an empty string, and initializes the audio data,
        sampling rate, spectrogram, and decibel spectrogram as empty numpy arrays.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.audio_file: pathlib.Path = pathlib.Path()
        self.audio: np.ndarray = np.array([])
        self.sampling_rate: int | float = 0
        self.spectrogram: np.ndarray = np.array([])
        self.db_spectrogram: np.ndarray = np.array([])
        self.metadata_parser = MetadataParser()

    def create(self, audio_file) -> None:
        """
        Load an audio file and compute its spectrogram.

        This function sets the audio file path, loads the audio data and its sampling
        rate using `librosa`, computes the short-time Fourier transform (STFT) of the
        audio data, and converts the spectrogram to decibel units.

        Parameters
        ----------
        audio_file : str
            The path to the audio file to be processed.

        Returns
        -------
        None
        """
        self.audio_file = audio_file
        self.audio, self.sampling_rate = librosa.load(str(self.audio_file), sr=None)

    def save_png(self) -> None:
        """
        Saves the spectrogram plot as a PNG image.

        Parameters
        ----------
        filename : str, optional
            The filename to save the image as. If not provided, the filename
            will be the name of the audio file with "_spectrogram" appended to
            it and ".png" as the file extension.

        Returns
        -------
        None
        """
        plt.figure(figsize=(14, 7))

        self.__set_titles()
        self.__set_x_axis()
        self.__set_y_axis()
        self.__set_graphics()

        plt.savefig(
            str(self.audio_file.parent / self.audio_file.stem)
            + "_"
            + self.audio_file.suffix[1:]
            + "_spectrogram.png"
        )
        plt.close()

    def __set_x_axis(self) -> None:
        """
        Set the x-axis for the spectrogram plot.

        This function uses the `plt.xticks` function to set the x-axis tick marks
        and labels. The tick marks are spaced every 60 seconds, and the labels
        are formatted as the time in minutes and seconds. The `plt.xlim` function
        is used to ensure the x-axis extends from 0 seconds to the total duration
        of the audio file.
        """
        audio_duration_sec = len(self.audio) / self.sampling_rate
        ticks = np.linspace(0, audio_duration_sec, num=15).tolist()
        labels = [f"{int(t/60):02d}:{int(t%60):02d}" for t in ticks]
        plt.xticks(ticks, labels)

    def __set_y_axis(self) -> None:
        """
        Set the y-axis for the spectrogram plot.

        This function uses the `plt.yticks` function to set the y-axis tick marks
        and labels. The tick marks are spaced every 5000 Hz, and the labels are
        formatted as the frequency value in Hz. The `plt.ylim` function is used
        to ensure the y-axis extends from 0 Hz to the Nyquist frequency.
        """
        nyquist_frequency = round(self.sampling_rate / 2, -3)
        ticks = np.linspace(0, nyquist_frequency, num=12).tolist()
        labels = [f"{t / 1000:.0f}" for t in ticks]
        plt.yticks(ticks, labels)

    def __set_graphics(self) -> None:
        """
        Set graphics for the spectrogram plot.

        This function sets the graphics for the spectrogram plot, including the
        colormap, aspect ratio, and extent of the plot. It also adds a colorbar
        with a format string of "%+2.0f dB" and uses the `plt.tight_layout` function
        to ensure the plot is correctly sized.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        plt.specgram(
            self.audio,
            Fs=self.sampling_rate,
            cmap="inferno",
            vmin=-120,
            vmax=0,
            NFFT=4096,
            mode="magnitude",
            scale="dB",
        )
        plt.colorbar(format="%+2.0f dB")
        plt.tight_layout(w_pad=0.5)

    def __set_titles(self) -> None:
        """
        Set titles for the spectrogram plot.

        This function sets the x and y axis labels, the title, and the subtitle
        of the spectrogram plot.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        plt.xlabel("Time (mm:ss)")
        plt.ylabel("Frequency (kHz)")
        plt.suptitle(f"'{self.audio_file.name}' spectrogram")
        plt.title(
            self.metadata_parser.get_metadata(self.audio_file),
            fontsize=10,
        )
