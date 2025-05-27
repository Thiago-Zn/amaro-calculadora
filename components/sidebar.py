"""
Componente de sidebar reutilizável para Amaro Aviation com correções de legibilidade
"""

import streamlit as st
from config.idiomas import get_text, detect_language_from_selection


def render_sidebar(lang: str = 'pt', current_page: str = "") -> str:
    """
    Renderiza a sidebar principal com cabeçalho, seleção de idioma e navegação,
    aplicando correções CSS para garantir legibilidade dos elementos.

    Args:
        lang: Código do idioma ('pt' ou 'en').
        current_page: Identificador da página atual (opcional).

    Returns:
        O código do idioma selecionado ('pt' ou 'en').
    """
    # CSS injetado para corrigir cores do select e opções
    st.markdown(
        """
        <style>
        /* Label do select em branco */
        section[data-testid="stSidebar"] label[for="language_selector"] {
            color: #FFFFFF !important;
            font-size: 0.875rem !important;
            margin-bottom: 0.25rem !important;
        }
        /* Fundo do dropdown */
        div[role="listbox"] {
            background: #FFFFFF !important;
            border: 1px solid #DADDE1 !important;
        }
        /* Texto de cada opção */
        div[role="option"] {
            color: #1F2937 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        # Cabeçalho da sidebar
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem; margin-bottom: 1rem;">
                <h3 style="color: #8C1D40; margin: 0;">✈️ Amaro Aviation</h3>
                <p style="color: #FFFFFF; font-size: 0.875rem; margin-top: 0.5rem;">
                    Simulador Estratégico de Custos
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # Seletor de idioma
        idioma_selecionado = st.selectbox(
            get_text('language', lang),
            ["🇧🇷 Português", "🇺🇸 English"],
            index=0 if lang == 'pt' else 1,
            key="language_selector"
        )
        lang = detect_language_from_selection(idioma_selecionado)
        st.markdown("---")

        # Navegação entre páginas
        render_navigation_help(current_page, lang)

    return lang


def render_navigation_help(current_page: str = "", lang: str = 'pt') -> None:
    """
    Renderiza a lista de navegação na sidebar, destacando a página atual.

    Args:
        current_page: Identificador da página atual.
        lang: Código do idioma ('pt' ou 'en').
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

    for page_key, description in pages_info[lang].items():
        is_current = current_page.endswith(page_key)
        bg_color = '#FFFFFF' if not is_current else '#8C1D40'
        text_color = '#8C1D40' if is_current else '#FFFFFF'
        icon = "👉" if is_current else "📄"
        st.markdown(
            f"<div style='display: flex; align-items: center; padding: 0.25rem 1rem; ``background: {bg_color}; color: {text_color}; border-radius: 4px;'>"
            f"{icon}&nbsp;<span>{description}</span></div>",
            unsafe_allow_html=True
        )
