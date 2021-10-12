# uk-politics

United Kingdom political party names, colors, and election data.

## Installation

This repository is available on PyPI, meaning it can be installed using:

```bash
pip install uk-politics
```

And used within `python` like so:

```python
import uk_politics
```

## Functionality

This module has three core aims:

 - Matching free-text entries to UK political party names
 - Searching historic election data
 - Matching party names to party colors

### Free text names

Use `uk_politics.find_party` to get the official name of the closest-named party.

```python
>>> uk_politics.find_party("Lib Dem")
'Liberal Democrats'
>>> uk_politics.find_party("SNP")
'Scottish National Party'
>>> uk_politics.find_party("Sinn Fein")
'Sinn Féin'
```

Sometimes the official name isn't the name used in everyday speech, 
or even [on the parliament website](https://www.parliament.uk/about/mps-and-lords/members/parties/), 
so we use these shorter names by default, with the option of the official names as well.

```python
>>> uk_politics.find_party("Tory")
'Conservative Party'
>>> uk_politics.find_party("Tory", return_short_name=False)
'Conservative and Unionist Party'
```

```python
>>> uk_politics.find_party("Tory")
'Conservative Party'
>>> uk_politics.find_party("Tory", return_short_name=False)
'Conservative and Unionist Party'
```

What about misspellings?
The module will warn you the first time it encounters a name
that it can't match to an existing nickname, 
and returns its best guess via fuzzy matching.

```python
>>> uk_politics.find_party("Labuor Party")
Renaming 'labuor party' -> 'Labour Party'
'Labour Party' 
```

You can turn this fuzzy matching functionality off to get an exception
instead of a warning.

```python
>>> uk_politics.find_party("Labuor Party", allow_fuzzy=False)
[...] uk_politics.exceptions.PartyNameNotFound: No party with name 'labuor party' was found.
```

Finally we have created a party named "No vote"
that exists just to catch the following sorts of situations:

```python
>>> uk_politics.find_party("Didn't vote")
'No vote'
```

How does this work?
We have compiled a list of nicknames we've observed
across platforms, websites, and data providers, 
and then use fuzzy matching the rest of the way.
The nicknames are stored in `/src/uk_politcs/data/party_nicknames.csv` so you can easily add to or alter them, 
and `null` values pass straight through as `None` .

### Searching election data

The House of Commons has [released historic election data](https://commonslibrary.parliament.uk/research-briefings/cbp-8647/)
which we have transformed and included as `/src/data/GE_results.tsv` , 
and created some tools to allow for filtering by region, country, date, etc..
If you want to see every seat and winning party in the most recent election just run:

```python
# Returns a list of all 650 constituencies and winning parties
>>> uk_politics.elections.seats()
[...]
>>> uk_politics.elections.seats()[0]
(E14000833|NEWCASTLE UPON TYNE NORTH|Tyne and Wear|North East|England|68486, 'Labour Party')
```

This is a tuple of type `(uk_politics.Location, str)` , 
and as you can see the `uk_politics.Location` object knows the following properties
of a constituency:

```python
>>> newcastle_north = uk_politics.elections.seats()[0][0]
>>> newcastle_north.ons_id
'E14000833'
>>> newcastle_north.constituency
'NEWCASTLE UPON TYNE NORTH'
>>> newcastle_north.county
'Tyne and Wear'
>>> newcastle_north.region
'North East'
>>> newcastle_north.country
'England'
>>> newcastle_north.electorate
68486
```

If you want to see not just who won, but the vote tally for each party
those are stored in `uk_politics.elections.COUNTS` .
For example:

```python
>>> import datetime
>>> election_2019 = datetime.date(2019,12,12)
>>> for count in uk_politics.elections.COUNTS:
...     if count.date == election_2019 and count.location.constituency == "DUNDEE EAST":
...         print(f"{count.party}: {count.votes}")
... 
Conservative and Unionist Party: 10986
Labour Party: 6045
Liberal Democrats: 3573
Scottish National Party: 24361
Other: 312
```

By default `uk_politics.elections.seats` assumes you want to know about the most recent election, 
but it has data on all elections back to 1997
(see `uk_politics.elections.DATES` for a list).
You can pass a date as the first argument
to `uk_politics.elections.seats` in order to grab that election data instead.
Likewise the function `uk_politics.elections.ran`

(which grabs a list of all parties with recorded vote counts)
can also be passed a date:

```python
>>> uk_politics.elections.ran(datetime.date(2001, 6, 7))
['Conservative and Unionist Party', 'Democratic Unionist Party', 'Labour Party', 'Liberal Democrats', 'Other', 'Plaid Cymru - the Party of Wales', 'Scottish National Party', 'Sinn Féin', 'Social Democratic and Labour Party', 'Speaker', 'Ulster Unionist Party']
```

Note the Speaker is included as their own party, 
since they traditionally sever links to any previous affiliation.

You can also use the `uk_politics.Location` class to filter by
any of the properties we listed for `newcastle_north` above.

```python
>>> wales_filter = uk_politics.Location(country="Wales")
>>> uk_politics.elections.ran(location_filter=wales_filter)
['Conservative and Unionist Party', 'Green Party of England and Wales', 'Labour Party', 'Liberal Democrats', 'Other', 'Plaid Cymru - the Party of Wales', 'Reform UK']
>>> uk_politics.elections.seats(location_filter=wales_filter)
[(W07000065|PRESELI PEMBROKESHIRE|Dyfed|Wales|Wales|59606, 'Conservative and Unionist Party'), ...]
```

The Location class supports `>=` and `<=` comparison; 
set a property to `None` to have it act as a wildcard.
These comparisons are only designed to work when
at least one of the Location objects is fully populated
with data.

```python
>>> west_glamorgan = uk_politics.elections.COUNTS[0].location
>>> wales = uk_politics.Location(country="Wales")
>>> wales >= west_glamorgan
True
>>> west_glamorgan >= wales
False
```

This data is only as nuanced as the House Of Commons historic data, 
and so smaller parties may have been grouped under Other in some years but not others.

### Finding the party color

`uk-politics` lets you grab a hex code straight from a party name (or nickname).

```
>>> uk_politics.color("Labour")
'#E4003B'
>>> uk_politics.color("Alliance")
'#F6CB2F'
```

Here's an example using the `seaborn` library:

```python
[...]
>>> import seaborn as sns
>>> sns.countplot(y=vote_column, palette={party: uk_politics.color(party) for party in vote_column.unique()})
[...]
```

## Development notes

Spelling: US American English

Linting: pylint, pydocstyle

Testing: pytest

Style guide: https://google.github.io/styleguide/pyguide.html

The code of the project is licensed under MIT license, 
with data provided under the licenses next to each data file.
