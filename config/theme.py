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
    text-transform: none !important;     
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
    transition: all 0.2s ease;
}}
.stButton>button:hover, .stDownloadButton>button:hover {{
    background: {AMARO_BORDO_HOVER};
    border-color: {AMARO_BORDO_HOVER};
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(140, 29, 64, 0.3);
}}
.stButton>button:active, .stDownloadButton>button:active {{
    background: {AMARO_BORDO_ACTIVE};
    border-color: {AMARO_BORDO_ACTIVE};
    transform: translateY(0);
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

/* ——— GRÁFICOS PLOTLY - FUNDO CORRIGIDO ——— */
.js-plotly-plot .plotly {{
    background-color: {AMARO_BRANCO} !important;
}}

.js-plotly-plot .plotly .main-svg {{
    background-color: {AMARO_BRANCO} !important;
}}

/* Container dos gráficos */
div[data-testid="stPlotlyChart"] {{
    background: {AMARO_BRANCO} !important;
    border: 1px solid #E3E4E8;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}}

/* Forçar fundo branco em todos os SVGs do Plotly */
.js-plotly-plot svg {{
    background-color: {AMARO_BRANCO} !important;
}}

/* Texto dos gráficos */
.js-plotly-plot text {{
    color: {AMARO_TXT_CINZA} !important;
    font-family: 'Inter', sans-serif !important;
}}

/* Grid dos gráficos mais suave */
.js-plotly-plot .gridlayer .crisp {{
    stroke: #F0F0F0 !important;
}}

/* ——— Métricas (st.metric) ——— */
[data-testid="stMetricValue"] {{
    color: {AMARO_BORDO} !important;
    font-weight: 700 !important;
    font-size: 1.8rem !important;
}}

[data-testid="stMetricLabel"] {{
    color: {AMARO_TXT_CINZA} !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

[data-testid="stMetricDelta"] {{
    color: #10B981 !important;
    font-weight: 500 !important;
}}

/* Container das métricas */
div[data-testid="stMetric"] {{
    background: {AMARO_BG_CINZA_CLARO};
    border: 1px solid #E3E4E8;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}

div[data-testid="stMetric"]:hover {{
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    transform: translateY(-1px);
    transition: all 0.2s ease;
}}

/* ——— Remoção de elementos desnecessários ——— */
#MainMenu, header, footer, .stDeployButton {{
    visibility: hidden !important;
    display: none !important;
}}

/* ——— Expanders ——— */
div[data-testid="stExpander"] {{
    border: 1px solid #E3E4E8;
    border-radius: 8px;
    background: {AMARO_BRANCO};
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}

div[data-testid="stExpander"] summary {{
    background: {AMARO_BG_CINZA_CLARO};
    border-radius: 6px 6px 0 0;
    padding: 1rem;
    font-weight: 600;
    color: {AMARO_BORDO};
}}

/* ——— Alertas do Streamlit ——— */
div[data-testid="stAlert"] {{
    border-radius: 8px;
    border: none;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}}

div[data-testid="stAlert"][data-baseweb="notification"] {{
    background: #F0FDF4 !important;
    border-left: 4px solid #10B981 !important;
}}

/* ——— Dataframes ——— */
div[data-testid="stDataFrame"] {{
    border: 1px solid #E3E4E8;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}}

/* ——— Spinner ——— */
div[data-testid="stSpinner"] > div {{
    border-top-color: {AMARO_BORDO} !important;
}}

/* ——— Corrigir divs aparecendo ——— */
div[data-testid="stMarkdownContainer"] div {{
    display: none;
}}

div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h4,
div[data-testid="stMarkdownContainer"] ul,
div[data-testid="stMarkdownContainer"] ol {{
    display: block !important;
}}

/* Esconder divs vazias que aparecem como texto */
div[data-testid="stMarkdownContainer"]:empty {{
    display: none !important;
}}

/* ——— Responsividade ——— */
@media (max-width: 768px) {{
    .block-container {{
        padding: 1rem 0.5rem !important;
    }}
    
    [data-testid="stMetricValue"] {{
        font-size: 1.4rem !important;
    }}
    
    div[data-testid="stPlotlyChart"] {{
        padding: 0.5rem;
    }}
}}
</style>
""",
        unsafe_allow_html=True,
    )