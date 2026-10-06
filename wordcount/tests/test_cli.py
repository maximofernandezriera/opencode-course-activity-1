"""Tests for CLI interface using typer CliRunner."""

from __future__ import annotations

import tempfile
import os
import pytest
from typer.testing import CliRunner

from wordcount.cli import app

runner = CliRunner()


class TestCLI:
    """End-to-end tests for wordcount CLI."""

    def test_help(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "wordcount" in result.output
        assert "Cuenta líneas" in result.output

    def test_stdin_default(self):
        result = runner.invoke(app, input="hello world\n")
        assert result.exit_code == 0
        assert "1" in result.output
        assert "2" in result.output
        assert "12" in result.output  # bytes/chars

    def test_stdin_explicit_dash(self):
        result = runner.invoke(app, ["-"], input="foo bar\n")
        assert result.exit_code == 0
        assert "2" in result.output  # 2 words

    def test_single_file(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("hola mundo\n")
            path = f.name

        try:
            result = runner.invoke(app, [path])
            assert result.exit_code == 0
            assert path in result.output
            assert "1" in result.output
            assert "2" in result.output
            assert "11" in result.output
        finally:
            os.unlink(path)

    def test_multiple_files(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f1:
            f1.write("file one\n")
            path1 = f1.name

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f2:
            f2.write("file two here\n")
            path2 = f2.name

        try:
            result = runner.invoke(app, [path1, path2])
            assert result.exit_code == 0
            assert path1 in result.output
            assert path2 in result.output
            assert "total" in result.output
        finally:
            os.unlink(path1)
            os.unlink(path2)

    def test_specific_flags(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("one two three\n")
            path = f.name

        try:
            # Test only lines (-l)
            result = runner.invoke(app, ["-l", path])
            assert result.exit_code == 0
            assert "1" in result.output
            assert "three" not in result.output

            # Test only words (-w)
            result = runner.invoke(app, ["-w", path])
            assert result.exit_code == 0
            assert "3" in result.output

            # Test chars (-m) and bytes (-c)
            result = runner.invoke(app, ["-m", "-c", path])
            assert result.exit_code == 0
            assert "14" in result.output  # chars or bytes
        finally:
            os.unlink(path)

    def test_chars_and_bytes_differ_for_unicode(self):
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False) as f:
            f.write("café\n")
            path = f.name

        try:
            chars_result = runner.invoke(app, ["-m", path])
            bytes_result = runner.invoke(app, ["-c", path])
            assert chars_result.exit_code == 0
            assert bytes_result.exit_code == 0
            assert "5" in chars_result.output
            assert "6" in bytes_result.output
        finally:
            os.unlink(path)

    def test_stdin_mixed_with_file(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("one\n")
            path = f.name

        try:
            result = runner.invoke(app, [path, "-"], input="two words\n")
            assert result.exit_code == 0
            assert path in result.output
            assert " -" in result.output
            assert "total" in result.output
        finally:
            os.unlink(path)

    def test_file_not_found(self):
        result = runner.invoke(app, ["/nonexistent/file_abc123.txt"])
        assert result.exit_code == 1
        assert "No such file" in result.output or "No existe el fichero" in result.output or "wordcount:" in result.output

    def test_mixed_existing_and_nonexistent(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            f.write("test content\n")
            path = f.name

        try:
            nonexistent = "/nonexistent/file_xyz987.txt"
            result = runner.invoke(app, [path, nonexistent])
            assert result.exit_code == 1
            assert path in result.output
            assert "wordcount:" in result.output
        finally:
            os.unlink(path)
