"""
Componente de sidebar para Amaro Aviation: cabeçalho e dropdown de idioma com legibilidade corrigida.
"""
import streamlit as st
from config.idiomas import get_text, detect_language_from_selection


def render_sidebar(lang: str = 'pt') -> str:
    """
    Renderiza a sidebar com cabeçalho e seletor de idioma, sem navegação de páginas.

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
    Injeta CSS para garantir contraste e legibilidade do dropdown de idioma em fundo bordô.
    """
    st.markdown(
        """
        <style>
        /* Fundo da sidebar */
        section[data-testid="stSidebar"]>div{background-color:#8C1D40!important;}
        /* Label do select */
        section[data-testid="stSidebar"] label[for="language_selector"]{
            color:#FFFFFF!important;
            font-size:0.875rem!important;
            margin-bottom:0.25rem!important;
            display:block;
        }
        /* Estilo do select principal */
        section[data-testid="stSidebar"] div[data-baseweb="select"]>div{
            background-color:#FFFFFF!important;
            color:#1F2937!important;
            border:1px solid #DADDE1!important;
            border-radius:6px!important;
            padding:0.5rem!important;
        }
        /* Fundo do dropdown de opções */
        section[data-testid="stSidebar"] div[data-baseweb="popover"]{
            background-color:#FFFFFF!important;
            border:1px solid #DADDE1!important;
            border-radius:6px!important;
        }
        /* Texto das opções */
        section[data-testid="stSidebar"] div[role="option"]{
            color:#1F2937!important;
            background-color:#FFFFFF!important;
        }
        /* Oculta header e footer padrão */
        #MainMenu, header, footer{visibility:hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_header() -> None:
    """
    Exibe o cabeçalho fixo da sidebar com título e subtítulo.
    """
    st.markdown(
        """
        <div style="text-align:center;padding:1rem;margin-bottom:1rem;">
          <h3 style="color:#FFFFFF;margin:0;">✈️ Amaro Aviation</h3>
          <p style="color:#FFFFFF;font-size:0.875rem;margin-top:0.25rem;">Simulador Estratégico de Custos</p>
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
