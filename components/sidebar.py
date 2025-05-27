import streamlit as st

# Importa e fallback de idioma
try:
    from config.idiomas import get_text, detect_language_from_selection
except ImportError:
    def get_text(key: str, lang: str) -> str:
        return "Idioma / Language" if key == 'language' else key.title()
    def detect_language_from_selection(selection: str) -> str:
        return 'pt' if 'Português' in selection else 'en'

# Cores da paleta Amaro
AMARO_BORDO = "#8C1D40"
AMARO_BRANCO = "#FFFFFF"
AMARO_PRETO = "#000000"


def render_sidebar(lang: str = 'pt') -> str:
    """
    Renderiza a sidebar com cabeçalho e seletor de idioma legível
    utilizando apenas preto, branco e bordo.

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

        # Seletor de idioma
        label = get_text('language', lang)
        options = ["🇧🇷 Português", "🇺🇸 English"]
        idx = 0 if lang == 'pt' else 1
        selection = st.selectbox(label, options, index=idx, key='language_selector')
        return detect_language_from_selection(selection)


def _inject_sidebar_css() -> None:
    """
    Injeta CSS na sidebar para estilizar o selectbox de idioma,
    usando apenas cores preto, branco e bordo.
    """
    st.markdown(f"""
<style>
/* 1. Fundo da sidebar */
section[data-testid="stSidebar"] > div:first-child {{
  background-color: {AMARO_BORDO} !important;
}}

/* 2. Label do selectbox */
section[data-testid="stSidebar"] label[for="language_selector"] {{
  color: {AMARO_BRANCO} !important;
  font-size: 0.875rem !important;
  margin-bottom: 0.25rem !important;
}}

/* 3. Caixa do select (campo) */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div:first-child {{
  background-color: {AMARO_BRANCO} !important;
  color: {AMARO_PRETO} !important;
  border: 1px solid {AMARO_BORDO} !important;
  border-radius: 6px !important;
  padding: 0.4rem 0.8rem !important;
  line-height: 1.5 !important;
}}

/* 4. Seta do select */
section[data-testid="stSidebar"] div[data-baseweb="select"] svg {{
  fill: {AMARO_PRETO} !important;
}}

/* 5. Hover/Focus no campo */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div:first-child:hover,
section[data-testid="stSidebar"] div[data-baseweb="select"] > div:first-child:focus-within {{
  border-color: {AMARO_BORDO} !important;
}}

/* 6. Dropdown de opções */
div[data-baseweb="popover"][role="listbox"] {{
  background-color: {AMARO_BRANCO} !important;
  border: 1px solid {AMARO_BORDO} !important;
  border-radius: 6px !important;
  max-height: 200px !important;
  overflow-y: auto !important;
}}

/* 7. Itens do dropdown */
div[data-baseweb="popover"] li[role="option"] {{
  padding: 0.5rem 0.75rem !important;
  color: {AMARO_PRETO} !important;
}}

/* 8. Hover no item */
div[data-baseweb="popover"] li[role="option"]:hover {{
  background-color: {AMARO_BORDO} !important;
  color: {AMARO_BRANCO} !important;
}}

/* 9. Oculta header/footer padrão */
#MainMenu, header, footer {{
  visibility: hidden !important;
}}
    /* 3.2. Texto selecionado (valor atual) */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div:first-child > div {
      color: {AMARO_PRETO} !important;
      opacity: 1 !important;
    }

</style>
""", unsafe_allow_html=True)
