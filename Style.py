import streamlit as st

def apply_global_styles():
    st.markdown("""
    <style>
    
    :root {
    --standard-text: 1rem;
    --small-text: 0.8rem;
    --big-text: 1.2rem;
    --heading-small: 1.7rem;
    --heading-big: 4.6rem;
}
    
    .stDeployButton {
    display: none;
    }
    [data-testid="stToolbar"] {
        display: none;
    }
   .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stImage"] img {
    border-radius: 0 !important;
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
        font-size: var(--big-text) !important;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
    }
    .hero h1 { font-size: var(--heading-big) !important; margin: .25rem 0; font-family: 'Inter', sans-serif; }
    .hero p { color: #FFFFFF; font-size: var(--standard-text) !important; max-width: 780px; font-family: 'Inter', sans-serif;}
    .p { color: #FFFFFF; font-size: var(--standard-text) !important; max-width: 780px; font-family: 'Inter', sans-serif;}
    div[data-testid="stMetric"] {
        border: 1px solid rgba(217, 41, 6,1);
        padding: 1rem;
        font-family: 'Inter', sans-serif;
    }
    .small-note { color: #9ba9cb; font-size: var(--small-text) !important; font-family: 'Inter', sans-serif; }

[data-testid="stMarkdownContainer"] h3 {
    font-size: var(--heading-small) !important;
}

.observatory-box {
    background-color: #000000;
    border: 1px solid #D92906;
    padding: 18px 22px;
    margin-top: 15px;
    display: inline-block;
    border-radius: 0;
}

.observatory-link {
    font-size: var(--big-text) !important;
    color: #FFFFFF !important;
    text-decoration: none !important;
}

.observatory-link:hover {
    color: #D92906 !important;
    
}
.observatory-box2 {
    background-color: #000000;
    border: 1px solid #D92906;
    padding: 16px 20px;
    margin-top: 20px;
    display: inline-block;
    border-radius: 0;
}
.home-link {
    font-size: var(--small-text) !important;
    color: #FFFFFF !important;
    text-decoration: none !important;
}
.stButton > button {
    border-radius: 0 !important;
    border: 1px solid #D92906 !important;
    background-color: #000000 !important;
    color: #FFFFFF !important;
}

.stButton > button:hover {
    background-color: #D92906 !important;
    color: #FFFFFF !important;
    border-color: #D92906 !important;
}


[data-testid="stSidebarNavSeparator"] {
    border: none !important;
    border-top: 1px solid #D92906 !important;

    margin-top: 20px !important;

}

[data-testid="stSidebarUserContent"] {
    padding: 0 !important;
}

[data-testid="stSidebarNav"] a:hover {
    background-color: #3C0000 !important;
    color: #FFFFFF !important;
    border-radius: 0 !important;
}

[data-testid="stSidebarNav"]::before {
    content: "MISSION CONTROL";
    display: block;

    font-family: 'Inter', sans-serif;
    font-size: var(--big-text) !important;
    font-weight: 400;
    letter-spacing: 0px;
    color: #FFFFFF;

    padding: 0px 8px 20px 8px !important;
    margin: 0px 0px 20px 0px !important;

    border-bottom: 1px solid #D92906;
    width: 100%;
    box-sizing: border-box;
}

[data-testid="stSidebarNavLinkContainer"] {
    font-family: 'Inter', sans-serif !important;
    max-width: 100% !important;
    border-radius: 0 !important;
}

[data-testid="stSidebarNav"] a:hover {
    background-color: #3C0000 !important;
    color: #FFFFFF !important;
    border-radius: 0 !important;
}

[data-testid="stSidebarNavSeparator"] {
    border: none !important;
    border-top: 1px solid #D92906 !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background-color: #D92906 !important;
    color: #FFFFFF !important;
    font-weight: 600;
    border-radius: 0 !important;
}
[data-testid="stSidebarNav"] [role="button"] {
    border-radius: 0 !important;
}

.sidebar-write {
    margin-top: 10px !important;
    margin-bottom: 10px !important;
    font-family: 'Inter', sans-serif;
    color: white;
    font-size: var(--standard-text) !important;
    
}

.sidebar-write-small {
    margin-top: 0px !important;
    margin-bottom: 20px !important;
    font-family: 'Inter', sans-serif;
    font-size: var(--small-text) !important;
    color: #808080 !important;
    line-height: 0.2 !important;
    font-weight: 600;
}

.info-box {
    background-color: #cf851f;
    color: #FFFFFF;
    border-radius: 0;
    padding: 14px 18px;
    font-family: 'Inter', sans-serif;
    font-size: var(--small-text) !important;
    font-weight: 500;
}

[data-testid="stMetricValue"] {
    font-size: var(--heading-small) !important;
}

[data-testid="stMetricLabel"] {
    font-size: var(--standard-text) !important;
}

[data-testid="stMetricDelta"] {
    font-size: var(--small-text) !important;
}

[data-testid="stSidebarNav"] span {
    font-size: var(--standard-text) !important;
    color: #FFFFFF !important;
    font-weight: 500;
    border-radius: 0 !important;
    }

    hr {
    border: none !important;
    border-top: 1px solid #D92906 !important;
    opacity: 1 !important;
    
}

hr.divider-one {
    border: none !important;
    border-top: 1px solid #D92906 !important;
    opacity: 1 !important;
    margin-top: 20px !important;
    margin-bottom: 20px !important;
}

[data-testid="stTextInputRootElement"] {
    background-color: #000000 !important; 
    border-radius: 0!important;
    border-color: #D92906 !important;
    border-width:1;
}

.planet-select-label {
    color: #FFFFFF !important;
    font-size: var(--standard-text) !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    margin-bottom: 8px;
}


[data-testid="stSelectbox"],
[data-testid="stSelectbox"] *,
[data-testid="stSelectbox"] *::before,
[data-testid="stSelectbox"] *::after {
    border-radius: 0 !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] {
    border-radius: 0 !important;
}

[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: #000000 !important;
    border: 1px solid #D92906 !important;
    border-radius: 0 !important;
    color: #FFFFFF !important;
    
}

[data-testid="stMultiSelect"] [role="group"] {
    background: #000000 !important;
    border: 1px solid #D92906 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

[data-testid="stMultiSelect"] [data-testid="stMultiSelectTagsContainer"] > * {
    border-radius: 0 !important;
}

[data-testid="stMultiSelect"] [data-testid="stMultiSelectTagsContainer"] > * * {
    border-radius: 0 !important;
}

[data-testid="stMultiSelect"] [data-testid="stMultiSelectTagsContainer"] button {
    border-radius: 0 !important;
}

[data-testid="stMultiSelect"] input {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

[data-testid="stMultiSelect"] input::placeholder {
    color: #FFFFFF !important;
    opacity: 1 !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #D92906 !important;
}

[data-testid="stDataFrame"] canvas {
    filter: none !important;
    color: #FFFFFF !important;
}



    </style>
    """, unsafe_allow_html=True)