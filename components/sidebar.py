# components/sidebar.py
import streamlit as st

# ---------------------------------------------------------------------
# 1. Fallback para o módulo de internacionalização
# ---------------------------------------------------------------------
try:
    from config.idiomas import get_text, detect_language_from_selection
except ImportError:
    print("AVISO: Módulo config.idiomas não encontrado. Usando fallbacks.")
    def get_text(key: str, lang: str) -> str:
        if key == "language":
            return "Idioma / Language"
        return key.replace("_", " ").title()

    def detect_language_from_selection(selection: str) -> str:
        if "Português" in selection:
            return "pt"
        return "en"

# ---------------------------------------------------------------------
# 2. Paleta oficial Amaro
# ---------------------------------------------------------------------
AMARO_BORDO  = "#8C1D40"
AMARO_BRANCO = "#FFFFFF"
AMARO_PRETO  = "#000000"

LANGUAGE_SELECTOR_KEY = "amaro_language_selector_sidebar"

# ---------------------------------------------------------------------
# 3. Função principal (novo nome)
# ---------------------------------------------------------------------
def render_sidebar_amaro_simplified(current_lang: str = "pt") -> str:
    _inject_css()

    with st.sidebar:
        # Cabeçalho
        st.markdown(
            f"""
            <div style="text-align:center; padding:1rem 0.5rem; margin-bottom:1rem;">
                <h3 style="color:{AMARO_BRANCO}; margin:0; font-size:1.25rem; font-weight:600;">
                    ✈️ Amaro Aviation
                </h3>
                <p style="color:{AMARO_BRANCO}; font-size:0.875rem; margin-top:0.35rem; opacity:0.9;">
                    Simulador Estratégico de Custos
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Seletor de idioma
        label = get_text("language", current_lang)
        opcoes = ["🇧🇷 Português", "🇺🇸 English"]

        try:
            display_atual = next(opt for opt in opcoes
                                 if detect_language_from_selection(opt) == current_lang)
            idx = opcoes.index(display_atual)
        except StopIteration:
            idx = 0

        selecionado = st.selectbox(
            label,
            opcoes,
            index=idx,
            key=LANGUAGE_SELECTOR_KEY,
        )
        return detect_language_from_selection(selecionado)

# ---------------------------------------------------------------------
# 4. Alias para manter compatibilidade com páginas antigas
# ---------------------------------------------------------------------
render_sidebar = render_sidebar_amaro_simplified  # noqa: E305
# ---------------------------------------------------------------------
# 5. CSS   (versão definitiva – só bordô, branco e preto)
# ---------------------------------------------------------------------
def _inject_css() -> None:
    """Injeta a folha de estilos da sidebar Amaro (paleta bordô/branco/preto)."""
    st.markdown(
        f"""
        <style>
        /* ===== 1. CONTAINER DA SIDEBAR ===== */
        section[data-testid="stSidebar"] > div:first-child {{
            background: {AMARO_BORDO} !important;
        }}

        /* ===== 2. LABEL DO SELECTBOX ===== */
        section[data-testid="stSidebar"] label[for*='{LANGUAGE_SELECTOR_KEY}'] {{
            color: {AMARO_BRANCO} !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            margin-bottom: 0.25rem !important;
        }}

        /* ===== 3. SELECTBOX FECHADO ===== */
        section[data-testid="stSidebar"] div[data-testid="stSelectbox"] {
            background: transparent !important;
            padding: 0 !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child {
            background: rgba(255, 255, 255, 0.9) !important;
            color: #333333 !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 6px !important;
            padding: 0.4rem 0.75rem !important;
            font-size: 0.875rem !important;
        }
        section[data-testid="stSidebar"] div[data-testid="stSelectbox"] svg {
            fill: #333333 !important;
        }

        /* ===== 4. DROPDOWN / POPOVER ===== */
        /* regra no elemento-raiz e em *todos* os descendentes p/ anular tema escuro */
        div[data-baseweb="popover"][role="listbox"],
        div[data-baseweb="popover"][role="listbox"] * {
            background: rgba(255, 255, 255, 0.95) !important;
            color: #333333 !important;
        }

        /* itens individuais: mantêm padding e fonte */
        div[data-baseweb="popover"][role="listbox"] [role="option"] {
            padding: 0.5rem 0.85rem !important;
            font-size: 0.875rem !important;
        }

        /* hover ou item selecionado */
        div[data-baseweb="popover"][role="listbox"] [role="option"]:hover,
        div[data-baseweb="popover"][role="listbox"] [role="option"][aria-selected="true"],
        div[data-baseweb="popover"][role="listbox"] [role="option"]:hover *,
        div[data-baseweb="popover"][role="listbox"] [role="option"][aria-selected="true"] * {
            background: #8C1D40 !important;
            color: #FFFFFF !important;
        }

        /* ===== 5. ESCONDE HEADER/FOOTER PADRÕES ===== */
        #MainMenu, header, footer {{ visibility: hidden !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )
