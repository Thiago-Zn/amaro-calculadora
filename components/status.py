"""
Componente para renderização de boxes de status - VERSÃO LIMPA
Removido o quadro verde irritante do "Sistema Operacional"
"""

import streamlit as st
import textwrap

# ------------------------------------------------------------------------
# Caixa de status genérica
# ------------------------------------------------------------------------
def render_status_box(status_type: str,
                      title: str,
                      message: str,
                      details: str | None = None) -> None:
    """
    Exibe um bloco de status (success, warning, error ou info).

    Args
    ----
    status_type : 'success' | 'warning' | 'error' | 'info'
    title       : título do box
    message     : texto principal (texto simples, SEM tags <div>)
    details     : texto adicional opcional (também texto puro)
    """

    # Configurações por tipo
    config = {
        'success': {
            'color': '#10B981',
            'bg_color': '#F0FDF4',
            'border_color': '#10B981',
            'icon': '✅'
        },
        'warning': {
            'color': '#F59E0B',
            'bg_color': '#FFFBEB',
            'border_color': '#F59E0B',
            'icon': '⚠️'
        },
        'error': {
            'color': '#DC2626',
            'bg_color': '#FEF2F2',
            'border_color': '#DC2626',
            'icon': '❌'
        },
        'info': {
            'color': '#0EA5E9',
            'bg_color': '#F0F9FF',
            'border_color': '#0EA5E9',
            'icon': 'ℹ️'
        }
    }
    
    style_config = config.get(status_type.lower(), config['info'])
    
    details_html = ""
    if details:
        details_html = f"""
        <div style="
            font-size: 0.875rem;
            margin-top: 0.5rem;
            opacity: 0.8;
        ">
            {details.strip()}
        </div>
        """
    
    st.markdown(f"""
    <div style="
        background: {style_config['bg_color']};
        border: 1px solid {style_config['border_color']};
        border-left: 4px solid {style_config['border_color']};
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    ">
        <div style="
            color: {style_config['color']};
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 0.25rem;
        ">
            {style_config['icon']} {title}
        </div>
        <div style="
            color: #374151;
            font-size: 0.875rem;
            line-height: 1.5;
        ">
            {message}
            {details_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_calculation_status(is_profitable, profit_value, message, lang='pt'):
    """
    Exibe um box de status baseado no resultado financeiro.

    Args:
        is_profitable (bool): True se houver lucro.
        profit_value (float): Valor de lucro ou prejuízo.
        message (str): Texto explicativo que antecede o valor.
        lang (str): 'pt' ou 'en'.
    """
    from utils.params import format_currency
    
    # Monta texto puro, sem tags HTML
    valor_formatado = format_currency(abs(profit_value), lang)
    texto = f"{message} {valor_formatado}"

    if is_profitable:
        render_status_box(
            "success",
            "Operação Lucrativa" if lang == "pt" else "Profitable Operation",
            texto
        )
    else:
        render_status_box(
            "warning",
            "Operação com Prejuízo" if lang == "pt" else "Operation at Loss",
            texto
        )

def render_system_status(params, lang='pt'):
    """
    FUNÇÃO COMPLETAMENTE REMOVIDA - NÃO FAZ MAIS NADA!
    
    Esta função agora simplesmente retorna True sem exibir nada.
    O irritante quadro verde foi COMPLETAMENTE removido.
    """
    # Verificação silenciosa apenas para funcionalidade
    if not params or not params.get("modelos_disponiveis"):
        return False
    
    # Não exibe mais NADA - nem quadro verde nem mensagem
    return True

def render_export_status(export_success, filename=None, lang='pt'):
    """
    Renderiza status de exportação
    
    Args:
        export_success: Boolean indicando sucesso
        filename: Nome do arquivo exportado (opcional)
        lang: Idioma
    """
    
    if export_success:
        message = 'Relatório exportado com sucesso' if lang == 'pt' else 'Report exported successfully'
        if filename:
            message += f': {filename}'
        
        render_status_box(
            'success',
            'Exportação Concluída' if lang == 'pt' else 'Export Completed',
            message
        )
    else:
        render_status_box(
            'error',
            'Erro na Exportação' if lang == 'pt' else 'Export Error',
            'Não foi possível exportar o relatório. Tente novamente.' if lang == 'pt'
            else 'Could not export report. Please try again.'
        )

def render_loading_status(message, lang='pt'):
    """
    Renderiza status de carregamento
    
    Args:
        message: Mensagem de carregamento
        lang: Idioma
    """
    
    st.markdown(f"""
    <div style="
        background: #F0F9FF;
        border: 1px solid #0EA5E9;
        border-left: 4px solid #0EA5E9;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    ">
        <div style="
            color: #0EA5E9;
            font-weight: 600;
            font-size: 1rem;
        ">
            ⏳ {message}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_progress_status(current_step, total_steps, step_name, lang='pt'):
    """
    Renderiza status de progresso
    
    Args:
        current_step: Passo atual
        total_steps: Total de passos
        step_name: Nome do passo atual
        lang: Idioma
    """
    
    progress = current_step / total_steps
    
    st.markdown(f"""
    <div style="
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    ">
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        ">
            <span style="font-weight: 600; color: #374151;">{step_name}</span>
            <span style="font-size: 0.875rem; color: #6B7280;">
                {current_step}/{total_steps}
            </span>
        </div>
        
        <div style="
            width: 100%;
            height: 8px;
            background: #E5E7EB;
            border-radius: 4px;
            overflow: hidden;
        ">
            <div style="
                width: {progress * 100}%;
                height: 100%;
                background: #8C1D40;
                transition: width 0.3s ease;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)