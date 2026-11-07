import streamlit as st

def apply_global_styles():
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
    color: #FFFFFF; font-size: 3.30rem; max-width:4000px; font-family: 'Inter', sans-serif;
}
[data-testid="stSidebarNav"] a:hover {
    background-color: #3C0000 !important;
    color: #FFFFFF !important;
}

/* Currently selected page */
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background-color: #D92906 !important;
    color: #FFFFFF !important;
    font-weight: 600;
}


/* Navigation text */
[data-testid="stSidebarNav"] span {
    font-size: 14px;
    color: #FFFFFF !important;
    font-weight: 500;
    }

    hr {
    border: none !important;
    border-top: 1px solid #D92906 !important;
    opacity: 1 !important;
}
[data-testid="stTextInputRootElement"] {
    background-color: #000000 !important; 
    border-radius: 0;
    border-width:0;
}


/* Multiselect outer container */
[data-testid="stMultiSelect"] [data-baseweb="select"] {
    background-color: #000000 !important;
}

/* Actual input/control background */
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
    background-color: #000000 !important;
    border: 1px solid #D92906 !important;
}

/* Inner value container */
[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
    background-color: #000000 !important;
}

/* Input text */
[data-testid="stMultiSelect"] input {
    color: white !important;
    background-color: transparent !important;
}

/* Selected tags */
[data-testid="stMultiSelect"] [data-baseweb="tag"] {
    background-color: #D92906 !important;
    color: white !important;
}


    </style>
    """, unsafe_allow_html=True)