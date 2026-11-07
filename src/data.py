
from pathlib import Path
import pandas as pd
import requests
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_FILE = ROOT / "data" / "exoplanets_sample.csv"

# NASA Exoplanet Archive TAP service. We request only fields used by this prototype.
TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
QUERY = """
select pl_name, hostname, discoverymethod, disc_year,
       pl_orbper, pl_rade, pl_bmasse, pl_eqt, sy_dist, st_teff
from pscomppars
where default_flag = 1
order by disc_year desc
"""

@st.cache_data(ttl=3600, show_spinner=False)
def load_planets():
    """Load confirmed planets from NASA; fall back to bundled demo data offline."""
    try:
        response = requests.get(
            TAP_URL,
            params={"query": " ".join(QUERY.split()), "format": "csv"},
            timeout=18,
        )
        response.raise_for_status()
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        if df.empty or "pl_name" not in df.columns:
            raise ValueError("NASA returned an empty or unexpected dataset.")
        df = clean_planets(df)
        if not df.empty:
            return df, "NASA Exoplanet Archive"
    except Exception:
        pass

    df = pd.read_csv(SAMPLE_FILE)
    return clean_planets(df), "Bundled sample data (offline fallback)"


def clean_planets(df):
    df = df.copy()
    expected = [
        "pl_name", "hostname", "discoverymethod", "disc_year",
        "pl_orbper", "pl_rade", "pl_bmasse", "pl_eqt", "sy_dist", "st_teff"
    ]
    for col in expected:
        if col not in df.columns:
            df[col] = pd.NA

    for col in expected[3:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["pl_name"] = df["pl_name"].fillna("Unnamed planet").astype(str)
    df["hostname"] = df["hostname"].fillna("Unknown star").astype(str)
    df["discoverymethod"] = df["discoverymethod"].fillna("Not reported").astype(str)
    return df.drop_duplicates(subset=["pl_name"]).reset_index(drop=True)


def format_value(value, unit="", decimals=2):
    if pd.isna(value):
        return "Not reported"
    return f"{value:,.{decimals}f}{unit}"
