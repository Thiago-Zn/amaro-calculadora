"""
Sistema de tema simplificado para Amaro Aviation
Versão clean e funcional
"""

import streamlit as st

def load_theme():
    """
    Carrega tema simplificado Amaro Aviation
    """
    st.markdown("""
    <style>
    /* Reset básico */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #8C1D40 0%, #A02050 100%);
        color: white;
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        border-radius: 0 0 12px 12px;
    }
    
    .main-header h1 {
        font-size: 2rem;
        font-weight: 600;
        margin: 0;
    }
    
    .main-header p {
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Cards simples */
    .metric-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .metric-card-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: #8C1D40;
        margin: 0.5rem 0;
    }
    
    .metric-card-label {
        font-size: 0.875rem;
        color: #6B7280;
        font-weight: 500;
    }
    
    /* Botões */
    .stButton > button {
        background: #8C1D40;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background: #A02050;
    }
    
    /* Tabs simples */
    .stTabs [data-baseweb="tab-list"] {
        background: #F8F9FA;
        border-radius: 8px;
        padding: 0.25rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: #8C1D40;
        color: white;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: #F8F9FA;
    }
    
    /* Remover elementos desnecessários */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Fix para DataFrames */
    .stDataFrame {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)