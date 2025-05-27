# components/header.py - VERSÃO ULTRA SIMPLES

import streamlit as st
from config.idiomas import get_text

def render_header(lang='pt'):
    """Header sem HTML complexo"""
    st.markdown(f"# ✈️ {get_text('app_title', lang)}")
    st.markdown(f"**{get_text('app_subtitle', lang)}**")
    st.markdown("---")

def render_page_header(title, subtitle=None, lang='pt'):
    """Page header simplificado"""
    title_text = get_text(title, lang) if isinstance(title, str) else title
    st.markdown(f"## {title_text}")
    
    if subtitle:
        subtitle_text = get_text(subtitle, lang) if isinstance(subtitle, str) else subtitle
        st.markdown(f"*{subtitle_text}*")
    
    st.markdown("---")

# ========================================

# components/sidebar.py - VERSÃO ULTRA SIMPLES

import streamlit as st
from config.idiomas import get_text, detect_language_from_selection

def render_sidebar(lang='pt'):
    """Sidebar sem HTML complexo"""
    with st.sidebar:
        st.markdown("### ✈️ Amaro Aviation")
        st.markdown("Simulador de Custos")
        st.markdown("---")
        
        # Seleção de idioma
        idioma_selecionado = st.selectbox(
            "Idioma / Language",
            ["🇧🇷 Português", "🇺🇸 English"],
            index=0 if lang == 'pt' else 1,
            key="language_selector"
        )
        
        lang_atual = detect_language_from_selection(idioma_selecionado)
        
        st.markdown("---")
        st.success("✅ Sistema Operacional")
        
        return lang_atual

# ========================================

# components/metrics.py - VERSÃO ULTRA SIMPLES

import streamlit as st
from utils.params import format_currency, format_percentage

def render_metric_card(label, value, delta=None, format_type="currency", lang='pt'):
    """Métrica usando st.metric nativo"""
    if format_type == "currency":
        formatted_value = format_currency(value, lang)
    elif format_type == "percentage":
        formatted_value = format_percentage(value, lang)
    else:
        formatted_value = str(value)
    
    # Usar metric nativo do Streamlit
    if delta is not None:
        st.metric(label, formatted_value, f"{delta:+.1f}%")
    else:
        st.metric(label, formatted_value)

def render_kpi_grid(kpis, columns=4, lang='pt'):
    """Grid usando colunas simples"""
    cols = st.columns(columns)
    
    for i, kpi in enumerate(kpis):
        with cols[i % columns]:
            render_metric_card(
                label=kpi['label'],
                value=kpi['value'],
                delta=kpi.get('delta'),
                format_type=kpi.get('format_type', 'currency'),
                lang=lang
            )

# ========================================

# components/status.py - VERSÃO ULTRA SIMPLES

import streamlit as st

def render_status_box(status_type, title, message):
    """Status usando alertas nativos do Streamlit"""
    full_message = f"**{title}**: {message}"
    
    if status_type == 'success':
        st.success(full_message)
    elif status_type == 'warning':
        st.warning(full_message)
    elif status_type == 'error':
        st.error(full_message)
    else:
        st.info(full_message)

def render_system_status(params, lang='pt'):
    """Status do sistema simplificado"""
    if not params:
        st.error("❌ Sistema não configurado")
        return False
    
    modelos = params.get('modelos_disponiveis', [])
    if not modelos:
        st.warning("⚠️ Nenhum modelo configurado")
        return False
    
    st.success(f"✅ Sistema OK - {len(modelos)} modelos")
    return True