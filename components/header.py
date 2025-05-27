"""
Componente de cabeçalho reutilizável para todas as páginas
"""

import streamlit as st
from config.idiomas import get_text

def render_header(lang='pt'):
    """
    Renderiza o cabeçalho principal da aplicação
    
    Args:
        lang: Idioma ('pt' ou 'en')
    """
    
    st.markdown(f"""
    <div class="main-header">
        <h1>✈️ {get_text('app_title', lang)}</h1>
        <p>{get_text('app_subtitle', lang)}</p>
    </div>
    """, unsafe_allow_html=True)

def render_page_header(title, subtitle=None, lang='pt'):
    """
    Renderiza cabeçalho específico da página
    
    Args:
        title: Título da página
        subtitle: Subtítulo opcional
        lang: Idioma
    """
    
    title_text = get_text(title, lang) if isinstance(title, str) and not title.startswith('<') else title
    
    header_html = f"""
    <div style="
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-left: 4px solid #8C1D40;
        border-radius: 0 8px 8px 0;
    ">
        <h2 style="
            color: #8C1D40;
            margin: 0;
            font-size: 1.8rem;
            font-weight: 600;
        ">{title_text}</h2>
    """
    
    if subtitle:
        subtitle_text = get_text(subtitle, lang) if isinstance(subtitle, str) else subtitle
        header_html += f"""
        <p style="
            color: #6B7280;
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
        ">{subtitle_text}</p>
        """
    
    header_html += "</div>"
    
    st.markdown(header_html, unsafe_allow_html=True)