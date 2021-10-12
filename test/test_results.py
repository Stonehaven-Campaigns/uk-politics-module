"""Test the contents of the results submodule."""
from datetime import datetime
import uk_politics


def test_all_votes():
    """Check at least one vote record."""
    assert len(uk_politics.elections.COUNTS) > 0


def test_filter_by_constituency():
    """Check filtering by Constituency.

    Check at least one result,
    check all results in right location.
    """
    location_filter = uk_politics.Location(constituency="BUCKINGHAM")
    buckingham_results = [vote for vote in uk_politics.elections.COUNTS
                          if location_filter >= vote.location]

    # Check these results are all for the right constituency
    print(buckingham_results[0])
    for vote in buckingham_results:
        assert vote.location.constituency == "BUCKINGHAM"
    assert len(buckingham_results) > 0


def test_filter_by_region():
    """Check filtering by Region.

    Check at least one result,
    check all results in right location.
    """
    location_filter = uk_politics.Location(region="Wales")
    wales_results = [vote for vote in uk_politics.elections.COUNTS
                     if location_filter >= vote.location]

    print(wales_results[0])
    for vote in wales_results:
        assert vote.location.region == "Wales"
    assert len(wales_results) > 0


def test_filter_by_date():
    """Check filtering by Date.

    Check at least one result,
    check all results are for given date.
    """
    date_filter = datetime(1997, 5, 1).date()
    election_results = [vote_total for vote_total in uk_politics.elections.COUNTS
                        if date_filter == vote_total.date]

    for vote in election_results:
        assert vote.date == date_filter
    assert len(election_results) > 0


def test_speaker():
    """Test that precisely one result each year is ascribed to Speaker."""
    for date in uk_politics.elections.DATES:
        election_results = [vote_total
                            for vote_total in uk_politics.elections.COUNTS
                            if date == vote_total.date]
        speaker_results = [vote_total for vote_total in election_results
                           if vote_total.party == "Speaker"]
        assert len(speaker_results) == 1


def test_electorate():
    """Test that the electorate count in a constituency makes sense."""
    election_2019 = datetime(2019, 12, 12).date()
    counts = [count for count in uk_politics.elections.COUNTS
              if uk_politics.Location(constituency="DUNDEE EAST") >= count.location
              if count.date == election_2019]
    electorate_first = counts[0].location.electorate
    for count in counts:
        assert count.location.electorate == electorate_first

    vote_turnout = sum([count.votes for count in counts]) / electorate_first
    assert abs(vote_turnout - 0.68) < 0.01
