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

import argparse
import pathlib
from spectrogram import Spectrogram


def main() -> None:
    """
    Main function to create and save a spectrogram image from an audio file.

    This function initializes a Spectrogram object, loads an audio file,
    generates its spectrogram, and saves it as a PNG image.
    """

    parser = argparse.ArgumentParser(description="Batch spectrogram creator")
    parser.add_argument("path", type=str, help="Path to the file or directory")
    args = parser.parse_args()

    print(f"Received path: {args.path}")

    spectrogram = Spectrogram()
    path = pathlib.Path(args.path).resolve()

    file_list = []
    if path.is_file():
        file_list.append(path)
    elif path.is_dir():
        file_list = [
            p
            for p in path.rglob("*")
            if p.is_file() and p.suffix.lower() in (".m4a", ".mp3", ".flac", ".wav")
        ]

    print(f"Found {len(file_list)} files")

    for i, file in enumerate(file_list):
        print(f"Processing file ({i+1}/{len(file_list)}): {file}")
        spectrogram.create(file)
        spectrogram.save_png()


if __name__ == "__main__":
    main()
