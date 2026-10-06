"""wordcount - A wc-like CLI tool in Python."""

from .core import Stats, count_stream

__all__ = ["Stats", "count_stream"]
__version__ = "0.1.0"