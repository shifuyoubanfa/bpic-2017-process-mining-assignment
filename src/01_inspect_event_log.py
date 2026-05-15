"""Initial inspection of the BPIC-17 event log.

This script reads the local BPIC-17 XES file, converts it to a pandas
DataFrame, writes basic metadata/statistics, and creates first inspection
figures for the assignment.
"""

from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pm4py
from pandas.api.types import is_bool_dtype, is_object_dtype, is_string_dtype


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = PROJECT_ROOT / "data" / "BPI Challenge 2017.xes"
RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = PROJECT_ROOT / "figures"

CASE_ID_COL = "case:concept:name"
ACTIVITY_COL = "concept:name"
TIMESTAMP_COL = "time:timestamp"
RESOURCE_COL = "org:resource"


def warn_missing(column: str, metric: str) -> None:
    """Print a clear warning when an expected XES column is unavailable."""
    warnings.warn(
        f"Column '{column}' not found. Skipping metric or plot: {metric}",
        stacklevel=2,
    )


def save_bar_plot(
    counts: pd.Series,
    output_stem: str,
    title: str,
    xlabel: str,
    ylabel: str,
    rotation: int = 45,
) -> None:
    """Save a bar plot in PNG and PDF format."""
    if counts.empty:
        warnings.warn(f"No data available for plot: {title}", stacklevel=2)
        return

    plt.figure(figsize=(12, 6))
    counts.plot(kind="bar")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=rotation, ha="right" if rotation else "center")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / f"{output_stem}.png", dpi=300)
    plt.savefig(FIGURES_DIR / f"{output_stem}.pdf")
    plt.close()


def save_histogram(
    values: pd.Series,
    output_stem: str,
    title: str,
    xlabel: str,
    ylabel: str,
    bins: int = 50,
) -> None:
    """Save a histogram in PNG and PDF format."""
    clean_values = values.dropna()
    if clean_values.empty:
        warnings.warn(f"No data available for plot: {title}", stacklevel=2)
        return

    plt.figure(figsize=(10, 6))
    plt.hist(clean_values, bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / f"{output_stem}.png", dpi=300)
    plt.savefig(FIGURES_DIR / f"{output_stem}.pdf")
    plt.close()


def build_column_overview(df: pd.DataFrame) -> pd.DataFrame:
    """Create a compact overview of all DataFrame columns."""
    rows = []
    for column in df.columns:
        if column.startswith("case:"):
            scope = "case"
        else:
            scope = "event"

        rows.append(
            {
                "column": column,
                "dtype": str(df[column].dtype),
                "attribute_scope": scope,
                "non_null_count": int(df[column].notna().sum()),
                "null_count": int(df[column].isna().sum()),
                "null_share": float(df[column].isna().mean()),
                "n_unique": int(df[column].nunique(dropna=True)),
            }
        )

    return pd.DataFrame(rows)


def calculate_statistics(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.Series | None]:
    """Calculate basic log statistics while tolerating missing XES fields."""
    stats: list[dict[str, float | int | str]] = []

    def add_stat(metric: str, value: float | int | str) -> None:
        stats.append({"metric": metric, "value": value})

    add_stat("number of events", len(df))

    if CASE_ID_COL in df.columns:
        case_lengths = df.groupby(CASE_ID_COL).size()
        add_stat("number of cases", int(case_lengths.shape[0]))
        add_stat("mean case length", float(case_lengths.mean()))
        add_stat("standard deviation of case length", float(case_lengths.std(ddof=0)))
        add_stat("min case length", int(case_lengths.min()))
        add_stat("median case length", float(case_lengths.median()))
        add_stat("max case length", int(case_lengths.max()))
    else:
        warn_missing(CASE_ID_COL, "case counts and case length statistics")
        case_lengths = pd.Series(dtype=float)
        add_stat("number of cases", np.nan)
        add_stat("mean case length", np.nan)
        add_stat("standard deviation of case length", np.nan)
        add_stat("min case length", np.nan)
        add_stat("median case length", np.nan)
        add_stat("max case length", np.nan)

    if ACTIVITY_COL in df.columns:
        add_stat("number of unique activities", int(df[ACTIVITY_COL].nunique(dropna=True)))
    else:
        warn_missing(ACTIVITY_COL, "unique activity count")
        add_stat("number of unique activities", np.nan)

    if RESOURCE_COL in df.columns:
        add_stat("number of resources", int(df[RESOURCE_COL].nunique(dropna=True)))
    else:
        warn_missing(RESOURCE_COL, "resource count")
        add_stat("number of resources", np.nan)

    case_attribute_cols = [
        column
        for column in df.columns
        if column.startswith("case:") and column != CASE_ID_COL
    ]
    event_attribute_cols = [column for column in df.columns if not column.startswith("case:")]
    categorical_event_cols = [
        column
        for column in event_attribute_cols
        if is_string_dtype(df[column])
        or is_object_dtype(df[column])
        or is_bool_dtype(df[column])
    ]
    add_stat("number of case attribute columns", len(case_attribute_cols))
    add_stat("number of event attribute columns", len(event_attribute_cols))
    add_stat("number of categorical event attributes", len(categorical_event_cols))

    variant_counts = None
    if CASE_ID_COL in df.columns and ACTIVITY_COL in df.columns:
        variants = (
            df.groupby(CASE_ID_COL, sort=False)[ACTIVITY_COL]
            .apply(lambda activities: " -> ".join(activities.dropna().astype(str)))
        )
        variant_counts = variants.value_counts()
        add_stat("number of process variants", int(variant_counts.shape[0]))
    else:
        warn_missing(f"{CASE_ID_COL} and/or {ACTIVITY_COL}", "process variant count")
        add_stat("number of process variants", np.nan)

    if CASE_ID_COL in df.columns and TIMESTAMP_COL in df.columns:
        timestamps = pd.to_datetime(df[TIMESTAMP_COL], errors="coerce", utc=True)
        grouped_timestamps = timestamps.groupby(df[CASE_ID_COL])
        case_duration_seconds = (
            grouped_timestamps.max() - grouped_timestamps.min()
        ).dt.total_seconds()
        add_stat("mean case duration in days", float((case_duration_seconds / 86400).mean()))
        add_stat("standard deviation of case duration in days", float((case_duration_seconds / 86400).std(ddof=0)))
        add_stat("mean case duration in minutes", float((case_duration_seconds / 60).mean()))
        add_stat("standard deviation of case duration in minutes", float((case_duration_seconds / 60).std(ddof=0)))
        add_stat("mean case duration in seconds", float(case_duration_seconds.mean()))
        add_stat("standard deviation of case duration in seconds", float(case_duration_seconds.std(ddof=0)))
        add_stat("min case duration in days", float((case_duration_seconds / 86400).min()))
        add_stat("median case duration in days", float((case_duration_seconds / 86400).median()))
        add_stat("max case duration in days", float((case_duration_seconds / 86400).max()))
    else:
        warn_missing(f"{CASE_ID_COL} and/or {TIMESTAMP_COL}", "case duration statistics")
        case_duration_seconds = pd.Series(dtype=float)
        for unit in ("days", "minutes", "seconds"):
            add_stat(f"mean case duration in {unit}", np.nan)
            add_stat(f"standard deviation of case duration in {unit}", np.nan)
        add_stat("min case duration in days", np.nan)
        add_stat("median case duration in days", np.nan)
        add_stat("max case duration in days", np.nan)

    return pd.DataFrame(stats), case_lengths, variant_counts


