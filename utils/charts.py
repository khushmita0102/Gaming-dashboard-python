"""
charts.py
---------
All chart-generation functions for the Gaming Analytics Dashboard.
Sage & Ivory design system — Inter typography, cream backgrounds, sage palette.
"""

from __future__ import annotations

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.helpers import (
    PALETTE, get_color_sequence,
    HIGHLIGHT_COLOR, ACCENT_COLOR, C,
)

# ── Inter font stack for Plotly ──────────────
_FONT = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"


# ──────────────────────────────────────────────────────────
# Shared chart theme
# ──────────────────────────────────────────────────────────

def _theme(fig: go.Figure, title: str = "", height: int | None = None) -> go.Figure:
    """
    Apply the Sage & Ivory theme to any Plotly figure.
    - Cream / transparent background
    - Sage gridlines
    - Inter font everywhere
    - Dark charcoal text
    """
    layout_kw: dict = dict(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(family=_FONT, size=16, color=C["text"]),
            x=0.0,
            xanchor="left",
            pad=dict(b=6),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=C["card"],
        font=dict(family=_FONT, color=C["text"], size=12),
        margin=dict(l=44, r=18, t=52, b=44),
        legend=dict(
            bgcolor="rgba(255,253,248,0.95)",
            bordercolor=C["border"],
            borderwidth=1,
            font=dict(family=_FONT, size=11, color=C["text"]),
        ),
        xaxis=dict(
            gridcolor=C["pale"],
            zerolinecolor="#C4D4BC",
            linecolor=C["border"],
            tickfont=dict(family=_FONT, size=11, color=C["muted"]),
            title=dict(font=dict(family=_FONT, size=12, color=C["muted"])),
        ),
        yaxis=dict(
            gridcolor=C["pale"],
            zerolinecolor="#C4D4BC",
            linecolor=C["border"],
            tickfont=dict(family=_FONT, size=11, color=C["muted"]),
            title=dict(font=dict(family=_FONT, size=12, color=C["muted"])),
        ),
        hoverlabel=dict(
            bgcolor=C["card"],
            bordercolor=C["border"],
            font=dict(family=_FONT, size=12, color=C["text"]),
        ),
    )
    if height:
        layout_kw["height"] = height
    fig.update_layout(**layout_kw)
    return fig


# ──────────────────────────────────────────────────────────
# Overview / Summary
# ──────────────────────────────────────────────────────────

def rating_distribution_histogram(df: pd.DataFrame) -> go.Figure:
    """Histogram of user ratings."""
    fig = px.histogram(
        df, x="user_rating", nbins=40,
        color_discrete_sequence=[HIGHLIGHT_COLOR],
        labels={"user_rating": "User Rating", "count": "Games"},
        opacity=0.88,
    )
    fig.update_traces(marker_line_color=C["pale"], marker_line_width=0.8)
    _theme(fig, "Distribution of User Ratings")
    fig.update_xaxes(title_text="User Rating (0–10)")
    fig.update_yaxes(title_text="Number of Games")
    return fig


# ──────────────────────────────────────────────────────────
# Genre Analysis
# ──────────────────────────────────────────────────────────

def games_per_genre_bar(df: pd.DataFrame, metric: str = "count") -> go.Figure:
    """Horizontal bar chart: games per genre (count or avg rating)."""
    if metric == "avg_rating":
        data = (
            df.groupby("genre")["user_rating"].mean()
            .reset_index().rename(columns={"user_rating": "value"})
            .sort_values("value", ascending=True)
        )
        x_label, title = "Average User Rating", "Average Rating by Genre"
    else:
        data = (
            df.groupby("genre").size()
            .reset_index(name="value")
            .sort_values("value", ascending=True)
        )
        x_label, title = "Number of Games", "Games per Genre"

    colors = get_color_sequence(len(data))
    fig = px.bar(
        data, x="value", y="genre", orientation="h",
        color="genre", color_discrete_sequence=colors,
        labels={"genre": "", "value": x_label},
    )
    fig.update_layout(showlegend=False)
    _theme(fig, title)
    fig.update_xaxes(title_text=x_label)
    fig.update_yaxes(title_text="")
    return fig


def genre_pie_chart(df: pd.DataFrame) -> go.Figure:
    """Donut chart of game counts by genre."""
    counts = df["genre"].value_counts().reset_index()
    counts.columns = ["genre", "count"]
    fig = px.pie(
        counts, names="genre", values="count",
        hole=0.44,
        color_discrete_sequence=get_color_sequence(len(counts)),
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        textfont=dict(family=_FONT, size=11, color="#FFFDF8"),
        hovertemplate="<b>%{label}</b><br>Games: %{value:,}<br>%{percent}<extra></extra>",
    )
    _theme(fig, "Genre Share")
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02),
    )
    return fig


