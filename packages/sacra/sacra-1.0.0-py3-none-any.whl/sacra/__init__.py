"""Sacra is derived from the Latin word _sacrum_.

It evokes things sacred, holy, part of rites, or works of art.
"""

try:
    from ._version import __version__, __version_tuple__
except ImportError:
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)