def create_figures(
    df: pd.DataFrame,
    case_lengths: pd.Series,
    variant_counts: pd.Series | None,
) -> None:
    """Create the initial event log inspection figures."""
    if ACTIVITY_COL in df.columns:
        top_activities = df[ACTIVITY_COL].value_counts().head(15)
        save_bar_plot(
            top_activities,
            "top_15_activities",
            "Top 15 Activities in BPIC-17 Event Log",
            "Activity",
            "Number of Events",
        )
    else:
        warn_missing(ACTIVITY_COL, "top activity plot")

    if not case_lengths.empty:
        save_histogram(
            case_lengths,
            "case_length_distribution",
            "Case Length Distribution in BPIC-17 Event Log",
            "Number of Events per Case",
            "Number of Cases",
        )

    if CASE_ID_COL in df.columns and TIMESTAMP_COL in df.columns:
        timestamps = pd.to_datetime(df[TIMESTAMP_COL], errors="coerce", utc=True)
        grouped_timestamps = timestamps.groupby(df[CASE_ID_COL])
        durations_days = (
            grouped_timestamps.max() - grouped_timestamps.min()
        ).dt.total_seconds() / 86400
        save_histogram(
            durations_days,
            "case_duration_distribution_days",
            "Case Duration Distribution in BPIC-17 Event Log",
            "Case Duration in Days",
            "Number of Cases",
        )
    else:
        warn_missing(f"{CASE_ID_COL} and/or {TIMESTAMP_COL}", "case duration plot")

    if variant_counts is not None and not variant_counts.empty:
        top_variants = variant_counts.head(15)
        variant_labels = [f"Variant {index}" for index in range(1, len(top_variants) + 1)]
        variant_mapping = pd.DataFrame(
            {
                "variant_label": variant_labels,
                "activity_sequence": top_variants.index,
                "case_count": top_variants.values,
            }
        )
        variant_mapping.to_csv(RESULTS_DIR / "top_15_variant_mapping.csv", index=False)

        plot_counts = pd.Series(top_variants.values, index=variant_labels)
        save_bar_plot(
            plot_counts,
            "top_15_variants",
            "Top 15 Process Variants in BPIC-17 Event Log",
            "Variant",
            "Number of Cases",
            rotation=0,
        )
    else:
        warnings.warn("No variant data available for top variant plot.", stacklevel=2)


def main() -> None:
    """Run the event log inspection workflow."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    if not LOG_PATH.exists():
        raise FileNotFoundError(
            f"Event log not found at {LOG_PATH}. "
            "Place the BPIC-17 XES file at data/BPI Challenge 2017.xes."
        )

    # Load the XES file with PM4Py and convert the event log to tabular form.
    print(f"Reading event log from: {LOG_PATH}")
    log = pm4py.read_xes(str(LOG_PATH))
    df = pm4py.convert_to_dataframe(log)

    # Print first-look information for interactive terminal inspection.
    print("\nDataFrame shape:")
    print(df.shape)
    print("\nColumns:")
    print(list(df.columns))
    print("\nDtypes:")
    print(df.dtypes)
    print("\nFirst 10 rows:")
    print(df.head(10))

    # Save metadata and basic statistics for reproducible reporting later.
    column_overview = build_column_overview(df)
    column_overview.to_csv(RESULTS_DIR / "column_overview.csv", index=False)

    statistics, case_lengths, variant_counts = calculate_statistics(df)
    statistics.to_csv(RESULTS_DIR / "basic_log_statistics.csv", index=False)

    # Create first inspection figures using only matplotlib.
    create_figures(df, case_lengths, variant_counts)

    print("\nSaved outputs:")
    print(f"- {RESULTS_DIR / 'column_overview.csv'}")
    print(f"- {RESULTS_DIR / 'basic_log_statistics.csv'}")
    print(f"- {RESULTS_DIR / 'top_15_variant_mapping.csv'}")
    print(f"- {FIGURES_DIR}")


if __name__ == "__main__":
    main()
