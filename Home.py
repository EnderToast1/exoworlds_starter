from pathlib import Path

import streamlit as st

from Style import apply_global_styles
from src.data import load_planets

ROOT = Path(__file__).resolve().parent
LOGO = ROOT / "static" / "EWE_Logo.png"



st.set_page_config(
    page_title="ExoWorlds | Explore the unknown",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_styles()

with st.sidebar:
    st.markdown(
        '<p class="sidebar-write">Use the pages above to discover real exoplanets, inspect their properties and experiment with hypothetical worlds</p>',
        unsafe_allow_html=True
    )
    st.markdown('<hr class="divider-one">', unsafe_allow_html=True)
    st.markdown(
        '<p class="sidebar-write">Wi-Fi Hiders</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="sidebar-write-small">Alex Battrick</p>\n<p class="sidebar-write-small">William Wain</p>',
        unsafe_allow_html=True
    )
    st.markdown('<hr class="divider-one">', unsafe_allow_html=True)


hero_text, hero_image = st.columns([4, 1])

with hero_text:
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">Beyond our solar system</div>
      <h1>Exo World Engineer</h1>
      <p>
        Explore real planets orbiting distant stars. Compare their extreme
        environments with Earth, then build an imaginary world of your own.
      </p>
    </div>
    """, unsafe_allow_html=True)

with hero_image:
    st.image(str(LOGO), use_container_width=True)
st.subheader("Choose your next discovery")
st.divider()
col1, col2, col3,col4 = st.columns(4)
with col1:
    st.markdown("### Cosmic Atlas")
    st.write("Search a catalogue of real exoplanets and uncover the universe.")
    st.markdown("""
    <div class="observatory-box2">
        <a class="home-link" href="/Cosmic_Atlas">
            Explore planets →
        </a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### Planet Observatory")
    st.write("Inspect a planet's orbit, size, temperature and host star.")
    st.markdown("""
        <div class="observatory-box2">
            <a class="home-link" href="/Planetary_Observatory">
                Open observatory →
            </a>
        </div>
        """, unsafe_allow_html=True)

with col3:
    st.markdown("### Stellar Comparison")
    st.write("Compare Exoplanet Data.")
    st.markdown("""
        <div class="observatory-box2">
            <a class="home-link" href="/Stellar_Comparison">
                Compare Exoplanets  →
            </a>
        </div>
        """, unsafe_allow_html=True)
with col4:
    st.markdown("### World Engineer")
    st.write("Change environmental conditions and see how a hypothetical world responds.")
    st.markdown("""
        <div class="observatory-box2">
            <a class="home-link" href="/World_Engineer">
                Build a world  →
            </a>
        </div>
        """, unsafe_allow_html=True)

st.divider()
with st.spinner("Opening the star catalogue..."):
    planets, data_source, load_error = load_planets()
st.subheader("A universe of possibilities")
a, b= st.columns(2)
a.metric("Worlds to explore", len(planets), help="The Number of confirmed exoplanets in the NASA API.")
b.metric("Our reference point", "Earth", help="Reference values are used for comparisons.")
