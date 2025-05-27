"""
Componente de cabeçalho corrigido e simplificado
"""

import streamlit as st
from config.idiomas import get_text

def render_header(lang='pt'):
    """
    Renderiza o cabeçalho principal - versão corrigida
    """
    st.markdown(f"""
    <div class="main-header">
        <h1>✈️ {get_text('app_title', lang)}</h1>
        <p>{get_text('app_subtitle', lang)}</p>
    </div>
    """, unsafe_allow_html=True)

def render_page_header(title, subtitle=None, lang='pt'):
    """
    Renderiza cabeçalho da página - versão simplificada
    """
    # Traduzir título se necessário
    if isinstance(title, str) and not title.startswith('<'):
        title_text = get_text(title, lang)
    else:
        title_text = title
    
    # HTML simplificado e bem formado
    header_html = f"""
    <div style="
        background: #F8F9FA;
        padding: 1.5rem;
        margin: -1rem -1rem 2rem -1rem;
        border-left: 4px solid #8C1D40;
        border-radius: 0 8px 8px 0;
    ">
        <h2 style="color: #8C1D40; margin: 0; font-size: 1.5rem;">{title_text}</h2>
    """
    
    if subtitle:
        if isinstance(subtitle, str):
            subtitle_text = get_text(subtitle, lang) if not subtitle.startswith('<') else subtitle
        else:
            subtitle_text = str(subtitle)
        
        header_html += f"""
        <p style="color: #6B7280; margin: 0.5rem 0 0 0; font-size: 1rem;">{subtitle_text}</p>
        """
    
    header_html += "</div>"
    
    st.markdown(header_html, unsafe_allow_html=True)