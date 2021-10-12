"""Parties have official names, short names, and nicknames.

This submodule attempts to link these different types of name.
The short name is the colloquial name as used by
https://www.parliament.uk/about/mps-and-lords/members/parties/ .
Example:
 - official name: Conservative and Unionist Party
 - short name: Conservative Party
 - nickname: Tory

The nicknames come from our own survey data.

The "Green Party" is not one party but a collection of parties,
with distinct chapters in Scotland, Northern Ireland,
and England & Wales. The election data, when presented to the user,
distinguishes between these parties with their official names
(which contain their country identifier), but all three official
names are shortened to Green Party.

The Co-operative Party is in alliance with the Labour party,
and all their seats are recorded as Labour seats in the data.

The Speaker is regarded as a party of one member.
"""

import logging
import functools
from typing import Optional

import pandas as pd
import fuzzywuzzy.process

from . import data_tables
from . import exceptions

_logger = logging.getLogger("uk-politics")

@functools.lru_cache
def official(nickname: Optional[str],
             allow_fuzzy_match=True,
             warn_on_fuzzy_match=True,
             exception_on_null_value=False) -> Optional[str]:
    """Return the official name of a party from a given nickname.

    The function uses fuzzy match (Levenstein distance, from fuzzywuzzy)
    to find the closest match by default;
    set `allow_fuzzy_match=False` to turn this off.
    These renames will appear as warnings.

    This function is cached to avoid running extra fuzzy matches,
    this also means that warnings will only appear the first time
    a given renaming takes place. By default nicknames that `pandas`
    considers to be a null value are passed through as None.

    Args:
        nickname (str): [description]
        allow_fuzzy_match (bool, optional): [description]. Defaults to True.
        warn_on_fuzzy_match (bool, optional): [description]. Defaults to True.

    Raises:
        exceptions.PartyNicknameEmpty: [description]
        exceptions.PartyNameNotFound: [description]

    Returns:
        official_name (str): The official name for the party
        that best matches our nicknames on record.
        For example:
            official_name("tories") -> "Conservative and Unionist Party"
    """
    if pd.isna(nickname):
        if exception_on_null_value:
            raise exceptions.PartyNicknameEmpty()
        return None

    assert nickname is not None # for typing

    nickname = nickname.lower().strip()
    if len(nickname) == 0:
        raise exceptions.PartyNicknameEmpty()

    if nickname in data_tables.PARTY_NICKNAMES:
        # In our database of nicknames
        return data_tables.PARTY_NICKNAMES[nickname]

    if allow_fuzzy_match:
        #types: ignore
        fuzzy_matched = fuzzywuzzy.process.extractOne(
            nickname, list(data_tables.PARTY_NICKNAMES.keys()))[0]
        proper_name = data_tables.PARTY_NICKNAMES[fuzzy_matched]
        if warn_on_fuzzy_match:
            _logger.warning("Renaming '%s' -> '%s'", nickname, proper_name)
        return proper_name

    raise exceptions.PartyNameNotFound(nickname)


def short(official_name: Optional[str]) -> Optional[str]:
    """Short name we use instead of the given official party name.

    Args:
        official_name (str): [description]

    Raises:
        exceptions.PartyNameNotFound: [description]

    Returns:
        shot_name (str): The short name for a given official party name.
        For example:
            short_name("Conservative and Unionist Party") -> "Conservative"
    """
    if official_name is None:
        return None
    official_name = official_name.lower()
    if official_name in data_tables.PARTY_SHORTNAMES:
        return data_tables.PARTY_SHORTNAMES[official_name]

    raise exceptions.PartyNameNotFound(official_name)

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