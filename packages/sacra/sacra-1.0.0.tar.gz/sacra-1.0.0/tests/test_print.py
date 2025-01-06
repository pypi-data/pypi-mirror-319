"""Tests for the _print module."""

from io import StringIO
from unittest.mock import patch

import pytest

from sacra._print import Print, fail, info, okay


@pytest.mark.parametrize(
    "fn, given, expected",
    [
        (fail, "Test", " \x1b[1m\x1b[31m⨯\x1b[0m › Test"),
        (info, "Test", " \x1b[1m\x1b[93m☉\x1b[0m › Test"),
        (okay, "Test", " \x1b[1m\x1b[32m◉\x1b[0m › Test"),
    ],
)
@pytest.mark.parametrize("stream", ["sys.stdout", "sys.stderr"])
def test_print(
    fn: Print,
    given: str,
    expected: str,
    stream: str,
) -> None:
    """Test that print functions behave as expected."""
    with patch(stream, new=StringIO()) as mock_stream:
        if stream == "sys.stdout":
            fn(given)
        else:
            fn(given, stderr=True)
        assert mock_stream.getvalue().rstrip("\n") == expected
