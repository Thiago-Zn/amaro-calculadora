"""
Tema claro Amaro Aviation (Streamlit ≥ 1.30)
"""

import streamlit as st

def load_theme():
    st.markdown(
        """
<style>
/* 1. Fundo sempre branco */
html, body, [data-testid="stAppViewContainer"]{
    background:#FFFFFF !important;
    color:#1F2937;
    font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
}

/* 2. Sidebar cinza-claro */
section[data-testid="stSidebar"]{
    background:#F8F9FA !important;
}

/* 3. Header principal */
.main-header{
    background:linear-gradient(135deg,#8C1D40 0%,#A02050 100%);
    color:#FFF; padding:2rem;
    margin:-1rem -1rem 2rem -1rem;
    text-align:center; border-radius:0 0 12px 12px;
}
.main-header h1{margin:0;font-weight:600;font-size:2rem}
.main-header p {margin:.5rem 0 0;font-size:1rem;opacity:.9}

/* 4. Botões */
.stButton>button{
    background:#8C1D40!important; color:#FFF!important;
    border:0!important; border-radius:6px!important;
    padding:.5rem 1rem!important; font-weight:500;
}
.stButton>button:hover{background:#A02050!important}

/* 5. Tabs */
[data-testid="stTabs"] [role="tablist"]{
    background:#F8F9FA; border-radius:8px; padding:.25rem;
}
[data-testid="stTabs"] [aria-selected="true"]{
    background:#8C1D40; color:#FFF;
}

/* 6. Métricas simples */
.metric-card{
    background:#FFF; border:1px solid #E5E7EB;
    border-radius:8px; padding:1.5rem; margin:1rem 0;
    box-shadow:0 2px 4px rgba(0,0,0,.05);
}
.metric-card-value{font-size:1.5rem;font-weight:600;color:#8C1D40}
.metric-card-label{font-size:.875rem;color:#6B7280;font-weight:500}

/* 7. Esconde menu padrão */
#MainMenu,header,footer{visibility:hidden}
</style>
        """,
        unsafe_allow_html=True,
    )
