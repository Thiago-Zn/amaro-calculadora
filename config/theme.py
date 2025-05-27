"""
Tema corporativo Amaro Aviation – 100 % estável
Compatível com Streamlit ≥ 1.30
"""

import streamlit as st

# Paleta básica Amaro
AMARO_BORDO          = "#8C1D40"
AMARO_BORDO_HOVER    = "#A02050"
AMARO_BORDO_ACTIVE   = "#731734"
AMARO_BRANCO         = "#FFFFFF"
AMARO_TXT_CINZA      = "#28323F"   # texto principal
AMARO_BG_CINZA_CLARO = "#F6F7FA"   # fundos suaves/cards


def load_theme() -> None:
    """Injeta o CSS no app."""
    st.markdown(
        f"""
<style>
/* =====================================================
   0. RESET BÁSICO
===================================================== */
html, body, [data-testid="stAppViewContainer"] {{
    background:{AMARO_BRANCO};
    color:{AMARO_TXT_CINZA};
    font-family:"Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}}

/* =====================================================
   1. SIDEBAR
===================================================== */
section[data-testid="stSidebar"] {{
    background:{AMARO_BORDO};
}}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] h5,
section[data-testid="stSidebar"] h6 {{
    color:{AMARO_BRANCO} !important;
}}

section[data-testid="stSidebar"] a {{
    color:{AMARO_BRANCO};
    border-radius:6px;
    padding:.45rem .8rem;
    display:block;
}}

section[data-testid="stSidebar"] a[aria-current="page"] {{
    background:{AMARO_BORDO_HOVER};
    font-weight:600;
}}

section[data-testid="stSidebar"] a:hover {{
    background:{AMARO_BORDO_HOVER};
}}

/* Remove a linha vertical entre sidebar e body */
section[data-testid="stSidebar"] + div div[data-testid="stVerticalBlock"] {{
    border-left:none;
}}

/* =====================================================
   2. BOTÕES (st.button, st.download_button)
===================================================== */
.stButton > button,
.stDownloadButton > button {{
    background:{AMARO_BORDO};
    color:{AMARO_BRANCO} !important;
    border:1px solid {AMARO_BORDO};
    border-radius:6px;
    font-weight:600;
    text-transform:uppercase;
    padding:.5rem 1.25rem;
}}
.stButton > button:hover,
.stDownloadButton > button:hover {{
    background:{AMARO_BORDO_HOVER};
    border-color:{AMARO_BORDO_HOVER};
}}
.stButton > button:active,
.stDownloadButton > button:active {{
    background:{AMARO_BORDO_ACTIVE};
    border-color:{AMARO_BORDO_ACTIVE};
}}

/* =====================================================
   3. TABS
===================================================== */
[data-testid="stTabs"] [role="tablist"] {{
    background:{AMARO_BG_CINZA_CLARO};
    border-radius:8px;
    padding:2px;
}}
[data-testid="stTabs"] [data-baseweb="tab"] {{
    color:{AMARO_TXT_CINZA};
    background:{AMARO_BRANCO};
    border:none;
    border-radius:6px;
    padding:.45rem 1.1rem;
    font-weight:500;
}}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {{
    background:{AMARO_BG_CINZA_CLARO};
}}
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {{
    background:{AMARO_BORDO};
    color:{AMARO_BRANCO};
    font-weight:600;
}}

/* =====================================================
   4. CARDS / CONTAINERS (use class="card-style" em st.container/markdown)
===================================================== */
.card-style,
div[data-testid="stMarkdownContainer"].card-style {{
    background:{AMARO_BRANCO};
    border:1px solid #E3E4E8;
    border-radius:8px;
    padding:1.25rem;
    box-shadow:0 2px 4px rgba(0,0,0,.08);
}}
.card-style:hover {{
    box-shadow:0 4px 8px rgba(0,0,0,.12);
}}

/* =====================================================
   5. STATUS BOXES (classes já usadas no seu projeto)
===================================================== */
.status-success {{background:#ECFDF5;border-left:5px solid #10B981;color:#065F46}}
.status-warning {{background:#FFFBEB;border-left:5px solid #F59E0B;color:#92400E}}
.status-info    {{background:#F0F9FF;border-left:5px solid #0EA5E9;color:#0C4A6E}}

/* 5-B Texto padrão no corpo principal (não afeta sidebar) */
div[data-testid="stAppViewContainer"] > .main .block-container,
div[data-testid="stAppViewContainer"] > .main .block-container * {{
    color:#1F2937 !important;  /* cinza-escuro Amaro */
}}

/* 5-C Remove a caixa “Sistema Operacional” */
div.status-success {{display:none !important;}}

/* =====================================================
   6. Esconde cabeçalho / rodapé nativos Streamlit
===================================================== */
#MainMenu, header, footer {{visibility:hidden}}
</style>
""",
        unsafe_allow_html=True,
    )
