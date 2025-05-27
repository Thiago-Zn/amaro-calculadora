"""
Componente de sidebar sem seletor de idioma para Amaro Aviation
O dropdown de idioma foi removido e substituído por um texto estático legível.
"""
import streamlit as st
from config.idiomas import detect_language_from_selection


def render_sidebar(lang: str = 'pt', current_page: str = '') -> str:
    """
    Renderiza a sidebar principal com cabeçalho, idioma estático e navegação.

    Args:
        lang: Código do idioma atual ('pt' ou 'en').
        current_page: Identificador da página ativa.

    Returns:
        O código do idioma selecionado ('pt' ou 'en').
    """
    _inject_sidebar_css()
    with st.sidebar:
        _render_header()
        _render_language_display(lang)
        _render_navigation(current_page, lang)
    return lang


def _inject_sidebar_css() -> None:
    """
    Injeta CSS para estilizar sidebar e itens de navegação.
    """
    st.markdown(
        """
        <style>
        /* Fundo geral da sidebar */
        section[data-testid="stSidebar"] > div {
            background-color: #8C1D40 !important;
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
        /* Oculta cabeçalho/rodapé padrão */
        #MainMenu, header, footer {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_header() -> None:
    """
    Renderiza o cabeçalho da sidebar.
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


def _render_language_display(lang: str) -> None:
    """
    Exibe o idioma atual como texto estático.
    """
    label = "🇧🇷 Português" if lang == 'pt' else "🇺🇸 English"
    st.markdown(
        f"<div style='text-align:center; color:#FFFFFF; font-size:0.875rem; margin-bottom:1rem;'>{label}</div>",
        unsafe_allow_html=True,
    )


def _render_navigation(current_page: str, lang: str) -> None:
    """
    Renderiza a navegação, destacando a página ativa.
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
    st.markdown('---')
    for key, desc in pages_info[lang].items():
        is_active = current_page.endswith(key)
        css = 'nav-item-active' if is_active else 'nav-item'
        icon = '👉' if is_active else '📄'
        st.markdown(
            f"<div class='{css}'>{icon}&nbsp;{desc}</div>",
            unsafe_allow_html=True,
        )
