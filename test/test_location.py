"""Test the Location class."""

import uk_politics
import uk_politics.location


def test_location_str():
    """Test the str(location) property."""
    count = uk_politics.elections.COUNTS[0]
    location = count.location
    for property_name in ["id", "constituency",
                          "county", "country", "region", "electorate"]:
        assert property_name + ":" in str(location)


def test_comparisons():
    """Test the >= and <= comparisons.

    These comparisons are only supposed to be performed
    where one side is a fully populated Location object (from the data)
    and the other is a filter created by the user.
    """
    location_one = uk_politics.Location(constituency="Home")
    location_two = uk_politics.Location(constituency="Away")
    assert location_one <= location_one
    assert location_one >= location_one
    assert not location_one <= location_two
    assert not location_one >= location_two


def test_location_from_string():
    """Turn a fully-populated Location object into a string and back."""
    location = uk_politics.elections.COUNTS[0].location
    as_string = repr(location)
    from_string = uk_politics.location.from_raw_string(as_string)
    assert location == from_string


def test_location_from_string_with_wildcards():
    """Turn a fully-populated Location object into a string and back."""
    location = uk_politics.location.from_raw_string("*|*|*|*|*|0")
    assert location.constituency is None
    assert location.electorate == 0
