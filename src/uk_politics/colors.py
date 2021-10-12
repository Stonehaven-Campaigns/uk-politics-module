r"""Function for searching for the current list of valid parties.

The colors themselves are from
https://en.wikipedia.org/wiki/Wikipedia:Index_of_United_Kingdom_political_parties_meta_attributes

Although there is no singular Green Party it is still likely
that someone will want to use our module to find a suitable color.
The historic color is supplied, along with a warning.
"""

from typing import Optional
import warnings
from . import data_tables
from . import exceptions


def by_official_party_name(party_name: Optional[str]) -> Optional[str]:
    """Return current hex color for a party.

    If no color is found for that party name try
    getting the official name using the politics.names submodule.

    Args:
        party_name (str): The official name of the party

    Raises:
        exceptions.NoColorForThisParty:
            If the given name is not in our data then an
            exception is raised.

    Returns:
        hexcode str: The (current) hex color for that party.
        For example:
            color("Brexit Party") -> "#12B6CF"
    """
    if party_name is None:
        return None

    if party_name in data_tables.PARTY_COLORS:
        if party_name == "Green Party":
            warnings.warn(("The Green Party has split into different chapters"
                           " in each country, each with different colors."
                           " The historic color (from when it was one party)"
                           " has been returned."), exceptions.UKPoliticsWarning)
        return data_tables.PARTY_COLORS[party_name]

    raise exceptions.NoColorForThisParty(party_name)

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