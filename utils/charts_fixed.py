"""
Gráficos funcionais com dados corretos e styling visível
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

# Cores Amaro Aviation
AMARO_COLORS = {
    'primary': '#8C1D40',
    'secondary': '#A02050', 
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'info': '#3B82F6',
    'dark': '#1F2937',
    'light': '#F8F9FA'
}

def create_base_layout():
    """Layout base para todos os gráficos"""
    return {
        'paper_bgcolor': 'white',
        'plot_bgcolor': 'white',
        'font': {
            'family': 'Inter, Arial, sans-serif',
            'size': 12,
            'color': AMARO_COLORS['dark']
        },
        'margin': {'l': 60, 'r': 60, 't': 80, 'b': 60},
        'showlegend': True,
        'legend': {
            'orientation': 'h',
            'yanchor': 'bottom',
            'y': -0.2,
            'xanchor': 'center',
            'x': 0.5
        }
    }

def grafico_composicao_receitas(receita_proprietario, taxa_amaro, lang='pt'):
    """
    Gráfico de pizza para composição de receitas
    """
    if not receita_proprietario or not taxa_amaro:
        return create_empty_chart("Sem dados de receita")
    
    labels = [
        'Receita do Proprietário (90%)' if lang == 'pt' else 'Owner Revenue (90%)',
        'Taxa Amaro (10%)' if lang == 'pt' else 'Amaro Fee (10%)'
    ]
    
    values = [receita_proprietario, taxa_amaro]
    colors = [AMARO_COLORS['success'], AMARO_COLORS['primary']]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(
            colors=colors,
            line=dict(color='white', width=3)
        ),
        textinfo='label+percent+value',
        textfont=dict(size=11, color='white'),
        hovertemplate='<b>%{label}</b><br>Valor: R$ %{value:,.0f}<br>Percentual: %{percent}<extra></extra>'
    )])
    
    # Adicionar valor total no centro
    total = sum(values)
    fig.add_annotation(
        text=f"<b>Total</b><br>R$ {total:,.0f}",
        x=0.5, y=0.5,
        font=dict(size=14, color=AMARO_COLORS['dark']),
        showarrow=False
    )
    
    layout = create_base_layout()
    layout.update({
        'title': {
            'text': 'Composição de Receitas' if lang == 'pt' else 'Revenue Composition',
            'x': 0.5,
            'font': {'size': 16, 'color': AMARO_COLORS['primary']}
        },
        'height': 400
    })
    
    fig.update_layout(layout)
    return fig

def grafico_breakdown_custos(custos_dict, lang='pt'):
    """
    Gráfico de barras horizontais para breakdown de custos
    """
    if not custos_dict or not any(custos_dict.values()):
        return create_empty_chart("Sem dados de custos")
    
    # Preparar dados
    labels = list(custos_dict.keys())
    values = list(custos_dict.values())
    
    # Traduzir labels se necessário
    if lang == 'pt':
        label_map = {
            'combustivel': 'Combustível',
            'tripulacao': 'Tripulação',
            'manutencao': 'Manutenção',
            'depreciacao': 'Depreciação',
            'seguro': 'Seguro',
            'hangar': 'Hangar'
        }
        labels = [label_map.get(label, label.title()) for label in labels]
    
    # Cores para cada categoria
    colors = [
        AMARO_COLORS['danger'],    # Combustível
        AMARO_COLORS['warning'],   # Tripulação
        AMARO_COLORS['info'],      # Manutenção
        AMARO_COLORS['success'],   # Depreciação
        AMARO_COLORS['secondary'], # Seguro
        AMARO_COLORS['primary']    # Hangar
    ][:len(labels)]
    
    fig = go.Figure(data=[go.Bar(
        y=labels,
        x=values,
        orientation='h',
        text=[f'R$ {v:,.0f}' for v in values],
        textposition='auto',
        textfont=dict(color='white', size=11),
        marker=dict(
            color=colors,
            line=dict(color='white', width=1)
        ),
        hovertemplate='<b>%{y}</b><br>Valor: R$ %{x:,.0f}<extra></extra>'
    )])
    
    layout = create_base_layout()
    layout.update({
        'title': {
            'text': 'Breakdown de Custos Operacionais' if lang == 'pt' else 'Operational Cost Breakdown',
            'x': 0.5,
            'font': {'size': 16, 'color': AMARO_COLORS['primary']}
        },
        'height': 400,
        'xaxis': {
            'title': 'Valor (R$)' if lang == 'pt' else 'Value (R$)',
            'tickformat': ',.0f',
            'gridcolor': '#E5E7EB',
            'linecolor': '#D1D5DB'
        },
        'yaxis': {
            'title': '',
            'gridcolor': '#E5E7EB',
            'linecolor': '#D1D5DB'
        }
    })
    
    fig.update_layout(layout)
    return fig

def grafico_comparativo_custos(custo_amaro, preco_mercado, lang='pt'):
    """
    Gráfico de barras comparativo Amaro vs Mercado
    """
    if not custo_amaro or not preco_mercado:
        return create_empty_chart("Sem dados para comparação")
    
    labels = [
        'Custo Amaro' if lang == 'pt' else 'Amaro Cost',
        'Preço Mercado' if lang == 'pt' else 'Market Price'
    ]
    
    values = [custo_amaro, preco_mercado]
    colors = [AMARO_COLORS['primary'], AMARO_COLORS['dark']]
    
    fig = go.Figure()
    
    # Adicionar barras
    for i, (label, value, color) in enumerate(zip(labels, values, colors)):
        fig.add_trace(go.Bar(
            name=label,
            x=[label],
            y=[value],
            text=f'R$ {value:,.0f}',
            textposition='outside',
            textfont=dict(size=12, color=AMARO_COLORS['dark']),
            marker=dict(
                color=color,
                line=dict(color='white', width=2)
            ),
            hovertemplate=f'<b>{label}</b><br>Valor: R$ {value:,.0f}<extra></extra>',
            width=0.6
        ))
    
    # Adicionar indicação de economia se houver
    economia = preco_mercado - custo_amaro
    if economia > 0:
        fig.add_annotation(
            x=0.5,
            y=max(values) * 0.8,
            text=f"💰 Economia<br>R$ {economia:,.0f}<br>({economia/preco_mercado*100:.1f}%)",
            showarrow=True,
            arrowhead=2,
            arrowcolor=AMARO_COLORS['success'],
            font=dict(color=AMARO_COLORS['success'], size=11),
            bgcolor="rgba(16, 185, 129, 0.1)",
            bordercolor=AMARO_COLORS['success'],
            borderwidth=1
        )
    
    layout = create_base_layout()
    layout.update({
        'title': {
            'text': 'Comparativo Visual' if lang == 'pt' else 'Visual Comparison',
            'x': 0.5,
            'font': {'size': 16, 'color': AMARO_COLORS['primary']}
        },
        'height': 400,
        'showlegend': False,
        'xaxis': {
            'title': '',
            'linecolor': '#D1D5DB'
        },
        'yaxis': {
            'title': 'Valor (R$)' if lang == 'pt' else 'Value (R$)',
            'tickformat': ',.0f',
            'gridcolor': '#E5E7EB',
            'linecolor': '#D1D5DB'
        }
    })
    
    fig.update_layout(layout)
    return fig

def grafico_projecao_temporal(dados_projecao, lang='pt'):
    """
    Gráfico de linha para projeção temporal
    """
    if not dados_projecao or 'meses' not in dados_projecao:
        return create_empty_chart("Sem dados de projeção")
    
    fig = go.Figure()
    
    # Receita acumulada
    if 'receitas' in dados_projecao:
        receitas_acc = [sum(dados_projecao['receitas'][:i+1]) for i in range(len(dados_projecao['receitas']))]
        fig.add_trace(go.Scatter(
            x=dados_projecao['meses'],
            y=receitas_acc,
            mode='lines+markers',
            name='Receita Acumulada' if lang == 'pt' else 'Accumulated Revenue',
            line=dict(color=AMARO_COLORS['success'], width=3),
            marker=dict(size=6, color=AMARO_COLORS['success']),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.1)'
        ))
    
    # Custos acumulados
    if 'custos' in dados_projecao:
        custos_acc = [sum(dados_projecao['custos'][:i+1]) for i in range(len(dados_projecao['custos']))]
        fig.add_trace(go.Scatter(
            x=dados_projecao['meses'],
            y=custos_acc,
            mode='lines+markers',
            name='Custo Acumulado' if lang == 'pt' else 'Accumulated Cost',
            line=dict(color=AMARO_COLORS['danger'], width=3),
            marker=dict(size=6, color=AMARO_COLORS['danger'])
        ))
    
    # Fluxo de caixa
    if 'fluxo_caixa' in dados_projecao:
        fig.add_trace(go.Scatter(
            x=dados_projecao['meses'],
            y=dados_projecao['fluxo_caixa'],
            mode='lines+markers',
            name='Fluxo de Caixa' if lang == 'pt' else 'Cash Flow',
            line=dict(color=AMARO_COLORS['primary'], width=4),
            marker=dict(size=8, color=AMARO_COLORS['primary'])
        ))
    
    # Linha de breakeven
    if dados_projecao.get('breakeven_mes'):
        fig.add_vline(
            x=dados_projecao['breakeven_mes'],
            line_dash="dash",
            line_color=AMARO_COLORS['warning'],
            line_width=2,
            annotation_text=f"Breakeven: {dados_projecao['breakeven_mes']} meses"
        )
    
    # Linha zero
    fig.add_hline(y=0, line_dash="solid", line_color="#6B7280", line_width=1)
    
    layout = create_base_layout()
    layout.update({
        'title': {
            'text': 'Projeção Financeira' if lang == 'pt' else 'Financial Projection',
            'x': 0.5,
            'font': {'size': 16, 'color': AMARO_COLORS['primary']}
        },
        'height': 500,
        'hovermode': 'x unified',
        'xaxis': {
            'title': 'Meses' if lang == 'pt' else 'Months',
            'gridcolor': '#E5E7EB',
            'linecolor': '#D1D5DB'
        },
        'yaxis': {
            'title': 'Valor (R$)' if lang == 'pt' else 'Value (R$)',
            'tickformat': ',.0f',
            'gridcolor': '#E5E7EB',
            'linecolor': '#D1D5DB'
        }
    })
    
    fig.update_layout(layout)
    return fig

def create_empty_chart(message="Sem dados disponíveis"):
    """
    Cria um gráfico vazio com mensagem
    """
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16, color=AMARO_COLORS['dark'])
    )
    
    layout = create_base_layout()
    layout.update({
        'height': 300,
        'xaxis': {'visible': False},
        'yaxis': {'visible': False}
    })
    
    fig.update_layout(layout)
    return fig

# Funções de conveniência para uso nas páginas
def render_chart_receitas(receita_proprietario, taxa_amaro, lang='pt'):
    """Renderiza gráfico de receitas"""
    fig = grafico_composicao_receitas(receita_proprietario, taxa_amaro, lang)
    return fig

def render_chart_custos(custos_dict, lang='pt'):
    """Renderiza gráfico de custos"""
    fig = grafico_breakdown_custos(custos_dict, lang)
    return fig

def render_chart_comparativo(custo_amaro, preco_mercado, lang='pt'):
    """Renderiza gráfico comparativo"""
    fig = grafico_comparativo_custos(custo_amaro, preco_mercado, lang)
    return fig