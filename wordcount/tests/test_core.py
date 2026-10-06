"""Tests for core counting logic."""

from __future__ import annotations
import io
import tempfile
import os

import pytest

from wordcount.core import Stats, count_stream, count_file


class TestStats:
    """Tests for Stats dataclass."""

    def test_default_values(self):
        s = Stats()
        assert s.lines == 0
        assert s.words == 0
        assert s.chars == 0
        assert s.bytes_count == 0

    def test_custom_values(self):
        s = Stats(lines=10, words=5, chars=50, bytes_count=50)
        assert s.lines == 10
        assert s.words == 5
        assert s.chars == 50
        assert s.bytes_count == 50

    def test_add_method(self):
        s1 = Stats(lines=5, words=10, chars=50, bytes_count=50)
        s2 = Stats(lines=3, words=7, chars=30, bytes_count=30)
        s3 = s1.add(s2)
        assert s3.lines == 8
        assert s3.words == 17
        assert s3.chars == 80
        assert s3.bytes_count == 80

    def test_add_operator(self):
        s1 = Stats(lines=5, words=10, chars=50, bytes_count=50)
        s2 = Stats(lines=3, words=7, chars=30, bytes_count=30)
        s3 = s1 + s2
        assert s3.lines == 8
        assert s3.words == 17
        assert s3.chars == 80
        assert s3.bytes_count == 80

    def test_frozen_dataclass(self):
        s = Stats(lines=5)
        with pytest.raises(AttributeError):
            s.lines = 10

    def test_equality(self):
        s1 = Stats(lines=5, words=10, chars=50, bytes_count=50)
        s2 = Stats(lines=5, words=10, chars=50, bytes_count=50)
        s3 = Stats(lines=3, words=7, chars=30, bytes_count=30)
        assert s1 == s2
        assert s1 != s3


class TestCountStream:
    """Tests for count_stream function."""

    def test_empty_stream(self):
        stream = io.StringIO("")
        stats = count_stream(stream)
        assert stats == Stats()

    def test_empty_bytes_stream(self):
        stream = io.BytesIO(b"")
        stats = count_stream(stream)
        assert stats == Stats()

    def test_single_line_no_newline(self):
        stream = io.StringIO("hello world")
        stats = count_stream(stream)
        assert stats.lines == 0
        assert stats.words == 2
        assert stats.chars == 11
        assert stats.bytes_count == 11

    def test_single_line_with_newline(self):
        stream = io.StringIO("hello world\n")
        stats = count_stream(stream)
        assert stats.lines == 1
        assert stats.words == 2
        assert stats.chars == 12
        assert stats.bytes_count == 12

    def test_multiple_lines(self):
        stream = io.StringIO("line one\nline two\nline three\n")
        stats = count_stream(stream)
        assert stats.lines == 3
        assert stats.words == 6
        assert stats.chars == 29
        assert stats.bytes_count == 29

    def test_multiple_spaces_and_tabs(self):
        stream = io.StringIO("  hello    world\t\tfoo  ")
        stats = count_stream(stream)
        assert stats.words == 3

    def test_unicode_characters(self):
        # Spanish accents
        stream = io.StringIO("café niño")
        stats = count_stream(stream)
        assert stats.chars == 9  # café (4) + space (1) + niño (4)
        assert stats.bytes_count == 11  # café (5 bytes) + space (1) + niño (5 bytes)

    def test_emoji(self):
        stream = io.StringIO("😀 🎉")
        stats = count_stream(stream)
        assert stats.chars == 3  # emoji + space + emoji
        # Each emoji is 4 bytes in UTF-8
        assert stats.bytes_count == 9  # 4 + 1 + 4

    def test_cjk_characters(self):
        stream = io.StringIO("你好世界")
        stats = count_stream(stream)
        assert stats.chars == 4
        # Each CJK char is 3 bytes in UTF-8
        assert stats.bytes_count == 12

    def test_binary_stream(self):
        stream = io.BytesIO(b"hello world\n")
        stats = count_stream(stream)
        assert stats.lines == 1
        assert stats.words == 2
        assert stats.chars == 12
        assert stats.bytes_count == 12

    def test_binary_stream_unicode(self):
        stream = io.BytesIO("café\n".encode("utf-8"))
        stats = count_stream(stream)
        assert stats.lines == 1
        assert stats.words == 1
        assert stats.chars == 5  # café + \n
        assert stats.bytes_count == 6  # café (5 bytes) + \n (1 byte)

    def test_binary_stream_invalid_utf8(self):
        # Invalid UTF-8 sequence
        stream = io.BytesIO(b"hello \xff world\n")
        stats = count_stream(stream)
        assert stats.lines == 1
        assert stats.words == 3  # "hello", replacement char, "world"
        assert stats.bytes_count == 14

    def test_streaming_chunks(self):
        # Words are counted correctly when a token crosses a chunk boundary.
        large_text = "x" * 20000
        stream = io.StringIO(large_text)
        stats = count_stream(stream)
        assert stats.words == 1
        assert stats.chars == 20000

    def test_binary_unicode_across_chunk_boundary(self):
        text = "a" * 8191 + "é b"
        stats = count_stream(io.BytesIO(text.encode("utf-8")))
        assert stats.words == 2
        assert stats.chars == len(text)
        assert stats.bytes_count == len(text.encode("utf-8"))

    def test_only_newlines(self):
        stream = io.StringIO("\n\n\n")
        stats = count_stream(stream)
        assert stats.lines == 3
        assert stats.words == 0
        assert stats.chars == 3
        assert stats.bytes_count == 3

    def test_mixed_whitespace(self):
        stream = io.StringIO(" \t\n \t \n")
        stats = count_stream(stream)
        assert stats.lines == 2
        assert stats.words == 0


class TestCountFile:
    """Tests for count_file function."""

    def test_count_file_basic(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("hello world\nthis is a test\n")
            temp_path = f.name

        try:
            stats = count_file(temp_path)
            assert stats.lines == 2
            assert stats.words == 6
            assert stats.chars == 27
            assert stats.bytes_count == 27
        finally:
            os.unlink(temp_path)

    def test_count_file_unicode(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("café\nniño\n")
            temp_path = f.name

        try:
            stats = count_file(temp_path)
            assert stats.lines == 2
            assert stats.words == 2
            assert stats.chars == 10
            # Bytes: café = 5 bytes, \n = 1, niño = 5, \n = 1, total = 12
            assert stats.bytes_count == 12
        finally:
            os.unlink(temp_path)

    def test_count_file_empty(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_path = f.name

        try:
            stats = count_file(temp_path)
            assert stats == Stats()
        finally:
            os.unlink(temp_path)

    def test_count_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            count_file("/nonexistent/file.txt")

    def test_count_file_is_directory(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(OSError):
                count_file(tmpdir)
