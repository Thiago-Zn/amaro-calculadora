"""
CORREÇÃO DIRETA - Sidebar funcional com seletor de idioma legível
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
    Sidebar com seletor de idioma FUNCIONANDO
    """
    
    # CSS específico para corrigir o seletor
    st.markdown("""
    <style>
    /* Sidebar background */
    section[data-testid="stSidebar"] > div:first-child {
        background: #8C1D40 !important;
        padding-top: 2rem !important;
    }
    
    /* Sidebar text color */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Language selector container */
    section[data-testid="stSidebar"] .stSelectbox {
        margin: 1rem 0 !important;
    }
    
    /* Language selector label */
    section[data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Language selector main box */
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: white !important;
        color: black !important;
        border: 2px solid white !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-weight: 500 !important;
        min-height: 44px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
    }
    
    /* Hover effect */
    section[data-testid="stSidebar"] .stSelectbox > div > div:hover {
        border-color: #A02050 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
    }
    
    /* Dropdown arrow */
    section[data-testid="stSidebar"] .stSelectbox svg {
        fill: black !important;
    }
    
    /* Dropdown menu */
    div[data-baseweb="popover"][role="listbox"] {
        background: white !important;
        border: 2px solid #8C1D40 !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3) !important;
        min-width: 180px !important;
    }
    
    /* Dropdown options */
    div[data-baseweb="popover"] [role="option"] {
        background: white !important;
        color: black !important;
        padding: 0.75rem 1rem !important;
        font-weight: 500 !important;
        border-bottom: 1px solid #f0f0f0 !important;
    }
    
    /* Dropdown option hover */
    div[data-baseweb="popover"] [role="option"]:hover {
        background: #8C1D40 !important;
        color: white !important;
    }
    
    /* Selected option */
    div[data-baseweb="popover"] [role="option"][aria-selected="true"] {
        background: #8C1D40 !important;
        color: white !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # Header da sidebar
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0.5rem; margin-bottom: 1.5rem;">
            <h3 style="color: white; margin: 0; font-size: 1.3rem; font-weight: 600;">
                ✈️ Amaro Aviation
            </h3>
            <p style="color: white; font-size: 0.9rem; margin-top: 0.4rem; opacity: 0.9;">
                Simulador Estratégico de Custos
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Seletor de idioma
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
            key="language_selector_main"
        )
        
        # Espaço
        st.markdown("<br>", unsafe_allow_html=True)

    return detect_language_from_selection(selected_display)