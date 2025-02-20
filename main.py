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


def get_file_list_from_path(path: pathlib.Path) -> list[pathlib.Path]:
    """
    Given a path to either a file or directory, return a list of file paths.

    If the path is a file, the list will contain only the resolved path of the file.
    If the path is a directory, the list will contain the resolved paths of all files
    in the directory.

    Parameters
    ----------
    path : pathlib.Path
        The path to the file or directory.

    Returns
    -------
    list[pathlib.Path]
        A list of file paths.
    """
    file_list = []
    if path.is_file():
        file_list.append(path.resolve())
    elif path.is_dir():
        for file in path.iterdir():
            if file.is_file():
                file_list.append(file.resolve())

    return file_list


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
    file_list = get_file_list_from_path(path)

    for file in file_list:
        if file.suffix.lower() in (".m4a", ".mp3", ".flac", ".wav"):
            print(f"Processing file: {file}")
            spectrogram.create(file)
            spectrogram.save_png()


if __name__ == "__main__":
    main()
