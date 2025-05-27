"""
Componente de sidebar para Amaro Aviation: cabeçalho e dropdown de idioma legível
Sem navegação de páginas, apenas seletor de idioma totalmente visível.
"""
import streamlit as st
from config.idiomas import get_text, detect_language_from_selection


def render_sidebar(lang: str = 'pt') -> str:
    """
    Renderiza a sidebar com cabeçalho e seletor de idioma, garantindo
    legibilidade do dropdown através de CSS customizado.

    Args:
        lang: Código do idioma inicial ('pt' ou 'en').

    Returns:
        Código do idioma selecionado ('pt' ou 'en').
    """
    _inject_sidebar_css()
    with st.sidebar:
        # Cabeçalho fixo
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
        # Rótulo customizado para o dropdown
        st.markdown(
            """
            <p class="language-label" style="color:#FFFFFF; font-size:0.875rem; margin-bottom:0.25rem;">
                Idioma / Language
            </p>
            """,
            unsafe_allow_html=True,
        )
        # Seletor de idioma sem label nativo
        idioma = st.selectbox(
            "",  # label vazio
            ["🇧🇷 Português", "🇺🇸 English"],
            index=0 if lang == 'pt' else 1,
            key="language_selector"
        )
        lang = detect_language_from_selection(idioma)
    return lang


def _inject_sidebar_css() -> None:
    """
    Injeta CSS no head para estilizar o selectbox de idioma:
      • Campo branco com texto escuro
      • Placeholder cinza médio
      • Seta escura
      • Dropdown de opções branco com texto escuro e hover
      • Oculta header/footer padrão
    """
    st.markdown(
        """
        <style>
        /* Fundo da sidebar */
        section[data-testid="stSidebar"] > div {
            background-color: #8C1D40 !important;
        }
        /* Campo do select: branco com texto escuro */
        div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
            border: 1px solid #DADDE1 !important;
            border-radius: 6px !important;
            padding: 0.375rem 0.75rem !important;
            line-height: 1.5 !important;
            position: relative !important;
        }
        /* Placeholder cinza médio */
        div[data-baseweb="select"] input::placeholder {
            color: #6B7280 !important;
        }
        /* Seta em cinza-escuro */
        div[data-baseweb="select"] svg {
            fill: #1F2937 !important;
        }
        /* Hover/focus no campo */
        div[data-baseweb="select"] > div:hover,
        div[data-baseweb="select"] > div:focus-within {
            border-color: #731734 !important;
            box-shadow: 0 0 0 2px rgba(140,29,64,0.2) !important;
            outline: none !important;
        }
        /* Dropdown global de opções: branco, scroll e hover */
        div[data-baseweb="popover"] {
            background-color: #FFFFFF !important;
            border: 1px solid #DADDE1 !important;
            border-radius: 6px !important;
            max-height: 200px !important;
            overflow-y: auto !important;
        }
        div[data-baseweb="popover"] li[role="option"] {
            padding: 0.5rem 0.75rem !important;
            color: #1F2937 !important;
        }
        div[data-baseweb="popover"] li[role="option"]:hover {
            background-color: #F6F7FA !important;
        }
        /* Oculta header/footer padrão do Streamlit */
        #MainMenu, header, footer { visibility: hidden !important; }
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
