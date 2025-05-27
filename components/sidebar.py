"""
Sidebar Amaro Aviation — paleta bordô/branco/preto
Coloque este arquivo em components/sidebar.py
"""

from __future__ import annotations
import streamlit as st

# ──────────────────────────────────────────────────────────────────────
# 1. I18N  ─ fallback se config.idiomas não estiver no projeto
# ──────────────────────────────────────────────────────────────────────
try:
    from config.idiomas import get_text, detect_language_from_selection
except ImportError:
    def get_text(key: str, lang: str) -> str:            # noqa: D401
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
    """Selectbox de idioma (branco/preto)."""
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
# 5. Folha de estilos — TODA a paleta aqui dentro
# ──────────────────────────────────────────────────────────────────────
def _inject_css() -> None:
    """Insere CSS na página garantindo 100 % da paleta desejada."""
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
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    margin-bottom: 0.25rem !important;
}}

/* === 3. Selectbox fechado === */
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] {{
    background: {AMARO_BORDO} !important;
    padding: 0 !important;
}}
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child {{
    background: {AMARO_BRANCO} !important;
    color: {AMARO_PRETO} !important;
    border: 1px solid {AMARO_BORDO} !important;
    border-radius: 6px !important;
    padding: 0.4rem 0.75rem !important;
    font-size: 0.875rem !important;
}}
section[data-testid="stSidebar"] div[data-testid="stSelectbox"] svg {{
    fill: {AMARO_PRETO} !important;
}}

/* === 4. Pop-over / dropdown === */
/* Aplicamos no nó raiz e em TODOS os descendentes para derrotar o tema escuro */
div[data-baseweb="popover"][role="listbox"],
div[data-baseweb="popover"][role="listbox"] * {{
    background: {AMARO_BRANCO} !important;
    color: {AMARO_PRETO} !important;
    font-size: 0.875rem !important;
}}
/* Espaçamento de cada item */
div[data-baseweb="popover"][role="listbox"] [role="option"] {{
    padding: 0.5rem 0.85rem !important;
}}
/* Hover e item já selecionado */
div[data-baseweb="popover"][role="listbox"] [role="option"]:hover,
div[data-baseweb="popover"][role="listbox"] [role="option"][aria-selected="true"],
div[data-baseweb="popover"][role="listbox"] [role="option"]:hover *,
div[data-baseweb="popover"][role="listbox"] [role="option"][aria-selected="true"] * {{
    background: {AMARO_BORDO} !important;
    color: {AMARO_BRANCO} !important;
}}

/* === 5. Esconde header e footer padrão do Streamlit === */
#MainMenu, header, footer {{
    visibility: hidden !important;
}}
</style>
        """,
        unsafe_allow_html=True,
    )
