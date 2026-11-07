import streamlit as st
from src.data import load_planets

st.set_page_config(page_title="Universe Explorer | ExoWorlds", page_icon="🔭", layout="wide")
st.title("🔭 Universe Explorer")
st.caption("Search confirmed exoplanets and find a world that catches your attention.")

with st.spinner("Opening the star catalogue..."):
    planets, source = load_planets()

st.caption(f"Data source: {source} · {len(planets):,} planets loaded")

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
    "pl_name", "hostname", "disc_year", "discoverymethod",
    "pl_rade", "pl_eqt", "sy_dist"
]].rename(columns={
    "pl_name": "Planet", "hostname": "Host star", "disc_year": "Year",
    "discoverymethod": "Discovery method", "pl_rade": "Radius (Earth)",
    "pl_eqt": "Temp. (K)", "sy_dist": "Distance (pc)"
})
st.dataframe(display, use_container_width=True, hide_index=True, height=420)

if not filtered.empty:
    st.subheader("Select a world")
    names = filtered["pl_name"].tolist()
    current = st.session_state.get("selected_planet")
    default_index = names.index(current) if current in names else 0
    selected = st.selectbox("Choose a planet to inspect", names, index=default_index)
    st.session_state["selected_planet"] = selected
    planet = filtered.loc[filtered["pl_name"] == selected].iloc[0]

    with st.container(border=True):
        st.markdown(f"### 🪐 {planet['pl_name']}")
        st.write(f"Orbits **{planet['hostname']}** · Discovered {int(planet['disc_year']) if planet['disc_year'] == planet['disc_year'] else 'in an unreported year'}")
        x, y, z = st.columns(3)
        x.metric("Radius", f"{planet['pl_rade']:.2f} Earth radii" if planet['pl_rade'] == planet['pl_rade'] else "Unknown")
        y.metric("Equilibrium temperature", f"{planet['pl_eqt']:.0f} K" if planet['pl_eqt'] == planet['pl_eqt'] else "Unknown")
        z.metric("Distance", f"{planet['sy_dist']:.1f} parsecs" if planet['sy_dist'] == planet['sy_dist'] else "Unknown")
        st.page_link("pages/2_Planet_Observatory.py", label="Open Planet Observatory →")
else:
    st.warning("No planets match those filters. Try clearing the search or discovery method.")
