import numpy as np
import pytest

from world_objects import _format_number


@pytest.mark.parametrize(
    "number, expected",
    [
        # Regular numbers
        (1.0, "1.0"),
        (1.23, "1.23"),
        (1.2345, "1.23..."),
        # Whole numbers
        (42, "42.0"),
        (0, "0.0"),
        # Very small numbers
        (9.249599090821459e-07, "0.0"),  # Below threshold
        (1.23e-9, "0.0"),  # Below threshold
        (1.23e-5, "0.0"),  # Above threshold but tiny
        # Large numbers with many decimals
        (123.45678901234567, "123.46..."),
        # Negative numbers
        (-1.23456, "-1.23..."),
        (-0.000000001, "0.0"),  # Small negative
        # Edge cases
        (0.001, "0.0"),
        (0.01, "0.01"),
        (0.0049, "0.0"),  # Should round down
        (0.0051, "0.00..."),  # Should round up
    ],
)
def test_format_number(number: float, expected: str) -> None:
    assert _format_number(number) == expected


@pytest.mark.parametrize(
    "number, digits, expected",
    [
        # Test with different precisions
        (1.23456, 1, "1.2..."),
        (1.23456, 3, "1.235..."),
        (1.23456, 4, "1.2346..."),
        # Edge cases with different precisions
        (0.0001234, 3, "0.0"),
        (123.456789, 0, "123.0"),
        (0.999999, 2, "1.0"),
    ],
)
def test_format_number_custom_digits(number: float, digits: int, expected: str) -> None:
    assert _format_number(number, digits) == expected


def test_format_number_with_numpy_types() -> None:
    # Test numpy number types
    assert _format_number(np.float64(1.23456)) == "1.23..."
    assert _format_number(np.float32(1.23456)) == "1.23..."
    assert _format_number(np.float16(1.23456)) == "1.23..."
