import streamlit as st
from config.idiomas import get_text, detect_language_from_selection


def render_sidebar(current_page: str, lang: str = 'pt') -> str:
    """
    Renderiza a sidebar principal com seleção de idioma e navegação

    Args:
        current_page: Identificador da página atual (nome do arquivo ou chave).
        lang: Código do idioma ('pt' ou 'en').

    Returns:
        Código do idioma selecionado ('pt' ou 'en').
    """
    with st.sidebar:
        # Cabeçalho da sidebar
        st.markdown(
            f"""
            <div style="text-align: center; padding: 1rem; margin-bottom: 1rem;">
                <h3 style="color: #8C1D40; margin: 0;">✈️ Amaro Aviation</h3>
                <p style="color: #6B7280; font-size: 0.875rem; margin-top: 0.5rem;">
                    Simulador Estratégico de Custos
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")

        # Seletor de idioma
        idioma_selecionado = st.selectbox(
            get_text('language', lang),
            ["🇧🇷 Português", "🇺🇸 English"],
            index=0 if lang == 'pt' else 1,
            key="language_selector"
        )
        lang_atual = detect_language_from_selection(idioma_selecionado)
        st.markdown("---")

        # Navegação entre páginas
        render_navigation_help(current_page, lang_atual)

    return lang_atual


def render_navigation_help(current_page: str, lang: str = 'pt') -> None:
    """
    Renderiza a lista de navegação na sidebar, destacando a página atual.

    Args:
        current_page: Identificador da página atual.
        lang: Código do idioma ('pt' ou 'en').
    """
    pages_info = {
        'pt': {
            '1_Estimativa_de_Lucro': 'Análise de rentabilidade mensal com charter',
            '2_Breakdown_de_Custos': 'Comparativo gestão própria vs Amaro',
            '3_Simulador_de_Rotas': 'Custo ponto-a-ponto por rota',
            '4_Projecao_e_Breakeven': 'Projeção de longo prazo e breakeven',
            '5_Configuracoes': 'Parâmetros e configurações'
        },
        'en': {
            '1_Estimativa_de_Lucro': 'Monthly profitability analysis with charter',
            '2_Breakdown_de_Custos': 'Own management vs Amaro comparison',
            '3_Simulador_de_Rotas': 'Point-to-point cost per route',
            '4_Projecao_e_Breakeven': 'Long-term projection and breakeven',
            '5_Configuracoes': 'Parameters and settings'
        }
    }

    title = "📚 Páginas Disponíveis" if lang == 'pt' else "📚 Available Pages"
    st.markdown(f"### {title}")

    for page_key, description in pages_info[lang].items():
        # Comparação exata do identificador da página
        is_current = current_page.endswith(page_key)
        icon = "👉" if is_current else "📄"
        style = (
            "font-weight: 600; color: #8C1D40;"
            if is_current else
            "color: #6B7280;"
        )
        st.markdown(
            f"{icon} <span style='{style}'>{description}</span>",
            unsafe_allow_html=True
        )
