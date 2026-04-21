import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from most_repetitive_element import (
    NoModeError,
    all_most_repetitive_elements,
    most_repetitive_element,
    parse_csv_numbers,
)


def test_most_repetitive_element_returns_unique_winner():
    assert most_repetitive_element([1, 2, 2, 3, 2, 3, 4, 5]) == 2


def test_most_repetitive_element_supports_non_numeric_hashable_values():
    assert most_repetitive_element(["a", "b", "a", "c", "a"]) == "a"


def test_most_repetitive_element_raises_for_empty_input():
    with pytest.raises(ValueError, match="Input cannot be empty"):
        most_repetitive_element([])


def test_most_repetitive_element_raises_when_tied_for_max_frequency():
    with pytest.raises(NoModeError, match="No unique most repetitive element"):
        most_repetitive_element([1, 1, 2, 2, 3])


def test_all_most_repetitive_elements_returns_all_ties():
    result = all_most_repetitive_elements([1, 1, 2, 2, 3])
    assert result == [1, 2]


def test_parse_csv_numbers_parses_ints_and_floats_with_spaces():
    assert parse_csv_numbers("1, 2.5, -3, 4.0") == [1, 2.5, -3, 4]


def test_parse_csv_numbers_rejects_empty_input():
    with pytest.raises(ValueError, match="Input cannot be empty"):
        parse_csv_numbers("   ")


def test_parse_csv_numbers_rejects_empty_values_between_commas():
    with pytest.raises(ValueError, match="avoid empty values"):
        parse_csv_numbers("1,,2")


def test_parse_csv_numbers_rejects_non_numeric_values():
    with pytest.raises(ValueError, match="Invalid numeric value"):
        parse_csv_numbers("1,apple,2")
