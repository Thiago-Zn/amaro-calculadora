"""
Componente para renderização de cards de métricas
"""

import streamlit as st
from utils.params import format_currency, format_percentage

def render_metric_card(label, value, delta=None, format_type="currency", lang='pt'):
    """
    Cria um card de métrica customizado
    
    Args:
        label: Rótulo da métrica
        value: Valor principal
        delta: Variação (opcional)
        format_type: Tipo de formatação ('currency', 'percentage', 'number', 'text')
        lang: Idioma
    
    Returns:
        String HTML do card
    """
    
    # Formatação do valor principal
    if format_type == "currency":
        formatted_value = format_currency(value, lang)
    elif format_type == "percentage":
        formatted_value = format_percentage(value, lang)
    elif format_type == "number":
        formatted_value = f"{value:,.0f}".replace(",", "." if lang == 'pt' else ",")
    else:
        formatted_value = str(value)
    
    # Delta opcional
    delta_html = ""
    if delta is not None:
        delta_color = "#10B981" if delta > 0 else "#EF4444"
        delta_symbol = "▲" if delta > 0 else "▼"
        if format_type == "percentage":
            delta_text = f"{abs(delta):.1f}%"
        else:
            delta_text = f"{abs(delta):,.0f}"
        
        delta_html = f"""
        <div style="
            color: {delta_color}; 
            font-size: 0.875rem;
            margin-top: 0.5rem;
            font-weight: 500;
        ">
            {delta_symbol} {delta_text}
        </div>
        """
    
    return f"""
    <div class="metric-card">
        <div class="metric-card-label">{label}</div>
        <div class="metric-card-value">{formatted_value}</div>
        {delta_html}
    </div>
    """

def render_highlight_metric(title, value, subtitle="", color="#8C1D40", format_type="currency", lang='pt'):
    """
    Renderiza métrica em destaque
    
    Args:
        title: Título da métrica
        value: Valor principal
        subtitle: Subtítulo opcional
        color: Cor de fundo
        format_type: Tipo de formatação
        lang: Idioma
    """
    
    # Formatação do valor
    if format_type == "currency":
        formatted_value = format_currency(value, lang)
    elif format_type == "percentage":
        formatted_value = format_percentage(value, lang)
    elif format_type == "number":
        formatted_value = f"{value:,.0f}".replace(",", "." if lang == 'pt' else ",")
    else:
        formatted_value = str(value)
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {color} 0%, {color}DD 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    ">
        <h3 style="font-size: 1.2rem; margin: 0; font-weight: 600;">{title}</h3>
        <div style="font-size: 2.5rem; font-weight: 700; margin: 1rem 0; line-height: 1;">
            {formatted_value}
        </div>
        <div style="font-size: 0.9rem; opacity: 0.9;">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)

def render_comparison_metrics(metrics_dict, lang='pt'):
    """
    Renderiza métricas de comparação lado a lado
    
    Args:
        metrics_dict: Dict com métricas no formato:
        {
            'label': 'Título',
            'value1': valor1,
            'value2': valor2,
            'label1': 'Label 1',
            'label2': 'Label 2',
            'format_type': 'currency'
        }
        lang: Idioma
    """
    
    # Formatação dos valores
    format_type = metrics_dict.get('format_type', 'currency')
    
    if format_type == "currency":
        value1_fmt = format_currency(metrics_dict['value1'], lang)
        value2_fmt = format_currency(metrics_dict['value2'], lang)
    elif format_type == "percentage":
        value1_fmt = format_percentage(metrics_dict['value1'], lang)
        value2_fmt = format_percentage(metrics_dict['value2'], lang)
    else:
        value1_fmt = str(metrics_dict['value1'])
        value2_fmt = str(metrics_dict['value2'])
    
    # Determinar qual é melhor (menor custo ou maior lucro)
    is_cost = 'custo' in metrics_dict['label'].lower() or 'cost' in metrics_dict['label'].lower()
    
    if is_cost:
        better1 = metrics_dict['value1'] < metrics_dict['value2']
        better2 = metrics_dict['value2'] < metrics_dict['value1']
    else:
        better1 = metrics_dict['value1'] > metrics_dict['value2']
        better2 = metrics_dict['value2'] > metrics_dict['value1']
    
    color1 = "#10B981" if better1 else "#6B7280"
    color2 = "#10B981" if better2 else "#6B7280"
    
    st.markdown(f"""
    <div style="
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin: 1rem 0;
    ">
        <div style="
            background: white;
            border: 2px solid {color1};
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
        ">
            <div style="color: #6B7280; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.05em;">
                {metrics_dict['label1']}
            </div>
            <div style="color: {color1}; font-size: 1.8rem; font-weight: 700; margin: 0.5rem 0;">
                {value1_fmt}
            </div>
        </div>
        
        <div style="
            background: white;
            border: 2px solid {color2};
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
        ">
            <div style="color: #6B7280; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.05em;">
                {metrics_dict['label2']}
            </div>
            <div style="color: {color2}; font-size: 1.8rem; font-weight: 700; margin: 0.5rem 0;">
                {value2_fmt}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_grid(kpis, columns=4, lang='pt'):
    """
    Renderiza grade de KPIs
    
    Args:
        kpis: Lista de dicts com KPIs no formato:
        [
            {
                'label': 'Label',
                'value': valor,
                'format_type': 'currency',
                'delta': variação (opcional)
            }
        ]
        columns: Número de colunas
        lang: Idioma
    """
    
    cols = st.columns(columns)
    
    for i, kpi in enumerate(kpis):
        with cols[i % columns]:
            card_html = render_metric_card(
                label=kpi['label'],
                value=kpi['value'],
                delta=kpi.get('delta'),
                format_type=kpi.get('format_type', 'currency'),
                lang=lang
            )
            st.markdown(card_html, unsafe_allow_html=True)