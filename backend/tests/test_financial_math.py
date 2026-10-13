"""Financial math utility tests."""

from app.utils.financial_math import future_value, required_monthly_contribution, safe_divide


def test_safe_divide_zero():
    assert safe_divide(10, 0, default=0) == 0


def test_future_value_no_return():
    result = future_value(1000, 500, 0, 12)
    assert result == 1000 + 500 * 12


def test_required_monthly_contribution():
    required = required_monthly_contribution(10000, 100000, 0.08, 24)
    assert required > 0
