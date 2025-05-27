"""
Tema Claro Definitivo Amaro Aviation
Compatível com Streamlit ≥ 1.30
"""

import streamlit as st

def load_theme() -> None:
    """Injeta o CSS corporativo essencial e as correções finais."""
    st.markdown(
        """
<style>
/* ——— 1. FUNDOS E TIPOGRAFIA GLOBAIS ——— */
html, body, [data-testid="stAppViewContainer"] {
    background: #FFFFFF !important;
    color:      #1F2937  !important;
    font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif!important;
}

/* ——— 2. SIDEBAR — fundo claro e texto escuro ——— */
section[data-testid="stSidebar"] {
    background: #F8F9FA !important;
    color:      #374151 !important;
}

/* ——— 2.1. ITEM ATIVO DA SIDEBAR — bordô e texto branco ——— */
section[data-testid="stSidebar"] a[aria-current="page"] {
    background:    #8C1D40 !important;
    color:         #FFFFFF !important;
    border-radius: 6px !important;
    font-weight:   600   !important;
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

/* ——— 7. CARTÕES DE MÉTRICA (se usar .metric-card) ——— */
.metric-card {
    background:    #FFFFFF!important;
    border:        1px solid #E5E7EB!important;
    border-radius: 8px!important;
    padding:       1.5rem!important;
    margin:        1rem 0!important;
    box-shadow:    0 2px 4px rgba(0,0,0,0.05)!important;
}
.metric-card-value {
    font-size:   1.5rem!important;
    font-weight: 600!important;
    color:       #8C1D40!important;
}
.metric-card-label {
    font-size:   0.875rem!important;
    color:       #6B7280!important;
    font-weight: 500!important;
}

/* ——— 8. OCULTAR ELEMENTOS PADRÕES DO STREAMLIT ——— */
#MainMenu, header, footer {
    visibility: hidden!important;
}
</style>
        """,
        unsafe_allow_html=True,
    )
