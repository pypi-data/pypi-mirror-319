"""Print functions to print in the style we wish for."""

import sys
from typing import Protocol

R = "\x1b[31m"
G = "\x1b[32m"
Y = "\x1b[93m"
END = "\x1b[0m"
BOLD = "\x1b[1m"
PROMPT = "›"
OKAY = f" {BOLD}{G}◉{END} {PROMPT}"
INFO = f" {BOLD}{Y}☉{END} {PROMPT}"
FAIL = f" {BOLD}{R}⨯{END} {PROMPT}"


class Print(Protocol):
    """Protocol using for typing these print functions."""

    def __call__(self, msg: str, stderr: bool = ...) -> None:
        """Indicate the function signature."""
        ...  # pragma: no cover


def okay(msg: str, stderr: bool = False) -> None:
    print(OKAY, msg, file=sys.stderr if stderr else sys.stdout)


def info(msg: str, stderr: bool = False) -> None:
    print(INFO, msg, file=sys.stderr if stderr else sys.stdout)


def fail(msg: str, stderr: bool = False) -> None:
    print(FAIL, msg, file=sys.stderr if stderr else sys.stdout)
