"""
app.py
------
Gaming Analytics Dashboard — Sage & Ivory premium design.
Run with:  streamlit run app.py

Pages
-----
1. Overview
2. Gaming Trends
3. Genre & Platform
4. Ratings & Performance
5. Game Explorer
6. Data Quality & Correlation
"""

import sys
import re
from pathlib import Path

ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import numpy as np
import streamlit as st

from data.data_processing import get_data, get_filter_options, apply_filters
from utils.helpers import fmt_number, fmt_rating, kpi_card_html, C
from utils.insights import generate_insights
import utils.charts as charts


# ──────────────────────────────────────────────
# Page configuration
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="Gaming Analytics Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Global CSS  ·  Sage & Ivory design system
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* ── Base typography ── */
    html, body,
    [class*="st-"],
    [data-testid="stAppViewContainer"],
    [data-testid="stSidebar"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        color: #343B35;
    }

    /* ── Page background ── */
    .stApp { background-color: #F7F8F2; }
    .block-container {
        padding: 1.6rem 2.2rem 2.4rem !important;
        max-width: 1380px;
    }

    /* ── Headings ── */
    h1 {
        font-size: 2.05rem !important;
        font-weight: 800 !important;
        color: #343B35 !important;
        letter-spacing: -0.6px !important;
        line-height: 1.2 !important;
        margin-bottom: 0.15rem !important;
    }
    h2 {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        color: #343B35 !important;
        letter-spacing: -0.3px !important;
        margin-bottom: 0 !important;
    }
    h3, h4 {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #343B35 !important;
    }
    p { color: #687168; line-height: 1.65; }

    /* ── Section divider ── */
    .divider {
        border: none;
        border-top: 1px solid #DDE8D5;
        margin: 1.1rem 0 1.3rem;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: #E8EEE2 !important;
        border-right: 1px solid #C4D4BC !important;
        overflow: hidden !important;
    }
    [data-testid="stSidebarCollapseButton"]   { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }

    /* ── Sidebar labels ── */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stRadio label {
        color: #343B35 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    /* ── Radio nav — active item highlight ── */
    [data-testid="stSidebar"] [data-baseweb="radio"] {
        gap: 2px;
    }
    [data-testid="stSidebar"] [data-baseweb="radio"] label {
        padding: 5px 10px;
        border-radius: 7px;
        transition: background 0.15s;
    }
    [data-testid="stSidebar"] [data-baseweb="radio"] label:hover {
        background: #D4E2CA;
    }

    /* ── Filter control borders ── */
    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div {
        border-radius: 8px !important;
        border-color: #C4D4BC !important;
        background: #F0F5EB !important;
    }

    /* ── Multiselect tags ── */
    [data-baseweb="tag"] {
        background-color: #477A5B !important;
        color: #FFFDF8 !important;
        border-radius: 5px !important;
        font-size: 0.78rem !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background-color: #477A5B !important;
        color: #FFFDF8 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        min-height: 38px !important;
        transition: background 0.18s ease !important;
    }
    .stButton > button:hover {
        background-color: #343B35 !important;
    }

    /* ── Download button ── */
    .stDownloadButton > button {
        background-color: #E7A64B !important;
        color: #343B35 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .stDownloadButton > button:hover {
        background-color: #C8881A !important;
        color: #FFFDF8 !important;
    }

    /* ── Slider track colour ── */
    [data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"] {
        background-color: #477A5B !important;
    }

    /* ── Streamlit native metric widgets ── */
    [data-testid="stMetric"] {
        background: #FFFDF8 !important;
        border: 1px solid #DDE8D5 !important;
        border-top: 3px solid #477A5B !important;
        border-radius: 10px !important;
        padding: 14px 12px !important;
    }
    [data-testid="stMetricLabel"] { color: #687168 !important; font-size: 0.78rem !important; }
    [data-testid="stMetricValue"] { color: #343B35 !important; font-size: 1.5rem  !important; font-weight: 700 !important; }
    [data-testid="stMetricDelta"] { font-size: 0.78rem !important; }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #FFFDF8 !important;
        border-bottom: 1.5px solid #DDE8D5 !important;
        border-radius: 8px 8px 0 0 !important;
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #687168 !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        border-radius: 6px 6px 0 0 !important;
        padding: 8px 18px !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #477A5B !important;
        font-weight: 700 !important;
        border-bottom: 2.5px solid #477A5B !important;
        background: #F4F8F0 !important;
    }

    /* ── Dataframes ── */
    [data-testid="stDataFrame"] {
        border-radius: 8px !important;
        border: 1px solid #DDE8D5 !important;
        overflow: hidden !important;
    }

    /* ── Text input ── */
    [data-testid="stTextInput"] input {
        border-radius: 8px !important;
        border-color: #C4D4BC !important;
        background: #FFFDF8 !important;
    }

    /* ── Alerts ── */
    .stAlert { border-radius: 8px !important; }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        border: 1px solid #DDE8D5 !important;
        border-radius: 8px !important;
        background: #FAFCF7 !important;
    }

    /* ── Checkbox ── */
    [data-baseweb="checkbox"] [data-checked="true"] div {
        background-color: #477A5B !important;
        border-color: #477A5B !important;
    }

    /* ── Selectbox ── */
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background: #FFFDF8 !important;
    }
    [data-testid="stSidebar"] h1 {
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    letter-spacing: -1px !important;
    line-height: 1.2 !important;
}
    </style>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────
# Load data
# ──────────────────────────────────────────────
raw_df, df_clean, cleaning_report = get_data()

if df_clean.empty:
    st.warning("No data available. Please check the dataset file and restart.")
    st.stop()


# ──────────────────────────────────────────────
# Sidebar — navigation & filters
# ──────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown(
        "<div style='"
        "padding:0px 10px 14px;"
        "margin-top: -35px;"
        "border-bottom:1px solid #C4D4BC;"
        "margin-bottom:10px;"
        "'>"
        "<div style='"
        "font-size:1.7rem;font-weight:800;"
        "color:#477A5B;letter-spacing:-0.3px;"
        "white-space:nowrap;"
        "font-family:Inter,sans-serif;"
        "'>Gaming Analytics</div>"
        "<div style='"
        "font-size:0.72rem;color:#687168;"
        "margin-top:2px;font-family:Inter,sans-serif;"
        "'>Gaming Insights & Intelligence</div>"
        "</div>",
        
        
        unsafe_allow_html=True,

    )
    # Navigation
    PAGE_MAP = {
        "Overview":                   "overview",
        "Gaming Trends":              "trends",
        "Genre & Platform":           "genre_platform",
        "Ratings & Performance":      "ratings",
        "Game Explorer":              "explorer",
        "Data Quality & Correlation": "quality",
    }
    selected_label = st.radio(
        "Page",
        list(PAGE_MAP.keys()),
        label_visibility="collapsed",
    )
    page = PAGE_MAP[selected_label]

    # Divider
    st.markdown(
        "<div style='border-top:1px solid #C4D4BC;margin:12px 0 10px;'></div>",
        unsafe_allow_html=True,
    )

    # Filter heading
    st.markdown(
        "<div style='"
        "font-size:0.7rem;font-weight:700;"
        "text-transform:uppercase;letter-spacing:0.1em;"
        "color:#687168;padding:0 2px 6px;"
        "font-family:Inter,sans-serif;"
        "'>Filters</div>",
        unsafe_allow_html=True,
    )

    opts = get_filter_options(df_clean)

    # Session state initialisation
    def reset_filters():
        st.session_state.sel_genres    = opts.get("genre", [])
        st.session_state.sel_platforms = opts.get("platform", [])
        st.session_state.sel_year_min  = opts.get("release_year", [2000])[0]
        st.session_state.sel_year_max  = opts.get("release_year", [2023])[-1]
        st.session_state.sel_rating_min = opts.get("user_rating_min", 0.0)
        st.session_state.sel_rating_max = opts.get("user_rating_max", 10.0)

    if "sel_genres" not in st.session_state:
        reset_filters()

    sel_genres = st.multiselect(
        "Genre",
        options=opts.get("genre", []),
        default=st.session_state.sel_genres,
        key="sel_genres",
    )
    sel_platforms = st.multiselect(
        "Platform",
        options=opts.get("platform", []),
        default=st.session_state.sel_platforms,
        key="sel_platforms",
    )

    year_list = opts.get("release_year", [2000, 2023])
    year_min, year_max = int(year_list[0]), int(year_list[-1])
    sel_year = st.slider(
        "Release Year",
        min_value=year_min, max_value=year_max,
        value=(
            int(st.session_state.get("sel_year_min", year_min)),
            int(st.session_state.get("sel_year_max", year_max)),
        ),
        step=1, key="sel_year_range",
    )

    r_min = float(opts.get("user_rating_min", 0.0))
    r_max = float(opts.get("user_rating_max", 10.0))
    sel_rating = st.slider(
        "User Rating",
        min_value=round(r_min, 1), max_value=round(r_max, 1),
        value=(
            round(float(st.session_state.get("sel_rating_min", r_min)), 1),
            round(float(st.session_state.get("sel_rating_max", r_max)), 1),
        ),
        step=0.1, key="sel_rating_range",
    )

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    if st.button("Reset Filters", use_container_width=True):
        reset_filters()
        st.rerun()

    st.markdown(
        "<div style='"
        "border-top:1px solid #C4D4BC;"
        "margin-top:14px;padding-top:10px;"
        "font-size:0.72rem;color:#687168;"
        "font-family:Inter,sans-serif;"
        f"'>{len(df_clean):,} total records</div>",
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────
# Apply filters
# ──────────────────────────────────────────────

filtered_df = apply_filters(
    df_clean,
    genres=sel_genres    if sel_genres    else opts.get("genre", []),
    platforms=sel_platforms if sel_platforms else opts.get("platform", []),
    year_range=sel_year,
    rating_range=sel_rating,
)

if filtered_df.empty:
    st.warning("No data matches the selected filters. Please adjust the sidebar filters.")
    st.stop()


# ──────────────────────────────────────────────
# Shared layout helpers
# ──────────────────────────────────────────────

def page_title(text: str, subtitle: str = "") -> None:
    """Render a page title with optional subtitle."""
    st.markdown(
        f"<h1 style='color:#343B35;margin-bottom:2px;'>{text}</h1>"
        + (
            f"<p style='color:#687168;font-size:0.9rem;"
            f"margin-top:2px;margin-bottom:0;'>{subtitle}</p>"
            if subtitle else ""
        ),
        unsafe_allow_html=True,
    )


def section_heading(text: str, subtitle: str = "") -> None:
    """Render a section heading with divider."""
    st.markdown(
        f"<h2 style='color:#343B35;margin-bottom:0;'>{text}</h2>"
        + (
            f"<p style='color:#687168;font-size:0.82rem;"
            f"margin-top:3px;margin-bottom:0;'>{subtitle}</p>"
            if subtitle else ""
        ),
        unsafe_allow_html=True,
    )
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)


def chart_card(fig, key: str = "") -> None:
    """Render a Plotly chart inside a styled white container."""
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True, key=key)


