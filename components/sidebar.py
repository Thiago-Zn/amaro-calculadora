import streamlit as st
from config.idiomas import get_text, detect_language_from_selection

def render_sidebar(lang: str = 'pt') -> str:
    """
    Renderiza a sidebar com cabeçalho e seletor de idioma,
    garantindo legibilidade do dropdown.
    """
    _inject_sidebar_css()
    with st.sidebar:
        # Cabeçalho
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

        # Seletor nativo com label
        label = get_text('language', lang)  # ex: "Idioma / Language"
        idioma = st.selectbox(
            label,
            ["🇧🇷 Português", "🇺🇸 English"],
            index=0 if lang == 'pt' else 1,
            key="language_selector"
        )
        return detect_language_from_selection(idioma)


def _inject_sidebar_css() -> None:
    """
    Injeta CSS para estilizar e melhorar usabilidade do selectbox:
      • Label em branco legível
      • Campo branco com texto escuro
      • Seta escura
      • Dropdown branco com opções legíveis e hover
      • Oculta header/footer nativos
    """
    st.markdown(
        """
        <style>
        /* 1. Fundo da sidebar */
        section[data-testid="stSidebar"] > div {
            background-color: #8C1D40 !important;
        }
        /* 2. Label nativo do select: texto branco */
        section[data-testid="stSidebar"] label[for="language_selector"] {
            color: #FFFFFF !important;
            font-size: 0.875rem !important;
            margin-bottom: 0.25rem !important;
        }
        /* 3. Campo do select (div interna) */
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
            border: 1px solid #DADDE1 !important;
            border-radius: 6px !important;
            padding: 0.35rem 0.75rem !important;
            line-height: 1.5 !important;
        }
        /* 4. Seta do select em cinza-escuro */
        section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
            fill: #1F2937 !important;
        }
        /* 5. Hover/focus no campo */
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover,
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within {
            border-color: #731734 !important;
            box-shadow: 0 0 0 2px rgba(140,29,64,0.2) !important;
        }
        /* 6. Dropdown de opções */
        section[data-testid="stSidebar"] div[data-baseweb="popover"] {
            background-color: #FFFFFF !important;
            border: 1px solid #DADDE1 !important;
            border-radius: 6px !important;
            max-height: 200px !important;
            overflow-y: auto !important;
        }
        /* 7. Cada opção no dropdown */
        section[data-testid="stSidebar"] div[data-baseweb="popover"] li[role="option"] {
            padding: 0.5rem 0.75rem !important;
            color: #1F2937 !important;
        }
        section[data-testid="stSidebar"] div[data-baseweb="popover"] li[role="option"]:hover {
            background-color: #F6F7FA !important;
        }
        /* 8. Oculta header/footer padrão */
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
