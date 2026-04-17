import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import dynamic_calculator as calc


def test_add_returns_sum_for_positive_values():
    assert calc.add(10, 5) == 15


def test_subtract_returns_difference_for_negative_values():
    assert calc.subtract(-3, -7) == 4


def test_multiply_returns_product_for_decimal_values():
    assert calc.multiply(2.5, 4) == 10.0


def test_divide_returns_quotient_for_valid_values():
    assert calc.divide(9, 3) == 3


def test_divide_by_zero_raises_meaningful_error():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        calc.divide(10, 0)


def test_get_number_accepts_negative_decimal(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "-5.75")
    assert calc.get_number("Enter a number: ") == -5.75


def test_get_number_retries_until_valid_input(monkeypatch, capsys):
    answers = iter(["not-a-number", "5.5"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert calc.get_number("Enter a number: ") == 5.5
    out = capsys.readouterr().out
    assert "Invalid number" in out


def test_run_calculator_addition_flow(monkeypatch, capsys):
    answers = iter(["1", "10", "20", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    calc.run_calculator()

    out = capsys.readouterr().out
    assert "Result of Addition: 30.0" in out
    assert "Thank you for using Dynamic Calculator!" in out


def test_run_calculator_handles_invalid_menu_choice(monkeypatch, capsys):
    answers = iter(["9", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    calc.run_calculator()

    out = capsys.readouterr().out
    assert "Invalid choice. Please select from 1 to 5." in out


def test_run_calculator_handles_division_by_zero_without_crashing(monkeypatch, capsys):
    answers = iter(["4", "8", "0", "5"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    calc.run_calculator()

    out = capsys.readouterr().out
    assert "Cannot divide by zero." in out
    assert "Thank you for using Dynamic Calculator!" in out
