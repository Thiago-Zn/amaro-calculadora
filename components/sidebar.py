"""
Componente de sidebar reutilizável
"""

import streamlit as st
from config.idiomas import get_text, detect_language_from_selection

def render_sidebar(lang='pt'):
    """
    Renderiza a sidebar principal com seleção de idioma
    
    Args:
        lang: Idioma atual
    
    Returns:
        String: Código do idioma selecionado
    """
    
    with st.sidebar:
        # Header da sidebar
        st.markdown("""
        <div style="text-align: center; padding: 1rem; margin-bottom: 1rem;">
            <h3 style="color: #8C1D40; margin: 0;">✈️ Amaro Aviation</h3>
            <p style="color: #6B7280; font-size: 0.875rem; margin-top: 0.5rem;">
                Simulador Estratégico de Custos
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Seleção de idioma
        idioma_selecionado = st.selectbox(
            get_text('language', lang),
            ["🇧🇷 Português", "🇺🇸 English"],
            index=0 if lang == 'pt' else 1,
            key="language_selector"
        )
        
        lang_atual = detect_language_from_selection(idioma_selecionado)
        
        st.markdown("---")
        
        # Informações do sistema
        render_system_info(lang_atual)
        
        return lang_atual

def render_system_info(lang='pt'):
    """
    Renderiza informações do sistema na sidebar
    
    Args:
        lang: Idioma
    """
    
    st.markdown(f"""
    <div style="
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #10B981;
        margin: 1rem 0;
    ">
        <div style="color: #10B981; font-weight: 600; font-size: 0.875rem; margin-bottom: 0.5rem;">
            ✅ {get_text('system_operational' if lang == 'pt' else 'system_operational', lang)}
        </div>
        <div style="color: #6B7280; font-size: 0.75rem;">
            Versão 3.0 - Multipage
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_navigation_help(current_page, lang='pt'):
    """
    Renderiza ajuda de navegação na sidebar
    
    Args:
        current_page: Página atual
        lang: Idioma
    """
    
    pages_info = {
        'pt': {
            '1_📈_Estimativa_de_Lucro': 'Análise de rentabilidade mensal com charter',
            '2_📊_Breakdown_de_Custos': 'Comparativo gestão própria vs Amaro',
            '3_✈️_Simulador_de_Rotas': 'Custo ponto-a-ponto por rota',
            '4_📆_Projecao_e_Breakeven': 'Projeção de longo prazo e breakeven',
            '5_⚙️_Configuracoes': 'Parâmetros e configurações'
        },
        'en': {
            '1_📈_Estimativa_de_Lucro': 'Monthly profitability analysis with charter',
            '2_📊_Breakdown_de_Custos': 'Own management vs Amaro comparison',
            '3_✈️_Simulador_de_Rotas': 'Point-to-point cost per route',
            '4_📆_Projecao_e_Breakeven': 'Long-term projection and breakeven',
            '5_⚙️_Configuracoes': 'Parameters and settings'
        }
    }
    
    st.markdown("### 📚 Páginas Disponíveis" if lang == 'pt' else "### 📚 Available Pages")
    
    for page_key, description in pages_info[lang].items():
        if page_key.replace('_', ' ') in current_page:
            icon = "👉"
            style = "font-weight: 600; color: #8C1D40;"
        else:
            icon = "📄"
            style = "color: #6B7280;"
            
        st.markdown(f"{icon} <span style='{style}'>{description}</span>", 
                   unsafe_allow_html=True)