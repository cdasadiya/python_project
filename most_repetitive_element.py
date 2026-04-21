"""Find the most repetitive element(s) in a list-like input."""

from collections import Counter
from typing import Any, Iterable


class NoModeError(ValueError):
    """Raised when there is no unique most repetitive element."""


def most_repetitive_element(values: Iterable[Any]) -> Any:
    """Return the single most repetitive element in ``values``.

    Rules:
    - Empty input raises ``ValueError``.
    - If multiple elements tie for highest frequency, ``NoModeError`` is raised.
    - Works with any hashable element type (int, str, tuple, etc.).
    """

    items = list(values)
    if not items:
        raise ValueError("Input cannot be empty.")

    counts = Counter(items)
    max_count = max(counts.values())
    top_items = [item for item, count in counts.items() if count == max_count]

    if len(top_items) != 1:
        raise NoModeError(
            "No unique most repetitive element exists (there is a tie for maximum frequency)."
        )

    return top_items[0]


def all_most_repetitive_elements(values: Iterable[Any]) -> list[Any]:
    """Return all element(s) tied for highest frequency.

    This helper is useful when ties should be handled instead of rejected.
    """

    items = list(values)
    if not items:
        raise ValueError("Input cannot be empty.")

    counts = Counter(items)
    max_count = max(counts.values())
    return [item for item, count in counts.items() if count == max_count]


def parse_csv_numbers(raw: str) -> list[float | int]:
    """Parse comma-separated numeric text into a list.

    Examples:
    - ``"1,2,2,3"`` -> ``[1, 2, 2, 3]``
    - ``"1, 2.5, -3"`` -> ``[1, 2.5, -3]``
    """

    cleaned = raw.strip()
    if not cleaned:
        raise ValueError("Input cannot be empty.")

    parts = [part.strip() for part in cleaned.split(",")]
    if any(not part for part in parts):
        raise ValueError("Invalid format: avoid empty values between commas.")

    parsed: list[float | int] = []
    for part in parts:
        try:
            number = float(part)
        except ValueError as error:
            raise ValueError(
                f"Invalid numeric value: {part!r}. Please provide comma-separated numbers."
            ) from error

        if number.is_integer():
            parsed.append(int(number))
        else:
            parsed.append(number)

    return parsed


def run_interactive() -> None:
    """Interactive runner for quick manual usage."""

    print("Most Repetitive Element Finder")
    print("Enter comma-separated numbers (example: 1,2,2,3,2,3,4,5)")

    raw = input("Input list: ")
    values = parse_csv_numbers(raw)

    try:
        winner = most_repetitive_element(values)
        print(f"Most repetitive element: {winner}")
    except NoModeError:
        tied = all_most_repetitive_elements(values)
        print(f"No unique most repetitive element. Tied elements: {tied}")


if __name__ == "__main__":
    run_interactive()
