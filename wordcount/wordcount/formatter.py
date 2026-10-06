"""Formatting utilities for wordcount output."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from .core import Stats


@dataclass(frozen=True, slots=True)
class ActiveFlags:
    """Track which count flags are active."""

    lines: bool = False
    words: bool = False
    chars: bool = False
    bytes_count: bool = False

    def any_active(self) -> bool:
        """Check if any flag is explicitly set."""
        return self.lines or self.words or self.chars or self.bytes_count

    def defaults(self) -> ActiveFlags:
        """Return flags with defaults applied (wc behavior)."""
        if self.any_active():
            return self
        # Default: lines, words, bytes (like wc)
        return ActiveFlags(lines=True, words=True, bytes_count=True)


def calculate_widths(stats_list: list[Stats], flags: ActiveFlags) -> list[int]:
    """Calculate column widths for aligned output."""
    # Header values for width calculation
    widths = []

    if flags.lines:
        max_lines = max((s.lines for s in stats_list), default=0)
        widths.append(max(len(str(max_lines)), 7))  # "lines" header is 5, but wc uses more

    if flags.words:
        max_words = max((s.words for s in stats_list), default=0)
        widths.append(max(len(str(max_words)), 7))

    if flags.chars:
        max_chars = max((s.chars for s in stats_list), default=0)
        widths.append(max(len(str(max_chars)), 7))

    if flags.bytes_count:
        max_bytes = max((s.bytes_count for s in stats_list), default=0)
        widths.append(max(len(str(max_bytes)), 7))

    return widths


def format_row(
    stats: Stats,
    filename: Optional[str],
    flags: ActiveFlags,
    widths: list[int],
) -> str:
    """Format a single row of output."""
    parts = []
    idx = 0

    if flags.lines:
        parts.append(f"{stats.lines:>{widths[idx]}}")
        idx += 1

    if flags.words:
        parts.append(f"{stats.words:>{widths[idx]}}")
        idx += 1

    if flags.chars:
        parts.append(f"{stats.chars:>{widths[idx]}}")
        idx += 1

    if flags.bytes_count:
        parts.append(f"{stats.bytes_count:>{widths[idx]}}")
        idx += 1

    if filename is not None:
        parts.append(filename)

    return " ".join(parts)


def format_output(
    results: list[tuple[Stats, Optional[str]]],
    flags: ActiveFlags,
) -> str:
    """Format complete output for multiple files."""
    if not results:
        return ""

    # Include the aggregate when sizing columns so large totals stay aligned.
    all_stats = [stats for stats, _ in results]
    if len(results) > 1:
        total = Stats()
        for stats, _ in results:
            total = total.add(stats)
        all_stats.append(total)
    widths = calculate_widths(all_stats, flags)

    lines = []
    for stats, filename in results:
        lines.append(format_row(stats, filename, flags, widths))

    # Add total line if multiple files
    if len(results) > 1:
        lines.append(format_row(total, "total", flags, widths))

    return "\n".join(lines)