def insight_card(icon: str, title: str, body: str, color: str) -> str:
    """Return HTML for a single insight card (no emojis in title/body)."""
    body_html = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", body)
    return (
        f'<div style="'
        f'background:{C["card"]};'
        f'border:1px solid {C["border"]};'
        f'border-left:3px solid {color};'
        f'border-radius:8px;'
        f'padding:14px 16px;'
        f'margin-bottom:10px;'
        f'box-shadow:0 1px 3px rgba(52,59,53,0.06);">'
        f'<div style="font-weight:700;color:{C["text"]};font-size:0.88rem;'
        f'font-family:Inter,sans-serif;margin-bottom:4px;">{title}</div>'
        f'<div style="color:{C["muted"]};font-size:0.82rem;'
        f'font-family:Inter,sans-serif;line-height:1.5;">{body_html}</div>'
        f'</div>'
    )


# ══════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════
if page == "overview":
    page_title(
        "Overview",
        "Interactive exploration of gaming data — genres, platforms, ratings, and release trends.",
    )
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # KPI row
    total_games      = len(filtered_df)
    unique_games     = filtered_df["game_name"].nunique()
    unique_genres    = filtered_df["genre"].nunique()
    unique_platforms = filtered_df["platform"].nunique()
    avg_rating       = filtered_df["user_rating"].mean()
    year_span = (
        f"{int(filtered_df['release_year'].min())}–{int(filtered_df['release_year'].max())}"
        if "release_year" in filtered_df.columns else "N/A"
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:  st.markdown(kpi_card_html("Total Records",  fmt_number(total_games)),     unsafe_allow_html=True)
    with c2:  st.markdown(kpi_card_html("Unique Games",   fmt_number(unique_games)),    unsafe_allow_html=True)
    with c3:  st.markdown(kpi_card_html("Genres",         fmt_number(unique_genres)),   unsafe_allow_html=True)
    with c4:  st.markdown(kpi_card_html("Platforms",      fmt_number(unique_platforms)),unsafe_allow_html=True)
    with c5:  st.markdown(kpi_card_html("Avg Rating",     fmt_rating(avg_rating)),      unsafe_allow_html=True)
    with c6:  st.markdown(kpi_card_html("Year Range",     year_span),                  unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # Two-column charts
    col_l, col_r = st.columns(2)
    with col_l:
        section_heading("Rating Distribution")
        chart_card(charts.rating_distribution_histogram(filtered_df), key="ov_hist")
    with col_r:
        section_heading("Genre Share")
        chart_card(charts.genre_pie_chart(filtered_df), key="ov_pie")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    section_heading("Top 15 Highest-Rated Games", "Based on current filter selection")
    chart_card(charts.top_rated_games_bar(filtered_df, n=15), key="ov_top")

    # Key insights
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    section_heading("Key Insights", "Automatically calculated from the filtered dataset")
    insights = generate_insights(filtered_df)
    cols = st.columns(2)
    for i, ins in enumerate(insights):
        with cols[i % 2]:
            st.markdown(
                insight_card(
                    ins.get("icon", ""),
                    ins.get("title", ""),
                    ins.get("body", ""),
                    ins.get("color", C["primary"]),
                ),
                unsafe_allow_html=True,
            )


# ══════════════════════════════════════════════
# PAGE 2 — GAMING TRENDS
# ══════════════════════════════════════════════
elif page == "trends":
    page_title("Gaming Trends", "How game releases and user ratings have evolved over time.")
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Releases per Year",
        "Rating Trends",
        "Platform Releases",
        "Year vs Rating",
    ])

    with tab1:
        chart_card(charts.releases_per_year_line(filtered_df), key="tr_line")
        with st.expander("About this chart"):
            st.write(
                "Shows the number of game records for each release year. "
                "A spike indicates a year with many releases or re-releases in the dataset."
            )

    with tab2:
        chart_card(charts.avg_rating_per_year_line(filtered_df), key="tr_avg")
        with st.expander("About this chart"):
            st.write(
                "Average user rating aggregated by release year. "
                "Year-to-year fluctuations may reflect sampling differences rather than true quality trends."
            )

    with tab3:
        chart_card(charts.releases_area_by_platform(filtered_df), key="tr_area")
        with st.expander("About this chart"):
            st.write(
                "Stacked area chart showing how game releases on each platform evolved over time. "
                "Hover over the chart to see exact counts."
            )

    with tab4:
        chart_card(charts.scatter_year_vs_rating(filtered_df), key="tr_scatter")
        with st.expander("About this chart"):
            st.write(
                "Each point represents a game record, coloured by genre. "
                "Look for horizontal clusters to see how a genre's ratings spread across years."
            )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    section_heading("Year-by-Year Summary")
    year_summary = (
        filtered_df.groupby("release_year")
        .agg(
            total_games  =("game_name",   "count"),
            unique_games =("game_name",   "nunique"),
            avg_rating   =("user_rating", "mean"),
            min_rating   =("user_rating", "min"),
            max_rating   =("user_rating", "max"),
        )
        .reset_index()
        .sort_values("release_year", ascending=False)
    )
    year_summary.columns = ["Year", "Records", "Unique Games", "Avg Rating", "Min Rating", "Max Rating"]
    for col in ["Avg Rating", "Min Rating", "Max Rating"]:
        year_summary[col] = year_summary[col].round(2)
    st.dataframe(year_summary, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════
# PAGE 3 — GENRE & PLATFORM
# ══════════════════════════════════════════════
elif page == "genre_platform":
    page_title("Genre & Platform", "Distribution, ratings, and trends across genres and platforms.")
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Genre section
    section_heading("Genre Analysis")
    metric_choice = st.radio(
        "View by",
        ["Game Count", "Average Rating"],
        horizontal=True,
        key="genre_metric",
    )
    metric_key = "count" if metric_choice == "Game Count" else "avg_rating"

    col_l, col_r = st.columns(2)
    with col_l:
        chart_card(charts.games_per_genre_bar(filtered_df, metric=metric_key), key="gp_bar")
    with col_r:
        chart_card(charts.genre_pie_chart(filtered_df), key="gp_pie")

    chart_card(charts.rating_by_genre_box(filtered_df), key="gp_box")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Platform section
    section_heading("Platform Analysis")
    col_l2, col_r2 = st.columns(2)
    with col_l2:
        chart_card(charts.games_per_platform_bar(filtered_df), key="gp_plt_bar")
    with col_r2:
        chart_card(charts.avg_rating_by_platform_bar(filtered_df), key="gp_plt_avg")

    chart_card(charts.rating_by_platform_box(filtered_df), key="gp_plt_box")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    section_heading("Platform × Genre Heatmap", "Number of game records per combination")
    chart_card(charts.platform_genre_heatmap(filtered_df), key="gp_heat")

    # Genre summary table
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    section_heading("Genre Summary Table")
    genre_table = (
        filtered_df.groupby("genre")
        .agg(
            records       =("game_name",   "count"),
            unique_games  =("game_name",   "nunique"),
            avg_rating    =("user_rating", "mean"),
            median_rating =("user_rating", "median"),
            min_rating    =("user_rating", "min"),
            max_rating    =("user_rating", "max"),
        )
        .reset_index()
        .sort_values("avg_rating", ascending=False)
    )
    genre_table.columns = [
        "Genre", "Records", "Unique Games",
        "Avg Rating", "Median Rating", "Min Rating", "Max Rating",
    ]
    for col in ["Avg Rating", "Median Rating", "Min Rating", "Max Rating"]:
        genre_table[col] = genre_table[col].round(2)
    st.dataframe(genre_table, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════
# PAGE 4 — RATINGS & PERFORMANCE
# ══════════════════════════════════════════════
elif page == "ratings":
    page_title("Ratings & Performance", "Distribution and comparison of user ratings.")
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    avg_r       = filtered_df["user_rating"].mean()
    med_r       = filtered_df["user_rating"].median()
    std_r       = filtered_df["user_rating"].std()
    max_r       = filtered_df["user_rating"].max()
    min_r       = filtered_df["user_rating"].min()
    pct_above_7 = (filtered_df["user_rating"] >= 7).mean() * 100

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:  st.markdown(kpi_card_html("Mean Rating",    f"{avg_r:.2f}"),         unsafe_allow_html=True)
    with c2:  st.markdown(kpi_card_html("Median Rating",  f"{med_r:.2f}"),         unsafe_allow_html=True)
    with c3:  st.markdown(kpi_card_html("Std Deviation",  f"{std_r:.2f}"),         unsafe_allow_html=True)
    with c4:  st.markdown(kpi_card_html("Highest Rating", f"{max_r:.2f}"),         unsafe_allow_html=True)
    with c5:  st.markdown(kpi_card_html("Lowest Rating",  f"{min_r:.2f}"),         unsafe_allow_html=True)
    with c6:  st.markdown(kpi_card_html("Rated 7 or Above", f"{pct_above_7:.1f}%"), unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Distribution",
        "By Genre",
        "By Platform",
        "Top & Bottom Games",
    ])

    with tab1:
        col_l, col_r = st.columns(2)
        with col_l:
            chart_card(charts.rating_distribution_histogram(filtered_df), key="ra_hist")
        with col_r:
            st.markdown("#### Descriptive Statistics")
            desc_df = (
                filtered_df["user_rating"].describe().round(3)
                .reset_index()
            )
            desc_df.columns = ["Statistic", "Value"]
            st.dataframe(desc_df, use_container_width=True, hide_index=True)

            st.markdown("#### Rating Buckets")
            bins   = [0, 2, 4, 6, 7, 8, 9, 10]
            labels = ["0–2", "2–4", "4–6", "6–7", "7–8", "8–9", "9–10"]
            bucket_series = pd.cut(filtered_df["user_rating"], bins=bins, labels=labels, right=True)
            bucket_counts = bucket_series.value_counts().sort_index().reset_index()
            bucket_counts.columns = ["Rating Range", "Count"]
            bucket_counts["Share (%)"] = (
                bucket_counts["Count"] / bucket_counts["Count"].sum() * 100
            ).round(1)
            st.dataframe(bucket_counts, use_container_width=True, hide_index=True)

    with tab2:
        chart_card(charts.rating_by_genre_box(filtered_df),               key="ra_gbox")
        chart_card(charts.rating_violin(filtered_df, col="genre"),         key="ra_gviolin")

    with tab3:
        chart_card(charts.rating_by_platform_box(filtered_df),             key="ra_pbox")
        chart_card(charts.rating_violin(filtered_df, col="platform"),      key="ra_pviolin")

    with tab4:
        n_top = st.slider("Top games to show", 5, 30, 15, step=5, key="top_slider")
        chart_card(charts.top_rated_games_bar(filtered_df, n=n_top),       key="ra_top")

        st.markdown("#### Lowest-Rated Games")
        n_bot = st.slider("Bottom games to show", 5, 30, 10, step=5, key="bot_slider")
        bottom = (
            filtered_df.nsmallest(n_bot, "user_rating")[
                ["game_name", "genre", "platform", "release_year", "user_rating"]
            ]
            .copy()
            .rename(columns={
                "game_name":    "Game",
                "genre":        "Genre",
                "platform":     "Platform",
                "release_year": "Year",
                "user_rating":  "Rating",
            })
        )
        bottom["Rating"] = bottom["Rating"].round(2)
        st.dataframe(bottom, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════
# PAGE 5 — GAME EXPLORER
# ══════════════════════════════════════════════
elif page == "explorer":
    page_title("Game Explorer", "Search, filter, and download the gaming dataset.")
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    col_search, col_sort_col, col_sort_dir = st.columns([3, 2, 1])
    with col_search:
        search_query = st.text_input(
            "Search by game name",
            placeholder="e.g. Minecraft, Zelda …",
            key="search_box",
            label_visibility="collapsed",
        )
    display_df = filtered_df.copy()
    if search_query.strip():
        display_df = display_df[
            display_df["game_name"].str.contains(search_query.strip(), case=False, na=False)
        ]

    available_cols = list(display_df.columns)
    with col_sort_col:
        sort_col = st.selectbox("Sort by", options=available_cols,
                                index=len(available_cols) - 1, label_visibility="collapsed")
    with col_sort_dir:
        sort_asc = st.checkbox("Asc", value=False)

    sel_cols = st.multiselect(
        "Columns to display", options=available_cols, default=available_cols,
        key="explorer_cols",
    )
    if not sel_cols:
        sel_cols = available_cols

    display_df = display_df[sel_cols].sort_values(sort_col, ascending=sort_asc)

    st.markdown(
        f"<p style='font-size:0.82rem;color:{C['muted']};margin-bottom:6px;'>"
        f"{len(display_df):,} records displayed</p>",
        unsafe_allow_html=True,
    )
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=480)

    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download as CSV",
        data=csv_bytes,
        file_name="filtered_games.csv",
        mime="text/csv",
        use_container_width=True,
    )

    if not display_df.empty and "user_rating" in display_df.columns:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        section_heading("Quick Stats")
        q1, q2, q3, q4 = st.columns(4)
        q1.metric("Records",    fmt_number(len(display_df)))
        q2.metric("Avg Rating", f"{display_df['user_rating'].mean():.2f}")
        q3.metric("Highest",    f"{display_df['user_rating'].max():.2f}")
        q4.metric("Lowest",     f"{display_df['user_rating'].min():.2f}")