def rating_by_genre_box(df: pd.DataFrame) -> go.Figure:
    """Box plot: rating distribution per genre."""
    order = (
        df.groupby("genre")["user_rating"].median()
        .sort_values(ascending=False).index.tolist()
    )
    fig = px.box(
        df, x="genre", y="user_rating", color="genre",
        category_orders={"genre": order},
        color_discrete_sequence=get_color_sequence(len(order)),
        labels={"genre": "", "user_rating": "User Rating"},
        notched=False,
    )
    fig.update_layout(showlegend=False)
    _theme(fig, "Rating Distribution by Genre")
    fig.update_xaxes(tickangle=-35, title_text="")
    fig.update_yaxes(title_text="User Rating")
    return fig


# ──────────────────────────────────────────────────────────
# Platform Analysis
# ──────────────────────────────────────────────────────────

def games_per_platform_bar(df: pd.DataFrame) -> go.Figure:
    """Vertical bar chart: games per platform."""
    data = (
        df.groupby("platform").size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    fig = px.bar(
        data, x="platform", y="count", color="platform",
        color_discrete_sequence=get_color_sequence(len(data)),
        labels={"platform": "Platform", "count": "Games"},
    )
    fig.update_layout(showlegend=False)
    _theme(fig, "Games per Platform")
    fig.update_xaxes(title_text="Platform")
    fig.update_yaxes(title_text="Number of Games")
    return fig


def avg_rating_by_platform_bar(df: pd.DataFrame) -> go.Figure:
    """Bar chart: average rating per platform."""
    data = (
        df.groupby("platform")["user_rating"].mean()
        .reset_index().sort_values("user_rating", ascending=False)
    )
    fig = px.bar(
        data, x="platform", y="user_rating", color="platform",
        color_discrete_sequence=get_color_sequence(len(data)),
        labels={"platform": "Platform", "user_rating": "Avg Rating"},
    )
    fig.update_layout(showlegend=False)
    _theme(fig, "Average Rating by Platform")
    fig.update_xaxes(title_text="Platform")
    fig.update_yaxes(title_text="Average Rating (0–10)")
    return fig


def platform_genre_heatmap(df: pd.DataFrame) -> go.Figure:
    """Heatmap: game count for each Platform × Genre combination."""
    pivot = df.pivot_table(
        index="platform", columns="genre",
        values="game_name", aggfunc="count", fill_value=0,
    )
    fig = px.imshow(
        pivot,
        color_continuous_scale=[
            [0.0, C["card"]],
            [0.25, C["pale"]],
            [0.6, C["secondary"]],
            [1.0, C["primary"]],
        ],
        labels=dict(x="Genre", y="Platform", color="Games"),
        aspect="auto",
    )
    _theme(fig, "Game Count — Platform × Genre", height=340)
    fig.update_xaxes(tickangle=-40, tickfont=dict(size=10))
    return fig


def rating_by_platform_box(df: pd.DataFrame) -> go.Figure:
    """Box plot: rating distribution per platform."""
    order = (
        df.groupby("platform")["user_rating"].median()
        .sort_values(ascending=False).index.tolist()
    )
    fig = px.box(
        df, x="platform", y="user_rating", color="platform",
        category_orders={"platform": order},
        color_discrete_sequence=get_color_sequence(len(order)),
        labels={"platform": "", "user_rating": "User Rating"},
    )
    fig.update_layout(showlegend=False)
    _theme(fig, "Rating Distribution by Platform")
    fig.update_xaxes(title_text="", tickangle=-15)
    fig.update_yaxes(title_text="User Rating")
    return fig


# ──────────────────────────────────────────────────────────
# Trend Analysis
# ──────────────────────────────────────────────────────────

def releases_per_year_line(df: pd.DataFrame) -> go.Figure:
    """Line chart: games released per year."""
    data = df.groupby("release_year").size().reset_index(name="count")
    fig = px.line(
        data, x="release_year", y="count", markers=True,
        color_discrete_sequence=[HIGHLIGHT_COLOR],
        labels={"release_year": "Year", "count": "Games Released"},
    )
    fig.update_traces(
        line_width=2.5, marker_size=6,
        marker_color=ACCENT_COLOR,
        marker_line_color=HIGHLIGHT_COLOR, marker_line_width=1.5,
    )
    _theme(fig, "Games Released per Year")
    fig.update_xaxes(title_text="Year", dtick=2)
    fig.update_yaxes(title_text="Number of Games")
    return fig


def avg_rating_per_year_line(df: pd.DataFrame) -> go.Figure:
    """Line chart: average user rating per release year."""
    data = (
        df.groupby("release_year")["user_rating"].mean()
        .reset_index().rename(columns={"user_rating": "avg_rating"})
    )
    fig = px.line(
        data, x="release_year", y="avg_rating", markers=True,
        color_discrete_sequence=[ACCENT_COLOR],
        labels={"release_year": "Year", "avg_rating": "Avg Rating"},
    )
    fig.update_traces(
        line_width=2.5, marker_size=6,
        marker_color=HIGHLIGHT_COLOR,
        marker_line_color=ACCENT_COLOR, marker_line_width=1.5,
    )
    _theme(fig, "Average User Rating per Year")
    fig.update_xaxes(title_text="Year", dtick=2)
    fig.update_yaxes(title_text="Average Rating (0–10)")
    return fig


def releases_area_by_platform(df: pd.DataFrame) -> go.Figure:
    """Stacked area chart: releases per year by platform."""
    data = df.groupby(["release_year", "platform"]).size().reset_index(name="count")
    fig = px.area(
        data, x="release_year", y="count", color="platform",
        color_discrete_sequence=get_color_sequence(data["platform"].nunique()),
        labels={"release_year": "Year", "count": "Games Released", "platform": "Platform"},
    )
    _theme(fig, "Yearly Releases by Platform")
    fig.update_xaxes(title_text="Year", dtick=2)
    fig.update_yaxes(title_text="Number of Games")
    return fig


def top_rated_games_bar(df: pd.DataFrame, n: int = 15) -> go.Figure:
    """Horizontal bar: top-n highest-rated games."""
    top = df.nlargest(n, "user_rating")[
        ["game_name", "platform", "genre", "user_rating"]
    ].copy()
    top["label"] = top["game_name"] + "  (" + top["platform"] + ")"
    top = top.sort_values("user_rating", ascending=True)
    fig = px.bar(
        top, x="user_rating", y="label", orientation="h",
        color="user_rating",
        color_continuous_scale=[
            [0.0, C["pale"]],
            [0.5, C["secondary"]],
            [1.0, C["primary"]],
        ],
        labels={"user_rating": "User Rating", "label": ""},
        hover_data={"genre": True, "platform": True},
    )
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    _theme(fig, f"Top {n} Highest-Rated Games", height=max(320, n * 28))
    fig.update_xaxes(title_text="User Rating")
    fig.update_yaxes(title_text="", tickfont=dict(size=10))
    return fig


# ──────────────────────────────────────────────────────────
# Ratings deep-dive
# ──────────────────────────────────────────────────────────

def rating_violin(df: pd.DataFrame, col: str = "genre") -> go.Figure:
    """Violin plot of ratings split by a categorical column."""
    order = (
        df.groupby(col)["user_rating"].median()
        .sort_values(ascending=False).index.tolist()
    )
    fig = px.violin(
        df, x=col, y="user_rating", color=col,
        box=True, points="outliers",
        category_orders={col: order},
        color_discrete_sequence=get_color_sequence(len(order)),
        labels={col: col.replace("_", " ").title(), "user_rating": "User Rating"},
    )
    fig.update_layout(showlegend=False)
    _theme(fig, f"Rating Violin — by {col.replace('_', ' ').title()}")
    fig.update_xaxes(tickangle=-35, title_text="")
    return fig


def scatter_year_vs_rating(df: pd.DataFrame) -> go.Figure:
    """Scatter: release year vs user rating, coloured by genre."""
    fig = px.scatter(
        df, x="release_year", y="user_rating", color="genre",
        color_discrete_sequence=get_color_sequence(df["genre"].nunique()),
        opacity=0.55,
        hover_data=["game_name", "platform"],
        labels={
            "release_year": "Release Year",
            "user_rating": "User Rating",
            "genre": "Genre",
        },
    )
    _theme(fig, "Release Year vs User Rating")
    fig.update_xaxes(title_text="Release Year")
    fig.update_yaxes(title_text="User Rating")
    return fig


# ──────────────────────────────────────────────────────────
# Correlation
# ──────────────────────────────────────────────────────────

def correlation_heatmap(df: pd.DataFrame) -> "go.Figure | None":
    """
    Pearson correlation heatmap.
    Returns None when fewer than 2 numeric columns exist.
    """
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(num_cols) < 2:
        return None

    corr = df[num_cols].corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    corr_masked = corr.where(~mask)

    fig = go.Figure(
        go.Heatmap(
            z=corr_masked.values,
            x=corr_masked.columns.tolist(),
            y=corr_masked.index.tolist(),
            colorscale=[
                [0.0,  C["coral"]],   # strong negative  → coral
                [0.35, C["card"]],    # near zero        → cream
                [0.5,  C["pale"]],    # zero             → pale sage
                [0.65, C["card"]],    # near zero other  → cream
                [1.0,  C["primary"]], # strong positive  → forest green
            ],
            zmin=-1, zmax=1,
            text=np.round(corr_masked.values, 2),
            texttemplate="%{text}",
            textfont=dict(family=_FONT, size=12, color=C["text"]),
            hovertemplate=(
                "<b>%{x}</b> vs <b>%{y}</b><br>r = %{z:.3f}<extra></extra>"
            ),
        )
    )
    _theme(fig, "Correlation Matrix (Pearson)")
    fig.update_layout(xaxis=dict(side="bottom"))
    return fig
