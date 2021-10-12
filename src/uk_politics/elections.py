r"""Election vote counts.

Election results are stored as a VoteTotal object;
one for each party / location / date combination.
Speakers are assigned to the party "Speaker".
"""
import dataclasses
import datetime
from typing import Dict, List, Optional, Tuple

from uk_politics import exceptions

from . import data_tables
from . import location
from . import names


@dataclasses.dataclass
class VoteTotal:
    """Vote total for a single party / location / date combination.

    Attributes:
        location (uk_politics.Location): Single constituency.
        date (datetime.date): Date on which the election happened.
        party (str): Official, current, name of the party.
        party_contemporary_styling (str): Party as recorded in the data.
        votes (int): Vote count for this party in this place on this day.

    The property `.party` is always the modern official name for the party,
    and `.party_contemporary_styling` is the
    short form used in the election data.
    For example some elections just write "PC" instead of
    "Plaid Cymru - the Party of Wales", so we record both.
    """

    location: location.Location
    date: datetime.date
    party: str
    party_contemporary_styling: str
    votes: int


def _vote_line_to_object(line: List[str]) -> VoteTotal:
    """Convert a line in a tsv file to a VoteTotal object."""
    count_location = location.from_raw_string(line[0])
    party_contemporary_styling = line[2]
    if party_contemporary_styling == "PC/SNP":
        # These were lumped together in some elections
        if count_location.country == "Scotland":
            party_contemporary_styling = "SNP"
        elif count_location.country == "Wales":
            party_contemporary_styling = "PC"
    elif party_contemporary_styling == "Green":
        # Green party is officially distinct between these regions
        # Use names.short to turn these all back into "Green Party"
        if count_location.country == "Scotland":
            party_contemporary_styling = "Scottish Green Party"
        elif count_location.country == "Northern Ireland":
            party_contemporary_styling = "Green Party Northern Ireland"
        else:
            party_contemporary_styling = "Green Party of England and Wales"

    party_official_name = names.official(
        party_contemporary_styling, warn_on_fuzzy_match=True)

    if party_official_name is None:
        raise exceptions.DataLineUnreadable(
            "\t".join(line), "party name could not be read")

    return VoteTotal(location=count_location,
                     date=datetime.datetime.strptime(
                         line[1], "%Y-%m-%d").date(),
                     party=party_official_name,
                     party_contemporary_styling=party_contemporary_styling,
                     votes=int(line[3]))


_ALL_VOTES_DF = data_tables.read_csv_to_dataframe("GE_results.tsv", "\t")

COUNTS: List[VoteTotal] = [_vote_line_to_object(vote[1])
                           for vote in _ALL_VOTES_DF.iterrows()]
"""A list of every party / date / location vote count."""

PARTIES_ORIGINAL_NAMES: List[str] = sorted(
    list({vote_count.party for vote_count in COUNTS}))
"""A list of every party name as styled in the original data."""

DATES: List[datetime.date] = sorted(
    list({vote_count.date for vote_count in COUNTS}))
"""The dates of the elections for which we have data."""

MOST_RECENT_ELECTION_DATE: datetime.date = max(DATES)
"""The date of the most recent election in the data."""


def seats(date: datetime.date = MOST_RECENT_ELECTION_DATE,
          location_filter: Optional[location.Location] = None
          ) -> List[Tuple[location.Location, str]]:
    """List the constituencies along with the name of the party that won.

    The Speaker is treated as their own party.
    See politics.elections.DATES for a list of dates.

    Args:
        date (datetime.date, optional):
            The date of the election to inspect.
            Defaults to MOST_RECENT_ELECTION_DATE.

    Returns:
        A list of tuples (List[Tuple[location.Location, str]]):
            Location
            Winning party
    """
    if location_filter is None:
        location_filter = location.Location()
    counts_for_this_date = [count for count in COUNTS
                            if location_filter >= count.location
                            if count.date == date]
    locations = {count.location for count in counts_for_this_date}
    constituency_winners: Dict[location.Location, str] = {}
    for loc in locations:
        party_counts = {count.party: count.votes
                        for count in counts_for_this_date
                        if count.location == loc}
        winner = max(party_counts.keys(), key=lambda x,
                     counter=party_counts: counter[x])
        constituency_winners[loc] = winner
    return list(constituency_winners.items())


def ran(
    date: datetime.date = MOST_RECENT_ELECTION_DATE,
    location_filter: Optional[location.Location] = None,
) -> List[str]:
    """Parties that ran on the given date in the given location.

    Leave location_filter as None to cover all locations.

    Args:
        date (datetime.date, optional):
            Date of election to inspect.
            Defaults to MOST_RECENT_ELECTION_DATE.
        location_filter (location.Location, optional):
            Only show parties that ran in locations within location_filter.
            Defaults to None (most general).

    Returns:
        List of parties (List[str])
    """
    if location_filter is None:
        parties = {count.party for count in COUNTS
                   if date == count.date}
    else:
        parties = {count.party for count in COUNTS
                   if location_filter >= count.location
                   if date == count.date}
    return sorted(list(parties))

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