"""
config/theme.py

Tema Claro Definitivo Amaro Aviation
Compatível com Streamlit ≥ 1.30
"""

import streamlit as st

def load_theme() -> None:
    """Injeta o CSS corporativo essencial e garante contraste ideal."""
    st.markdown(
        """
<style>
/* ——— 1. FUNDOS E TIPOGRAFIA GLOBAIS ——— */
html, body, [data-testid="stAppViewContainer"] {
    background: #FFFFFF !important;
    color:      #1F2937  !important;
    font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif!important;
}

/* ——— 2. SIDEBAR — fundo bordô e texto branco ——— */
section[data-testid="stSidebar"] {
    background: #8C1D40 !important;
    color:      #FFFFFF !important;
}

/* ——— 2.1. Todos os links da sidebar — texto branco ——— */
section[data-testid="stSidebar"] a {
    color: #FFFFFF !important;
}

/* ——— 2.2. Item ativo na sidebar — bordô mais escuro, texto branco ——— */
section[data-testid="stSidebar"] a[aria-current="page"] {
    background:    #A02050 !important;
    color:         #FFFFFF !important;
    border-radius: 6px !important;
    font-weight:   600   !important;
}

/* ——— 2.3. Sombra nos links da sidebar ao hover ——— */
section[data-testid="stSidebar"] a:hover {
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15) !important;
}

/* ——— 3. HEADER PRINCIPAL — gradiente bordô ——— */
.main-header {
    background:    linear-gradient(135deg,#8C1D40 0%,#A02050 100%) !important;
    color:         #FFFFFF !important;
    padding:       2rem !important;
    margin:        -1rem -1rem 2rem -1rem !important;
    text-align:    center !important;
    border-radius: 0 0 12px 12px !important;
}
.main-header h1 {
    margin:     0   !important;
    font-size:  2rem!important;
    font-weight:600!important;
}
.main-header p {
    margin:     0.5rem 0 0 0!important;
    font-size:  1rem!important;
    opacity:    0.9!important;
}

/* ——— 4. BOTÕES — bordô com hover leve ——— */
.stButton>button {
    background:      #8C1D40!important;
    color:           #FFFFFF!important;
    border:          none!important;
    border-radius:   6px!important;
    padding:         0.5rem 1rem!important;
    font-weight:     500!important;
    text-transform:  uppercase!important;
}
.stButton>button:hover {
    background: #A02050!important;
}

/* ——— 5. TABS — fundo claro e ativo bordô ——— */
[data-testid="stTabs"] [role="tablist"] {
    background:    #F8F9FA!important;
    border-radius: 8px!important;
    padding:       0.25rem!important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #8C1D40!important;
    color:      #FFFFFF!important;
}

/* ——— 6. METRICS — rótulo escuro e valor bordô ——— */
div[data-testid="stMetric"] label {
    color:      #374151!important;
    font-weight: 500!important;
}
div[data-testid="stMetric"] span {
    color:      #8C1D40!important;
    font-weight: 600!important;
    font-size:  1.25rem!important;
}

/* ——— 7. FEATURE CARDS — sombra ao hover ——— */
.feature-card {
    background:    #FFFFFF!important;
    border:        1px solid #E5E7EB!important;
    border-radius: 12px!important;
    padding:       2rem!important;
    margin-bottom: 1.5rem!important;
    transition:    box-shadow 0.2s ease!important;
}
.feature-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.1)!important;
}

</style>
        """,
        unsafe_allow_html=True,
    )
