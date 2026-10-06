"""CLI entry point for wordcount."""

from __future__ import annotations
import sys
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from .core import count_file, count_stream, Stats
from .formatter import ActiveFlags, format_output

app = typer.Typer(
    add_completion=False,
    help="wordcount - Cuenta líneas, palabras y caracteres (estilo wc).",
    no_args_is_help=False,
)


@app.command(name="wordcount")
def main(
    files: Annotated[
        Optional[list[Path]],
        typer.Argument(help="Archivos a procesar (stdin si se omite o '-')"),
    ] = None,
    lines: Annotated[
        bool,
        typer.Option("-l", "--lines", help="Contar líneas"),
    ] = False,
    words: Annotated[
        bool,
        typer.Option("-w", "--words", help="Contar palabras"),
    ] = False,
    chars: Annotated[
        bool,
        typer.Option("-m", "--chars", help="Contar caracteres"),
    ] = False,
    bytes_flag: Annotated[
        bool,
        typer.Option("-c", "--bytes", help="Contar bytes"),
    ] = False,
) -> None:
    """
    Cuenta líneas, palabras, caracteres y bytes en archivos o stdin.

    Comportamiento similar a wc(1). Si no se especifica ninguna opción,
    se muestran líneas, palabras y bytes por defecto.
    """
    # Build flags with defaults
    flags = ActiveFlags(
        lines=lines,
        words=words,
        chars=chars,
        bytes_count=bytes_flag,
    ).defaults()

    # With no paths, read stdin without printing an input name (like wc).
    if files is None:
        stats = count_stream(sys.stdin)
        output = format_output([(stats, None)], flags)
        typer.echo(output)
        return

    # Process multiple files
    results: list[tuple[Stats, Optional[str]]] = []
    exit_code = 0

    for filepath in files:
        try:
            if str(filepath) == "-":
                stats = count_stream(sys.stdin)
                name = None if len(files) == 1 else "-"
            else:
                stats = count_file(str(filepath))
                name = str(filepath)
            results.append((stats, name))
        except OSError as e:
            typer.echo(f"wordcount: {filepath}: {e.strerror}", err=True)
            exit_code = 1

    if results:
        output = format_output(results, flags)
        typer.echo(output)

    # Exit with error code if any file failed
    raise typer.Exit(code=exit_code)


if __name__ == "__main__":
    app()
