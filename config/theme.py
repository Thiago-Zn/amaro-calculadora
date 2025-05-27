"""
Sistema de tema corporativo Amaro Aviation
Carrega CSS customizado da identidade visual da empresa
"""

import streamlit as st

def load_theme():
    """
    Carrega o tema CSS corporativo Amaro Aviation
    Baseado no design system da empresa
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Configurações globais */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #FFFFFF;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #8C1D40 0%, #A02050 100%);
        color: white;
        padding: 3rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    /* Cards de métricas */
    .metric-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .metric-card-value {
        font-size: 2rem;
        font-weight: 700;
        color: #8C1D40;
        margin: 0.5rem 0;
    }
    
    .metric-card-label {
        font-size: 0.875rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Tabelas customizadas */
    .comparison-table {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .comparison-table th {
        background: #F3F4F6;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
        padding: 1rem;
    }
    
    .comparison-table td {
        padding: 1rem;
        border-bottom: 1px solid #E5E7EB;
    }
    
    /* Botões personalizados */
    .stButton > button {
        background: #8C1D40;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #A02050;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(140, 29, 64, 0.3);
    }
    
    /* Tabs estilizadas */
    .stTabs [data-baseweb="tab-list"] {
        background: #F9FAFB;
        border-radius: 12px;
        padding: 0.25rem;
        gap: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: #8C1D40;
        color: white;
    }
    
    /* Sidebar refinada */
    .css-1d391kg {
        background: #F9FAFB;
    }
    
    /* Métricas de destaque */
    .highlight-metric {
        background: linear-gradient(135deg, #8C1D40 0%, #A02050 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .highlight-metric h3 {
        font-size: 1.5rem;
        margin: 0;
    }
    
    .highlight-metric .value {
        font-size: 3rem;
        font-weight: 700;
        margin: 1rem 0;
    }
    
    /* Configurações do data editor */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Ocultar elementos Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)