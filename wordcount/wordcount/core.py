"""Core counting logic for wordcount."""

from __future__ import annotations
import codecs
from dataclasses import dataclass
from typing import BinaryIO, TextIO, Union


@dataclass(frozen=True, slots=True)
class Stats:
    """Container for count statistics."""

    lines: int = 0
    words: int = 0
    chars: int = 0
    bytes_count: int = 0

    def add(self, other: Stats) -> Stats:
        """Return a new Stats with the sum of self and other."""
        return Stats(
            lines=self.lines + other.lines,
            words=self.words + other.words,
            chars=self.chars + other.chars,
            bytes_count=self.bytes_count + other.bytes_count,
        )

    def __add__(self, other: Stats) -> Stats:
        """Allow using + operator to combine Stats."""
        return self.add(other)


def count_stream(stream: Union[TextIO, BinaryIO]) -> Stats:
    """
    Count lines, words, characters, and bytes from a stream.

    Reads in chunks to handle large files efficiently.
    """
    lines = 0
    words = 0
    chars = 0
    bytes_count = 0

    chunk_size = 8192
    first_chunk = stream.read(chunk_size)
    is_binary = isinstance(first_chunk, bytes)
    decoder = codecs.getincrementaldecoder("utf-8")(errors="replace") if is_binary else None
    pending_word = ""

    def consume_text(text: str, *, final: bool = False) -> None:
        nonlocal lines, words, chars, pending_word
        lines += text.count("\n")
        chars += len(text)
        combined = pending_word + text
        pieces = combined.split()
        if not pieces:
            pending_word = ""
        elif final or combined[-1].isspace():
            words += len(pieces)
            pending_word = ""
        else:
            words += len(pieces) - 1
            pending_word = pieces[-1]

    chunk = first_chunk
    while chunk:
        if is_binary:
            bytes_count += len(chunk)
            consume_text(decoder.decode(chunk))
        else:
            bytes_count += len(chunk.encode("utf-8"))
            consume_text(chunk)
        chunk = stream.read(chunk_size)

    if is_binary:
        consume_text(decoder.decode(b"", final=True), final=True)
    else:
        consume_text("", final=True)

    return Stats(lines=lines, words=words, chars=chars, bytes_count=bytes_count)


def count_file(filepath: str) -> Stats:
    """
    Count statistics for a file.

    Opens in binary mode for accurate byte counting.
    """
    with open(filepath, "rb") as f:
        return count_stream(f)
