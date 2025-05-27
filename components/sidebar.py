"""
Componente de sidebar para Amaro Aviation: cabeçalho e dropdown de idioma com legibilidade e usabilidade aprimoradas.
"""
import streamlit as st
from config.idiomas import get_text, detect_language_from_selection


def render_sidebar(lang: str = 'pt') -> str:
    """
    Renderiza a sidebar com cabeçalho e seletor de idioma, aplicando CSS para contraste,
    legibilidade, espaçamento e feedback visual em hover/focus.

    Args:
        lang: Código do idioma inicial ('pt' ou 'en').

    Returns:
        Código do idioma selecionado ('pt' ou 'en').
    """
    _inject_sidebar_css()
    with st.sidebar:
        _render_header()
        lang = _render_language_selector(lang)
    return lang


def _inject_sidebar_css() -> None:
    """
    Injeta CSS para estilizar e melhorar usabilidade do select na sidebar.
    """
    st.markdown(
        """
        <style>
        /* Fundo da sidebar */
        section[data-testid="stSidebar"]>div { background-color: #8C1D40 !important; }

        /* Label do select */
        section[data-testid="stSidebar"] label[for="language_selector"] {
            color: #FFFFFF !important;
            font-size: 0.875rem !important;
            margin-bottom: 0.25rem !important;
            display: block;
        }

        /* Container do select (campo) */
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
            border: 1px solid #DADDE1 !important;
            border-radius: 6px !important;
            padding: 0.35rem 0.75rem !important;
            line-height: 1.5 !important;
            position: relative;
        }

        /* Placeholder mais escuro */
        section[data-testid="stSidebar"] div[data-baseweb="select"] input::placeholder {
            color: #9CA3AF !important;
        }

        /* Hover e focus no campo */
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover,
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within {
            border-color: #8C1D40 !important;
            box-shadow: 0 0 0 2px rgba(140, 29, 64, 0.2) !important;
        }

        /* Seta do select em cor escura */
        section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
            fill: #1F2937 !important;
        }

        /* Dropdown de opções */
        section[data-testid="stSidebar"] div[data-baseweb="popover"] {
            background-color: #FFFFFF !important;
            border: 1px solid #DADDE1 !important;
            border-radius: 6px !important;
            max-height: 200px !important;
            overflow-y: auto !important;
        }
        section[data-testid="stSidebar"] div[data-baseweb="popover"] div[role="option"] {
            padding: 0.5rem 0.75rem !important;
            color: #1F2937 !important;
        }
        section[data-testid="stSidebar"] div[data-baseweb="popover"] div[role="option"]:hover {
            background-color: #F6F7FA !important;
        }

        /* Oculta header/footer padrão */
        #MainMenu, header, footer { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_header() -> None:
    """
    Exibe o cabeçalho da sidebar com título e subtítulo.
    """
    st.markdown(
        """
        <div style="text-align:center; padding:1rem; margin-bottom:1rem;">
            <h3 style="color:#FFFFFF; margin:0;">✈️ Amaro Aviation</h3>
            <p style="color:#FFFFFF; font-size:0.875rem; margin-top:0.25rem;">
                Simulador Estratégico de Custos
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_language_selector(lang: str) -> str:
    """
    Cria o selectbox para escolha de idioma e retorna o idioma selecionado.
    """
    idioma = st.selectbox(
        get_text('language', lang),
        ["🇧🇷 Português", "🇺🇸 English"],
        index=0 if lang == 'pt' else 1,
        key="language_selector"
    )
    return detect_language_from_selection(idioma)
