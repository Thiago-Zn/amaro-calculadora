"""
Sidebar Clean - Design baseado no site oficial da Amaro Aviation
"""

import streamlit as st

try:
    from config.idiomas import get_text, detect_language_from_selection
except ImportError:
    def get_text(key: str, lang: str) -> str:
        if key == "language":
            return "Idioma / Language"
        return key.replace("_", " ").title()

    def detect_language_from_selection(selection: str) -> str:
        return "pt" if "Português" in selection else "en"

def render_sidebar(current_lang: str = "pt") -> str:
    """
    Sidebar clean inspirada no design oficial da Amaro Aviation
    """
    
    # CSS específico para sidebar clean
    st.markdown("""
    <style>
    /* === SIDEBAR CLEAN AMARO === */
    section[data-testid="stSidebar"] {
        background: #8C1D40 !important;
        border-right: none !important;
    }
    
    section[data-testid="stSidebar"] > div:first-child {
        background: #8C1D40 !important;
        padding: 2rem 1rem !important;
    }
    
    /* === HEADER DA SIDEBAR === */
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 1rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }
    
    .sidebar-logo {
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .sidebar-tagline {
        color: rgba(255,255,255,0.9);
        font-size: 0.875rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* === SELETOR DE IDIOMA CLEAN === */
    section[data-testid="stSidebar"] .stSelectbox {
        margin: 1.5rem 0 !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        margin-bottom: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    /* Caixa principal do seletor - CLEAN e MODERNA */
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: white !important;
        color: #333333 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 1rem 1.25rem !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        min-height: 48px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        transition: all 0.2s ease !important;
    }
    
    /* Hover effect suave */
    section[data-testid="stSidebar"] .stSelectbox > div > div:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
    }
    
    /* Seta do dropdown */
    section[data-testid="stSidebar"] .stSelectbox svg {
        fill: #333333 !important;
        width: 18px !important;
        height: 18px !important;
    }
    
    /* === DROPDOWN CLEAN === */
    div[data-baseweb="popover"][role="listbox"] {
        background: white !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2) !important;
        padding: 0.5rem 0 !important;
        min-width: 200px !important;
    }
    
    /* Opções do dropdown */
    div[data-baseweb="popover"] [role="option"] {
        background: white !important;
        color: #333333 !important;
        padding: 1rem 1.25rem !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        border: none !important;
        margin: 0 0.5rem !important;
        border-radius: 8px !important;
        transition: all 0.15s ease !important;
    }
    
    /* Hover nas opções */
    div[data-baseweb="popover"] [role="option"]:hover {
        background: #F8F9FA !important;
        color: #8C1D40 !important;
        transform: translateX(4px) !important;
    }
    
    /* Opção selecionada */
    div[data-baseweb="popover"] [role="option"][aria-selected="true"] {
        background: #8C1D40 !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* === NAVEGAÇÃO LIMPA === */
    section[data-testid="stSidebar"] .stRadio {
        margin-top: 2rem !important;
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 1rem !important;
    }
    
    /* === FOOTER DA SIDEBAR === */
    .sidebar-footer {
        position: absolute;
        bottom: 2rem;
        left: 1rem;
        right: 1rem;
        text-align: center;
        border-top: 1px solid rgba(255,255,255,0.2);
        padding-top: 1rem;
    }
    
    .sidebar-footer p {
        color: rgba(255,255,255,0.7) !important;
        font-size: 0.75rem !important;
        margin: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # Header elegante da sidebar
        st.markdown("""
        <div class="sidebar-header">
            <h1 class="sidebar-logo">✈️ Amaro Aviation</h1>
            <p class="sidebar-tagline">Simulador Estratégico de Custos</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Seletor de idioma clean
        label = get_text("language", current_lang)
        options = ["🇧🇷 Português", "🇺🇸 English"]

        try:
            cur_display = next(
                opt for opt in options
                if detect_language_from_selection(opt) == current_lang
            )
            idx = options.index(cur_display)
        except StopIteration:
            idx = 0

        selected_display = st.selectbox(
            label,
            options,
            index=idx,
            key="language_selector_clean"
        )
        
        # Espaço para respirar
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
        
        # Footer sutil (opcional)
        st.markdown("""
        <div class="sidebar-footer">
            <p>v3.0 • Design Clean</p>
        </div>
        """, unsafe_allow_html=True)