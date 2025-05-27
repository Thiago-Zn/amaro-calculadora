"""
Tema Claro Definitivo Amaro Aviation
Compatível com Streamlit ≥ 1.30
"""

import streamlit as st

def load_theme() -> None:
    """Injeta o CSS corporativo essencial e garante contraste ideal."""
    st.markdown(
        """
<style>
/* 1. FUNDOS E TIPOGRAFIA GLOBAIS */
html, body, [data-testid="stAppViewContainer"] {
    background: #FFFFFF !important;
    color: #1F2937   !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* 2. SIDEBAR – FUNDO CLARO E TEXTO ESCURO */
section[data-testid="stSidebar"] {
    background: #F8F9FA !important;
    color:      #374151 !important;
}

/* 2.1. ITEM ATIVO DA SIDEBAR – FUNDO BORDÔ, TEXTO BRANCO */
section[data-testid="stSidebar"] a[aria-current="page"] {
    background:    #8C1D40 !important;
    color:         #FFFFFF !important;
    border-radius: 6px;
    font-weight:   600;
}

/* 3. HEADER PRINCIPAL – GRADIENTE BORDÔ */
.main-header {
    background:        linear-gradient(135deg, #8C1D40 0%, #A02050 100%);
    color:             #FFFFFF;
    padding:           2rem;
    margin:            -1rem -1rem 2rem -1rem;
    text-align:        center;
    border-radius:     0 0 12px 12px;
}
.main-header h1 {
    margin:     0;
    font-size:  2rem;
    font-weight: 600;
}
.main-header p {
    margin:      0.5rem 0 0 0;
    font-size:   1rem;
    opacity:     0.9;
}

/* 4. BOTÕES – BORDÔ COM HOVER LEVE */
.stButton > button {
    background:        #8C1D40 !important;
    color:             #FFFFFF !important;
    border:            none !important;
    border-radius:     6px !important;
    padding:           0.5rem 1rem !important;
    font-weight:       500 !important;
    text-transform:    uppercase;
}
.stButton > button:hover {
    background: #A02050 !important;
}

/* 5. TABS – FUNDO CLARO E SELECIONADO EM BORDÔ */
[data-testid="stTabs"] [role="tablist"] {
    background:    #F8F9FA;
    border-radius: 8px;
    padding:       0.25rem;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #8C1D40;
    color:      #FFFFFF;
}

/* 6. METRICS – RÓTULO ESCURO, VALOR BORDÔ */
div[data-testid="stMetric"] label {
    color:      #374151 !important;
    font-weight: 500      !important;
}
div[data-testid="stMetric"] span {
    color:      #8C1D40 !important;
    font-weight: 600      !important;
    font-size:  1.25rem   !important;
}

/* 7. CARTÕES DE MÉTRICA PERSONALIZADOS (se usar .metric-card) */
.metric-card {
    background:    #FFFFFF;
    border:        1px solid #E5E7EB;
    border-radius: 8px;
    padding:       1.5rem;
    margin:        1rem 0;
    box-shadow:    0 2px 4px rgba(0,0,0,0.05);
}
.metric-card-value {
    font-size:   1.5rem;
    font-weight: 600;
    color:       #8C1D40;
}
.metric-card-label {
    font-size:   0.875rem;
    color:       #6B7280;
    font-weight: 500;
}

/* 8. OCULTAR ELEMENTOS PADRÕES DO STREAMLIT */
#MainMenu, header, footer {
    visibility: hidden;
}
</style>
        """,
        unsafe_allow_html=True,
    )
