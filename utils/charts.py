"""charts.py - Sistema de gráficos premium com design Amaro Aviation"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Paleta de cores Amaro Aviation
AMARO_COLORS = {
    'primary': '#8c1d40',
    'secondary': '#a02050', 
    'success': '#27AE60',
    'warning': '#F39C12',
    'danger': '#E74C3C',
    'info': '#3498DB',
    'light': '#F8F9FA',
    'dark': '#2C3E50',
    'market': '#95A5A6'
}

def get_amaro_template():
    """Template personalizado Amaro Aviation"""
    return {
        'layout': {
            'font': {'family': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif', 'size': 12},
            'paper_bgcolor': 'white',
            'plot_bgcolor': 'white',
            'colorway': [AMARO_COLORS['primary'], AMARO_COLORS['secondary'], 
                        AMARO_COLORS['success'], AMARO_COLORS['info']],
            'margin': {'l': 80, 'r': 80, 't': 100, 'b': 80},
            'title': {
                'font': {'size': 18, 'color': AMARO_COLORS['dark']},
                'x': 0.5,
                'xanchor': 'center'
            },
            'xaxis': {
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': '#E5E5E5',
                'linecolor': '#CCCCCC',
                'titlefont': {'size': 14},
                'tickfont': {'size': 11}
            },
            'yaxis': {
                'showgrid': True,
                'gridwidth': 1,
                'gridcolor': '#E5E5E5',
                'linecolor': '#CCCCCC',
                'titlefont': {'size': 14},
                'tickfont': {'size': 11}
            }
        }
    }

def grafico_composicao(custos_dict, title="Composição de Custos"):
    """
    Gráfico de pizza premium para composição de custos
    """
    if not custos_dict or not any(custos_dict.values()):
        return go.Figure().add_annotation(
            text="Sem dados para exibir",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    labels = list(custos_dict.keys())
    values = list(custos_dict.values())
    
    # Cores específicas por categoria
    color_map = {
        'Combustível': AMARO_COLORS['primary'],
        'Piloto': AMARO_COLORS['secondary'],
        'Manutenção': AMARO_COLORS['info'],
        'Depreciação': AMARO_COLORS['warning']
    }
    
    colors = [color_map.get(label, AMARO_COLORS['dark']) for label in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(
            colors=colors,
            line=dict(color='white', width=3)
        ),
        textinfo='label+percent',
        textfont=dict(size=12),
        hovertemplate='<b>%{label}</b><br>' +
                     'Valor: R$ %{value:,.2f}<br>' +
                     'Percentual: %{percent}<br>' +
                     '<extra></extra>'
    )])
    
    # Adicionar valor total no centro
    total = sum(values)
    fig.add_annotation(
        text=f"<b>Total</b><br>R$ {total:,.0f}",
        x=0.5, y=0.5,
        font=dict(size=16, color=AMARO_COLORS['dark']),
        showarrow=False
    )
    
    fig.update_layout(
        title=title,
        template=get_amaro_template()['layout'],
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05
        ),
        height=450
    )
    
    return fig

def grafico_comparativo(custo_amaro, preco_mercado, title="Comparativo Amaro vs. Mercado"):
    """
    Gráfico de barras comparativo premium
    """
    categorias = ['Amaro Aviation', 'Preço de Mercado']
    valores = [custo_amaro, preco_mercado]
    colors = [AMARO_COLORS['primary'], AMARO_COLORS['market']]
    
    fig = go.Figure()
    
    for i, (categoria, valor, cor) in enumerate(zip(categorias, valores, colors)):
        fig.add_trace(go.Bar(
            name=categoria,
            x=[categoria],
            y=[valor],
            marker_color=cor,
            text=f'R$ {valor:,.0f}',
            textposition='outside',
            textfont=dict(size=14, color=AMARO_COLORS['dark']),
            hovertemplate=f'<b>{categoria}</b><br>' +
                         f'Valor: R$ {valor:,.2f}<br>' +
                         '<extra></extra>',
            width=0.6
        ))
    
    # Adicionar linha de economia
    economia = preco_mercado - custo_amaro
    if economia > 0:
        fig.add_shape(
            type="line",
            x0=-0.4, y0=custo_amaro, x1=0.6, y1=custo_amaro,
            line=dict(color=AMARO_COLORS['success'], width=3, dash="dash")
        )
        
        fig.add_annotation(
            x=0.1, y=custo_amaro + economia/2,
            text=f"Economia<br>R$ {economia:,.0f}",
            showarrow=True,
            arrowhead=2,
            arrowcolor=AMARO_COLORS['success'],
            font=dict(color=AMARO_COLORS['success'], size=12)
        )
    
    fig.update_layout(
        title=title,
        template=get_amaro_template()['layout'],
        yaxis_title='Valor (R$)',
        yaxis_tickformat=',.0f',
        showlegend=False,
        height=400,
        bargap=0.4
    )
    
    return fig

def grafico_evolucao_mensal(dados_mensais, title="Evolução de Lucros Mensais"):
    """
    Gráfico de linha para evolução mensal
    """
    if not dados_mensais:
        return go.Figure().add_annotation(
            text="Sem dados para exibir",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    meses = list(dados_mensais.keys())
    lucros = list(dados_mensais.values())
    
    fig = go.Figure()
    
    # Linha principal
    fig.add_trace(go.Scatter(
        x=meses,
        y=lucros,
        mode='lines+markers',
        name='Lucro Mensal',
        line=dict(color=AMARO_COLORS['primary'], width=4),
        marker=dict(
            size=10,
            color=AMARO_COLORS['primary'],
            line=dict(color='white', width=2)
        ),
        fill='tonexty',
        fillcolor=f"rgba({int(AMARO_COLORS['primary'][1:3], 16)}, {int(AMARO_COLORS['primary'][3:5], 16)}, {int(AMARO_COLORS['primary'][5:7], 16)}, 0.1)",
        hovertemplate='<b>%{x}</b><br>Lucro: R$ %{y:,.0f}<extra></extra>'
    ))
    
    # Linha de meta (se aplicável)
    if lucros:
        meta = max(lucros) * 0.8  # Meta de 80% do máximo
        fig.add_hline(
            y=meta,
            line_dash="dash",
            line_color=AMARO_COLORS['success'],
            annotation_text=f"Meta: R$ {meta:,.0f}"
        )
    
    fig.update_layout(
        title=title,
        template=get_amaro_template()['layout'],
        xaxis_title='Mês',
        yaxis_title='Lucro (R$)',
        yaxis_tickformat=',.0f',
        height=400
    )
    
    return fig

def grafico_breakdown_detalhado(custos_por_categoria, title="Breakdown Detalhado de Custos"):
    """
    Gráfico de barras empilhadas para breakdown detalhado
    """
    if not custos_por_categoria:
        return go.Figure().add_annotation(
            text="Sem dados para exibir",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    categorias = list(custos_por_categoria.keys())
    
    fig = go.Figure()
    
    # Cores para cada subcategoria
    cores_breakdown = [
        AMARO_COLORS['primary'],
        AMARO_COLORS['secondary'],
        AMARO_COLORS['info'],
        AMARO_COLORS['warning'],
        AMARO_COLORS['success']
    ]
    
    for i, categoria in enumerate(categorias):
        valores = custos_por_categoria[categoria]
        if isinstance(valores, dict):
            subcategorias = list(valores.keys())
            valores_sub = list(valores.values())
            
            for j, (subcat, valor) in enumerate(zip(subcategorias, valores_sub)):
                fig.add_trace(go.Bar(
                    name=subcat,
                    x=[categoria],
                    y=[valor],
                    marker_color=cores_breakdown[j % len(cores_breakdown)],
                    hovertemplate=f'<b>{subcat}</b><br>Valor: R$ {valor:,.2f}<extra></extra>'
                ))
        else:
            fig.add_trace(go.Bar(
                name=categoria,
                x=[categoria],
                y=[valores],
                marker_color=cores_breakdown[i % len(cores_breakdown)],
                hovertemplate=f'<b>{categoria}</b><br>Valor: R$ {valores:,.2f}<extra></extra>'
            ))
    
    fig.update_layout(
        title=title,
        template=get_amaro_template()['layout'],
        barmode='stack',
        yaxis_title='Valor (R$)',
        yaxis_tickformat=',.0f',
        height=400
    )
    
    return fig

def grafico_economia_anual(modelos_economia, title="Economia Anual por Modelo"):
    """
    Gráfico de barras horizontais para economia anual
    """
    if not modelos_economia:
        return go.Figure().add_annotation(
            text="Sem dados para exibir",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    modelos = list(modelos_economia.keys())
    economias = list(modelos_economia.values())
    
    # Cores baseadas na economia (verde para positiva, vermelho para negativa)
    cores = [AMARO_COLORS['success'] if eco > 0 else AMARO_COLORS['danger'] for eco in economias]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=modelos,
        x=economias,
        orientation='h',
        marker_color=cores,
        text=[f'R$ {eco:,.0f}' for eco in economias],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Economia Anual: R$ %{x:,.0f}<extra></extra>'
    ))
    
    # Linha vertical no zero
    fig.add_vline(x=0, line_dash="solid", line_color=AMARO_COLORS['dark'], line_width=1)
    
    fig.update_layout(
        title=title,
        template=get_amaro_template()['layout'],
        xaxis_title='Economia Anual (R$)',
        xaxis_tickformat=',.0f',
        yaxis_title='Modelo',
        height=max(400, len(modelos) * 60),
        showlegend=False
    )
    
    return fig

def grafico_dashboard_executivo(kpis_dict):
    """
    Dashboard executivo com múltiplos gráficos
    """
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Composição de Custos', 'Evolução Mensal', 
                       'Comparativo por Modelo', 'Metas vs. Realizado'),
        specs=[[{"type": "pie"}, {"type": "scatter"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Gráfico 1: Pizza de custos
    if 'custos' in kpis_dict:
        custos = kpis_dict['custos']
        fig.add_trace(
            go.Pie(labels=list(custos.keys()), values=list(custos.values()),
                  hole=0.3, marker_colors=[AMARO_COLORS['primary'], 
                  AMARO_COLORS['secondary'], AMARO_COLORS['info']]),
            row=1, col=1
        )
    
    # Gráfico 2: Evolução
    if 'evolucao' in kpis_dict:
        evolucao = kpis_dict['evolucao']
        fig.add_trace(
            go.Scatter(x=list(evolucao.keys()), y=list(evolucao.values()),
                      mode='lines+markers', line_color=AMARO_COLORS['primary']),
            row=1, col=2
        )
    
    # Gráfico 3: Comparativo
    if 'comparativo' in kpis_dict:
        comp = kpis_dict['comparativo']
        fig.add_trace(
            go.Bar(x=list(comp.keys()), y=list(comp.values()),
                  marker_color=AMARO_COLORS['secondary']),
            row=2, col=1
        )
    
    # Gráfico 4: Metas
    if 'metas' in kpis_dict:
        metas = kpis_dict['metas']
        fig.add_trace(
            go.Bar(x=['Meta', 'Realizado'], y=[metas.get('meta', 0), metas.get('realizado', 0)],
                  marker_color=[AMARO_COLORS['warning'], AMARO_COLORS['success']]),
            row=2, col=2
        )
    
    fig.update_layout(
        height=600,
        template=get_amaro_template()['layout'],
        title_text="Dashboard Executivo - Amaro Aviation"
    )
    
    return fig

def grafico_tendencia_mercado(dados_mercado, dados_amaro, title="Tendência: Amaro vs. Mercado"):
    """
    Gráfico de área para comparar tendências
    """
    if not dados_mercado or not dados_amaro:
        return go.Figure().add_annotation(
            text="Dados insuficientes para análise de tendência",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    periodos = list(dados_mercado.keys())
    
    fig = go.Figure()
    
    # Área do mercado
    fig.add_trace(go.Scatter(
        x=periodos,
        y=list(dados_mercado.values()),
        fill='tonexty',
        mode='lines',
        name='Preço de Mercado',
        line_color=AMARO_COLORS['market'],
        fillcolor=f"rgba({int(AMARO_COLORS['market'][1:3], 16)}, {int(AMARO_COLORS['market'][3:5], 16)}, {int(AMARO_COLORS['market'][5:7], 16)}, 0.3)"
    ))
    
    # Área Amaro
    fig.add_trace(go.Scatter(
        x=periodos,
        y=list(dados_amaro.values()),
        fill='tonexty',
        mode='lines',
        name='Custo Amaro',
        line_color=AMARO_COLORS['primary'],
        fillcolor=f"rgba({int(AMARO_COLORS['primary'][1:3], 16)}, {int(AMARO_COLORS['primary'][3:5], 16)}, {int(AMARO_COLORS['primary'][5:7], 16)}, 0.3)"
    ))
    
    fig.update_layout(
        title=title,
        template=get_amaro_template()['layout'],
        xaxis_title='Período',
        yaxis_title='Valor (R$)',
        yaxis_tickformat=',.0f',
        height=400,
        hovermode='x unified'
    )
    
    return fig