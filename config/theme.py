import streamlit as st

def load_theme():
    st.markdown("""
<style>
/* ===== TEMA LIMPO AMARO AVIATION ===== */
/* Baseado no design oficial: clean, branco, moderno */

/* === RESET GERAL === */
.stApp {
    background-color: #FFFFFF !important;
    color: #333333 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

/* Container principal */
.block-container {
    background: #FFFFFF !important;
    padding: 2rem 1.5rem !important;
    max-width: 1200px !important;
}

/* === SIDEBAR CLEAN === */
section[data-testid="stSidebar"] {
    background: #8C1D40 !important;
    border-right: none !important;
}

section[data-testid="stSidebar"] > div:first-child {
    background: #8C1D40 !important;
    padding-top: 2rem !important;
}

/* Texto da sidebar */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* === SELETOR DE IDIOMA FUNCIONAL === */
section[data-testid="stSidebar"] .stSelectbox label {
    color: white !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    margin-bottom: 0.5rem !important;
}

/* Caixa do seletor - BRANCA e LEGÍVEL */
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: white !important;
    color: #333333 !important;
    border: 2px solid white !important;
    border-radius: 8px !important;
    padding: 0.75rem 1rem !important;
    font-weight: 500 !important;
    min-height: 44px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
}

section[data-testid="stSidebar"] .stSelectbox svg {
    fill: #333333 !important;
}

/* Dropdown do seletor */
div[data-baseweb="popover"][role="listbox"] {
    background: white !important;
    border: 2px solid #8C1D40 !important;
    border-radius: 8px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.15) !important;
}

div[data-baseweb="popover"] [role="option"] {
    background: white !important;
    color: #333333 !important;
    padding: 0.75rem 1rem !important;
    font-weight: 500 !important;
}

div[data-baseweb="popover"] [role="option"]:hover {
    background: #8C1D40 !important;
    color: white !important;
}

/* === CONTEÚDO PRINCIPAL CLEAN === */
/* Títulos */
h1, h2, h3, h4, h5, h6 {
    color: #8C1D40 !important;
    font-weight: 600 !important;
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
}

h1 {
    font-size: 2.5rem !important;
    margin-top: 0 !important;
}

/* Texto normal */
p, li, span, div {
    color: #333333 !important;
    line-height: 1.6 !important;
}

/* === MÉTRICAS CLEAN === */
div[data-testid="stMetric"] {
    background: white !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stMetric"]:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.12) !important;
    transform: translateY(-2px) !important;
}

[data-testid="stMetricValue"] {
    color: #8C1D40 !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
}

[data-testid="stMetricLabel"] {
    color: #666666 !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

[data-testid="stMetricDelta"] {
    color: #10B981 !important;
    font-weight: 600 !important;
}

/* === GRÁFICOS CLEAN === */
.js-plotly-plot {
    background-color: white !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}

.js-plotly-plot .plotly {
    background-color: white !important;
}

.js-plotly-plot svg {
    background-color: white !important;
}

div[data-testid="stPlotlyChart"] {
    background: white !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    margin: 1rem 0 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}

/* === BOTÕES CLEAN === */
.stButton > button {
    background: #8C1D40 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.75rem 2rem !important;
    font-size: 0.875rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.025em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 4px rgba(140, 29, 64, 0.2) !important;
}

.stButton > button:hover {
    background: #A02050 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(140, 29, 64, 0.3) !important;
}

.stDownloadButton > button {
    background: #10B981 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.75rem 2rem !important;
}

.stDownloadButton > button:hover {
    background: #059669 !important;
    transform: translateY(-2px) !important;
}

/* === INPUTS CLEAN === */
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: white !important;
    border: 2px solid #E5E7EB !important;
    border-radius: 8px !important;
    color: #333333 !important;
    padding: 0.75rem 1rem !important;
    font-size: 0.875rem !important;
    transition: all 0.2s ease !important;
}

.stSelectbox > div > div:focus-within,
.stNumberInput > div > div:focus-within,
.stTextInput > div > div:focus-within {
    border-color: #8C1D40 !important;
    box-shadow: 0 0 0 3px rgba(140, 29, 64, 0.1) !important;
}

/* Labels dos inputs */
.stSelectbox label,
.stNumberInput label,
.stTextInput label,
.stSlider label {
    color: #333333 !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    margin-bottom: 0.5rem !important;
}

/* === SLIDER CLEAN === */
.stSlider > div > div > div > div {
    background: #8C1D40 !important;
}

.stSlider > div > div > div > div > div {
    background: #8C1D40 !important;
    border: 3px solid white !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
}

/* === TABS CLEAN === */
[data-testid="stTabs"] [role="tablist"] {
    background: #F8F9FA !important;
    border-radius: 12px !important;
    padding: 4px !important;
    border: 1px solid #E5E7EB !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    color: #666666 !important;
    border-radius: 8px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {
    background: white !important;
    color: #8C1D40 !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
}

/* === ALERTAS CLEAN === */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    margin: 1rem 0 !important;
}

/* Success */
div[data-testid="stAlert"][data-baseweb="notification"]:has([data-testid="stSuccessIcon"]) {
    background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%) !important;
    border-left: 4px solid #10B981 !important;
    color: #065F46 !important;
}

/* Warning */  
div[data-testid="stAlert"][data-baseweb="notification"]:has([data-testid="stWarningIcon"]) {
    background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%) !important;
    border-left: 4px solid #F59E0B !important;
    color: #92400E !important;
}

/* Error */
div[data-testid="stAlert"][data-baseweb="notification"]:has([data-testid="stErrorIcon"]) {
    background: linear-gradient(135deg, #FEF2F2 0%, #FECACA 100%) !important;
    border-left: 4px solid #EF4444 !important;
    color: #991B1B !important;
}

/* Info */
div[data-testid="stAlert"][data-baseweb="notification"]:has([data-testid="stInfoIcon"]) {
    background: linear-gradient(135deg, #F0F9FF 0%, #DBEAFE 100%) !important;
    border-left: 4px solid #3B82F6 !important;
    color: #1E40AF !important;
}

/* === EXPANDERS CLEAN === */
div[data-testid="stExpander"] {
    background: white !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    margin: 1rem 0 !important;
}

div[data-testid="stExpander"] summary {
    background: #F8F9FA !important;
    border-radius: 11px 11px 0 0 !important;
    padding: 1rem 1.5rem !important;
    font-weight: 600 !important;
    color: #333333 !important;
    border-bottom: 1px solid #E5E7EB !important;
}

/* === DATAFRAMES CLEAN === */
div[data-testid="stDataFrame"] {
    background: white !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}

/* === RESPONSIVIDADE === */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem 0.5rem !important;
    }
    
    h1 {
        font-size: 2rem !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    
    div[data-testid="stMetric"] {
        padding: 1rem !important;
    }
}

/* === ANIMAÇÕES SUAVES === */
* {
    transition: all 0.2s ease !important;
}

/* === SCROLLBAR CLEAN === */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #F8F9FA;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: #8C1D40;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #A02050;
}
</style>
""", unsafe_allow_html=True)