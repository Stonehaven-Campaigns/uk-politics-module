"""Functions for importing data."""
import os
import csv
from typing import Dict, Tuple
import pandas as pd

from . import exceptions


def data_path(filename: str) -> str:
    """Get full path to a file in the data folder.

    Args:
        filename (str): The data file's name.

    Returns:
        path (str): The full path to the file.
    """
    return os.path.join(os.path.dirname(__file__), "data", filename)


def test_data_file(short_name: str) -> None:
    """Raise exception if data file unavailable.

    Args:
        short_name (str): file name.

    Raises:
        exceptions.DataFileMissingOrUnreadable

    Returns:
        None
    """
    path = data_path(short_name)
    if not os.path.isfile(path):
        raise exceptions.DataFileMissingOrUnreadable(short_name)


def read_csv_to_dict(short_name: str) -> Dict[str, str]:
    """Load csv into memory.

    Args:
        short_name (str): file name.

    Returns:
        Dict[str, str]: A dictionary of first column -> second column
    """
    path = data_path(short_name)
    test_data_file(short_name)
    with open(path, "r", encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file, delimiter=",")
        mapping = {rows[0]: rows[1] for rows in csv_reader}
    return mapping


def read_nicknames_file(
    short_name: str
) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Read a nicknames csv file into two dictionaries.

    The file is in the format:
        official,short,*other_nicknames

    Args:
        short_name (str): [description]

    Returns:
        A tuple of dictionaries (Tuple[Dict[str, str], Dict[str, str]]):
            nicknames_to_official
            official_to_short_name
    """
    nicknames_to_official: Dict[str, str] = {}
    official_to_short_name: Dict[str, str] = {}
    path = data_path(short_name)
    test_data_file(short_name)
    with open(path, "r", encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for row in csv_reader:
            official = row[0].strip()
            short = row[1].strip()
            nicknames_to_official[short.lower()] = official
            nicknames_to_official[official.lower()] = official
            official_to_short_name[official.lower()] = short
            for nickname in row[2:]:
                nicknames_to_official[nickname.lower()] = official
    # Green Party, with its different chapters, needs to be set by hand
    nicknames_to_official["green party"] = "Green Party"
    return nicknames_to_official, official_to_short_name


def read_csv_to_dataframe(
    short_name: str,
    separator: str = ","
) -> "pd.DataFrame":
    """Load csv into pandas dataframe.

    Args:
        short_name (str): Name of data file.
        separator (str, optional): Separator used in the file. Defaults to ",".

    Returns:
        data: dataframe
    """
    path = data_path(short_name)
    test_data_file(short_name)
    dataframe = pd.read_csv(path, sep=separator)
    return dataframe


PARTY_NICKNAMES, PARTY_SHORTNAMES = read_nicknames_file("party_nicknames.csv")
"""Official names from the nicknames we have on record."""

PARTY_COLORS = read_csv_to_dict("party_colors.csv")
"""Web color names for the parties."""

"""MIT License

Copyright (c) 2021 Stonehaven

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""