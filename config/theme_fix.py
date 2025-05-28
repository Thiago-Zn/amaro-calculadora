"""
TEMA CORRIGIDO - SELECTBOX VISÍVEL E GRÁFICOS FUNCIONANDO
"""

import streamlit as st

def load_theme():
    """CSS MÍNIMO que GARANTE selectbox visível"""
    st.markdown("""
    <style>
    /* ===== FIX DEFINITIVO PARA SELECTBOX ===== */
    
    /* 1. SELECTBOX - TEXTO SEMPRE VISÍVEL */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #8C1D40 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* 2. TEXTO DENTRO DO SELECTBOX - PRETO FORTE */
    div[data-baseweb="select"] span {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* 3. DROPDOWN ABERTO - FUNDO BRANCO */
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
        border: 2px solid #8C1D40 !important;
    }
    
    /* 4. OPÇÕES DO DROPDOWN - TEXTO PRETO */
    ul[role="listbox"] li {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 500 !important;
    }
    
    /* 5. OPÇÃO HOVER - DESTAQUE CLARO */
    ul[role="listbox"] li:hover {
        background-color: #8C1D40 !important;
        color: #FFFFFF !important;
    }
    
    /* 6. OPÇÃO SELECIONADA - DESTAQUE FORTE */
    ul[role="listbox"] li[aria-selected="true"] {
        background-color: #8C1D40 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    
    /* ===== SIDEBAR SELECTBOX ESPECÍFICO ===== */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 3px solid #FFFFFF !important;
    }
    
    section[data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    /* ===== GRÁFICOS VISÍVEIS ===== */
    div[data-testid="stPlotlyChart"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        padding: 10px !important;
        min-height: 400px !important;
    }
    
    /* ===== MÉTRICAS VISÍVEIS ===== */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF !important;
        border: 1px solid #8C1D40 !important;
        border-radius: 8px !important;
        padding: 15px !important;
    }
    
    div[data-testid="metric-container"] label {
        color: #666666 !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="metric-container"] div[data-testid="metric-value"] {
        color: #8C1D40 !important;
        font-weight: 700 !important;
        font-size: 24px !important;
    }
    
    /* ===== BOTÕES FUNCIONAIS ===== */
    .stButton > button {
        background-color: #8C1D40 !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 20px !important;
    }
    
    .stButton > button:hover {
        background-color: #A02050 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    
    /* ===== GARANTIR VISIBILIDADE GERAL ===== */
    .stApp {
        background-color: #FFFFFF !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1F2937 !important;
    }
    
    p, span, div {
        color: #1F2937 !important;
    }
    
    /* Labels dos inputs */
    .stSelectbox label,
    .stNumberInput label,
    .stSlider label {
        color: #1F2937 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)