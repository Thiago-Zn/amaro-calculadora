import streamlit as st

# Importa e fallback de idioma
try:
    from config.idiomas import get_text, detect_language_from_selection
except ImportError:
    def get_text(key: str, lang: str) -> str:
        return "Idioma / Language" if key == 'language' else key.title()
    def detect_language_from_selection(selection: str) -> str:
        return 'pt' if 'Português' in selection else 'en'

# Cores oficiais Amaro
AMARO_BORDO = "#8C1D40"
AMARO_BRANCO = "#FFFFFF"
AMARO_PRETO = "#000000"


def render_sidebar(lang: str = 'pt') -> str:
    """
    Renderiza a sidebar com cabeçalho e seletor de idioma
    utilizando apenas preto, branco e bordô.

    Args:
        lang: Código do idioma inicial ('pt' ou 'en').
    Returns:
        Novo código de idioma selecionado.
    """
    _inject_sidebar_css()
    with st.sidebar:
        # Cabeçalho
        st.markdown(
            f"""
            <div style="text-align:center; padding:1rem;">
                <h3 style="color:{AMARO_BRANCO}; margin:0; font-size:1.25rem;">✈️ Amaro Aviation</h3>
                <p style="color:{AMARO_BRANCO}; margin:0.5rem 0 1rem; font-size:0.875rem;">Simulador Estratégico de Custos</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Seletor de idioma
        label = get_text('language', lang)
        options = ["🇧🇷 Português", "🇺🇸 English"]
        idx = 0 if lang == 'pt' else 1
        selection = st.selectbox(label, options, index=idx, key='language_selector')
        return detect_language_from_selection(selection)


def _inject_sidebar_css() -> None:
    """
    Injeta CSS para estilizar o seletor de idioma na sidebar:
      • Label em branco
      • Campo branco com texto preto e bordô
      • Dropdown de opções branco com texto preto e hover de bordô
      • Oculta header/footer padrão
    """
    st.markdown(
        f"""
<style>
/* Sidebar background */
section[data-testid="stSidebar"] > div:first-child {{
  background-color: {AMARO_BORDO} !important;
}}
/* Label do selectbox */
section[data-testid="stSidebar"] label[for="language_selector"] {{
  color: {AMARO_BRANCO} !important;
  font-size: 0.875rem !important;
  margin-bottom: 0.25rem !important;
}}
/* Caixa do select */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div:first-child {{
  background-color: {AMARO_BRANCO} !important;
  color: {AMARO_PRETO} !important;
  border: 1px solid {AMARO_BORDO} !important;
  border-radius: 6px !important;
  padding: 0.5rem !important;
}}
/* Seta do select */
section[data-testid="stSidebar"] div[data-baseweb="select"] svg {{
  fill: {AMARO_PRETO} !important;
}}
/* Dropdown de opções */
div[data-baseweb="popover"][role="listbox"] {{
  background-color: {AMARO_BRANCO} !important;
  border: 1px solid {AMARO_BORDO} !important;
  border-radius: 6px !important;
  max-height: 200px !important;
  overflow-y: auto !important;
}}
/* Itens do dropdown */
div[data-baseweb="popover"] li[role="option"] {{
  color: {AMARO_PRETO} !important;
  padding: 0.5rem 0.75rem !important;
}}
/* Hover no item */
div[data-baseweb="popover"] li[role="option"]:hover {{
  background-color: {AMARO_BORDO} !important;
  color: {AMARO_BRANCO} !important;
}}
/* Esconde header/footer padrão */
#MainMenu, header, footer {{
  visibility: hidden !important;
}}
</style>
""",
        unsafe_allow_html=True,
    )
