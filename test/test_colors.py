"""Test the party_color functionality."""

import re
import pytest
import uk_politics
import uk_politics.data_tables
import uk_politics.exceptions


def test_example_given():
    """party_color("Brexit Party") -> "#12B6CF" is in the docstring."""
    assert uk_politics.color("Reform UK") == "#12B6CF"


def test_invalid_party_name():
    """Passing an invalid party should raise an exception."""
    with pytest.raises(uk_politics.exceptions.NoColorForThisParty):
        uk_politics.colors.by_official_party_name("")


def test_hex_code():
    """All the values should be hex codes."""
    for color in uk_politics.data_tables.PARTY_COLORS.values():
        assert re.match("^#[0-9A-F]{6}$", color) is not None


def test_no_vote():
    """Party "No vote" is a party from the point of view of having a color."""
    assert uk_politics.color("No vote") == "#333333"


def test_green_party():
    """The green party has warnings regarding color choice."""
    with pytest.warns(uk_politics.exceptions.UKPoliticsWarning):
        uk_politics.color("Green")
