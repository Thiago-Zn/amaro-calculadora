import streamlit as st
# Presume que estas funções existem no seu projeto e funcionam como esperado.
# Se elas não existirem, você precisará criá-las ou adaptar o código.
try:
    from config.idiomas import get_text, detect_language_from_selection
except ImportError:
    # Fallback simples se o módulo de idiomas não for encontrado (para teste)
    print("Aviso: Módulo config.idiomas não encontrado. Usando fallbacks para get_text e detect_language_from_selection.")
    def get_text(key: str, lang: str) -> str:
        if key == 'language':
            return "Idioma / Language" if lang == 'pt' else "Language"
        return key.replace('_', ' ').title()

    def detect_language_from_selection(selection: str) -> str:
        if "Português" in selection or "Portuguese" in selection :
            return 'pt'
        return 'en'

# --- Constantes de Cores para Consistência ---
AMARO_BORDO = "#8C1D40"
AMARO_BRANCO = "#FFFFFF"
TEXTO_ESCURO_SELECT = "#1F2937"
FUNDO_BRANCO_SELECT = "#FFFFFF"
FUNDO_HOVER_SELECT_ITEM = "#F6F7FA" # Cinza bem claro para hover de item
BORDA_SELECT = "#DADDE1" # Cinza claro para bordas
BORDA_SELECT_FOCUS = "#731734" # Bordô mais escuro para foco
BOX_SHADOW_SELECT_FOCUS = "rgba(140,29,64,0.2)" # Sombra suave para foco

