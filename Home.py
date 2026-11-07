import streamlit as st

from Style import apply_global_styles

st.set_page_config(
    page_title="ExoWorlds | Explore the unknown",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_styles()

with st.sidebar:
    st.markdown("**MISSION CONTROL**")
    st.write("Use the pages above to discover real exoplanets, inspect their properties and experiment with hypothetical worlds.")
    st.divider()

st.markdown("""
<div class="hero">
  <div class="eyebrow">Beyond our solar system</div>
  <h1>Exo World Engineer</h1>
  <p>Explore real planets orbiting distant stars. Compare their extreme environments
  with Earth, then build a imaginary world of your own.</p>
</div>
""", unsafe_allow_html=True)

st.subheader("Choose your next discovery")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### Universe Explorer")
    st.write("Search a catalogue of real exoplanets and uncover the universe.")
    st.page_link("pages/1_Universe_Explorer.py", label="Explore planets →")
with col2:
    st.markdown("### Planet Observatory")
    st.write("Inspect a planet's orbit, size, temperature and host star.")
    st.page_link("pages/2_Planet_Observatory.py", label="Open observatory →")
with col3:
    st.markdown("### World Builder")
    st.write("Change environmental conditions and see how a hypothetical world responds.")
    st.page_link("pages/3_World_Builder.py", label="Build a world →")

st.divider()
st.subheader("A universe of possibilities")
a, b, c = st.columns(3)
a.metric("Worlds to explore", "Number", help="Approximate order of magnitude; the catalogue changes as discoveries are confirmed.")
b.metric("Our starting point", "Earth", help="Reference values are used for comparisons.")
c.metric("Your role", "Explorer", help="The application uses scientific measurements and transparent calculations, not AI agents.")
