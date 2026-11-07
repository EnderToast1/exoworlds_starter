import random
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from Style import apply_global_styles
from src.orbitPlot import display_orbit
from src.data import load_planets
def compare_with_earth(
    planet_name,
    value,
    property_name,
    earth_value=1,
    earth_label="Earth = 1",
    unit="",
    decimals=2
):
    st.subheader(f"Comparison: {property_name}")

    if pd.notna(value):
        fig = go.Figure(go.Bar(
            x=["Earth", planet_name],
            y=[earth_value, value],
            marker_color=["#50C878", "#69b7f0"],
            text=[
                round(earth_value, decimals),
                round(value, decimals)
            ],
            textposition="outside",
        ))

        fig.update_layout(
            height=330,
            yaxis_title=f"{property_name} ({earth_label})",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e9edff",
            margin=dict(l=10, r=10, t=20, b=10),
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.markdown(f"""
        <div class="info-box">
            A {property_name.lower()} measurement is not available
            for this planet.
        </div>
        """, unsafe_allow_html=True)


import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def compare_planets(
    planet1_name,
    value1,
    planet2_name,
    value2,
    property_name,
    decimals=2
):
    st.subheader(f"Comparison: {property_name}")

    # Check whether either planet has a measurement
    available = []
    missing = []

    if pd.notna(value1):
        available.append((planet1_name, value1))
    else:
        missing.append(planet1_name)

    if pd.notna(value2):
        available.append((planet2_name, value2))
    else:
        missing.append(planet2_name)

    if available:
        names = [item[0] for item in available]
        values = [item[1] for item in available]

        fig = go.Figure(go.Bar(
            x=names,
            y=values,
            marker_color=["#50C878", "#69b7f0"][:len(available)],
            text=[f"{v:,.{decimals}f}" for v in values],
            textposition="outside",
        ))

        fig.update_layout(
            height=330,
            yaxis_title=f"{property_name}",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e9edff",
            margin=dict(l=10, r=10, t=20, b=10),
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)

    if missing:
        st.markdown(f"""
        <div class="info-box">
            No {property_name.lower()} measurement available for:
            {", ".join(missing)}
        </div>
        """, unsafe_allow_html=True)

def select_random_planet():
    names = planets["pl_name"].tolist()
    random_name = random.choice(names)

    st.session_state["selected_planet"] = random_name
    st.session_state["planet_selector"] = random_name




apply_global_styles()
ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "static" / "EWE_Logo.png"

left, right = st.columns([4, 1])
with left:
    st.set_page_config(page_title="Planetary Observatory | ExoWorlds", page_icon="", layout="wide")
    st.title("Planetary Observatory")
    st.caption("A closer look at exoplanet properties.")
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

planets, data_source, load_error = load_planets()

st.caption(f"Data source: {data_source}")

if load_error:
    st.warning(f"NASA data could not be loaded: {load_error}")
if planets.empty:
    st.error("No planet data is available.")
    st.stop()

names = planets["pl_name"].tolist()

saved = st.session_state.get("selected_planet")
index = names.index(saved) if saved in names else 0

with st.container():
    st.markdown(
        '<p class="planet-select-label">Select a planet</p>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([4, 1])

    with col1:
        name = st.selectbox(
            "Select a planet",
            names,
            index=index,
            label_visibility="collapsed",
            key="planet_selector"
        )

    with col2:
        st.button(
            "🎲 Random",
            use_container_width=True,
            on_click=select_random_planet
        )

st.session_state["selected_planet"] = name

p = planets.loc[planets["pl_name"] == name].iloc[0]

st.markdown(f"## {p['pl_name']}")
st.write(f"Host star: **{p['hostname']}** · Discovery method: **{p['discoverymethod']}**")

def metric_value(value, suffix="", decimals=2):
    return f"{value:,.{decimals}f}{suffix}" if pd.notna(value) else "Not reported"

cols = st.columns(4)
cols[0].metric("Radius", metric_value(p["pl_rade"], " Earth radii"))
cols[1].metric("Mass", metric_value(p["pl_bmasse"], " Earth masses"))
cols[2].metric("Orbital period", metric_value(p["pl_orbper"], " days"))
cols[3].metric("Equilibrium temperature", metric_value(p["pl_eqt"], " K", 0))

st.divider()
left, right = st.columns([1.1, 1])
with left:
    compare_with_earth(
        p["pl_name"],
        p["pl_rade"],
        "Radius (Multiple)",
        earth_label="Earth radii"
    )

with right:
    st.subheader("Host star and discovery")
    st.write(f"**Host star temperature:** {metric_value(p['st_teff'], ' K', 0)}")
    st.write(f"**Orbital radius around Host star:** {metric_value(p['pl_orbsmax'], ' AU', 3)}")
    st.write(f"**Orbital eccentricity:** {metric_value(p['pl_orbeccen'], '', 4)}")
    st.write(f"**Distance from Solar System:** {metric_value(p['sy_dist'], ' parsecs')}")
    st.write(f"**Discovery year:** {int(p['disc_year']) if pd.notna(p['disc_year']) else 'Not reported'}")
    st.write(f"**Method:** {p['discoverymethod']}")

st.caption(f"Source: {data_source}. Planetary measurements are not direct photographs of the planet's surface.")


left,right =st.columns([1, 1])
with left:
    compare_with_earth(
        p["pl_name"],
        p["pl_bmasse"],
        "Mass (Multiple)",
        earth_label="Earth masses"
    )
with right:
    compare_with_earth(
        p["pl_name"],
        p["pl_orbper"],
        "Orbital period (Days)",
        earth_label="Earth Days"
    )

left,right =st.columns([1, 1])
with left:
    compare_planets(
        "Earth",
        0.0167,
        p["pl_name"],
        p["pl_orbeccen"],
        "Eccentricity",
        5,

    )

with right:
    compare_planets(
        "Earth",
        288,
        p["pl_name"],
        p["pl_eqt"],
        "Temperature (Kelvin)",
2
    )

display_orbit(
    p["pl_name"],
    p["pl_orbsmax"],
    p["pl_orbeccen"],
    p["pl_orbper"]
)