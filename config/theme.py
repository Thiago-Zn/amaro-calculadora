"""
config/theme.py
Tema Amaro Aviation ― inspirado no site oficial
"""

import streamlit as st

def load_theme() -> None:
    st.markdown(
        """
<style>
/* === Paleta === */
:root{
  --bordo:#8C1D40;
  --bordo-light:#A02050;
  --bordo-dark:#731734;
  --grafite:#424242;
  --white:#FFFFFF;
  --gray-text:#1F2937;
  --gray-bg:#F4F4F4;
  --gray-border:#D6D6D6;
}

/* === Corpo === */
html,body,[data-testid="stAppViewContainer"]{
  background:var(--white)!important;
  color:var(--gray-text)!important;
  font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif!important;
}

/* === Sidebar === */
section[data-testid="stSidebar"]{
  background:var(--bordo)!important;
  color:var(--white)!important;
}
section[data-testid="stSidebar"] *{
  color:var(--white)!important;
}
section[data-testid="stSidebar"] a{
  padding:.5rem .9rem;
  border-radius:6px;
  transition:background .2s,box-shadow .2s;
}
section[data-testid="stSidebar"] a:hover{
  background:var(--bordo-light)!important;
  box-shadow:0 2px 6px rgba(0,0,0,.25);
}
section[data-testid="stSidebar"] a[aria-current="page"]{
  background:var(--bordo-dark)!important;
  font-weight:600;
}

/* === Header (barra preta do site) === */
[data-testid="stHeader"]{
  background:var(--grafite)!important;
  color:var(--white)!important;
}

/* === Botões === */
.stButton>button{
  background:var(--bordo)!important;
  color:var(--white)!important;
  border:1px solid var(--bordo);
  border-radius:6px!important;
  padding:.45rem 1.2rem!important;
  text-transform:uppercase;
  font-weight:600;
}
.stButton>button:hover{
  background:var(--bordo-light)!important;
}

/* === Tabs === */
[data-testid="stTabs"] [role="tablist"]{
  background:var(--gray-bg);
  border-radius:8px;
  padding:.2rem;
}
[data-testid="stTabs"] [data-baseweb="tab"]{
  background:transparent;
  color:var(--gray-text);
  padding:.55rem 1rem;
  border-radius:6px;
  transition:background .2s;
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover{
  background:var(--gray-bg);
}
[data-testid="stTabs"] [aria-selected="true"]{
  background:var(--bordo);
  color:var(--white);
  font-weight:600;
}

/* === Card utilitário (classe opcional `card-style`) === */
.card-style{
  background:var(--white);
  border:1px solid var(--gray-border);
  border-radius:8px;
  padding:1rem;
  box-shadow:0 1px 3px rgba(0,0,0,.05);
}

/* ==== Esconder menu/rodapé === */
header,footer,#MainMenu{visibility:hidden}
/* === Correção de contraste na sidebar === */
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] svg{
  color: #FFFFFF !important;
  fill : #FFFFFF !important;
}
/* ícone / texto do item ativo já ficam bordô-escuro de fundo;
   mantenha o texto branco: */
section[data-testid="stSidebar"] a[aria-current="page"] *,
section[data-testid="stSidebar"] a:hover *{
  color:#FFFFFF !important;
  fill :#FFFFFF !important;
}
.stButton>button{
  color:#FFFFFF !important;
}

</style>
        """,
        unsafe_allow_html=True
    )
