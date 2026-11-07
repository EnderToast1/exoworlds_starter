import math
from pathlib import Path

import pandas as pd
import streamlit as st

from Style import apply_global_styles


def get_temperature_colour(temperature):
    if pd.isna(temperature):
        return "#808080"

    # Temperature gradient stops
    stops = [
        (-100, (80, 160, 255)),   # Blue
        (-20,  (155, 212, 245)),  # Light blue
        (20,   (76, 170, 131)),   # Green
        (65,   (217, 120, 67)),   # Orange
        (150,  (220, 45, 45)),    # Red
        (500,  (150, 20, 50))     # Dark red
    ]

    temperature = max(stops[0][0], min(temperature, stops[-1][0]))

    for i in range(len(stops) - 1):
        t1, c1 = stops[i]
        t2, c2 = stops[i + 1]

        if t1 <= temperature <= t2:
            ratio = (temperature - t1) / (t2 - t1)

            rgb = tuple(
                int(c1[j] + (c2[j] - c1[j]) * ratio)
                for j in range(3)
            )

            return "#{:02x}{:02x}{:02x}".format(*rgb)

    return "#808080"


def calculate_habitability(temperature, atmosphere, water, gravity):
    """
    Calculates an Earth-like habitability score from 0–100.

    temperature: °C
    atmosphere: atmospheric pressure in atm
    water: percentage of surface covered by liquid water
    gravity: relative to Earth's gravity (1g)
    """

    # Individual factor scores
    temp_score = math.exp(-((temperature - 15) / 40) ** 2)

    pressure_score = math.exp(-((atmosphere - 1.0) / 1.2) ** 2)

    if 40 <= water <= 80:
        water_score = 1.0
    elif 20 <= water < 40 or 80 < water <= 95:
        water_score = 0.7
    elif 5 <= water < 20 or 95 < water <= 100:
        water_score = 0.3
    else:
        water_score = 0.0

    gravity_score = math.exp(-((gravity - 1.0) / 0.6) ** 2)

    # Weighted average
    weighted_score = (
        0.35 * temp_score +
        0.25 * pressure_score +
        0.25 * water_score +
        0.15 * gravity_score
    )

    # Penalise extremely unsuitable conditions
    weakest_factor = min(
        temp_score,
        pressure_score,
        water_score,
        gravity_score
    )

    score = round(
        100 * weighted_score * (0.3 + 0.7 * weakest_factor)
    )

    # Hard limits for unsuitable essential conditions
    if temp_score < 0.05 or pressure_score < 0.05 or water_score == 0:
        score = min(score, 15)

    return score





apply_global_styles()
ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "static" / "EWE_Logo.png"

left, right = st.columns([4, 1])
with left:
    st.set_page_config(page_title="World Engineer | ExoWorlds", page_icon="", layout="wide")
    st.title(" World Engineer")
    st.caption("Create a hypothetical planet by changing its physical environment.")
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



left, right = st.columns([1, 1.2])
with left:
    st.subheader("Planet parameters")
    radius = st.slider("Planet radius (Earth = 1)", 0.2, 3.5, 1.0, 0.1)
    temperature = st.slider("Average surface temperature (°C)", -150, 150, 15, 1)
    atmosphere = st.slider("Atmospheric pressure (atm)", 0.0, 15.0, 1.0, 0.1)
    water = st.slider("Surface water coverage (%)", 0, 100, 70, 5)
    gravity = st.slider("Surface gravity (Earth = 1)", 0.2, 5.0, 1.0, 0.1)

# Simple transparent heuristic score; not a scientific habitability probability.
score=calculate_habitability(temperature, atmosphere, water, gravity)

with right:
    st.subheader("Your world")
    # Use temperature and water coverage to create a simple illustrative colour.
    world_colour=get_temperature_colour(temperature)
    if temperature < -20:
        world_name = "Frozen world"
    elif temperature > 65:
        world_name = "Scorched world"
    else:
        world_name = "Temperate-looking world"

    st.markdown(f"""
    <div style="display:flex;justify-content:center;align-items:center;min-height:270px;
                background:radial-gradient(circle,rgba(72,92,160,.22),rgba(10,15,30,.1) 65%);
                border-radius:22px;">
      <div style="width:{100*radius}px;height:{100*radius}px;border-radius:50%;
                  background:radial-gradient(circle at 32% 28%, #ffffffaa, transparent 18%),
                  radial-gradient(circle at 35% 35%, {world_colour}, #17264f 78%);
                  box-shadow:0 0 45px {world_colour}88, inset -22px -18px 35px #050817;
                  border:1px solid #ffffff33;"></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"### {world_name}")
    st.metric("Illustrative environment score", f"{score}/100")
    st.progress(score / 100)

st.divider()
st.subheader("World profile")
a, b, c = st.columns(3)
a.metric("Radius", f"{radius:.1f} × Earth")
b.metric("Gravity", f"{gravity:.1f}g")
c.metric("Water coverage", f"{water}%")
st.write(f"**Atmosphere:** {atmosphere:.1f} Earth atmospheres")
st.write(f"**Average temperature:** {temperature} °C")

if score >= 75:
    st.success("Your settings produce a relatively Earth-like combination in this simplified model.")
elif score >= 45:
    st.warning("Some conditions are more extreme than Earth's. Explore which changes improve the score.")
else:
    st.error("This combination is very different from Earth's reference conditions.")

st.caption("The score is a custom demonstration, not a NASA metric, scientific habitability estimate or probability of life.")


