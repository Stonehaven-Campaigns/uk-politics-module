"""Tests for the data_tables module."""
import pytest
import uk_politics.exceptions
import uk_politics.data_tables


def test_file_not_found_exception():
    """Checking for file not found expection when loading data table."""
    with pytest.raises(uk_politics.exceptions.DataFileMissingOrUnreadable):
        uk_politics.data_tables.test_data_file(".csv")
