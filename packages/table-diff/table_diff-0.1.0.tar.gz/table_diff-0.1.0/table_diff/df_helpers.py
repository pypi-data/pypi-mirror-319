"""Helpers for working with Polars DataFrames."""

# SPDX-License-Identifier: MIT
# Copyright (c) 2024 Parker L

import polars as pl


def assert_unique_key(
    df: pl.DataFrame,
    unique_key: list[str] | str,
) -> None:
    """Assert that all rows of `unique_key` are unique.

    Args:
        df: The DataFrame to check.
        unique_key: The column(s) that should be unique.

    Raises:
        AssertionError: If the check fails.

    """
    if isinstance(unique_key, str):
        unique_key = [unique_key]

    df_grouped = (
        df.group_by(unique_key)
        .agg(
            rows_with_this_key=pl.len(),
        )
        .filter(pl.col("rows_with_this_key") > pl.lit(1))
    )
    problem_row_count = df_grouped.height

    if problem_row_count > 0:
        msg = f"{problem_row_count:,}/{df.height:,} rows are not unique"
        raise AssertionError(msg)


def assert_col_has_no_nulls(df: pl.DataFrame, col: str) -> None:
    """Assert that the supplied column has no null values.

    Args:
        df: The DataFrame to check.
        col: The column to check.

    Raises:
        AssertionError: If the check fails.

    """
    non_null_count = df[col].count()
    null_count = df.height - non_null_count
    if null_count > 0:
        msg = f"{null_count:,}/{df.height:,} values in column are null"
        raise AssertionError(msg)


def df_to_markdown(df: pl.DataFrame) -> str:
    """Convert a DataFrame to a markdown table.

    Returns:
        A markdown table string.

    """
    with pl.Config() as cfg:
        cfg.set_tbl_formatting("ASCII_MARKDOWN")
        # TODO: Probably add more options here.
        return str(df)
