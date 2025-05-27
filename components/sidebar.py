import streamlit as st

# Tenta importar funções de idioma, senão usa fallback
try:
    from config.idiomas import get_text, detect_language_from_selection
except ImportError:
    def get_text(key: str, lang: str) -> str:
        return "Idioma / Language" if key == 'language' else key.title()
    def detect_language_from_selection(sel: str) -> str:
        return 'pt' if 'Português' in sel else 'en'

# Paleta de cores Amaro
AMARO_BORDO = "#8C1D40"
AMARO_BRANCO = "#FFFFFF"
AMARO_TEXT_DARK = "#1F2937"
AMARO_BORDER = "#DADDE1"
AMARO_HOVER_BG = "#F6F7FA"
AMARO_FOCUS_BORDER = "#731734"
AMARO_FOCUS_SHADOW = "rgba(140,29,64,0.2)"


def render_sidebar(lang: str = 'pt') -> str:
    """
    Renderiza a sidebar com cabeçalho e seletor de idioma legível.

    Args:
        lang: Código do idioma inicial ('pt' ou 'en').
    Returns:
        O código do idioma selecionado ('pt' ou 'en').
    """
    _inject_sidebar_css()
    with st.sidebar:
        # Cabeçalho da Amaro Aviation
        st.markdown(f"""
<div style="text-align:center; padding:1rem;">
    <h3 style="color:{AMARO_BRANCO}; margin:0; font-size:1.25rem;">✈️ Amaro Aviation</h3>
    <p style="color:{AMARO_BRANCO}; margin:0.25rem 0 1rem; font-size:0.875rem;">Simulador Estratégico de Custos</p>
</div>
""", unsafe_allow_html=True)

        # Seleção de idioma
        label = get_text('language', lang)
        options = ["🇧🇷 Português", "🇺🇸 English"]
        index = 0 if lang == 'pt' else 1
        selection = st.selectbox(label, options, index=index, key='language_selector')
        return detect_language_from_selection(selection)


def _inject_sidebar_css() -> None:
    """
    Injeta CSS para estilizar o seletor de idioma na sidebar:
      - Label branco legível sobre bordô
      - Caixa branca com texto escuro e seta visível
      - Dropdown de opções branco com hover claro
      - Oculta header/footer nativos
    """
    st.markdown(f"""
<style>
/* Fundo da sidebar */
section[data-testid="stSidebar"] > div:first-child {{{{
    background-color: {AMARO_BORDO} !important;
}}}}
/* Label do selectbox */
section[data-testid="stSidebar"] label[for="language_selector"] {{{{
    color: {AMARO_BRANCO} !important;
    font-size: 0.875rem !important;
    margin-bottom: 0.25rem !important;
}}}}
/* Caixa do select */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div:first-child {{{{
    background-color: {AMARO_BRANCO} !important;
    color: {AMARO_TEXT_DARK} !important;
    border: 1px solid {AMARO_BORDER} !important;
    border-radius: 6px !important;
    padding: 0.35rem 0.75rem !important;
    line-height: 1.5 !important;
}}}}
/* Seta da caixa */
section[data-testid="stSidebar"] div[data-baseweb="select"] svg {{{{
    fill: {AMARO_TEXT_DARK} !important;
}}}}
/* Hover/focus na caixa */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div:first-child:hover,
section[data-testid="stSidebar"] div[data-baseweb="select"] > div:first-child:focus-within {{{{
    border-color: {AMARO_FOCUS_BORDER} !important;
    box-shadow: 0 0 0 2px {AMARO_FOCUS_SHADOW} !important;
}}}}
/* Dropdown de opções */
div[data-baseweb="popover"][role="listbox"] {{{{
    background-color: {AMARO_BRANCO} !important;
    border: 1px solid {AMARO_BORDER} !important;
    border-radius: 6px !important;
    max-height: 200px !important;
    overflow-y: auto !important;
}}}}
div[data-baseweb="popover"] li[role="option"] {{{{
    padding: 0.5rem 0.75rem !important;
    color: {AMARO_TEXT_DARK} !important;
}}}}
div[data-baseweb="popover"] li[role="option"]:hover {{{{
    background-color: {AMARO_HOVER_BG} !important;
}}}}
/* Oculta header/footer padrão */
#MainMenu, header, footer {{{{
    visibility:hidden !important;
}}}}
</style>
""", unsafe_allow_html=True)