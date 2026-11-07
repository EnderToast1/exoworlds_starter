from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Stellar Comparison | ExoWorlds",
    layout="wide"
)

from Style import apply_global_styles
from src.data import load_planets

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
