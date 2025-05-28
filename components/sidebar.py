"""
Sidebar Amaro Aviation — Versão corrigida com seletor de idioma funcional
"""

import streamlit as st

# ──────────────────────────────────────────────────────────────────────
# 1. I18N  ─ fallback se config.idiomas não estiver no projeto
# ──────────────────────────────────────────────────────────────────────
try:
    from config.idiomas import get_text, detect_language_from_selection
except ImportError:
    def get_text(key: str, lang: str) -> str:
        """Retorna string traduzida ou rótulo padrão."""
        if key == "language":
            return "Idioma / Language"
        return key.replace("_", " ").title()

    def detect_language_from_selection(selection: str) -> str:
        """Converte string exibida em código de idioma ('pt' / 'en')."""
        return "pt" if "Português" in selection else "en"

# ──────────────────────────────────────────────────────────────────────
# 2. Constantes de cor (paleta oficial)
# ──────────────────────────────────────────────────────────────────────
AMARO_BORDO   = "#8C1D40"
AMARO_BRANCO  = "#FFFFFF"
AMARO_PRETO   = "#000000"
LANGUAGE_SELECTOR_KEY = "amaro_language_selector_sidebar"

# ──────────────────────────────────────────────────────────────────────
# 3. Função pública — importe-a nas páginas Streamlit
# ──────────────────────────────────────────────────────────────────────
def render_sidebar(current_lang: str = "pt") -> str:
    """
    Desenha a sidebar e devolve o idioma escolhido.

    Parameters
    ----------
    current_lang : str
        Código de idioma atualmente ativo ('pt' ou 'en').

    Returns
    -------
    str
        Código de idioma após a seleção do usuário.
    """
    _inject_css()

    with st.sidebar:
        _header()
        display = _language_select(current_lang)

    return detect_language_from_selection(display)

# ──────────────────────────────────────────────────────────────────────
# 4. Componentes privados
# ──────────────────────────────────────────────────────────────────────
def _header() -> None:
    """Cabeçalho com logotipo e tagline."""
    st.markdown(
        f"""
        <div style="text-align:center; padding:1rem 0.5rem; margin-bottom:1rem;">
            <h3 style="color:{AMARO_BRANCO}; margin:0; font-size:1.25rem; font-weight:600;">
                ✈️ Amaro Aviation
            </h3>
            <p style="color:{AMARO_BRANCO}; font-size:0.875rem; margin-top:0.35rem; opacity:0.9;">
                Simulador Estratégico de Custos
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _language_select(current_lang: str) -> str:
    """Selectbox de idioma com melhor visibilidade."""
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

    return st.selectbox(
        label,
        options,
        index=idx,
        key=LANGUAGE_SELECTOR_KEY,
    )

# ──────────────────────────────────────────────────────────────────────
# 5. CSS melhorado para maior legibilidade
# ──────────────────────────────────────────────────────────────────────
def _inject_css() -> None:
    """CSS corrigido para melhor visibilidade do seletor de idioma."""
    st.markdown(
        f"""
<style>
/* === 1. Container da sidebar === */
section[data-testid="stSidebar"] > div:first-child {{
    background: {AMARO_BORDO} !important;
}}

/* === 2. Label do selectbox === */
section[data-testid="stSidebar"] label[for*='{LANGUAGE_SELECTOR_KEY}'] {{
    color: {AMARO_BRANCO} !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.5rem !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
}}

/* === 3. Selectbox principal - MELHORADA === */
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] {{
    background: {AMARO_BORDO} !important;
    padding: 0 !important;
}}

/* Container principal do select */
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] > div > div {{
    background: {AMARO_BRANCO} !important;
    color: {AMARO_PRETO} !important;
    border: 2px solid {AMARO_BORDO} !important;
    border-radius: 8px !important;
    padding: 0.75rem 1rem !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    min-height: 44px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
}}

/* Hover effect no selectbox */
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] > div > div:hover {{
    border-color: {AMARO_BRANCO} !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
}}

/* Seta do dropdown */
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] svg {{
    fill: {AMARO_PRETO} !important;
    width: 16px !important;
    height: 16px !important;
}}

/* === 4. Dropdown / Pop-over - MELHORADO === */
div[data-baseweb="popover"][role="listbox"] {{
    background: {AMARO_BRANCO} !important;
    border: 2px solid {AMARO_BORDO} !important;
    border-radius: 8px !important;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2) !important;
    min-width: 200px !important;
}}

/* Itens do dropdown */
div[data-baseweb="popover"][role="listbox"] [role="option"] {{
    background: {AMARO_BRANCO} !important;
    color: {AMARO_PRETO} !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    padding: 0.75rem 1rem !important;
    border-bottom: 1px solid #f0f0f0 !important;
}}

/* Hover nos itens */
div[data-baseweb="popover"][role="listbox"] [role="option"]:hover {{
    background: {AMARO_BORDO} !important;
    color: {AMARO_BRANCO} !important;
}}

/* Item selecionado */
div[data-baseweb="popover"][role="listbox"] [role="option"][aria-selected="true"] {{
    background: {AMARO_BORDO} !important;
    color: {AMARO_BRANCO} !important;
    font-weight: 600 !important;
}}

/* === 5. Esconde elementos padrão do Streamlit === */
#MainMenu, header, footer {{
    visibility: hidden !important;
}}

/* === 6. Melhoria geral na sidebar === */
section[data-testid="stSidebar"] {{
    border-right: 3px solid {AMARO_BORDO} !important;
}}

section[data-testid="stSidebar"] > div {{
    padding-top: 2rem !important;
}}
</style>
        """,
        unsafe_allow_html=True,
    )