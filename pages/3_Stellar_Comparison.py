from pathlib import Path
import random
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from Style import apply_global_styles
from src.data import load_planets


st.set_page_config(
    page_title="Stellar Comparison | ExoWorlds",
    layout="wide"
)
comparison_options = {
    "Radius (Earth Multiple)": ("pl_rade", 3),
    "Mass (Earth Multiple)": ("pl_bmasse", 3),
    "Density (g/cm³)": ("pl_dens", 4),
    "Orbital Period (Days)": ("pl_orbper", 2),
    "Orbital Eccentricity": ("pl_orbeccen", 4),
    "Equilibrium Temperature (Kelvin)": ("pl_eqt", 0),
    "Orbital Radius (AU)": ("pl_orbsmax", 4)
}




def select_random_planet_1():
    st.session_state["planet_selector_1"] = random.choice(names)


def select_random_planet_2():
    st.session_state["planet_selector_2"] = random.choice(names)

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



apply_global_styles()

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "static" / "EWE_Logo.png"
left, right = st.columns([4, 1])
with left:
    st.title("Stellar Comparison")
    st.markdown(
        '<p class="search-caption">Compare exoplanets.</p>',
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

planets, data_source, load_error = load_planets()

names = planets["pl_name"].tolist()
# Restore previously selected planets
saved1 = st.session_state.get("selected_planet_1")
saved2 = st.session_state.get("selected_planet_2")

index1 = names.index(saved1) if saved1 in names else 0
index2 = names.index(saved2) if saved2 in names else min(1, len(names) - 1)

with st.container():

    st.markdown(
        '<p class="planet-select-label">Select planets to compare</p>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        select_col, random_col = st.columns([4, 1])

        with select_col:
            name1 = st.selectbox(
                "First planet",
                names,
                index=index1,
                label_visibility="collapsed",
                key="planet_selector_1"
            )

        with random_col:
            st.button(
                "🎲",
                use_container_width=True,
                on_click=select_random_planet_1
            )

    with col2:
        select_col, random_col = st.columns([4, 1])

        with select_col:
            name2 = st.selectbox(
                "Second planet",
                names,
                index=index2,
                label_visibility="collapsed",
                key="planet_selector_2"
            )

        with random_col:
            st.button(
                "🎲 ",
            use_container_width=True,
            on_click=select_random_planet_2
            )

st.session_state["selected_planet_1"] = name1
st.session_state["selected_planet_2"] = name2

p1 = planets.loc[planets["pl_name"] == name1].iloc[0]
p2 = planets.loc[planets["pl_name"] == name2].iloc[0]

st.markdown("### Select comparison data")

selected_property = st.selectbox(
    "Data point",
    list(comparison_options.keys()),
    label_visibility="collapsed"
)

column, decimal = comparison_options[selected_property]

compare_planets(
    p1["pl_name"],
    p1[column],
    p2["pl_name"],
    p2[column],
    selected_property,
    decimal
)