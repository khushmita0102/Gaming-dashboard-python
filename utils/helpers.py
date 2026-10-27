"""
helpers.py
----------
Reusable helper utilities shared across the Gaming Analytics Dashboard.

Sage & Ivory design tokens
──────────────────────────
  #F7F8F2   Main background
  #E8EEE2   Sidebar background
  #FFFDF8   Card / panel background
  #477A5B   Primary sage green
  #8FAF86   Secondary sage
  #DDE8D5   Pale sage / border
  #343B35   Dark text
  #687168   Secondary text
  #E7A64B   Amber highlight
  #6BAA9B   Muted teal
  #D98270   Muted coral
  #8BA9B4   Dusty blue
  #B99AB5   Muted mauve
"""

from __future__ import annotations
import pandas as pd
import numpy as np

# ──────────────────────────────────────────────
# Design tokens (single source of truth)
# ──────────────────────────────────────────────
C = {
    "bg":         "#F7F8F2",
    "sidebar":    "#E8EEE2",
    "card":       "#FFFDF8",
    "primary":    "#477A5B",
    "secondary":  "#8FAF86",
    "pale":       "#DDE8D5",
    "text":       "#343B35",
    "muted":      "#687168",
    "border":     "#DDE8D5",
    "amber":      "#E7A64B",
    "teal":       "#6BAA9B",
    "coral":      "#D98270",
    "blue":       "#8BA9B4",
    "mauve":      "#B99AB5",
}

# Chart colour palette — deterministic, contrast-safe
PALETTE = [
    "#477A5B",   # primary sage
    "#E7A64B",   # amber
    "#6BAA9B",   # teal
    "#D98270",   # coral
    "#8BA9B4",   # dusty blue
    "#B99AB5",   # mauve
    "#8FAF86",   # light sage
    "#C8A96A",   # muted gold
    "#5C8F70",   # mid sage
    "#A3C4BC",   # pale teal
    "#E8C99A",   # pale amber
    "#9DB5C0",   # pale blue
    "#343B35",   # dark charcoal
    "#C4B5C2",   # pale mauve
]

HIGHLIGHT_COLOR = C["primary"]
ACCENT_COLOR    = C["amber"]
BACKGROUND_COLOR = C["bg"]
CARD_COLOR      = C["card"]
TEXT_COLOR      = C["text"]
BORDER_COLOR    = C["border"]


def get_color_sequence(n: int = 14) -> list:
    """Return a repeating list of hex colours for Plotly (deterministic)."""
    return (PALETTE * ((n // len(PALETTE)) + 1))[:n]


# ──────────────────────────────────────────────
# Number formatting
# ──────────────────────────────────────────────

def fmt_number(n, decimals: int = 0) -> str:
    if pd.isna(n):
        return "N/A"
    if decimals == 0:
        return f"{int(n):,}"
    return f"{n:,.{decimals}f}"


def fmt_rating(r: float) -> str:
    if pd.isna(r):
        return "N/A"
    return f"{r:.2f} / 10"


# ──────────────────────────────────────────────
# Safe aggregation
# ──────────────────────────────────────────────

def safe_mean(series: pd.Series) -> float:
    if series.empty or series.isna().all():
        return float("nan")
    return series.mean()


def safe_top_n(df: pd.DataFrame, col: str, n: int = 10) -> pd.DataFrame:
    if col not in df.columns or df.empty:
        return pd.DataFrame()
    return df.nlargest(n, col)


def column_exists(df: pd.DataFrame, *cols: str) -> bool:
    return all(c in df.columns for c in cols)


# ──────────────────────────────────────────────
# KPI card HTML  — no emojis, typography-driven
# ──────────────────────────────────────────────

def kpi_card_html(label: str, value: str, icon: str = "", delta: str = "") -> str:
    """
    Returns a styled HTML KPI card.
    - label : uppercase small label shown below the value
    - value : the metric value string
    - icon  : ignored (kept for backwards-compat; emojis removed)
    - delta : optional small secondary line in amber
    """
    delta_html = (
        f'<div style="font-size:0.72rem;color:{C["amber"]};margin-top:5px;font-weight:600;">'
        f'{delta}</div>'
    ) if delta else ""

    return (
        f'<div style="'
        f'background:{C["card"]};'
        f'border:1.5px solid {C["border"]};'
        f'border-top:3px solid {C["primary"]};'
        f'border-radius:10px;'
        f'padding:18px 14px 14px;'
        f'text-align:center;'
        f'box-shadow:0 1px 4px rgba(52,59,53,0.07);'
        f'height:100%;'
        f'">'
        f'<div style="'
        f'font-size:1.75rem;'
        f'font-weight:700;'
        f'color:{C["primary"]};'
        f'line-height:1.1;'
        f'font-family:Inter,sans-serif;'
        f'">{value}</div>'
        f'<div style="'
        f'font-size:0.72rem;'
        f'color:{C["muted"]};'
        f'margin-top:6px;'
        f'text-transform:uppercase;'
        f'letter-spacing:0.08em;'
        f'font-weight:600;'
        f'font-family:Inter,sans-serif;'
        f'">{label}</div>'
        f'{delta_html}'
        f'</div>'
    )
