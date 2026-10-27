# 🎮 Gaming Analytics Dashboard

**MCA Data Science Mini-Project — Interactive Python Dashboard**

---

## Project Objective

Build a fully interactive, data-driven analytics dashboard that explores gaming trends, genre distributions, platform comparisons, and user-rating patterns using the provided `games_dataset.csv`. The dashboard demonstrates practical skills in Python programming, data preprocessing, exploratory data analysis (EDA), and interactive data visualisation.

---

## Dataset Description

| Field | Description |
|---|---|
| **Game Name** | Title of the video game |
| **Genre** | Game genre (Action, Adventure, Horror, Puzzle, Racing, Role-playing, Shooter, Simulation, Sports, Stealth, Strategy, Survival, Fighting, Platformer) |
| **Platform** | Platform the game is available on (PC, PlayStation, Xbox, Nintendo Switch, Mobile) |
| **Release Year** | Year the game was released (2000–2023) |
| **User Rating** | Community user rating on a 0–10 scale |

---

## Technologies Used

| Library | Purpose |
|---|---|
| **Python 3.10+** | Core programming language |
| **Streamlit ≥ 1.32** | Interactive dashboard UI |
| **Pandas ≥ 2.0** | Data loading, cleaning, aggregation |
| **NumPy ≥ 1.26** | Numerical operations |
| **Plotly ≥ 5.18** | All interactive charts |

---

## Features & Dashboard Pages

### 🏠 Overview
- 6 dynamic KPI cards (Total Records, Unique Games, Genres, Platforms, Avg Rating, Year Range)
- Rating distribution histogram
- Genre share donut chart
- Top 15 highest-rated games bar chart
- Auto-generated key insights (8 insight cards)

### 📈 Gaming Trends
- Games released per year — line chart
- Average rating per year — line chart
- Releases by platform — stacked area chart
- Release year vs rating — scatter plot (coloured by genre)
- Year-by-year summary table (sortable)

### 🎭 Genre & Platform Analysis
- Games per genre — horizontal bar (switchable: count / avg rating)
- Genre share — donut chart
- Rating distribution by genre — boxplot
- Games per platform — vertical bar
- Average rating per platform — bar chart
- Rating distribution by platform — boxplot
- Platform × Genre heatmap
- Genre summary statistics table

### ⭐ Ratings & Performance
- 6 rating KPI cards (Mean, Median, Std Dev, Max, Min, % ≥ 7)
- Rating histogram + descriptive stats + bucket breakdown
- Rating violin plots by genre and platform
- Top N / Bottom N games table (adjustable slider)

### 🔍 Game Explorer
- Full filtered dataset table with 500-row scrollable view
- Text search by game name
- Column selector (show/hide columns)
- Sort by any column (asc/desc)
- CSV download button for the current view

### 🔗 Data Quality & Correlation
- Dataset dimensions and cleaning summary
- Column data types
- Missing values report
- Numerical summary statistics
- Categorical variable summary
- Cleaning operations log
- Pearson correlation heatmap
- Correlation coefficient table with strength interpretation

---

## Data Preprocessing

1. **Column rename** — snake_case (e.g. `Game Name` → `game_name`)
2. **Whitespace stripping** — removes leading/trailing spaces from all string fields
3. **Duplicate removal** — exact duplicate rows are dropped
4. **Release Year** — coerced to integer; unparseable rows dropped
5. **User Rating** — coerced to float; unparseable rows dropped; clipped to [0, 10]
6. **Text standardisation** — Title Case applied to `game_name`, `genre`, `platform`
7. **NaN strings** — literal `"nan"` strings replaced with proper `NaN`

All preprocessing is cached using `@st.cache_data` for performance.

---

## Project Structure

```
gaming-dashboard/
├── app.py                    # Main Streamlit application entry point
├── games_dataset.csv         # Dataset (place here before running)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── data/
│   ├── __init__.py
│   └── data_processing.py    # Load, clean, filter the dataset
├── utils/
│   ├── __init__.py
│   ├── charts.py             # All Plotly chart functions
│   ├── insights.py           # Dynamic insight generation
│   └── helpers.py            # Formatting helpers, colour palette, KPI card HTML
└── .streamlit/
    └── config.toml           # Dark theme configuration
```

---

## Installation & Setup

### 1. Create and activate a virtual environment

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify the dataset is present

Make sure `games_dataset.csv` is in the `gaming-dashboard/` folder (same level as `app.py`).

### 4. Launch the dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`.

---

## Important Implementation Details

