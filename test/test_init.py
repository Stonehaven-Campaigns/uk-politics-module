"""Test the functions exposed at the top level of the module.

This isn't a full test of each method's capabilities,
just checking that the method is exposed at the top level namespace.
"""

import warnings
import pytest
import uk_politics
import uk_politics.exceptions


def test_color():
    """Check that uk_politics.color works."""
    assert uk_politics.color("Liberal Democrats") == "#FAA61A"


def test_location():
    """Check that uk_politics.Location works.

    Just creation and comparison here.
    """
    wales = uk_politics.Location(country="Wales")
    west_glamorgan = uk_politics.elections.COUNTS[0].location
    assert wales >= west_glamorgan
    assert not west_glamorgan >= wales


def test_find_party():
    """Check that uk_politics.find_party works."""
    assert uk_politics.find_party(
        "Tory", return_short_name=True) == "Conservative Party"


def test_find_empty():
    """Passing an empty string should raise assertion error."""
    with pytest.raises(uk_politics.exceptions.PartyNicknameEmpty):
        assert uk_politics.find_party("") == ""


def test_scottish_labour():
    """Test variations on Scottish Labour return Labour not SNP.

    The name is a bit too close to two different parties.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", module="uk_politics")
        assert uk_politics.find_party("Scottish Labour") == "Labour Party"
        assert uk_politics.find_party("Scottish labour") == "Labour Party"


def test_rename_gives_warning(caplog):
    """Test that a bad name prompts a rename warning."""
    uk_politics.find_party("labuor")
    print(caplog.records)
    expected = "Renaming 'labuor' -> 'Labour Party'"
    assert expected in caplog.text
