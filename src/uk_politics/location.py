r"""A container for (possibly wildcard) location data."""

import dataclasses
from typing import Any, List, Optional


@dataclasses.dataclass()
class Location:
    """Location specification.

    Leave options as None to act as wildcards.
    The ons_id term in particular in inconsistent between elections
    (or at least elections up until the standardisation of ONS ids)
    so is best left as None.
    Comparisons are made as though lower case.

    When comparing Locations:
        A >= B if A is more general than, or equal to, B.
    Note that this comparison only properly works when B
    contains no wildcards. Use of "A > B" is discouraged.

    When inspecting str(Location) the None entries
    are represented as "*" as befits a wildcard.

    Attributes:
        constituency: str
        county: str
        region: str
        country: str
        ons_id: str
        electorate: int
    """

    constituency: Optional[str] = None
    county: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    ons_id: Optional[str] = None
    electorate: Optional[int] = None

    def __init__(self,
                 ons_id: Optional[str] = None,
                 constituency: Optional[str] = None,
                 county: Optional[str] = None,
                 region: Optional[str] = None,
                 country: Optional[str] = None,
                 electorate: Optional[int] = None):
        """Create a location filter.

        There is no difference between a Location object
        and a location filter; but users are expected to
        only ever create filters. Location objects are populated
        from the data files at import time.
        """
        self.ons_id = ons_id
        self.constituency = constituency
        self.county = county
        self.region = region
        self.country = country
        self.electorate = electorate

    def _contains_loc_as_raw_string(self, raw_string: str) -> bool:
        """Compare self against a raw string.

        None is treated as a wildcard.
        Ignores the `electorate` attribute.
        """
        string_properties = raw_string.split("|")
        for index, prop in enumerate(self._string_properties_list):
            if prop is not None:
                if prop.lower() != string_properties[index].lower():
                    return False

        return True

    def __ge__(self, other: "Location") -> bool:
        """Compare against another Location object.

        self >= other if self is more general.
        """
        return self._contains_loc_as_raw_string(repr(other))

    def __le__(self, other: "Location") -> bool:
        """Compare against another Location object.

        self <= other if other is more general.
        """
        return other.__ge__(self)

    @property
    def _string_properties_list(self) -> List[Optional[str]]:
        """Those properties that take string values.

        These are the properties used for comparison.
        """
        return [self.ons_id,
                self.constituency,
                self.county,
                self.region,
                self.country]

    def __str__(self) -> str:
        """Location data in human-readable format."""
        return (f"id:{_wildcard_if_none(self.ons_id)} "
                f"constituency:{_wildcard_if_none(self.constituency)} "
                f"county:{_wildcard_if_none(self.county)} "
                f"region:{_wildcard_if_none(self.region)} "
                f"country:{_wildcard_if_none(self.country)} "
                f"electorate:{_wildcard_if_none(self.electorate)}")

    def __repr__(self) -> str:
        """Coerce to |-separated string."""
        return "|".join(list(map(_wildcard_if_none, self._string_properties_list))
                        + [_wildcard_if_none(self.electorate)])

    def __eq__(self, other: object) -> bool:
        """Check equality by checking string representation.

        Note that this will not be stable between years,
        since the electorate will be of different sizes.
        You may want to instead compare ons_id or name.
        """
        return repr(self) == repr(other)

    def __hash__(self) -> int:
        """Hash based on repr."""
        return hash(repr(self))


def _wildcard_if_none(potentially_none: Any) -> str:
    """Turn None into *, otherwise returns str form of argument."""
    if potentially_none is None:
        return "*"
    return str(potentially_none)


def from_raw_string(raw: str) -> Location:
    """Turn a |-separated string into a Location object."""
    def wildcard_to_nonetype(string):
        if string == "*":
            return None
        return string
    split: List[Optional[str]] = list(
        map(wildcard_to_nonetype, raw.split("|"))
    )
    if split[5] is None:
        electorate = None
    else:
        electorate = int(split[5])
    return Location(split[0], split[1], split[2],
                    split[3], split[4], electorate)

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