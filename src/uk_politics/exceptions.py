"""A namespace for exception handling."""


class UKPoliticsException(Exception):
    """Base exception class for the politics module."""


class UKPoliticsWarning(Warning):
    """Base warning class for the politics module."""


class DataLineUnreadable(UKPoliticsException):
    """A line in the data isn't well-formed."""

    def __init__(self, offending_line: str, additional_context):
        """Raise exception citing line and issue."""
        super().__init__(
            (f"The line '{offending_line}' could not"
             f" be parsed because {additional_context}"))


class DataFileMissingOrUnreadable(UKPoliticsException):
    """Exception for missing or unreadable data file."""

    def __init__(self, short_name: str):
        """Raise exception with name of offending file."""
        super().__init__(
            f"Data file {short_name} missing or cannot be read."
        )


class PartyNameNotFound(UKPoliticsException):
    """Could not find a party of the given name."""

    def __init__(self, needle: str):
        """Raise exception announcing problem name."""
        super().__init__(f"No party with name '{needle}' was found.")


class PartyNicknameEmpty(UKPoliticsException):
    """No party can have an empty or null nickname."""

    def __init__(self):
        """Raise exception announcing empty nickname."""
        super().__init__("The search string is not allowed"
                         " to be empty or null.")


class NoColorForThisParty(UKPoliticsException):
    """Could not find a color for the given party."""

    def __init__(self, needle: str):
        """Raise exception announcing problem name."""
        super().__init__(f"No color was found for party '{needle}'.")

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