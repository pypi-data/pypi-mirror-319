"""CLI (Command Line Interface) entry point for table_diff."""

# SPDX-License-Identifier: MIT
# Copyright (c) 2024 Parker L

import json
import sys
from pathlib import Path

import polars as pl
import typed_argparse as tap
from ordered_set import OrderedSet

from table_diff.pdf_export import export_markdown_to_pdf
from table_diff.report_markdown import generate_markdown_report


def load_table(path: Path) -> pl.DataFrame:
    """Load a table from a CSV or Parquet file.

    Args:
        path (Path): The path to the file.

    Returns:
        pl.DataFrame: The loaded DataFrame.

    Raises:
        ValueError: If the file format is not supported.

    """
    if path.suffix.lower() == ".csv":
        return pl.read_csv(path)
    if path.suffix.lower() in {".parquet", ".pq"}:
        return pl.read_parquet(path)

    # Else:
    msg = f"Unsupported file format: {path.suffix}"
    raise ValueError(msg)


class Args(tap.TypedArgs):
    """CLI arguments for table_diff."""

    old_path: Path = tap.arg(
        "--old",
        positional=True,
        help="Path to the old CSV/Parquet table.",
    )
    new_path: Path = tap.arg(
        "--new",
        positional=True,
        help="Path to the new CSV/Parquet table.",
    )
    unique_key: list[str] | None = tap.arg(
        "-u",
        "--unique-key",
        nargs="*",
        help="Column(s) that form a unique key for the DataFrames.",
    )
    output_markdown_path: Path | None = tap.arg(
        "--md",
        "--markdown",
        "--output",
        help="Optional path to save the report. If not provided, the report is printed to stdout.",
    )
    output_pdf_path: Path | None = tap.arg(
        "--pdf",
        help="Optional path to save the report as a PDF. If not provided, PDF is not generated.",
    )


def runner(args: Args) -> None:
    """Run the main application with the provided arguments.

    Raises:
        FileNotFoundError: If the specified file does not exist.

    """
    path_old = args.old_path
    path_new = args.new_path

    if not path_old.exists():
        msg = f"File not found: {path_old}"
        raise FileNotFoundError(msg)
    if not path_new.exists():
        msg = f"File not found: {path_new}"
        raise FileNotFoundError(msg)

    df_old = load_table(path_old)
    df_new = load_table(path_new)

    if (args.unique_key is None) or (len(args.unique_key) == 0):
        # No unique key provided. For now, just print the common columns and exit.
        # TODO: Could try to automatically-detect columns by working lef-to-right.
        common_cols = OrderedSet(df_new.columns) & OrderedSet(df_old.columns)
        sys.stderr.write("No unique key provided. Columns present in both tables:\n\n")
        sys.stderr.write(json.dumps(list(common_cols)))
        sys.stderr.write("\n\n")
        sys.stderr.write("Please provide a unique key using: -u col1 col2")
        sys.stderr.write("\n")
        sys.exit(3)

    else:  # `unique_key` is provided
        unique_key: list[str] = args.unique_key

    report = generate_markdown_report(
        df_old,
        df_new,
        unique_key=unique_key,
        old_filename=path_old.name,
        new_filename=path_new.name,
    )

    if args.output_markdown_path:
        args.output_markdown_path.write_text(report)
    else:
        sys.stdout.write(report)

    if args.output_pdf_path:
        export_markdown_to_pdf(report, args.output_pdf_path)


def main() -> None:
    """CLI entry point for table_diff."""
    tap.Parser(Args).bind(runner).run()


if __name__ == "__main__":
    main()
