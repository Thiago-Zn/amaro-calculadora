import streamlit as st

def load_theme():
    st.markdown("""
<style>
/* === CORREÇÕES DIRETAS === */

/* Remover fundo preto dos dropdowns */
.stSelectbox > div > div > div {
    background-color: white !important;
    color: black !important;
}

/* Seletor de idioma na sidebar */
section[data-testid="stSidebar"] .stSelectbox > div > div > div {
    background: white !important;
    color: black !important;
    border: 2px solid #8C1D40 !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
}

/* Dropdown options */
div[data-baseweb="popover"] {
    background: white !important;
    border: 1px solid #8C1D40 !important;
    border-radius: 6px !important;
}

div[data-baseweb="popover"] [role="option"] {
    background: white !important;
    color: black !important;
    padding: 0.5rem 1rem !important;
}

div[data-baseweb="popover"] [role="option"]:hover {
    background: #8C1D40 !important;
    color: white !important;
}

/* Gráficos com fundo branco */
.js-plotly-plot {
    background-color: white !important;
}

.js-plotly-plot .plotly {
    background-color: white !important;
}

.js-plotly-plot svg {
    background-color: white !important;
}

/* Container dos gráficos */
div[data-testid="stPlotlyChart"] {
    background: white !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: #8C1D40 !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Botões */
.stButton > button {
    background-color: #8C1D40 !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.25rem !important;
}

.stButton > button:hover {
    background-color: #A02050 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 8px rgba(140, 29, 64, 0.3) !important;
}

/* Métricas */
div[data-testid="stMetric"] {
    background: #F8F9FA !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}

[data-testid="stMetricValue"] {
    color: #8C1D40 !important;
    font-weight: 700 !important;
    font-size: 1.8rem !important;
}

[data-testid="stMetricLabel"] {
    color: #1F2937 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Esconder elementos desnecessários */
#MainMenu, header, footer, .stDeployButton {
    visibility: hidden !important;
    display: none !important;
}

/* Títulos */
h1, h2, h3, h4, h5, h6 {
    color: #8C1D40 !important;
    font-weight: 600 !important;
}

/* Texto normal */
p, li, span, div {
    color: #1F2937 !important;
}

/* Inputs gerais */
.stNumberInput > div > div > input,
.stTextInput > div > div > input {
    background: #F8F9FA !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 6px !important;
    color: #1F2937 !important;
}

/* Slider */
.stSlider > div > div > div > div {
    background-color: #8C1D40 !important;
}

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: white !important;
    color: #1F2937 !important;
    border-radius: 6px !important;
}

[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {
    background: #8C1D40 !important;
    color: white !important;
}

/* Alertas */
div[data-testid="stAlert"] {
    border-radius: 8px !important;
    border: none !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
}

/* Expanders */
div[data-testid="stExpander"] {
    border: 1px solid #E5E7EB !important;
    border-radius: 8px !important;
    background: white !important;
}

/* Dataframes */
div[data-testid="stDataFrame"] {
    border: 1px solid #E5E7EB !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}

/* Fix para divs aparecendo */
div[data-testid="stMarkdownContainer"] div:empty {
    display: none !important;
}

/* Responsividade */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem 0.5rem !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
    }
}
</style>
""", unsafe_allow_html=True)