def render_sidebar_amaro(current_lang: str = 'pt') -> str:
    """
    Renderiza a sidebar da Amaro Aviation com cabeçalho estilizado e 
    um seletor de idioma legível.

    Args:
        current_lang (str): O idioma atualmente selecionado (ex: 'pt' ou 'en').

    Returns:
        str: O código do idioma selecionado pelo usuário (ex: 'pt' ou 'en').
    """
    _apply_sidebar_styling()

    with st.sidebar:
        # 1. Cabeçalho da Sidebar
        st.markdown(
            f"""
            <div style="text-align:center; padding:1rem 0.5rem; margin-bottom:1rem;">
                <h3 style="color:{AMARO_BRANCO}; margin:0; font-size: 1.25rem;">✈️ Amaro Aviation</h3>
                <p style="color:{AMARO_BRANCO}; font-size:0.875rem; margin-top:0.25rem;">
                    Simulador Estratégico de Custos
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 2. Seletor de Idioma
        label_idioma = get_text('language', current_lang)
        opcoes_idioma = ["🇧🇷 Português", "🇺🇸 English"]
        
        # Determina o índice com base no current_lang
        try:
            current_display_value = next(opt for opt in opcoes_idioma if detect_language_from_selection(opt) == current_lang)
            indice_selecionado = opcoes_idioma.index(current_display_value)
        except StopIteration:
            indice_selecionado = 0 # Default para Português se não encontrar

        selected_language_display = st.selectbox(
            label_idioma,
            opcoes_idioma,
            index=indice_selecionado,
            key="language_selector_amaro" # Chave única e específica
        )
        
        return detect_language_from_selection(selected_language_display)

def _apply_sidebar_styling() -> None:
    """
    Injeta CSS para estilizar a sidebar da Amaro Aviation, com foco especial
    na legibilidade do st.selectbox (seletor de idioma).
    """
    st.markdown(
        f"""
        <style>
            /* === CONFIGURAÇÕES GERAIS DA SIDEBAR === */
            section[data-testid="stSidebar"] > div:first-child {{ /* Aplica ao container principal da sidebar */
                background-color: {AMARO_BORDO} !important;
            }}

            /* Oculta header/footer padrão do Streamlit, se desejado */
            #MainMenu, header, footer {{
                visibility: hidden !important;
            }}

            /* === ESTILOS PARA O st.selectbox (SELETOR DE IDIOMA) === */

            /* 1. Label do selectbox (ex: "Idioma / Language") */
            section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p {{ /* Seletor comum para o texto do label */
                color: {AMARO_BRANCO} !important;
                font-size: 0.9rem !important; /* Tamanho do label */
                font-weight: 500 !important;
                margin-bottom: 0.2rem !important; /* Espaço abaixo do label */
            }}
            /* Fallback se o seletor acima não funcionar para o seu caso específico */
            section[data-testid="stSidebar"] label[for*="language_selector_amaro"] {{
                 color: {AMARO_BRANCO} !important;
                 font-size: 0.9rem !important;
                 font-weight: 500 !important;
                 margin-bottom: 0.2rem !important;
            }}

            /* 2. Caixa principal do selectbox (onde o valor selecionado aparece) */
            section[data-testid="stSidebar"] div[data-baseweb="select"] > div:first-child {{
                background-color: {FUNDO_BRANCO_SELECT} !important;
                color: {TEXTO_ESCURO_SELECT} !important; /* Texto escuro no campo */
                border: 1px solid {BORDA_SELECT} !important;
                border-radius: 6px !important;
                padding-top: 0.30rem !important; /* Ajustes finos de padding */
                padding-bottom: 0.30rem !important;
                padding-left: 0.65rem !important;
                font-size: 0.875rem !important;
            }}

            /* 3. Seta (ícone dropdown) do selectbox */
            section[data-testid="stSidebar"] div[data-baseweb="select"] svg {{
                fill: {TEXTO_ESCURO_SELECT} !important; /* Seta escura */
            }}

            /* 4. Hover/Focus na caixa principal do selectbox */
            section[data-testid="stSidebar"] div[data-baseweb="select"] > div:first-child:hover,
            section[data-testid="stSidebar"] div[data-baseweb="select"] > div:first-child:focus-within {{
                border-color: {BORDA_SELECT_FOCUS} !important;
                box-shadow: 0 0 0 2px {BOX_SHADOW_SELECT_FOCUS} !important;
            }}

            /* === ESTILOS PARA O DROPDOWN (LISTA DE OPÇÕES) === */
            /* O dropdown (popover) é renderizado fora da árvore DOM da sidebar. */
            
            /* 5. Container do dropdown (popover) */
            /* Este seletor mira o popover que é usado pelo selectbox. */
            div[data-baseweb="popover"][role="listbox"] {{ 
                 background-color: {FUNDO_BRANCO_SELECT} !important;
                 border: 1px solid {BORDA_SELECT} !important;
                 border-radius: 6px !important;
                 box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important; /* Sombra sutil no dropdown */
            }}

            /* 6. Itens individuais (<li>) dentro do dropdown */
            div[data-baseweb="popover"] ul[role="listbox"] li[role="option"] {{
                padding: 0.5rem 0.75rem !important;
                color: {TEXTO_ESCURO_SELECT} !important;    /* COR DO TEXTO DA OPÇÃO */
                background-color: {FUNDO_BRANCO_SELECT} !important; /* FUNDO DA OPÇÃO */
                font-size: 0.875rem !important;
                line-height: 1.4 !important;
            }}

            /* 7. Hover sobre um item do dropdown */
            div[data-baseweb="popover"] ul[role="listbox"] li[role="option"]:hover {{
                background-color: {FUNDO_HOVER_SELECT_ITEM} !important;
                color: {TEXTO_ESCURO_SELECT} !important; /* Mantém texto escuro no hover */
            }}
            
            /* 8. Item atualmente selecionado DENTRO DO DROPDOWN (quando aberto) */
            div[data-baseweb="popover"] ul[role="listbox"] li[aria-selected="true"] {{
                background-color: {AMARO_BORDO} !important; 
                color: {AMARO_BRANCO} !important; 
            }}
            div[data-baseweb="popover"] ul[role="listbox"] li[aria-selected="true"]:hover {{
                background-color: {BORDA_SELECT_FOCUS} !important; /* Bordô mais escuro no hover do selecionado */
                color: {AMARO_BRANCO} !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )