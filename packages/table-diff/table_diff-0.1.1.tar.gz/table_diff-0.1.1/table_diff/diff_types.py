"""Types which represent the output of a diff."""

# SPDX-License-Identifier: MIT
# Copyright (c) 2024 Parker L

from dataclasses import dataclass
from typing import Literal

import polars as pl
from ordered_set import OrderedSet
from polars.datatypes.group import FLOAT_DTYPES

from table_diff.df_helpers import df_to_markdown
from table_diff.log_helpers import format_frac, format_list_with_count


@dataclass(kw_only=True)
class CompareColsResult:
    """Representation of the difference between two tables, in terms of columns.

    Returns:
        A list of general observations about the differences between the two tables.

    """

    cols_in_old: list[str]
    cols_in_new: list[str]
    cols_in_old_only: list[str]  # "dropped"
    cols_in_new_only: list[str]  # "added"
    cols_in_both: list[str]

    unique_key: list[str]
    compare_cols: list[str]  # columns to compare the values in

    @staticmethod
    def evaluate(
        df_old: pl.DataFrame, df_new: pl.DataFrame, *, unique_key: list[str]
    ) -> "CompareColsResult":
        """Construct self by evaluating the difference between the cols.

        Returns:
            A CompareColsResult object.

        """
        # Intersection: in both sets, using NEW sort order
        cols_in_both = OrderedSet(df_new.columns) & OrderedSet(df_old.columns)

        return CompareColsResult(
            cols_in_old=df_old.columns,
            cols_in_new=df_new.columns,
            cols_in_old_only=list(OrderedSet(df_old.columns) - set(df_new.columns)),
            cols_in_new_only=list(OrderedSet(df_new.columns) - set(df_old.columns)),
            cols_in_both=list(cols_in_both),
            unique_key=unique_key,
            compare_cols=list(cols_in_both - set(unique_key)),
        )

    def to_log_str(self: "CompareColsResult") -> str:
        """Convert to string for logging.

        Returns:
            A string representation of the comparison.

        """
        lines = [
            "==== Column Name Comparison ====",
            ("Columns in both tables " + format_list_with_count(self.cols_in_both, "col")),
            (
                "Columns in old but not new (DROPPED) "
                + format_list_with_count(self.cols_in_old_only, "col")
            ),
            (
                "Columns in new but not old (ADDED) "
                + format_list_with_count(self.cols_in_new_only, "col")
            ),
        ]

        return "\n".join(lines)


@dataclass(kw_only=True)
class CompareUniqueKeyResult:
    """Representation of difference between two tables, in terms of rows added/removed by the PK.

    The difference looks at the unique key being added/removed/in common.
    """

    rows_added_count: int
    rows_removed_count: int
    rows_in_both_sides_count: int

    df_rows_added: pl.DataFrame
    df_rows_removed: pl.DataFrame
    df_rows_in_both: pl.DataFrame

    @staticmethod
    def evaluate(
        df_old: pl.DataFrame, df_new: pl.DataFrame, *, unique_key: list[str]
    ) -> "CompareUniqueKeyResult":
        """Construct self by determining the differences between the primary keys.

        Returns:
            A CompareUniqueKeyResult object.

        """
        # Primary key comparison
        # Check for rows in old that are not in new.
        # Note: Both anti joins are 1:1.
        df_rows_added = df_new.join(df_old, on=unique_key, how="anti", join_nulls=True)
        df_rows_removed = df_old.join(df_new, on=unique_key, how="anti", join_nulls=True)

        df_rows_in_both = df_old.join(
            df_new, on=unique_key, how="inner", validate="1:1", join_nulls=True
        )

        return CompareUniqueKeyResult(
            rows_added_count=df_rows_added.height,
            rows_removed_count=df_rows_removed.height,
            rows_in_both_sides_count=df_rows_in_both.height,
            df_rows_added=df_rows_added,
            df_rows_removed=df_rows_removed,
            df_rows_in_both=df_rows_in_both,
        )


