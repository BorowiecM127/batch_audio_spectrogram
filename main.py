"""
Main entry point for the spectrogram generation application.

This script demonstrates how to use the `Spectrogram` class to load an audio file,
compute its spectrogram, and save the spectrogram as a PNG image.

Usage:
    python main.py <audio_file> [<output_file>]

Arguments:
    audio_file (str): The path to the audio file.
    output_file (str, optional): The filename to save the spectrogram image as.
        If not provided, the filename will be the name of the audio file with
        "_spectrogram" appended to it and ".png" as the file extension.
"""

from spectrogram import Spectrogram


def main() -> None:
    """
    Main function to create and save a spectrogram image from an audio file.

    This function initializes a Spectrogram object, loads an audio file,
    generates its spectrogram, and saves it as a PNG image.
    """

    spectrogram = Spectrogram()
    spectrogram.create("voice.flac")
    spectrogram.save_png()


if __name__ == "__main__":
    main()
