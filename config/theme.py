import streamlit as st

AMARO_BORDO          = "#8C1D40"
AMARO_BORDO_HOVER    = "#A02050"
AMARO_BORDO_ACTIVE   = "#731734"
AMARO_BRANCO         = "#FFFFFF"
AMARO_TXT_CINZA      = "#1F2937"
AMARO_BG_CINZA_CLARO = "#F6F7FA"

def load_theme() -> None:
    st.markdown(
        f"""
<style>
/* ——— Reset & Fonte ——— */
html, body, [data-testid="stAppViewContainer"] {{
    background: {AMARO_BRANCO};
    color: {AMARO_TXT_CINZA};
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}}
.block-container {{
    padding: 2rem 1.5rem !important;
}}

/* ——— Sidebar ——— */
section[data-testid="stSidebar"] {{
    background: {AMARO_BORDO};
}}
section[data-testid="stSidebar"] * {{
    color: {AMARO_BRANCO} !important;
    text-transform: capitalize !important;     /* Capitaliza itens */
}}
section[data-testid="stSidebar"] a[aria-current="page"] {{
    background: {AMARO_BORDO_HOVER};
    font-weight: 600;
}}
section[data-testid="stSidebar"] a:hover {{
    background: {AMARO_BORDO_HOVER};
}}

/* ——— Botões ——— */
.stButton>button, .stDownloadButton>button {{
    background: {AMARO_BORDO};
    color: {AMARO_BRANCO} !important;
    border: 1px solid {AMARO_BORDO};
    border-radius: 6px;
    font-weight: 600;
    text-transform: uppercase;
    padding: .5rem 1.25rem;
}}
.stButton>button:hover, .stDownloadButton>button:hover {{
    background: {AMARO_BORDO_HOVER};
    border-color: {AMARO_BORDO_HOVER};
}}
.stButton>button:active, .stDownloadButton>button:active {{
    background: {AMARO_BORDO_ACTIVE};
    border-color: {AMARO_BORDO_ACTIVE};
}}

/* ——— Tabs ——— */
[data-testid="stTabs"] [role="tablist"] {{
    background: {AMARO_BG_CINZA_CLARO};
    border-radius: 8px;
    padding: 2px;
}}
[data-testid="stTabs"] [data-baseweb="tab"] {{
    color: {AMARO_TXT_CINZA};
    background: {AMARO_BRANCO};
    border-radius: 6px;
    padding: .45rem 1.1rem;
    font-weight: 500;
}}
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {{
    background: {AMARO_BORDO};
    color: {AMARO_BRANCO};
    font-weight: 600;
}}

/* ——— Inputs ——— */
.stSelectbox, .stNumberInput, .stTextInput, .stTextArea,
.stDateInput, .stTimeInput, div[data-baseweb="select"],
input, textarea {{
    background: {AMARO_BG_CINZA_CLARO} !important;
    color: {AMARO_TXT_CINZA} !important;
    border: 1px solid #DADDE1 !important;
    border-radius: 6px !important;
}}
input::placeholder, textarea::placeholder {{
    color: #6B7280 !important;
}}

/* ——— Cards ——— */
.card-style, div[data-testid="stMarkdownContainer"].card-style {{
    background: {AMARO_BRANCO};
    border: 1px solid #E3E4E8;
    border-radius: 8px;
    padding: 1.25rem;
    box-shadow: 0 2px 4px rgba(0,0,0,.08);
}}
.card-style:hover {{
    box-shadow: 0 4px 8px rgba(0,0,0,.12);
}}

/* ——— Status ——— */
.status-success {{
    background: #F0FBF9;
    border-left: 5px solid {AMARO_BORDO};
    color: {AMARO_TXT_CINZA} !important;
    padding: .75rem 1rem;
    border-radius: .375rem;
}}
.status-warning {{
    background: #FFFBEB;
    border-left: 5px solid #F59E0B;
    color: #92400E;
}}
.status-info {{
    background: #F0F9FF;
    border-left: 5px solid #0EA5E9;
    color: #0C4A6E;
}}

/* ——— Tipografia ——— */
h1, h2, h3, h4, h5, h6 {{
    color: {AMARO_BORDO} !important;
    margin-top: 1.5rem;
    margin-bottom: .75rem;
    font-weight: 600;
}}
p, li {{
    color: {AMARO_TXT_CINZA} !important;
    line-height: 1.6;
    margin-bottom: .75rem;
}}

/* ——— Ícones recolore para bordô ——— */
[data-testid="stMarkdownContainer"] img,
[data-testid="stMarkdownContainer"] svg {{
    filter: brightness(0) saturate(100%) invert(13%) sepia(72%) saturate(757%) hue-rotate(325deg);
    /* converte tons para aproximar do #8C1D40 */
}}

/* ——— Esconde header/rodapé nativos ——— */
#MainMenu, header, footer {{
    visibility: hidden;
}}
</style>
""",
        unsafe_allow_html=True,
    )
