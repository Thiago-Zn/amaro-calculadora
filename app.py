import streamlit as st
from PIL import Image, UnidentifiedImageError
from PIL import Image
from pathlib import Path

# Configuração geral da aplicação
st.set_page_config(
    page_title="Amaro Aviation - Calculadora",
    page_icon="🛩️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Caminho da logo
logo_path = Path("assets/logo_amaro.png")

with st.sidebar:
    try:
        if logo_path.exists():
            logo = Image.open(logo_path)
            st.image(logo, use_column_width=True)
        else:
            st.warning("Logo não encontrada em assets/logo_amaro.png")
    except UnidentifiedImageError:
        st.warning("Arquivo de logo inválido. Use uma imagem .png válida.")

# Barra lateral com logo e menu
with st.sidebar:
    if logo_path.exists():
        logo = Image.open(logo_path)
        st.image(logo, use_column_width=True)
    else:
        st.warning("Logo não encontrada em: assets/logo_amaro.png")

    st.markdown("## Bem-vindo à Calculadora Amaro Aviation")
    st.markdown(
        "Use o menu lateral para navegar entre as funcionalidades:\n\n"
        "- ✈️ Custo por Trecho\n"
        "- 📈 Lucros Mensais\n"
        "- 🎯 Meta de Receita\n"
        "- 📊 Comparativo de Economia\n"
        "- ⚙️ Configurações Internas\n"
        "- 🧾 Modo Cliente\n"
    )
    st.markdown("---")
    st.markdown("Versão interna • Uso exclusivo da equipe Amaro Aviation")