# ══════════════════════════════════════════════
# PAGE 6 — DATA QUALITY & CORRELATION
# ══════════════════════════════════════════════

elif page == "quality":
    page_title("Data Quality & Correlation", "Dataset diagnostics and statistical relationships.")
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    tab_dq, tab_corr = st.tabs(["Data Quality Report", "Correlation Analysis"])

    with tab_dq:
        section_heading("Dataset Dimensions")
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Raw Rows",           fmt_number(len(raw_df)) if not raw_df.empty else "N/A")
        d2.metric("Clean Rows",         fmt_number(len(df_clean)))
        d3.metric("Columns",            len(df_clean.columns))
        d4.metric("Duplicates Removed", fmt_number(cleaning_report.get("duplicates_removed", 0)))

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        section_heading("Column Data Types")
        dtype_df = pd.DataFrame({
            "Column":    df_clean.dtypes.index,
            "Data Type": df_clean.dtypes.values.astype(str),
        })
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        section_heading("Missing Values")
        missing     = df_clean.isnull().sum()
        missing_pct = (missing / len(df_clean) * 100).round(2)
        missing_df  = pd.DataFrame({
            "Column":         missing.index,
            "Missing Count":  missing.values,
            "Missing %":      missing_pct.values,
        })
        if missing_df["Missing Count"].sum() == 0:
            st.success("No missing values in the cleaned dataset.")
        else:
            st.dataframe(missing_df, use_container_width=True, hide_index=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        section_heading("Numerical Summary Statistics")
        num_df = df_clean.select_dtypes(include=np.number)
        if not num_df.empty:
            st.dataframe(num_df.describe().round(3), use_container_width=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        section_heading("Categorical Summary")
        cat_df = df_clean.select_dtypes(include=["object", "string"])
        if not cat_df.empty:
            cat_rows = []
            for col in cat_df.columns:
                vc = cat_df[col].value_counts()
                cat_rows.append({
                    "Column":        col,
                    "Unique Values": cat_df[col].nunique(),
                    "Most Frequent": vc.index[0],
                    "Frequency":     int(vc.iloc[0]),
                })
            st.dataframe(pd.DataFrame(cat_rows), use_container_width=True, hide_index=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        section_heading("Cleaning Operations")
        ops = [
            ("Columns renamed to snake_case",                                              "Done"),
            ("Whitespace stripped from string columns",                                    "Done"),
            (f"Duplicate rows removed: {cleaning_report.get('duplicates_removed', 0)}",   "Done"),
            (f"Rows dropped (invalid Release Year): {cleaning_report.get('rows_dropped_bad_year', 0)}", "Done"),
            (f"Rows dropped (invalid User Rating): {cleaning_report.get('rows_dropped_bad_rating', 0)}", "Done"),
            (f"Ratings clipped to [0, 10]: {cleaning_report.get('ratings_clipped', 0)} values", "Done"),
            ("Text standardised to Title Case",                                            "Done"),
            ("Literal 'nan' strings replaced with NaN",                                   "Done"),
        ]
        for desc, status in ops:
            st.markdown(f"- **{status}** — {desc}")

    with tab_corr:
        section_heading(
            "Correlation Analysis",
            "Pearson correlation coefficients between numerical variables in the filtered dataset.",
        )
        num_cols = filtered_df.select_dtypes(include=np.number).columns.tolist()
        if len(num_cols) >= 2:
            fig_corr = charts.correlation_heatmap(filtered_df)
            if fig_corr is not None:
                chart_card(fig_corr, key="corr_heat")

            corr_matrix = filtered_df[num_cols].corr().round(4)
            st.markdown("#### Correlation Coefficients")
            st.dataframe(corr_matrix, use_container_width=True)

            st.markdown("#### Interpretation Guide")
            st.info(
                "r = 1.0 → Perfect positive correlation\n\n"
                "r = −1.0 → Perfect negative correlation\n\n"
                "r ≈ 0 → Little or no linear relationship\n\n"
                "|r| ≥ 0.7 → Strong  ·  |r| 0.4–0.7 → Moderate  ·  |r| < 0.4 → Weak\n\n"
                "Note: correlation does not imply causation."
            )

            pairs = []
            for i in range(len(num_cols)):
                for j in range(i + 1, len(num_cols)):
                    pairs.append({
                        "Variable 1": num_cols[i],
                        "Variable 2": num_cols[j],
                        "r": round(corr_matrix.iloc[i, j], 4),
                    })
            if pairs:
                st.markdown("#### Strongest Correlations")
                st.dataframe(
                    pd.DataFrame(pairs).sort_values("r", key=abs, ascending=False),
                    use_container_width=True, hide_index=True,
                )
        else:
            st.info(
                "Only one numerical column is present (user_rating). "
                "The scatter chart below shows its relationship with release year."
            )
            chart_card(charts.scatter_year_vs_rating(filtered_df), key="corr_scatter")
            r_val = filtered_df["release_year"].corr(filtered_df["user_rating"])
            st.metric("Pearson r — Release Year vs User Rating", f"{r_val:.4f}")
            st.caption(
                "A near-zero value confirms no meaningful linear relationship between "
                "release year and user rating in this dataset."
            )


# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown(
    f"<div style='"
    f"border-top:1px solid {C['border']};"
    f"margin-top:2.5rem;"
    f"padding-top:14px;"
    f"text-align:center;"
    f"font-size:0.73rem;"
    f"color:{C['muted']};"
    f"font-family:Inter,sans-serif;"
    f"'>"
    f"Gaming Analytics Dashboard &nbsp;·&nbsp; MCA Data Science Mini-Project &nbsp;·&nbsp; "
    f"Built with Streamlit, Pandas &amp; Plotly"
    f"</div>",
    unsafe_allow_html=True,
)
