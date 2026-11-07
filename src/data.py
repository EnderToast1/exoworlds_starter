
from pathlib import Path
import pandas as pd
import requests
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_FILE = ROOT / "data" / "exoplanets_sample.csv"

# NASA Exoplanet Archive TAP service. We request only fields used by this prototype.
TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
QUERY = """
select  pl_name,
    hostname,
    discoverymethod,
    disc_year,
    pl_orbper,
    pl_orbeccen,
    pl_rade,
    pl_bmasse,
    pl_dens,
    pl_eqt,
    sy_dist,
    st_teff,
    pl_orbsmax
from pscomppars
order by disc_year desc
"""

@st.cache_data(ttl=3600, show_spinner=False)
def load_planets():
    """Load confirmed exoplanets from NASA, with an offline fallback."""

    try:
        response = requests.get(
            TAP_URL,
            params={
                "query": " ".join(QUERY.split()),
                "format": "csv"
            },
            timeout=60
        )
        print(response.status_code)
        print(response.text[:500])

        response.raise_for_status()

        from io import StringIO

        df = pd.read_csv(StringIO(response.text))

        if df.empty or "pl_name" not in df.columns:
            raise ValueError("NASA returned an empty or unexpected dataset.")

        df = clean_planets(df)

        if not df.empty:
            return df, "NASA Exoplanet Archive", None

    except Exception as e:
        error = f"{type(e).__name__}: {e}"
        print(f"NASA API error: {error}")

        # Check whether fallback data exists
        if not SAMPLE_FILE.exists():
            raise FileNotFoundError(
                f"Sample dataset not found: {SAMPLE_FILE}\n"
                f"NASA API error: {error}"
            )

        df = pd.read_csv(SAMPLE_FILE)

        return clean_planets(df), "Bundled sample data (offline fallback)", error

def clean_planets(df):
    df = df.copy()

    expected = [
        "pl_name", "hostname", "discoverymethod", "disc_year",
        "pl_orbper", "pl_orbeccen", "pl_rade", "pl_bmasse",
        "pl_dens", "pl_eqt", "sy_dist", "st_teff","pl_orbsmax"
    ]

    # Add any missing columns
    for col in expected:
        if col not in df.columns:
            df[col] = pd.NA

    # Convert numeric columns
    numeric_columns = [
        "disc_year",
        "pl_orbper",
        "pl_orbeccen",
        "pl_rade",
        "pl_bmasse",
        "pl_dens",
        "pl_eqt",
        "sy_dist",
        "st_teff",
        "pl_orbsmax"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Clean text columns
    df["pl_name"] = df["pl_name"].fillna("Unnamed planet").astype(str)
    df["hostname"] = df["hostname"].fillna("Unknown star").astype(str)
    df["discoverymethod"] = (
        df["discoverymethod"].fillna("Not reported").astype(str)
    )

    return df[expected].drop_duplicates(
        subset=["pl_name"]
    ).reset_index(drop=True)