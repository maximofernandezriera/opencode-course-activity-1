"""Tests for formatter module."""

from __future__ import annotations

import pytest

from wordcount.core import Stats
from wordcount.formatter import (
    ActiveFlags,
    calculate_widths,
    format_row,
    format_output,
)


class TestActiveFlags:
    """Tests for ActiveFlags dataclass."""

    def test_any_active_false(self):
        flags = ActiveFlags()
        assert not flags.any_active()

    def test_any_active_true(self):
        flags = ActiveFlags(lines=True)
        assert flags.any_active()

        flags = ActiveFlags(words=True)
        assert flags.any_active()

        flags = ActiveFlags(chars=True)
        assert flags.any_active()

        flags = ActiveFlags(bytes_count=True)
        assert flags.any_active()

    def test_defaults_when_active(self):
        flags = ActiveFlags(lines=True)
        assert flags.defaults() == flags

    def test_defaults_when_inactive(self):
        flags = ActiveFlags()
        defaults = flags.defaults()
        assert defaults.lines is True
        assert defaults.words is True
        assert defaults.bytes_count is True
        assert defaults.chars is False


class TestCalculateWidths:
    """Tests for calculate_widths function."""

    def test_calculate_widths_default_flags(self):
        stats_list = [
            Stats(lines=5, words=20, bytes_count=100),
            Stats(lines=105, words=500, bytes_count=2050),
        ]
        flags = ActiveFlags(lines=True, words=True, bytes_count=True).defaults()
        widths = calculate_widths(stats_list, flags)
        # Should be based on max values: 105 (3 chars), 500 (3 chars), 2050 (4 chars)
        # Minimum width is 7
        assert widths == [7, 7, 7]

    def test_calculate_widths_large_numbers(self):
        stats_list = [
            Stats(lines=12345678, words=999, bytes_count=10),
        ]
        flags = ActiveFlags(lines=True, words=True, bytes_count=True)
        widths = calculate_widths(stats_list, flags)
        assert widths == [8, 7, 7]

    def test_calculate_widths_subset_flags(self):
        stats_list = [Stats(lines=10, words=20, chars=30, bytes_count=40)]
        flags = ActiveFlags(chars=True)
        widths = calculate_widths(stats_list, flags)
        assert widths == [7]


class TestFormatRow:
    """Tests for format_row function."""

    def test_format_row_with_filename(self):
        stats = Stats(lines=1, words=2, bytes_count=12)
        flags = ActiveFlags(lines=True, words=True, bytes_count=True).defaults()
        widths = [7, 7, 7]
        row = format_row(stats, "file.txt", flags, widths)
        assert row == "      1       2      12 file.txt"

    def test_format_row_without_filename(self):
        stats = Stats(lines=1, words=2, bytes_count=12)
        flags = ActiveFlags(lines=True, words=True, bytes_count=True).defaults()
        widths = [7, 7, 7]
        row = format_row(stats, None, flags, widths)
        assert row == "      1       2      12"

    def test_format_row_custom_flags(self):
        stats = Stats(lines=5, words=10, chars=50, bytes_count=50)
        flags = ActiveFlags(chars=True, words=True)
        widths = [7, 7]
        row = format_row(stats, "test.txt", flags, widths)
        assert row == "     10      50 test.txt"


class TestFormatOutput:
    """Tests for format_output function."""

    def test_format_output_empty(self):
        assert format_output([], ActiveFlags()) == ""

    def test_format_output_single_file(self):
        results = [(Stats(lines=1, words=2, bytes_count=5), "file1.txt")]
        flags = ActiveFlags(lines=True, words=True, bytes_count=True).defaults()
        output = format_output(results, flags)
        assert output == "      1       2       5 file1.txt"

    def test_format_output_multiple_files_with_total(self):
        results = [
            (Stats(lines=1, words=2, bytes_count=5), "file1.txt"),
            (Stats(lines=3, words=4, bytes_count=10), "file2.txt"),
        ]
        flags = ActiveFlags(lines=True, words=True, bytes_count=True).defaults()
        output = format_output(results, flags)
        expected = (
            "      1       2       5 file1.txt\n"
            "      3       4      10 file2.txt\n"
            "      4       6      15 total"
        )
        assert output == expected

    def test_format_output_width_accounts_for_total(self):
        results = [
            (Stats(lines=6_000_000, words=1, bytes_count=1), "a.txt"),
            (Stats(lines=6_000_000, words=1, bytes_count=1), "b.txt"),
        ]
        output = format_output(results, ActiveFlags(lines=True))
        rows = output.splitlines()
        assert rows[-1].startswith("12000000 total")
