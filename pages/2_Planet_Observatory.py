import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from Style import apply_global_styles
from src.data import load_planets

apply_global_styles()

st.set_page_config(page_title="Planet Observatory | ExoWorlds", page_icon="🌍", layout="wide")
st.title("🌍 Planet Observatory")
st.caption("A closer look at the properties astronomers have measured.")

planets, source = load_planets()
if planets.empty:
    st.error("No planet data is available.")
    st.stop()

names = planets["pl_name"].tolist()
saved = st.session_state.get("selected_planet")
index = names.index(saved) if saved in names else 0
name = st.selectbox("Select a planet", names, index=index)
st.session_state["selected_planet"] = name
p = planets.loc[planets["pl_name"] == name].iloc[0]

st.markdown(f"## 🪐 {p['pl_name']}")
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
    st.subheader("Compared with Earth")
    radius = p["pl_rade"]
    if pd.notna(radius):
        fig = go.Figure(go.Bar(
            x=["Earth", p["pl_name"]],
            y=[1, radius],
            marker_color=["#4f83cc", "#a78bfa"],
            text=[1, round(radius, 2)],
            textposition="outside",
        ))
        fig.update_layout(
            height=330, yaxis_title="Radius (Earth = 1)",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e9edff", margin=dict(l=10, r=10, t=20, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("A radius measurement is not available for this planet.")

with right:
    st.subheader("Host star and discovery")
    st.write(f"**Host star temperature:** {metric_value(p['st_teff'], ' K', 0)}")
    st.write(f"**Distance from Earth:** {metric_value(p['sy_dist'], ' parsecs')}")
    st.write(f"**Discovery year:** {int(p['disc_year']) if pd.notna(p['disc_year']) else 'Not reported'}")
    st.write(f"**Method:** {p['discoverymethod']}")
    st.info("Measurements can be uncertain or unavailable. This prototype displays archive values rather than inventing missing measurements.")

st.caption(f"Source: {source}. Planetary measurements are not direct photographs of the planet's surface.")
