"""Test the contents of uk_politics.elections."""

import datetime
import uk_politics


def test_ran():
    """Sixteen parties ran that year, including "Speaker"."""
    assert len(uk_politics.elections.ran(datetime.date(2019, 12, 12))) == 16


def test_seats():
    """Should be 650."""
    assert len(uk_politics.elections.seats()) == 650

def test_seats_is_list():
    """Should return a list of tuples."""
    assert len(uk_politics.elections.seats()[0]) == 2
