"""
data_processing.py
------------------
Handles all data loading, cleaning, and preprocessing for the Gaming Analytics Dashboard.
Dataset columns: Game Name, Genre, Platform, Release Year, User Rating
"""

from __future__ import annotations

import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st


# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
DATA_DIR = Path(__file__).parent.parent  # project root
CSV_FILENAME = "games_dataset.csv"


# ─────────────────────────────────────────────
# Load & Cache
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_raw_data() -> "pd.DataFrame | None":
    """
    Load the raw CSV from the project root.
    Returns None and shows an error if the file is not found.
    """
    csv_path = DATA_DIR / CSV_FILENAME
    if not csv_path.exists():
        st.error(
            f"⚠️ Dataset not found at `{csv_path}`. "
            "Please place **games_dataset.csv** in the project root folder."
        )
        return None
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as exc:
        st.error(f"Failed to read CSV: {exc}")
        return None


@st.cache_data(show_spinner=False)
def clean_data(df: pd.DataFrame) -> "tuple[pd.DataFrame, dict]":
    """
    Clean and preprocess the raw dataframe.

    Cleaning steps:
    1. Rename columns to snake_case for consistency.
    2. Strip leading/trailing whitespace from string columns.
    3. Drop exact duplicate rows.
    4. Cast Release Year to integer (drop rows where it's unparseable).
    5. Cast User Rating to float (drop rows where it's unparseable).
    6. Clip ratings to [0, 10] to remove impossible values.
    7. Standardise capitalisation for Genre, Platform, Game Name.

    Returns
    -------
    cleaned_df : pd.DataFrame
        The cleaned dataframe.
    report : dict
        A summary of cleaning actions performed.
    """
    if df is None:
        return pd.DataFrame(), {}

    report = {}
    cleaned = df.copy()

    # ── 1. Rename columns ────────────────────
    col_map = {}
    for c in cleaned.columns:
        col_map[c] = (
            c.strip()
             .lower()
             .replace(" ", "_")
             .replace("-", "_")
        )
    cleaned.rename(columns=col_map, inplace=True)
    report["column_rename"] = col_map

    # ── 2. Strip whitespace from strings ─────
    str_cols = cleaned.select_dtypes(include=["object", "string"]).columns
    for col in str_cols:
        cleaned[col] = cleaned[col].astype(str).str.strip()
    report["whitespace_stripped_cols"] = list(str_cols)

    # ── 3. Drop exact duplicates ──────────────
    before_dedup = len(cleaned)
    cleaned.drop_duplicates(inplace=True)
    cleaned.reset_index(drop=True, inplace=True)
    report["duplicates_removed"] = before_dedup - len(cleaned)

    # ── 4. Fix Release Year ───────────────────
    before_year = len(cleaned)
    cleaned["release_year"] = pd.to_numeric(cleaned["release_year"], errors="coerce")
    cleaned.dropna(subset=["release_year"], inplace=True)
    cleaned["release_year"] = cleaned["release_year"].astype(int)
    report["rows_dropped_bad_year"] = before_year - len(cleaned)

    # ── 5. Fix User Rating ────────────────────
    before_rating = len(cleaned)
    cleaned["user_rating"] = pd.to_numeric(cleaned["user_rating"], errors="coerce")
    cleaned.dropna(subset=["user_rating"], inplace=True)
    report["rows_dropped_bad_rating"] = before_rating - len(cleaned)

    # ── 6. Clip ratings ───────────────────────
    clipped = ((cleaned["user_rating"] < 0) | (cleaned["user_rating"] > 10)).sum()
    cleaned["user_rating"] = cleaned["user_rating"].clip(0, 10)
    report["ratings_clipped"] = int(clipped)

    # ── 7. Standardise text capitalisation ───
    for col in ["game_name", "genre", "platform"]:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].str.title()

    # ── 8. Replace lingering "nan" strings ───
    cleaned.replace("Nan", np.nan, inplace=True)
    cleaned.replace("nan", np.nan, inplace=True)

    cleaned.reset_index(drop=True, inplace=True)
    report["final_row_count"] = len(cleaned)
    report["final_col_count"] = len(cleaned.columns)

    return cleaned, report


def get_data() -> "tuple[pd.DataFrame, pd.DataFrame, dict]":
    """
    Convenience wrapper: returns (raw_df, cleaned_df, cleaning_report).
    """
    raw = load_raw_data()
    if raw is None:
        return pd.DataFrame(), pd.DataFrame(), {}
    cleaned, report = clean_data(raw)
    return raw, cleaned, report


def get_filter_options(df: pd.DataFrame) -> dict:
    """
    Extract unique sorted values for every filterable column.
    Returns a dict keyed by column name.
    """
    options = {}
    for col in ["genre", "platform", "game_name"]:
        if col in df.columns:
            vals = sorted(df[col].dropna().unique().tolist())
            options[col] = vals

    if "release_year" in df.columns:
        years = sorted(df["release_year"].dropna().unique().astype(int).tolist())
        options["release_year"] = years

    if "user_rating" in df.columns:
        options["user_rating_min"] = float(df["user_rating"].min())
        options["user_rating_max"] = float(df["user_rating"].max())

    return options


def apply_filters(
    df: pd.DataFrame,
    genres: list,
    platforms: list,
    year_range: tuple,
    rating_range: tuple,
) -> pd.DataFrame:
    """
    Apply sidebar filter selections and return the filtered dataframe.
    """
    filtered = df.copy()

    if genres and "genre" in filtered.columns:
        filtered = filtered[filtered["genre"].isin(genres)]

    if platforms and "platform" in filtered.columns:
        filtered = filtered[filtered["platform"].isin(platforms)]

    if "release_year" in filtered.columns:
        filtered = filtered[
            (filtered["release_year"] >= year_range[0])
            & (filtered["release_year"] <= year_range[1])
        ]

    if "user_rating" in filtered.columns:
        filtered = filtered[
            (filtered["user_rating"] >= rating_range[0])
            & (filtered["user_rating"] <= rating_range[1])
        ]

    return filtered.reset_index(drop=True)
