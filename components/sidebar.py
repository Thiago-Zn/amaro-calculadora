import streamlit as st

# Tenta importar funções de internacionalização do projeto.
# Se não encontrar, usa implementações de fallback para permitir
# que o componente seja testado ou usado de forma isolada.
try:
    from config.idiomas import get_text, detect_language_from_selection
except ImportError:
    print("AVISO: Módulo config.idiomas não encontrado. Usando fallbacks.")
    def get_text(key: str, lang: str) -> str:
        """Fallback para obter texto traduzido."""
        if key == 'language':
            return "Idioma / Language" # Label padrão
        return key.replace('_', ' ').title()

    def detect_language_from_selection(selection: str) -> str:
        """Fallback para detectar código de idioma a partir da seleção."""
        if "Português" in selection or "Portuguese" in selection:
            return 'pt'
        return 'en'

# --- Constantes de Cores Oficiais Amaro Aviation ---
AMARO_BORDO = "#8C1D40"
AMARO_BRANCO = "#FFFFFF"
AMARO_PRETO = "#000000" # Preto para texto sobre fundo branco

# --- Constantes para Nomes de Chave e Seletores (para consistência) ---
LANGUAGE_SELECTOR_KEY = "amaro_language_selector_sidebar"

def render_sidebar_amaro_simplified(current_lang: str = 'pt') -> str:
    """
    Renderiza a sidebar da Amaro Aviation com cabeçalho estilizado e
    um seletor de idioma legível, utilizando apenas as cores
    preto, branco e bordô.

    Args:
        current_lang (str): O idioma atualmente selecionado (ex: 'pt' ou 'en').

    Returns:
        str: O código do idioma selecionado pelo usuário (ex: 'pt' ou 'en').
    """
    _inject_simplified_sidebar_css()

    with st.sidebar:
        # 1. Cabeçalho da Sidebar
        st.markdown(
            f"""
            <div style="text-align:center; padding: 1rem 0.5rem; margin-bottom:1rem;">
                <h3 style="color:{AMARO_BRANCO}; margin:0; font-size: 1.25rem; font-weight: 600;">✈️ Amaro Aviation</h3>
                <p style="color:{AMARO_BRANCO}; font-size:0.875rem; margin-top:0.35rem; opacity: 0.9;">
                    Simulador Estratégico de Custos
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 2. Seletor de Idioma
        label_idioma = get_text('language', current_lang)
        opcoes_idioma = ["🇧🇷 Português", "🇺🇸 English"]
        
        # Determina o índice inicial com base no current_lang
        try:
            # Procura a opção de display que corresponde ao código de idioma atual
            current_display_value = next(
                opt for opt in opcoes_idioma 
                if detect_language_from_selection(opt) == current_lang
            )
            indice_selecionado = opcoes_idioma.index(current_display_value)
        except StopIteration:
            # Se não encontrar correspondência (ex: current_lang é inválido), usa o primeiro item
            indice_selecionado = 0 

        selected_language_display = st.selectbox(
            label_idioma,
            opcoes_idioma,
            index=indice_selecionado,
            key=LANGUAGE_SELECTOR_KEY # Chave única e específica para o CSS
        )
        
        return detect_language_from_selection(selected_language_display)

def _inject_simplified_sidebar_css() -> None:
    """
    Injeta CSS para estilizar a sidebar da Amaro Aviation,
    com foco na legibilidade do st.selectbox (seletor de idioma)
    usando apenas as cores preto, branco e bordô.
    """
    st.markdown(
        f"""
        <style>
            /* === CONFIGURAÇÕES GERAIS DA SIDEBAR === */
            section[data-testid="stSidebar"] > div:first-child {{
                background-color: {AMARO_BORDO} !important;
            }}

            /* Oculta header/footer padrão do Streamlit, se desejado */
            #MainMenu, header, footer {{
                visibility: hidden !important;
            }}

            /* === ESTILOS PARA O st.selectbox (SELETOR DE IDIOMA) === */

            /* 1. Label do selectbox (ex: "Idioma / Language") */
            /* O seletor `label[for*='{LANGUAGE_SELECTOR_KEY}']` é mais robusto */
            section[data-testid="stSidebar"] label[for*='{LANGUAGE_SELECTOR_KEY}'] {{
                color: {AMARO_BRANCO} !important;
                font-size: 0.875rem !important;
                font-weight: 500 !important;
                margin-bottom: 0.25rem !important; /* Espaço abaixo do label */
            }}
            /* Fallback para o parágrafo dentro do label, se o seletor acima não pegar */
            section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p {{
                color: {AMARO_BRANCO} !important;
            }}


            /* 2. Caixa principal do selectbox (onde o valor selecionado aparece) */
            section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child {{
                background-color: {AMARO_BRANCO} !important;
                color: {AMARO_PRETO} !important; /* Texto preto no campo */
                border: 1px solid {AMARO_BORDO} !important; /* Borda bordô */
                border-radius: 6px !important;
                padding-top: 0.4rem !important; 
                padding-bottom: 0.4rem !important;
                padding-left: 0.75rem !important;
                font-size: 0.875rem !important;
            }}

            /* 3. Seta (ícone dropdown) do selectbox */
            section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] svg {{
                fill: {AMARO_PRETO} !important; /* Seta preta */
            }}

            /* 4. Hover/Focus na caixa principal do selectbox */
            section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child:hover,
            section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child:focus-within {{
                border-color: {AMARO_BORDO} !important; /* Mantém borda bordô */
                /* Opcional: adicionar um box-shadow sutil se desejar, mas usando cores da paleta */
                /* box-shadow: 0 0 0 2px rgba(140, 29, 64, 0.25) !important; */
            }}

            /* === ESTILOS PARA O DROPDOWN (LISTA DE OPÇÕES SUSPENSAS) === */
            /* O dropdown (popover) é renderizado fora da árvore DOM da sidebar. */
            
            /* 5. Container do dropdown (popover) */
            div[data-baseweb="popover"][role="listbox"] {{ 
                 background-color: {AMARO_BRANCO} !important; /* Fundo branco */
                 border: 1px solid {AMARO_BORDO} !important; /* Borda bordô */
                 border-radius: 6px !important;
                 box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important; 
            }}

            /* 6. Itens individuais (<li>) dentro do dropdown */
            div[data-baseweb="popover"] ul[role="listbox"] li[role="option"] {{
                padding: 0.5rem 0.85rem !important;
                color: {AMARO_PRETO} !important;    /* Texto preto na opção */
                background-color: {AMARO_BRANCO} !important; /* Fundo branco na opção */
                font-size: 0.875rem !important;
                line-height: 1.4 !important;
            }}

            /* 7. Hover sobre um item do dropdown */
            div[data-baseweb="popover"] ul[role="listbox"] li[role="option"]:hover {{
                background-color: {AMARO_BORDO} !important; /* Fundo bordô no hover */
                color: {AMARO_BRANCO} !important; /* Texto branco no hover */
            }}
            
            /* 8. Item atualmente selecionado DENTRO DO DROPDOWN (quando aberto) */
            /* Geralmente, Streamlit aplica um estilo próprio para o item selecionado. */
            /* Este estilo garante consistência com o hover. */
            div[data-baseweb="popover"] ul[role="listbox"] li[aria-selected="true"] {{
                background-color: {AMARO_BORDO} !important; 
                color: {AMARO_BRANCO} !important; 
            }}
            /* Para garantir que o hover no item selecionado não mude a aparência */
            div[data-baseweb="popover"] ul[role="listbox"] li[aria-selected="true"]:hover {{
                background-color: {AMARO_BORDO} !important; 
                color: {AMARO_BRANCO} !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )