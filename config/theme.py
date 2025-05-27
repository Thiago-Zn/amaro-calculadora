"""
config/theme.py

Tema Claro Amaro Aviation – Compatível com Streamlit ≥ 1.30
"""

import streamlit as st

def load_theme() -> None:
    """Injeta o CSS corporativo enxuto e definitivo."""
    st.markdown(
        """
<style>
  /* === Variáveis de cor === */
  :root {
    --amaro-bordo: #8C1D40;
    --amaro-bordo-escuro: #A02050;
    --amaro-branco: #FFFFFF;
    --amaro-cinza-texto: #1F2937;
    --amaro-cinza-fundo: #F8F9FA;
    --amaro-cinza-borda: #E5E7EB;
  }

  /* 1) Corpo e fonte globais */
  html, body, [data-testid="stAppViewContainer"] {
    background: var(--amaro-branco) !important;
    color:      var(--amaro-cinza-texto) !important;
    font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif!important;
  }

  /* 2) Sidebar – fundo bordô, texto branco */
  section[data-testid="stSidebar"] {
    background: var(--amaro-bordo) !important;
    color: var(--amaro-branco)   !important;
  }
  /* Links (páginas) na sidebar */
  section[data-testid="stSidebar"] a {
    color: var(--amaro-branco) !important;
    padding: 0.5rem;
    border-radius: 6px;
    transition: background 0.2s, box-shadow 0.2s;
  }
  section[data-testid="stSidebar"] a:hover {
    background: var(--amaro-bordo-escuro) !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  }
  /* Item ativo */
  section[data-testid="stSidebar"] a[aria-current="page"] {
    background: var(--amaro-bordo-escuro) !important;
    font-weight: 600;
  }

  /* 3) Header principal – gradiente bordô + texto branco */
  .main-header {
    background:    linear-gradient(135deg, var(--amaro-bordo), var(--amaro-bordo-escuro)) !important;
    color:         var(--amaro-branco) !important;
    padding:       2rem !important;
    margin:        -1rem -1rem 2rem -1rem !important;
    text-align:    center !important;
    border-radius: 0 0 12px 12px !important;
  }
  .main-header h1, .main-header p {
    color: var(--amaro-branco) !important;
  }

  /* 4) Botões bordô */
  .stButton>button {
    background: var(--amaro-bordo) !important;
    color:      var(--amaro-branco) !important;
    border-radius: 6px !important;
    padding: 0.5rem 1rem !important;
    text-transform: uppercase !important;
  }
  .stButton>button:hover {
    background: var(--amaro-bordo-escuro) !important;
  }

  /* 5) Tabs */
  [data-testid="stTabs"] [role="tablist"] {
    background: var(--amaro-cinza-fundo) !important;
    border-radius: 8px !important;
    padding: 0.2rem !important;
  }
  [data-testid="stTabs"] [aria-selected="true"] {
    background: var(--amaro-bordo) !important;
    color: var(--amaro-branco) !important;
  }

  /* 6) Cards e containers */
  .card-style {
    background: var(--amaro-branco) !important;
    border: 1px solid var(--amaro-cinza-borda) !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
    margin-bottom: 1rem !important;
  }

  /* 7) Esconder menu e rodapé padrão */
  #MainMenu, header, footer {
    visibility: hidden !important;
  }
</style>
        """,
        unsafe_allow_html=True
    )
