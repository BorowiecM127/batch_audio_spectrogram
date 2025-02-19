"""
# spectrogram.py

This script processes an audio file to generate and display its spectrogram.
It utilizes the `librosa` library to load the audio file and compute its spectrogram.
The spectrogram is then converted to decibel units and visualized using `matplotlib`.
The x-axis of the spectrogram is formatted to display time in minutes and seconds.
"""

import librosa
import numpy as np
import matplotlib.pyplot as plt


class Spectrogram:
    """
    A class representing a spectrogram of an audio file.

    The Spectrogram class provides methods for loading an audio file, computing its spectrogram,
    and saving the spectrogram as a PNG image. The class also provides private helper methods
    for customizing the spectrogram plot.

    Attributes:
        audio_file (str): The path to the audio file.
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
        self.audio_file: str = ""
        self.audio: np.ndarray = np.array([])
        self.sampling_rate: int | float = 0
        self.spectrogram: np.ndarray = np.array([])
        self.db_spectrogram: np.ndarray = np.array([])

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
        self.audio, self.sampling_rate = librosa.load(audio_file, sr=None)
        self.spectrogram = librosa.stft(self.audio)
        self.db_spectrogram = librosa.amplitude_to_db(abs(self.spectrogram), ref=np.max)

    def save_png(self, filename: str = "") -> None:
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

        self.__set_titles__()
        self.__set_x_axis__()
        self.__set_y_axis__()
        self.__set_graphics__()

        plt.savefig(
            filename
            if filename != ""
            else f"{self.audio_file.replace('.', '_')}_spectrogram.png"
        )
        plt.clf()

    def __set_x_axis__(self) -> None:
        """
        Set the x-axis for the spectrogram plot.

        This function uses the `plt.xticks` function to set the x-axis tick marks
        and labels. The tick marks are spaced every 60 seconds, and the labels
        are formatted as the time in minutes and seconds. The `plt.xlim` function
        is used to ensure the x-axis extends from 0 seconds to the total duration
        of the audio file.
        """

        plt.xticks(
            np.arange(0, len(self.audio) / self.sampling_rate, 60).tolist()
            + [len(self.audio) / self.sampling_rate],
            [
                f"{int(t/60):02d}:{int(t%60):02d}"
                for t in np.arange(0, len(self.audio) / self.sampling_rate, 60).tolist()
                + [len(self.audio) / self.sampling_rate]
            ],
        )

    def __set_y_axis__(self) -> None:
        """
        Set the y-axis for the spectrogram plot.

        This function uses the `plt.yticks` function to set the y-axis tick marks
        and labels. The tick marks are spaced every 5000 Hz, and the labels are
        formatted as the frequency value in Hz. The `plt.ylim` function is used
        to ensure the y-axis extends from 0 Hz to the Nyquist frequency.
        """
        plt.yticks(
            np.arange(0, self.sampling_rate / 2, 5000).tolist()
            + [self.sampling_rate / 2],
            [f"{f:.0f}" for f in np.arange(0, self.sampling_rate / 2000, 5)]
            + [str(int(self.sampling_rate / 2000))],
        )
        plt.ylim(0, self.sampling_rate / 2)

    def __set_graphics__(self) -> None:
        """
        Set the graphics for the spectrogram plot.

        This function uses the `plt.imshow` function to display the spectrogram
        as an image. The `origin="lower"` argument is used to ensure the origin
        of the image is at the lower left corner of the plot. The `cmap="inferno"`
        argument is used to select the color map, and the `aspect="auto"` argument
        is used to ensure the aspect ratio of the image is automatically determined.
        The `extent` argument is used to specify the extent of the image in data
        coordinates. Finally, the `plt.colorbar` function is used to add a color bar
        to the plot, with the format of the color bar labels specified as "%+2.0f dB".
        """
        plt.imshow(
            self.db_spectrogram,
            origin="lower",
            cmap="inferno",
            aspect="auto",
            extent=(0, len(self.audio) / self.sampling_rate, 0, self.sampling_rate / 2),
        )
        plt.colorbar(format="%+2.0f dB")

    def __set_titles__(self) -> None:
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
        plt.xlabel("Time")
        plt.ylabel("Frequency (kHz)")
        plt.suptitle(f"'{self.audio_file}' spectrogram")
        plt.title(
            f"Encoding: {1}, Bitrate: {2}, Sampling Rate: {3}, Channels: {4}",
            fontsize=10,
        )
