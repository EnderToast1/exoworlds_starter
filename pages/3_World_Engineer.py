import math
import streamlit as st

from Style import apply_global_styles

apply_global_styles()

st.set_page_config(page_title="World Engineer | ExoWorlds", page_icon="", layout="wide")
st.title(" World Engineer")
st.caption("Create a hypothetical planet by changing its physical environment.")

with st.sidebar:
    st.markdown("**MISSION CONTROL**")
    st.write("Use the pages above to discover real exoplanets, inspect their properties and experiment with hypothetical worlds.")
    st.divider()
    st.markdown("Wi-Fi Hiders")
    st.caption("Alex Battrick")
    st.caption("William Wain")
    st.divider()


st.info("This is an educational toy model, not a validated climate simulator. Its outputs are illustrative and should not be interpreted as evidence that a planet could support life.")

left, right = st.columns([1, 1.2])
with left:
    st.subheader("Planet parameters")
    radius = st.slider("Planet radius (Earth = 1)", 0.3, 3.0, 1.0, 0.1)
    temperature = st.slider("Average surface temperature (°C)", -150, 150, 15, 1)
    atmosphere = st.slider("Atmospheric pressure (Earth = 1)", 0.0, 5.0, 1.0, 0.1)
    water = st.slider("Surface water coverage (%)", 0, 100, 70, 5)
    gravity = st.slider("Surface gravity (Earth = 1)", 0.2, 3.0, 1.0, 0.1)

# Simple transparent heuristic score; not a scientific habitability probability.
temp_score = max(0.0, 1.0 - abs(temperature - 15) / 120)
pressure_score = max(0.0, 1.0 - abs(atmosphere - 1.0) / 3.0)
water_score = 1.0 if 20 <= water <= 90 else 0.5
gravity_score = max(0.0, 1.0 - abs(gravity - 1.0) / 2.0)
score = round(100 * (0.4 * temp_score + 0.25 * pressure_score + 0.2 * water_score + 0.15 * gravity_score))

with right:
    st.subheader("Your world")
    # Use temperature and water coverage to create a simple illustrative colour.
    if temperature < -20:
        world_colour = "#9bd4f5"
        world_name = "Frozen world"
    elif temperature > 65:
        world_colour = "#d97843"
        world_name = "Scorched world"
    else:
        world_colour = "#4caa83"
        world_name = "Temperate-looking world"

    st.markdown(f"""
    <div style="display:flex;justify-content:center;align-items:center;min-height:270px;
                background:radial-gradient(circle,rgba(72,92,160,.22),rgba(10,15,30,.1) 65%);
                border-radius:22px;">
      <div style="width:190px;height:190px;border-radius:50%;
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
b.metric("Gravity", f"{gravity:.1f} × Earth")
c.metric("Water coverage", f"{water}%")

st.write(f"**Atmosphere:** {atmosphere:.1f} Earth atmospheres")
st.write(f"**Average temperature:** {temperature} °C")

if score >= 75:
    st.success("Your settings produce a relatively Earth-like combination in this simplified model.")
elif score >= 45:
    st.warning("Some conditions are more extreme than Earth's. Explore which changes improve the score.")
else:
    st.error("This combination is very different from Earth's reference conditions.")

st.caption("The score is a custom demonstration heuristic, not a NASA metric, scientific habitability estimate or probability of life.")
