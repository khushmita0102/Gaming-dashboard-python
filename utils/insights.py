"""
insights.py
-----------
Dynamically calculates key insights from the currently filtered dataset.
All insights are recalculated on every filter change — nothing is hardcoded.
No emojis in icon field (design requirement); icons kept as empty string.
"""

from __future__ import annotations
import pandas as pd


def generate_insights(df: pd.DataFrame) -> "list[dict]":
    """
    Return a list of insight dicts.

    Keys per dict
    -------------
    icon  : empty string (emojis removed per design spec)
    title : short descriptive label
    body  : one sentence with optional **bold** markers
    color : hex accent for the left border of the card
    """
    if df is None or df.empty:
        return [{
            "icon":  "",
            "title": "No Data",
            "body":  "No records match the current filters.",
            "color": "#D98270",
        }]

    insights = []

    # Most common genre
    if "genre" in df.columns:
        vc = df["genre"].value_counts()
        if not vc.empty:
            top_genre = vc.index[0]
            count = vc.iloc[0]
            pct = count / len(df) * 100
            insights.append({
                "icon":  "",
                "title": "Most Popular Genre",
                "body":  (
                    f"**{top_genre}** leads with {count:,} games "
                    f"({pct:.1f}% of the current selection)."
                ),
                "color": "#477A5B",
            })

    # Most common platform
    if "platform" in df.columns:
        vc = df["platform"].value_counts()
        if not vc.empty:
            top_platform = vc.index[0]
            count = vc.iloc[0]
            insights.append({
                "icon":  "",
                "title": "Dominant Platform",
                "body":  (
                    f"**{top_platform}** hosts the most titles with "
                    f"{count:,} games in the current selection."
                ),
                "color": "#E7A64B",
            })

    # Highest-rated genre
    if "genre" in df.columns and "user_rating" in df.columns:
        genre_avg = df.groupby("genre")["user_rating"].mean()
        if not genre_avg.empty:
            best = genre_avg.idxmax()
            avg_r = genre_avg.max()
            insights.append({
                "icon":  "",
                "title": "Highest-Rated Genre",
                "body":  (
                    f"**{best}** games achieve the highest average "
                    f"user rating of **{avg_r:.2f} / 10**."
                ),
                "color": "#6BAA9B",
            })

    # Highest-rated platform
    if "platform" in df.columns and "user_rating" in df.columns:
        plat_avg = df.groupby("platform")["user_rating"].mean()
        if not plat_avg.empty:
            best = plat_avg.idxmax()
            avg_r = plat_avg.max()
            insights.append({
                "icon":  "",
                "title": "Highest-Rated Platform",
                "body":  (
                    f"**{best}** titles average the highest rating "
                    f"of **{avg_r:.2f} / 10**."
                ),
                "color": "#8BA9B4",
            })

    # Peak release year
    if "release_year" in df.columns:
        vc = df["release_year"].value_counts()
        if not vc.empty:
            peak_year = vc.index[0]
            count = vc.iloc[0]
            insights.append({
                "icon":  "",
                "title": "Peak Release Year",
                "body":  (
                    f"**{peak_year}** had the most releases with "
                    f"**{count:,}** game records."
                ),
                "color": "#8FAF86",
            })

    # Rating overview
    if "user_rating" in df.columns:
        avg = df["user_rating"].mean()
        med = df["user_rating"].median()
        insights.append({
            "icon":  "",
            "title": "Rating Overview",
            "body":  (
                f"Mean rating is **{avg:.2f} / 10** (median **{med:.2f}**) "
                f"across **{len(df):,}** records."
            ),
            "color": "#C8A96A",
        })

    # Top-rated game
    if "game_name" in df.columns and "user_rating" in df.columns:
        idx        = df["user_rating"].idxmax()
        top_game   = df.loc[idx, "game_name"]
        top_rating = df.loc[idx, "user_rating"]
        plat       = df.loc[idx, "platform"] if "platform" in df.columns else ""
        plat_str   = f" on {plat}" if plat else ""
        insights.append({
            "icon":  "",
            "title": "Top-Rated Game",
            "body":  (
                f"**{top_game}**{plat_str} holds the highest rating "
                f"of **{top_rating:.2f} / 10** in the current filter."
            ),
            "color": "#E7A64B",
        })

    # Year span
    if "release_year" in df.columns:
        min_y = int(df["release_year"].min())
        max_y = int(df["release_year"].max())
        span  = max_y - min_y
        insights.append({
            "icon":  "",
            "title": "Release Year Span",
            "body":  (
                f"The selection spans **{span} years**, "
                f"from **{min_y}** to **{max_y}**."
            ),
            "color": "#477A5B",
        })

    return insights
