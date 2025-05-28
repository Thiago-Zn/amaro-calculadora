"""
Sidebar DEFINITIVO com sistema de idioma funcionando
Integrado com tradução e persistência
"""

import streamlit as st

# Importar sistema de tradução corrigido
try:
    from config.idiomas import get_text, detect_language_from_selection, get_language_options, get_current_language_display
    from utils.session_state import persistent_selectbox
except ImportError:
    # Fallback se importação falhar
    def get_text(key, lang='pt'):
        return key.replace("_", " ").title()
    
    def detect_language_from_selection(selection):
        return 'pt' if '🇧🇷' in selection or 'Português' in selection else 'en'
    
    def get_language_options():
        return ["🇧🇷 Português", "🇺🇸 English"]
    
    def get_current_language_display(lang):
        return "🇧🇷 Português" if lang == 'pt' else "🇺🇸 English"

def render_sidebar(default_lang='pt'):
    """
    Sidebar DEFINITIVO com seleção de idioma funcionando
    
    Args:
        default_lang: Idioma padrão caso não haja seleção
    
    Returns:
        str: Código do idioma selecionado ('pt' ou 'en')
    """
    
    # CSS para sidebar limpa e funcional
    st.markdown("""
    <style>
    /* === SIDEBAR AMARO AVIATION === */
    section[data-testid="stSidebar"] {
        background: #8C1D40 !important;
        border-right: none !important;
    }
    
    section[data-testid="stSidebar"] > div:first-child {
        background: #8C1D40 !important;
        padding: 2rem 1rem !important;
    }
    
    /* === HEADER DA SIDEBAR === */
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 1rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid rgba(255,255,255,0.2);
    }
    
    .sidebar-logo {
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .sidebar-tagline {
        color: rgba(255,255,255,0.9);
        font-size: 0.875rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* === SELETOR DE IDIOMA FUNCIONAL === */
    section[data-testid="stSidebar"] .stSelectbox {
        margin: 1.5rem 0 !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        margin-bottom: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    /* Caixa do seletor - BRANCA e LEGÍVEL */
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: white !important;
        color: #333333 !important;
        border: 2px solid white !important;
        border-radius: 10px !important;
        padding: 1rem 1.25rem !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        min-height: 48px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        transition: all 0.2s ease !important;
    }
    
    /* Hover effect */
    section[data-testid="stSidebar"] .stSelectbox > div > div:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.2) !important;
    }
    
    /* Seta do seletor */
    section[data-testid="stSidebar"] .stSelectbox svg {
        fill: #333333 !important;
        width: 18px !important;
        height: 18px !important;
    }
    
    /* === DROPDOWN FUNCIONAL === */
    div[data-baseweb="popover"][role="listbox"] {
        background: white !important;
        border: 2px solid #8C1D40 !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2) !important;
        padding: 0.5rem 0 !important;
        min-width: 200px !important;
    }
    
    /* Opções do dropdown */
    div[data-baseweb="popover"] [role="option"] {
        background: white !important;
        color: #333333 !important;
        padding: 1rem 1.25rem !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        border: none !important;
        margin: 0 0.5rem !important;
        border-radius: 8px !important;
        transition: all 0.15s ease !important;
    }
    
    /* Hover nas opções */
    div[data-baseweb="popover"] [role="option"]:hover {
        background: #F8F9FA !important;
        color: #8C1D40 !important;
        transform: translateX(4px) !important;
    }
    
    /* Opção selecionada */
    div[data-baseweb="popover"] [role="option"][aria-selected="true"] {
        background: #8C1D40 !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* === FOOTER DA SIDEBAR === */
    .sidebar-footer {
        position: absolute;
        bottom: 2rem;
        left: 1rem;
        right: 1rem;
        text-align: center;
        border-top: 1px solid rgba(255,255,255,0.2);
        padding-top: 1rem;
    }
    
    .sidebar-footer p {
        color: rgba(255,255,255,0.7) !important;
        font-size: 0.75rem !important;
        margin: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # Header da sidebar
        st.markdown("""
        <div class="sidebar-header">
            <h1 class="sidebar-logo">✈️ Amaro Aviation</h1>
            <p class="sidebar-tagline">Simulador Estratégico de Custos</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ============================================================
        # SELEÇÃO DE IDIOMA COM PERSISTÊNCIA
        # ============================================================
        
        # Obter idioma atual do session_state ou usar padrão
        current_lang = st.session_state.get('selected_language', default_lang)
        
        # Opções de idioma
        language_options = get_language_options()
        
        # Determinar seleção atual
        try:
            current_display = get_current_language_display(current_lang)
            if current_display in language_options:
                current_index = language_options.index(current_display)
            else:
                current_index = 0
        except:
            current_index = 0
        
        # Selectbox de idioma
        selected_display = persistent_selectbox(
            get_text("language", current_lang),
            options=language_options,
            index=current_index,
            key="language_selector_sidebar"
        )
        
        # Detectar idioma selecionado
        selected_lang = detect_language_from_selection(selected_display)
        
        # Atualizar session_state se mudou
        if selected_lang != current_lang:
            st.session_state['selected_language'] = selected_lang
            # Forçar rerun para aplicar nova tradução
            st.rerun()
        
        # Espaço para separar conteúdo
        st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
        
        # ============================================================
        # INFORMAÇÕES DO SISTEMA (OPCIONAL)
        # ============================================================
        
        # Mostrar informações sobre a página atual (se desejar)
        try:
            # Detectar página atual baseada na URL ou session_state
            current_page = st.session_state.get('current_page', 'Principal')
            
            st.markdown(f"""
            <div style="color: rgba(255,255,255,0.8); font-size: 0.8rem; text-align: center; margin: 1rem 0;">
                <p>📍 Página: {current_page}</p>
            </div>
            """, unsafe_allow_html=True)
            
        except:
            pass  # Ignorar se não conseguir detectar página
        
        # ============================================================
        # FOOTER DA SIDEBAR
        # ============================================================
        st.markdown("""
        <div class="sidebar-footer">
            <p>v3.0 • Sistema Corrigido</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Retornar idioma selecionado
    return selected_lang

def set_current_page(page_name):
    """Função para definir página atual (opcional)"""
    st.session_state['current_page'] = page_name

def get_current_language():
    """Função utilitária para obter idioma atual"""
    return st.session_state.get('selected_language', 'pt')

def reset_language_selection():
    """Reset da seleção de idioma (para debug)"""
    if 'selected_language' in st.session_state:
        del st.session_state['selected_language']
    if 'language_selector_sidebar' in st.session_state:
        del st.session_state['language_selector_sidebar']

# Teste da função se executado diretamente
if __name__ == "__main__":
    print("🧪 Testando sidebar...")
    
    # Simular session_state
    class MockSessionState:
        def __init__(self):
            self.data = {}
        
        def get(self, key, default=None):
            return self.data.get(key, default)
        
        def __setitem__(self, key, value):
            self.data[key] = value
        
        def __contains__(self, key):
            return key in self.data
    
    # Mock st.session_state
    st.session_state = MockSessionState()
    
    # Testar detecção de idioma
    assert detect_language_from_selection("🇧🇷 Português") == 'pt'
    assert detect_language_from_selection("🇺🇸 English") == 'en'
    assert detect_language_from_selection("Qualquer coisa") == 'pt'
    
    print("✅ Sidebar funcionando corretamente!")