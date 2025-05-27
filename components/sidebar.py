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
    Injeta CSS para estilizar e melhorar usabilidade do select de idioma na sidebar:
      - Label com fundo bordô e texto branco
      - Campo de seleção com fundo branco e texto escuro
      - Placeholder cinza médio
      - Seta escura
      - Dropdown de opções com scroll
      - Feedback visual em hover/focus
      - Oculta header/footer nativos
    """
    st.markdown(
        """
        <style>
        /* 1. Sidebar: fundo bordô */
        section[data-testid="stSidebar"] > div {
            background-color: #8C1D40 !important;
        }

        /* 2. Label do select: fundo bordô, texto branco */
        section[data-testid="stSidebar"] label[for="language_selector"] {
            background-color: #731734 !important;
            color: #FFFFFF !important;
            padding: 0.25rem 0.5rem !important;
            border-radius: 4px !important;
            font-size: 0.875rem !important;
            margin-bottom: 0.5rem !important;
            display: block !important;
        }

        /* 3. Container do select (campo): fundo branco, texto escuro */
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
            border: 1px solid #DADDE1 !important;
            border-radius: 6px !important;
            padding: 0.35rem 0.75rem !important;
            line-height: 1.5 !important;
            position: relative !important;
        }

        /* 4. Placeholder: cinza médio */
        section[data-testid="stSidebar"] div[data-baseweb="select"] input::placeholder {
            color: #6B7280 !important;
        }

        /* 5. Seta do select em cor escura */
        section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
            fill: #1F2937 !important;
        }

        /* 6. Hover/Focus no campo selecionável */
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover,
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within {
            border-color: #731734 !important;
            box-shadow: 0 0 0 2px rgba(140, 29, 64, 0.2) !important;
            outline: none !important;
        }

        /* 7. Dropdown de opções: fundo branco, scroll e hover */
        section[data-testid="stSidebar"] div[data-baseweb="popover"] {
            background-color: #FFFFFF !important;
            border: 1px solid #DADDE1 !important;
            border-radius: 6px !important;
            max-height: 200px !important;
            overflow-y: auto !important;
        }
        section[data-testid="stSidebar"] div[data-baseweb="popover"] li[role="option"] {
            padding: 0.5rem 0.75rem !important;
            color: #1F2937 !important;
        }
        section[data-testid="stSidebar"] div[data-baseweb="popover"] li[role="option"]:hover {
            background-color: #F6F7FA !important;
        }

        /* 8. Oculta header/footer padrão do Streamlit */
        #MainMenu, header, footer {
            visibility: hidden !important;
        }
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
