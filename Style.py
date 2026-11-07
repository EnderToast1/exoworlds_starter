import streamlit as st

def apply_global_styles():
    st.markdown("""
    <style>
   .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
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
    .p { color: #FFFFFF; font-size: 1.08rem; max-width: 780px; font-family: 'Inter', sans-serif;}
    div[data-testid="stMetric"] {
        border: 1px solid rgba(217, 41, 6,1);
        padding: 1rem;
        font-family: 'Inter', sans-serif;
    }
    .small-note { color: #9ba9cb; font-size: .85rem; font-family: 'Inter', sans-serif; }

.observatory-box {
    background-color: #000000;
    border: 1px solid #D92906;
    padding: 18px 22px;
    margin-top: 15px;
    display: inline-block;
    border-radius: 0;
}

.observatory-link {
    font-size: 1.25rem !important;
    color: #FFFFFF !important;
    text-decoration: none !important;
}

.observatory-link:hover {
    color: #D92906 !important;
    
}


[data-testid="stSidebarNavSeparator"] {
    border: none !important;
    border-top: 1px solid #D92906 !important;
}
[data-testid="stSidebarNavLinkContainer"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    max-width: 100% !important;
    border-radius: 0 !important;

}

[data-testid="stSidebarNav"] a:hover {
    background-color: #3C0000 !important;
    color: #FFFFFF !important;
    border-radius: 0 !important;
}

/* Currently selected page */
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background-color: #D92906 !important;
    color: #FFFFFF !important;
    font-weight: 600;
    border-radius: 0 !important;
}
[data-testid="stSidebarNav"] [role="button"] {
    border-radius: 0 !important;
}

.info-box {
    background-color: #cf851f;
    color: #FFFFFF;
    border-radius: 0;
    padding: 14px 18px;
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    font-weight: 500;
}

/* Metric values */
[data-testid="stMetricValue"] {
    font-size: 1.5rem !important;
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    font-size: 0.9rem !important;
}

/* Metric descriptions */
[data-testid="stMetricDelta"] {
    font-size: 0.7rem !important;
}


/* Navigation text */
[data-testid="stSidebarNav"] span {
    font-size: 14px;
    color: #FFFFFF !important;
    font-weight: 500;
    border-radius: 0 !important;
    }

    hr {
    border: none !important;
    border-top: 1px solid #D92906 !important;
    opacity: 1 !important;
}
[data-testid="stTextInputRootElement"] {
    background-color: #000000 !important; 
    border-radius: 0!important;
    border-color: #D92906 !important;
    border-width:1;
}

.planet-select-label {
    color: #FFFFFF !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    margin-bottom: 8px;
}

/* Selectbox styling */
/* Force square corners on the entire selectbox */
[data-testid="stSelectbox"],
[data-testid="stSelectbox"] *,
[data-testid="stSelectbox"] *::before,
[data-testid="stSelectbox"] *::after {
    border-radius: 0 !important;
}



/* Main select control */
[data-testid="stSelectbox"] [data-baseweb="select"] {
    border-radius: 0 !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: #000000 !important;
    border: 1px solid #D92906 !important;
    border-radius: 0 !important;
    color: #FFFFFF !important;
    
}


/* Main multiselect container */
[data-testid="stMultiSelect"] [role="group"] {
    background: #000000 !important;
    border: 1px solid #D92906 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

/* Selected option tags */
[data-testid="stMultiSelect"] [data-testid="stMultiSelectTagsContainer"] > * {
    border-radius: 0 !important;
}

/* All nested elements inside selected tags */
[data-testid="stMultiSelect"] [data-testid="stMultiSelectTagsContainer"] > * * {
    border-radius: 0 !important;
}

/* Selected tag backgrounds */
[data-testid="stMultiSelect"] [data-testid="stMultiSelectTagsContainer"] button {
    border-radius: 0 !important;
}

/* Text and input */
[data-testid="stMultiSelect"] input {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

[data-testid="stMultiSelect"] input::placeholder {
    color: #FFFFFF !important;
    opacity: 1 !important;
}



/* Dataframe outer border */
[data-testid="stDataFrame"] {
    border: 1px solid #D92906 !important;
}

/* Force white gridlines inside the dataframe */
[data-testid="stDataFrame"] canvas {
    filter: none !important;
}

/* Dataframe header and cell text */
[data-testid="stDataFrame"] canvas {
    color: #FFFFFF !important;
}



    </style>
    """, unsafe_allow_html=True)