@dataclass(kw_only=True)
class ColumnDiff:
    """Representation of the difference between a column."""

    column_name: str
    df_diff: pl.DataFrame

    row_difference_count: int
    row_difference_summary: Literal["No rows differ.", "Some rows differ.", "All rows differ."]
    row_difference_description: str

    count_val_to_null: int
    count_null_to_val: int
    count_val_to_val: int

    total_rows_cnt: int

    @staticmethod
    def evaluate(
        column_name: str,
        df_old_cmp: pl.DataFrame,
        df_new_cmp: pl.DataFrame,
        *,
        unique_key: list[str],
    ) -> "ColumnDiff":
        """Compare a single column between old and new.

        Returns:
            A ColumnDiff object representing the comparison between the two columns.

        """
        df_col_compare = df_old_cmp.select(
            [*unique_key, pl.col(column_name).alias(f"{column_name}_OLD")]
        ).join(
            df_new_cmp.select([*unique_key, pl.col(column_name).alias(f"{column_name}_NEW")]),
            on=unique_key,
            how="inner",
            validate="1:1",
        )
        total_rows_cnt = df_col_compare.height

        # Create a df of the mismatched rows for this column
        if (
            df_old_cmp[column_name].dtype in FLOAT_DTYPES
            and df_new_cmp[column_name].dtype in FLOAT_DTYPES
        ):
            # Floats are tricky, so we'll compare to within 0.001% of the mean of the two values
            # TODO: might want to be a bit more precise for lat/long values
            df_col_compare_diff = df_col_compare.filter(  # type: ignore reportUnknownMemberType
                (pl.col(f"{column_name}_OLD") - pl.col(f"{column_name}_NEW")).abs()
                > (
                    pl.lit(0.00001)
                    * pl.mean_horizontal(
                        pl.col(f"{column_name}_OLD"), pl.col(f"{column_name}_NEW")
                    ).abs()
                )
            )

        elif df_old_cmp[column_name].dtype != df_new_cmp[column_name].dtype:
            # Cast to string for comparison.
            df_col_compare_diff = df_col_compare.filter(  # type: ignore reportUnknownMemberType
                pl.col(f"{column_name}_OLD")
                .cast(pl.String)
                .eq_missing(pl.col(f"{column_name}_NEW").cast(pl.String))
                .not_()
            )

        else:
            df_col_compare_diff = df_col_compare.filter(  # type: ignore reportUnknownMemberType
                pl.col(f"{column_name}_OLD").eq_missing(pl.col(f"{column_name}_NEW")).not_()
            )

        # Categorize each value transition.
        df_col_compare_diff = df_col_compare_diff.with_columns(
            ANALYSIS_transition_type=(
                pl.when(
                    pl.col(f"{column_name}_OLD").is_null()
                    & pl.col(f"{column_name}_NEW").is_not_null()
                )
                .then(pl.lit("null_to_val"))
                .when(
                    pl.col(f"{column_name}_OLD").is_not_null()
                    & pl.col(f"{column_name}_NEW").is_null()
                )
                .then(pl.lit("val_to_null"))
                .when(
                    pl.col(f"{column_name}_OLD").is_not_null()
                    & pl.col(f"{column_name}_NEW").is_not_null()
                )
                .then(pl.lit("val_to_val"))
                .otherwise(pl.lit("ERROR"))
            )
        )

        # This to-Enum conversion is mostly an assert against the 'ERROR' case.
        df_col_compare_diff = df_col_compare_diff.with_columns(
            pl.col("ANALYSIS_transition_type").cast(
                pl.Enum(["null_to_val", "val_to_null", "val_to_val"])
            )
        )

        # Summarize the changes.
        if df_col_compare_diff.height == 0:
            row_difference_description = "NO DIFFERENCE"
            row_difference_summary = "No rows differ."
        elif df_col_compare_diff.height == total_rows_cnt:
            row_difference_description = f"ALL {df_col_compare_diff.height:,} ROWS DIFFER"
            row_difference_summary = "Some rows differ."
        else:
            row_difference_description = "SOME ROWS DIFFER: " + format_frac(
                df_col_compare_diff.height, total_rows_cnt
            )
            row_difference_summary = "All rows differ."

        # Do some counting.
        count_null_to_val = df_col_compare_diff.filter(  # type: ignore reportUnknownMemberType
            pl.col("ANALYSIS_transition_type") == pl.lit("null_to_val")
        ).height
        count_val_to_null = df_col_compare_diff.filter(  # type: ignore reportUnknownMemberType
            pl.col("ANALYSIS_transition_type") == pl.lit("val_to_null")
        ).height
        count_val_to_val = df_col_compare_diff.filter(  # type: ignore reportUnknownMemberType
            pl.col("ANALYSIS_transition_type") == pl.lit("val_to_val")
        ).height

        return ColumnDiff(
            column_name=column_name,
            df_diff=df_col_compare_diff,
            row_difference_count=df_col_compare_diff.height,
            row_difference_summary=row_difference_summary,
            row_difference_description=row_difference_description,
            count_null_to_val=count_null_to_val,
            count_val_to_null=count_val_to_null,
            count_val_to_val=count_val_to_val,
            total_rows_cnt=total_rows_cnt,
        )

    def to_log_str(self: "ColumnDiff") -> str:
        """Convert to string for logging.

        Returns:
            A string representation of the comparison, for logging purposes.

        """
        # TODO: Add the transition type counts here, probably
        out = (
            f"==== Column '{self.column_name}' Comparison: "
            f"{self.row_difference_description} ===="
        )

        if self.df_diff.height > 0:
            out += "\n" + str(self.df_diff)

        return out

    def to_markdown_str(self: "ColumnDiff") -> str:
        """Convert to string for markdown.

        Returns:
            A string representation of the comparison, for markdown purposes.

        """
        out = [
            (
                f'### Column "`{self.column_name}`" Comparison '
                f"({self.row_difference_count / self.total_rows_cnt:.1%})"
            ),
            f"* {self.row_difference_description}",  # Like 'NO DIFFERENCE' or 'SOME ROWS ...'
        ]

        if self.df_diff.height > 0:
            if self.count_null_to_val > 0:
                out.append(f"    * {self.count_null_to_val:,} rows changed from NULL to a value.")
            if self.count_val_to_null > 0:
                out.append(f"    * {self.count_val_to_null:,} rows changed from a value to NULL.")
            if self.count_val_to_val > 0:
                out.append(
                    f"    * {self.count_val_to_val:,} rows changed from one value to another."
                )

            out.append("\n" + df_to_markdown(self.df_diff))

            # TODO: Try grouping by [old_val, new_val], and if any stand out as common (e.g.,
            # >0.5% of rows), mention that here as a new table (top 10 old-new pairs).

        return "\n".join(out)
