"""
Componente de sidebar reutilizável para Amaro Aviation – corrigido para legibilidade e funcionamento.
"""
import streamlit as st
from config.idiomas import get_text, detect_language_from_selection


def render_sidebar(lang: str = 'pt', current_page: str = '') -> str:
    """
    Renderiza a sidebar principal com cabeçalho, seleção de idioma e navegação.
    Aplica CSS para garantir legibilidade dos elementos em fundo bordô.

    Args:
        lang: Código do idioma inicial ('pt' ou 'en').
        current_page: Identificador da página atual (nome do arquivo ou chave).

    Returns:
        O código do idioma selecionado ('pt' ou 'en').
    """
    _inject_sidebar_css()
    with st.sidebar:
        _render_header()
        lang = _render_language_selector(lang)
        _render_navigation(current_page, lang)
    return lang


def _inject_sidebar_css() -> None:
    """
    Injeta CSS personalizado na sidebar para corrigir cores do seletor,
    fundo do dropdown e estilo de navegação.
    """
    st.markdown(
        """
        <style>
        /* Fundo geral da sidebar */
        section[data-testid="stSidebar"]>div>div {
            background-color: #8C1D40 !important;
        }
        /* Label do seletor de idioma */
        section[data-testid="stSidebar"] label[for="language_selector"] {
            color: #FFFFFF !important;
            font-size: 0.875rem !important;
            margin-bottom: 0.25rem !important;
        }
        /* Campo de seleção (input) */
        section[data-testid="stSidebar"] div[data-baseweb="select"]>div {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
        }
        /* Dropdown de opções */
        section[data-testid="stSidebar"] div[data-baseweb="popover"] {
            background-color: #FFFFFF !important;
            border: 1px solid #DADDE1 !important;
        }
        section[data-testid="stSidebar"] div[role="option"] {
            background-color: #FFFFFF !important;
            color: #1F2937 !important;
        }
        /* Itens de navegação */
        .nav-item {
            display: flex;
            align-items: center;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            color: #FFFFFF;
            text-decoration: none;
        }
        .nav-item:hover {
            background-color: #731734;
        }
        .nav-item-active {
            display: flex;
            align-items: center;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            background-color: #FFFFFF;
            color: #8C1D40 !important;
            font-weight: 600;
        }
        /* Oculta header/rodapé padrão */
        #MainMenu, header, footer {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_header() -> None:
    """
    Renderiza o cabeçalho fixo da sidebar.
    """
    st.markdown(
        """
        <div style="text-align:center; padding:1rem; margin-bottom:1rem;">
            <h3 style="color:#FFFFFF; margin:0;">✈️ Amaro Aviation</h3>
            <p style="color:#FFFFFF; font-size:0.875rem; margin-top:0.5rem;">
                Simulador Estratégico de Custos
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_language_selector(lang: str) -> str:
    """
    Renderiza o selectbox de idioma e retorna o idioma escolhido.
    """
    idioma_selecionado = st.selectbox(
        get_text('language', lang),
        ["🇧🇷 Português", "🇺🇸 English"],
        index=0 if lang == 'pt' else 1,
        key="language_selector"
    )
    return detect_language_from_selection(idioma_selecionado)


def _render_navigation(current_page: str, lang: str) -> None:
    """
    Renderiza a lista de navegação sem título, destacando a página ativa.
    """
    pages_info = {
        'pt': {
            'Estimativa_de_Lucro': 'Análise de rentabilidade mensal com charter',
            'Breakdown_de_Custos': 'Comparativo gestão própria vs Amaro',
            'Simulador_de_Rotas': 'Custo ponto-a-ponto por rota',
            'Projecao_e_Breakeven': 'Projeção de longo prazo e breakeven',
            'Configuracoes': 'Parâmetros e configurações'
        },
        'en': {
            'Estimativa_de_Lucro': 'Monthly profitability analysis with charter',
            'Breakdown_de_Custos': 'Own management vs Amaro comparison',
            'Simulador_de_Rotas': 'Point-to-point cost per route',
            'Projecao_e_Breakeven': 'Long-term projection and breakeven',
            'Configuracoes': 'Parameters and settings'
        }
    }
    # Espaçamento antes da navegação
    st.markdown('---')
    for key, desc in pages_info[lang].items():
        is_active = current_page.endswith(key)
        css_class = 'nav-item-active' if is_active else 'nav-item'
        icon = '👉' if is_active else '📄'
        st.markdown(
            f"<div class=\"{css_class}\">{icon}&nbsp;{desc}</div>",
            unsafe_allow_html=True
        )
