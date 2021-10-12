r"""UK Politics.

Covers the names and colors of the UK political parties,
as well as election vote counts for the major parties in
every election and constituency since 1997.
This is based on data released by the House of Commons,
see GE_results.tsv.licence for details.

Example uses:
    uk_politics.elections.seats(datetime.date(2019,12,12)) ->
        list constituencies and winning parties
    uk_politics.color("Labour Party") -> "#E4003B"
    uk_politics.find_party("Tories") -> "Conservative and Unionist Party"
    uk_politics.find_party("Tories", return_short_name=True) -> "Conservative Party"

Licencing summary:
    This module contains Parliamentary information
    licensed under the Open Parliament Licence v3.0.
    The data files (in the data directory) contain
    licencing information alongside each file.

Submodules:
    uk_politics.elections holds vote count data for each election
    uk_politics.names holds functions for official-, short-, and nick-names
    uk_politics.colors maps party names to colors

Hidden submodules:
    uk_politics.data_tables handles most of the data extraction
    uk_politics.location
        holds a custom Location class (useful for filtering election data)
        exposed as politics.Location
    uk_politics.exceptions holds exceptions

Spelling:
    In the interest of international consistency we will use EN_US spellings.

"""

from typing import Optional
from . import colors
from . import elections
from . import names

# Bring the following elements forward in the namespace
from .location import Location


def color(party_name_or_nickname: Optional[str]) -> Optional[str]:
    """Color (hex code) for a party based on a name or nickname.

    For finer control see politics.names and politics.colors.
    Returns the current color for a party.

    Args:
        party_name_or_nickname (str)

    Returns:
        color (str): The hex code (including "#") assigned to that party.
        For example:
            color("Tory") -> '#0087DC'
    """
    official_name = names.official(party_name_or_nickname)
    return colors.by_official_party_name(official_name)


def find_party(nickname: Optional[str], return_short_name: bool = False, allow_fuzzy: bool = True) -> Optional[str]:
    """Find a party based on nickname.

    By default this allows fuzzy matching,
    but warns the user when it is applied.
    For finer control see `politics.names.official` and
    `politics.names.short`.

    Args:
        nickname (str): unofficial name for party you want to search for
        return_short_name (bool, optional):
            Return short name, rather than the sometimes unwieldy
            official name. Defaults to False.
        allow_fuzzy (bool, optional):
            Allow fuzzy searching to try and find the correct party.
            Defaults to True.

    Returns:
        name (str): The official name of the party best matching the nickname.
    """
    official_name = names.official(nickname, allow_fuzzy_match=allow_fuzzy)

    if return_short_name:
        return names.short(official_name)

    return official_name


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