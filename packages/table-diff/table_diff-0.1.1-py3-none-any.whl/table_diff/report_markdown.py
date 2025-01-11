"""Tools to generate a plain text diff report for table_diff."""

# SPDX-License-Identifier: MIT
# Copyright (c) 2024 Parker L

import polars as pl

from table_diff.df_helpers import df_to_markdown
from table_diff.diff_evaluate import (
    assert_df_ready_for_compare,
    compare_each_column_into_table,
    compare_for_general_observations,
    regroup_column_diffs_by_type,
)
from table_diff.diff_types import ColumnDiff, CompareColsResult, CompareUniqueKeyResult


def generate_markdown_report(
    df_old: pl.DataFrame,
    df_new: pl.DataFrame,
    *,
    unique_key: list[str],
    old_filename: str | None = None,
    new_filename: str | None = None,
    # TODO: Add settings about which diff types to include, etc.
) -> str:
    """Generate a plain text report of the differences between two DataFrames.

    Returns:
        A string representation of the differences between the two DataFrames.

    """
    assert_df_ready_for_compare(df_old, unique_key=unique_key)
    assert_df_ready_for_compare(df_new, unique_key=unique_key)

    compare_unique_key_result = CompareUniqueKeyResult.evaluate(
        df_old, df_new, unique_key=unique_key
    )
    compare_cols_result = CompareColsResult.evaluate(df_old, df_new, unique_key=unique_key)
    column_diffs: dict[str, ColumnDiff] = compare_each_column_into_table(
        df_old, df_new, unique_key=unique_key, compare_cols_result=compare_cols_result
    )
    general_observations = compare_for_general_observations(
        df_old,
        df_new,
        unique_key=unique_key,
        compare_unique_key_result=compare_unique_key_result,
        compare_cols_result=compare_cols_result,
    )

    lines = [
        "# Comparison of the two DataFrames",
        "",
        f"* Comparing `{old_filename}` (old, left) to `{new_filename}` (new, right)",
        # Hide: f"* Columns to compare: {compare_cols_result.compare_cols}",
    ]

    if len(unique_key) == 1:
        lines.append(f"* Unique key: `{unique_key[0]}`")
    else:
        lines.append(f"* Unique key ({len(unique_key)} columns):")
        lines.extend([f"    * `{col}`" for col in unique_key])

    lines.append("")

    # General observations
    lines.extend(["## General Observations", ""])
    if general_observations:
        lines.extend([f"* {observation}" for observation in general_observations])
    else:
        lines.append("No general observations.")

    # Columns in both
    lines.extend(["", "## Column Comparison", ""])

    lines.append(
        "### Columns in both DataFrames" f" [{len(compare_cols_result.cols_in_both)} cols]"
    )
    for col in compare_cols_result.cols_in_both:
        if col in unique_key:
            lines.append(f"* `{col}` (Unique Key)")
        else:
            lines.append(f"* `{col}` ({column_diffs[col].row_difference_description})")
    lines.append("")  # noqa: FURB113

    # Columns in old only
    lines.append(
        "### Columns in old DataFrame only (DROPPED) "
        f"[{len(compare_cols_result.cols_in_old_only)} cols]"
    )
    lines.extend([f"* `{col}`" for col in compare_cols_result.cols_in_old_only] + [""])

    # Columns in new only
    lines.append(
        "### Columns in new DataFrame only (ADDED)"
        f" [{len(compare_cols_result.cols_in_new_only)} cols]"
    )
    lines.extend([f"* `{col}`" for col in compare_cols_result.cols_in_new_only] + [""])

    # Rows
    lines.extend(["## Row Comparison (Unique Key)", ""])
    lines.extend(
        [
            f"* Rows in old: {df_old.height:,}",
            f"* Rows in new: {df_new.height:,}",
            f"* Rows added (new only): {compare_unique_key_result.rows_added_count:,}",
            f"* Rows removed (old only): {compare_unique_key_result.rows_removed_count:,}",
            f"* Rows in both: {compare_unique_key_result.rows_in_both_sides_count:,}",
            "",
        ]
    )

    lines.extend(
        [
            "### Rows Added",
            f"{compare_unique_key_result.rows_added_count:,} rows added.",
            df_to_markdown(compare_unique_key_result.df_rows_added),
            "",
            "### Rows Removed",
            f"{compare_unique_key_result.rows_removed_count:,} rows removed.",
            df_to_markdown(compare_unique_key_result.df_rows_removed),
            "",
            "### Rows in Both",
            f"{compare_unique_key_result.rows_in_both_sides_count:,} rows in both old and new.",
            df_to_markdown(compare_unique_key_result.df_rows_in_both),
            "",
        ]
    )

    regroup_column_diffs_by_type(column_diffs)

    # Column diffs
    lines.extend(["## Column Diffs", ""])
    for col_diff in column_diffs.values():
        lines.extend(col_diff.to_markdown_str().splitlines())
        lines.append("")

    lines.extend(["", ""])

    # TODO: Could do the join with a system-specific newline character selection.
    return "\n".join(lines)
