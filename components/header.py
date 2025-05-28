"""
Header Components - VERSÃO CORRIGIDA
Removidos problemas de HTML que causavam aparecer tags </div>
"""

import streamlit as st
from config.idiomas import get_text


def render_header(lang='pt'):
    """
    Header principal da aplicação - VERSÃO LIMPA
    """
    # Título principal usando markdown simples
    st.markdown(f"# ✈️ {get_text('app_title', lang)}")
    
    # Subtítulo
    st.markdown(f"**{get_text('app_subtitle', lang)}**")
    
    # Separador
    st.markdown("---")


def render_page_header(title, subtitle=None, lang='pt'):
    """
    Header de página específica - VERSÃO LIMPA SEM HTML
    
    Args:
        title: Título da página (pode ser chave de tradução)
        subtitle: Subtítulo opcional (pode ser chave de tradução)
        lang: Idioma
    """
    # Processar título
    if isinstance(title, str):
        if title in ['page_profit', 'page_breakdown', 'page_simulator', 'page_projection', 'page_settings']:
            title_text = get_text(title, lang)
        else:
            title_text = title
    else:
        title_text = str(title)
    
    # Exibir título da página
    st.markdown(f"## {title_text}")
    
    # Exibir subtítulo se fornecido
    if subtitle:
        if isinstance(subtitle, str):
            # Verificar se é chave de tradução
            subtitle_text = get_text(subtitle, lang) if subtitle in [
                'page_profit', 'page_breakdown', 'page_simulator', 
                'page_projection', 'page_settings'
            ] else subtitle
        else:
            subtitle_text = str(subtitle)
        
        st.markdown(f"*{subtitle_text}*")
    
    # Separador
    st.markdown("---")


def render_section_header(title, icon="", lang='pt'):
    """
    Header de seção - VERSÃO SIMPLES
    
    Args:
        title: Título da seção
        icon: Ícone opcional (emoji)
        lang: Idioma
    """
    # Processar título
    title_text = get_text(title, lang) if isinstance(title, str) else str(title)
    
    # Montar texto com ícone se fornecido
    header_text = f"{icon} {title_text}" if icon else title_text
    
    # Exibir usando markdown simples
    st.markdown(f"### {header_text}")


def render_info_box(title, content, type="info", lang='pt'):
    """
    Box de informações - VERSÃO USANDO STREAMLIT NATIVO
    
    Args:
        title: Título do box
        content: Conteúdo do box
        type: Tipo (info, success, warning, error)
        lang: Idioma
    """
    # Processar título e conteúdo
    title_text = get_text(title, lang) if isinstance(title, str) else str(title)
    content_text = get_text(content, lang) if isinstance(content, str) else str(content)
    
    # Texto completo
    full_message = f"**{title_text}**\n\n{content_text}"
    
    # Usar elementos nativos do Streamlit
    if type == "success":
        st.success(full_message)
    elif type == "warning":
        st.warning(full_message)
    elif type == "error":
        st.error(full_message)
    else:
        st.info(full_message)


def render_metric_header(label, value, help_text="", lang='pt'):
    """
    Header de métrica - VERSÃO USANDO ST.METRIC
    
    Args:
        label: Label da métrica
        value: Valor da métrica
        help_text: Texto de ajuda opcional
        lang: Idioma
    """
    # Processar textos
    label_text = get_text(label, lang) if isinstance(label, str) else str(label)
    help_text_final = get_text(help_text, lang) if help_text and isinstance(help_text, str) else help_text
    
    # Usar st.metric nativo
    if help_text_final:
        st.metric(label_text, value, help=help_text_final)
    else:
        st.metric(label_text, value)


def render_clean_title(text, level=1, lang='pt'):
    """
    Título limpo sem HTML - APENAS MARKDOWN
    
    Args:
        text: Texto do título
        level: Nível do título (1-6)
        lang: Idioma
    """
    # Processar texto
    title_text = get_text(text, lang) if isinstance(text, str) else str(text)
    
    # Definir marcação baseada no nível
    markdown_prefix = "#" * max(1, min(6, level))
    
    # Exibir usando markdown puro
    st.markdown(f"{markdown_prefix} {title_text}")


def render_breadcrumb(items, lang='pt'):
    """
    Breadcrumb simples - APENAS TEXTO
    
    Args:
        items: Lista de itens do breadcrumb
        lang: Idioma
    """
    if not items:
        return
    
    # Processar itens
    processed_items = []
    for item in items:
        if isinstance(item, str):
            processed_items.append(get_text(item, lang))
        else:
            processed_items.append(str(item))
    
    # Criar breadcrumb como texto simples
    breadcrumb_text = " > ".join(processed_items)
    
    # Exibir usando markdown
    st.markdown(f"*{breadcrumb_text}*")


def render_status_indicator(status, message="", lang='pt'):
    """
    Indicador de status simples
    
    Args:
        status: Status ('success', 'warning', 'error', 'info')
        message: Mensagem opcional
        lang: Idioma
    """
    # Ícones por status
    status_icons = {
        'success': '✅',
        'warning': '⚠️',
        'error': '❌',
        'info': 'ℹ️'
    }
    
    # Processar mensagem
    message_text = get_text(message, lang) if message and isinstance(message, str) else str(message) if message else ""
    
    # Montar texto final
    icon = status_icons.get(status, 'ℹ️')
    full_text = f"{icon} {message_text}" if message_text else icon
    
    # Exibir usando markdown simples
    st.markdown(full_text)