- **Pathlib** is used to locate the CSV relative to `app.py`, so the app works regardless of the working directory.
- **`@st.cache_data`** caches both the raw load and the cleaning step — reloading the page is fast.
- **Session state** is used to track sidebar filter selections and support the Reset Filters button without stale values.
- **Empty-filter guard** — if filters return zero rows the app shows a warning and stops rendering instead of crashing.
- **Division-by-zero** — all percentage calculations use `.sum()` checks before dividing.
- **No hardcoded results** — every KPI, insight, and chart recalculates dynamically from the filtered DataFrame.

---

## Key Python Functions Reference

| Function | File | Purpose |
|---|---|---|
| `load_raw_data()` | `data_processing.py` | Reads CSV with pathlib, returns raw DataFrame |
| `clean_data(df)` | `data_processing.py` | Cleans and returns (cleaned_df, report) |
| `apply_filters(df, ...)` | `data_processing.py` | Applies sidebar filter selections |
| `generate_insights(df)` | `insights.py` | Returns list of computed insight dicts |
| `kpi_card_html(...)` | `helpers.py` | Generates styled HTML KPI card string |
| `rating_distribution_histogram(df)` | `charts.py` | Plotly histogram of ratings |
| `games_per_genre_bar(df, metric)` | `charts.py` | Bar chart, switchable metric |
| `platform_genre_heatmap(df)` | `charts.py` | 2D heatmap of game counts |
| `releases_per_year_line(df)` | `charts.py` | Time-series line chart |
| `correlation_heatmap(df)` | `charts.py` | Pearson r heatmap |

---

## Viva Questions & Answers

**Q1. What is Streamlit and why was it chosen?**  
Streamlit is an open-source Python library that converts Python scripts into interactive web apps with minimal code. It was chosen because it requires no HTML/CSS/JavaScript knowledge, supports reactive widgets, and is widely used for data science prototyping and dashboards.

**Q2. What is `@st.cache_data` and why is it important?**  
`@st.cache_data` caches the return value of a function after its first call. On subsequent calls with the same arguments Streamlit returns the cached result without re-executing the function. This is critical here because loading and cleaning a CSV on every user interaction would be slow and wasteful.

**Q3. How does filtering work in this dashboard?**  
The `apply_filters()` function in `data_processing.py` receives the cleaned DataFrame and the user's sidebar selections (genres, platforms, year range, rating range). It chains Pandas boolean masks and returns a new filtered DataFrame. All charts and KPIs receive this filtered frame, so every element updates simultaneously.

**Q4. What is Plotly Express and how does it differ from Plotly Graph Objects?**  
Plotly Express (`px`) is a high-level API that creates common chart types with a single function call. Plotly Graph Objects (`go`) is the lower-level API that provides full control over every visual element. This project uses `px` for most charts and `go` for the correlation heatmap where fine-grained control over the matrix masking was needed.

**Q5. What data cleaning steps were applied and why?**  
Seven steps were applied: column renaming for consistency; whitespace stripping to avoid mismatches; duplicate removal to avoid inflated counts; type coercion for numeric columns with invalid entries; rating clipping to remove values outside [0,10]; text standardisation to Title Case so groupby works correctly; and replacement of literal "nan" strings with proper NaN values.

**Q6. What does correlation analysis tell us about this dataset?**  
The Pearson correlation heatmap shows the linear relationship between `release_year` and `user_rating`. A value near zero confirms there is no strong linear trend between when a game was released and how users rated it, meaning newer games are not necessarily rated higher or lower than older ones.

**Q7. How does the dashboard handle empty filter results?**  
After `apply_filters()` returns the filtered DataFrame, `app.py` immediately checks `if filtered_df.empty` and calls `st.warning()` followed by `st.stop()`. This prevents any chart function from receiving an empty frame and avoids division-by-zero or index errors.

**Q8. What is the difference between `pd.cut()` and `pd.qcut()`?**  
`pd.cut()` divides data into bins of equal width (fixed boundary points). `pd.qcut()` divides data into bins with equal number of records (quantile-based). This project uses `pd.cut()` for the rating buckets page because the fixed ranges (0–2, 2–4, …) are more intuitive for a 0–10 rating scale.

**Q9. Why are vectorised Pandas operations preferred over Python loops?**  
Pandas operations like `.str.strip()`, `.groupby()`, and boolean masking run on the underlying NumPy arrays in compiled C/Cython code, which is orders of magnitude faster than a Python `for` loop iterating row by row. For a dataset with thousands of records this difference is very noticeable.

**Q10. How is session state used in the sidebar?**  
`st.session_state` stores the current filter values between Streamlit re-runs. The Reset Filters button calls a function that writes the original all-selected defaults back into session state keys and then calls `st.rerun()` to re-render the page with those defaults, effectively resetting every filter simultaneously.
