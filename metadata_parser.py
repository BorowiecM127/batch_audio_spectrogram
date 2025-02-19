"""
Metadata parsing module for audio files.

This module provides a class, `MetadataParser`,
for parsing metadata from audio files using FFmpeg's ffprobe command.
It can extract metadata such as codec, sample rate, bitrate, duration, and channel layout.

Classes:
    MetadataParser: A class for parsing metadata from audio files.

Functions:
    None

Exceptions:
    None

Variables:
    None

Notes:
    This module requires FFmpeg to be installed and available in the system's PATH.
"""

import json
from ffmpeg import FFmpeg


class MetadataParser:
    """
    A class for parsing metadata from audio files.

    The MetadataParser class provides methods for retrieving metadata from audio files
    using FFmpeg's ffprobe command.
    It can extract metadata such as codec, sample rate, bitrate, duration, and channel layout.

    Attributes:
        None

    Methods:
        get_metadata(audio_file):
            Retrieves metadata from an audio file using FFmpeg's ffprobe command.
    """

    def get_metadata(self, audio_file) -> str:
        """
        Retrieves metadata from an audio file using FFmpeg's ffprobe command.

        Parameters
        ----------
        audio_file : str
            The path to the audio file.

        Returns
        -------
        str
            A string containing needed metadata

        """
        ffprobe = FFmpeg(executable="ffprobe").input(
            audio_file,
            print_format="json",
            show_streams=None,
        )

        media = json.loads(ffprobe.execute())
        return self.__build_file_metadata__(media)

    def __build_file_metadata__(self, json_file: dict) -> str:
        """
        Builds a string containing the metadata of an audio file.

        Parameters
        ----------
        json_file : dict
            A dictionary containing the metadata of the audio file.

        Returns
        -------
        str
            A string containing the metadata of the audio file.

        """
        media_info = json_file["streams"][0]
        return (
            str(media_info.get("codec_long_name", None))
            + ", "
            + self.__get_bitrate_or_bits_per_sample(media_info)
            + ", "
            + str(media_info.get("channel_layout", None))
            + ", "
            + str(media_info.get("sample_rate", None))
            + " Hz"
            + ", "
            + self.__get_duration(media_info)
        )

    def __get_bitrate_or_bits_per_sample(self, media_info: dict) -> str:
        """
        Returns either the bitrate or bits per sample of an audio file.

        Parameters
        ----------
        media_info : dict
            A dictionary containing the metadata of the audio file.

        Returns
        -------
        str
            A string containing either the bitrate in kb/s or bits per sample

        """
        if "bit_rate" in media_info:
            return str(int(media_info["bit_rate"]) / 1000) + " kb/s"
        return str(media_info.get("bits_per_raw_sample", None)) + " bit"

    def __get_duration(self, media_info: dict) -> str:
        """
        Returns the duration of an audio file in mm:ss format.

        Parameters
        ----------
        media_info : dict
            A dictionary containing the metadata of the audio file.

        Returns
        -------
        str
            A string containing the duration of the audio file in mm:ss format.
        """

        return (
            str(int(float(media_info.get("duration", 0)) // 60))
            + ":"
            + str(int(float(media_info.get("duration", 0)) % 60))
        )
