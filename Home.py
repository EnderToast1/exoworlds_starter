import streamlit as st

st.set_page_config(
    page_title="ExoWorlds | Explore the unknown",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Shared visual styling
st.markdown("""
<style>
    .stApp {
        background:
            color: #ffffff;
            font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background: #000000;
        border-right: 1px solid rgba(255, 255, 255, 1);
    }
    .hero {
        border-radius: 24px;
        margin-bottom: 1.4rem;
        font-family: 'Inter', sans-serif;
    }
    .eyebrow {
        color: #D92906;
        text-transform: uppercase;
        letter-spacing: .18em;
        font-size: .95rem;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
    }
    .hero h1 { font-size: clamp(2.5rem, 6vw, 4.6rem); margin: .25rem 0; font-family: 'Inter', sans-serif; }
    .hero p { color: #FFFFFF; font-size: 1.08rem; max-width: 780px; font-family: 'Inter', sans-serif;}
    div[data-testid="stMetric"] {
        border: 1px solid rgba(217, 41, 6,1);
        padding: 1rem;
        font-family: 'Inter', sans-serif;
    }
    .small-note { color: #9ba9cb; font-size: .85rem; font-family: 'Inter', sans-serif; }

[data-testid="stSidebarNavSeparator"] {
    border: none !important;
    border-top: 1px solid #D92906 !important;
}
[data-testid="stSidebarNavLinkContainer"] {

}

    hr {
    border: none !important;
    border-top: 1px solid #D92906 !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)

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
