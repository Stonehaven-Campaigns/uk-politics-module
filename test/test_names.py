"""Test the party module functionality."""

import warnings
import pytest
import uk_politics
import uk_politics.data_tables
import uk_politics.exceptions

CONSERVATIVES_NICKNAMES = ["tory", "Tory",
                           "torie", "Torie",
                           "torys", "Torys",
                           "tories", "Tories"]


def test_find_tories():
    """Understand variations on "tory" as "Conservative and Unionist Party"."""
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", module="uk_politics")
        for nickname in CONSERVATIVES_NICKNAMES:
            print(nickname)
            assert uk_politics.names.official(
                nickname) == "Conservative and Unionist Party"

        assert uk_politics.names.short(
            "Conservative and Unionist Party") == "Conservative Party"


def test_do_not_find_tories_without_fuzzy():
    """Without fuzzy matching we raise an exception."""
    for nickname in [nickname
                     for nickname in CONSERVATIVES_NICKNAMES
                     if nickname.lower() not in
                     uk_politics.data_tables.PARTY_NICKNAMES]:
        print(nickname)
        with pytest.raises(uk_politics.exceptions.PartyNameNotFound):
            uk_politics.names.official(nickname, allow_fuzzy_match=False)


EXTRANEOUS_PARTIES = {"England":
                      ["Scottish National Party", "Sinn Fein",
                       "Democratic Unionist Party", "Plaid Cymru"],
                      "Scotland":
                      ["Sinn Fein", "Democratic Unionist Party",
                       "Plaid Cymru"],
                      "Northern Ireland":
                      ["Scottish National Party",
                       "Plaid Cymru"],
                      "Wales":
                      ["Scottish National Party", "Sinn Fein",
                       "Democratic Unionist Party"]
                      }


def test_current_parties_for_edge_cases():
    """Listed parties should not appear in the given country."""
    for country, party_list in EXTRANEOUS_PARTIES.items():
        official_name_party_list = list(
            map(uk_politics.names.official, party_list))
        print(country, official_name_party_list)

        parties_in_this_country = uk_politics.elections.ran(
            location_filter=uk_politics.Location(country=country))
        print(parties_in_this_country)

        assert set(parties_in_this_country).isdisjoint(
            official_name_party_list)


today_party_list = ["Conservatives",
                    "Democratic Unionist Party",
                    "GPEW",
                    "Green Party of Scotland",
                    "Green Party of Northern Ireland",
                    "Labour",
                    "Liberal Democrats",
                    "Other",
                    "Plaid Cymru",
                    "Reform UK (formerly Brexit party)",
                    "Scottish National Party",
                    "Sinn Fein"]


def test_current_parties():
    """Check that all parties listed ran in 2019."""
    for party in today_party_list:
        official_name = uk_politics.names.official(party)
        assert official_name in uk_politics.elections.ran()


def test_green_party():
    """The Green Party is the short name for multiple parties."""
    assert uk_politics.names.official("green party") == "Green Party"


def test_empty_name():
    """Test passing empty nickname raises the right error."""
    with pytest.raises(uk_politics.exceptions.PartyNicknameEmpty):
        uk_politics.names.official("")


def test_null_name_value():
    """Test null value for name data."""
    with pytest.raises(uk_politics.exceptions.PartyNicknameEmpty):
        uk_politics.names.official(None, exception_on_null_value=True)

    assert uk_politics.names.official(None) is None


def test_short_null_name_value():
    """Test null value for name data."""
    assert uk_politics.names.short(None) is None


def test_short_name_invalid_value():
    """Test invalid party name."""
    with pytest.raises(uk_politics.exceptions.PartyNameNotFound):
        uk_politics.names.short("None")
