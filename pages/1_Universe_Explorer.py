from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Universe Explorer | ExoWorlds",
    layout="wide"
)

from Style import apply_global_styles
from src.data import load_planets

apply_global_styles()

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "static" / "EWE_Logo.png"
left, right = st.columns([4, 1])
with left:
    st.title("Universe Explorer")
    st.markdown(
        '<p class="search-caption">Search confirmed exoplanets.</p>',
        unsafe_allow_html=True
    )
with right:
    st.image(str(LOGO), use_container_width=True)

with st.sidebar:
    st.markdown("**MISSION CONTROL**")
    st.write("Use the pages above to discover real exoplanets, inspect their properties and experiment with hypothetical worlds.")
    st.divider()
    st.markdown("Wi-Fi Hiders")
    st.caption("Alex Battrick")
    st.caption("William Wain")
    st.divider()

with st.spinner("Opening the star catalogue..."):
    planets, data_source, load_error = load_planets()

    st.caption(f"Data source: {data_source} · {len(planets):,} planets loaded")

    if load_error:
        st.warning(f"NASA data could not be loaded: {load_error}")



st.caption("")

c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    search = st.text_input("Search by planet or host star", placeholder="e.g. Kepler, TRAPPIST, 51 Pegasi")
with c2:
    years = planets["disc_year"].dropna()
    min_year = int(years.min()) if not years.empty else 1990
    max_year = int(years.max()) if not years.empty else 2026
    year_range = st.slider("Discovery year", min_year, max_year, (min_year, max_year))
with c3:
    methods = sorted(planets["discoverymethod"].dropna().unique().tolist())
    selected_methods = st.multiselect("Discovery method", methods, default=[])

filtered = planets.copy()
if search:
    mask = (
        filtered["pl_name"].str.contains(search, case=False, na=False)
        | filtered["hostname"].str.contains(search, case=False, na=False)
    )
    filtered = filtered[mask]
if not filtered["disc_year"].dropna().empty:
    filtered = filtered[
        filtered["disc_year"].isna()
        | filtered["disc_year"].between(year_range[0], year_range[1])
    ]
if selected_methods:
    filtered = filtered[filtered["discoverymethod"].isin(selected_methods)]

m1, m2, m3 = st.columns(3)
m1.metric("Matching planets", f"{len(filtered):,}")
m2.metric("Host stars", f"{filtered['hostname'].nunique():,}")
m3.metric("Discovery methods", f"{filtered['discoverymethod'].nunique():,}")

st.divider()
st.subheader("Planet catalogue")
display = filtered[[
    "pl_name",
    "hostname",
    "disc_year",
    "discoverymethod",
    "pl_rade",
    "pl_dens",
    "pl_orbper",
    "pl_orbeccen",
    "pl_eqt",
    "sy_dist"
]].rename(columns={
    "pl_name": "Planet",
    "hostname": "Host star",
    "disc_year": "Year",
    "discoverymethod": "Discovery method",
    "pl_rade": "Radius (Earth)",
    "pl_dens": "Density (g/cm³)",
    "pl_orbper": "Orbital Period (days)",
    "pl_orbeccen": "Eccentricity",
    "pl_eqt": "Temp. (K)",
    "sy_dist": "Distance (pc)"
})

st.dataframe(display, use_container_width=True, hide_index=True, height=420)


st.caption("")

st.markdown("""
<div class="observatory-box">
    <a class="observatory-link" href="/Planet_Observatory">
        Open Planet Observatory →
    </a>
</div>
""", unsafe_allow_html=True)
