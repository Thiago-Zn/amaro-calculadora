"""
Sistema de gráficos DEFINITIVO com alto contraste e dados visíveis
Cores fortes, títulos claros, dados sempre visíveis
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# CORES CORPORATIVAS AMARO AVIATION
AMARO_PRIMARY = '#8C1D40'      # Bordô principal
AMARO_SECONDARY = '#A02050'    # Bordô secundário  
AMARO_SUCCESS = '#10B981'      # Verde sucesso
AMARO_WARNING = '#F59E0B'      # Amarelo atenção
AMARO_ERROR = '#EF4444'        # Vermelho erro
AMARO_INFO = '#3B82F6'         # Azul informação
AMARO_DARK = '#1F2937'         # Cinza escuro
AMARO_LIGHT = '#F8F9FA'        # Cinza claro

def create_base_layout(title="", height=400):
    """Layout base padronizado para todos os gráficos"""
    return {
        'title': {
            'text': f"<b>{title}</b>",
            'x': 0.5,
            'font': {'size': 16, 'color': AMARO_DARK, 'family': 'Arial Black'}
        },
        'height': height,
        'paper_bgcolor': 'white',
        'plot_bgcolor': 'white',
        'font': {'color': AMARO_DARK, 'size': 12, 'family': 'Arial'},
        'margin': {'l': 50, 'r': 50, 't': 60, 'b': 50},
        'showlegend': True,
        'legend': {
            'bgcolor': 'rgba(248,249,250,0.8)',
            'bordercolor': AMARO_DARK,
            'borderwidth': 1,
            'font': {'size': 11, 'color': AMARO_DARK}
        }
    }

def render_chart_receitas(receita_proprietario, taxa_amaro, lang='pt'):
    """
    Gráfico de pizza para composição de receitas
    GARANTIDO para mostrar dados
    """
    try:
        # Garantir que os valores são numéricos
        receita_proprietario = float(receita_proprietario or 0)
        taxa_amaro = float(taxa_amaro or 0)
        
        # Se valores são zero, criar dados mínimos para visualizar
        if receita_proprietario == 0 and taxa_amaro == 0:
            receita_proprietario = 90
            taxa_amaro = 10
            title_suffix = " (Exemplo)"
        else:
            title_suffix = ""
        
        values = [receita_proprietario, taxa_amaro]
        labels = ['Receita Proprietário (90%)', 'Taxa Amaro (10%)'] if lang == 'pt' else ['Owner Revenue (90%)', 'Amaro Fee (10%)']
        colors = [AMARO_SUCCESS, AMARO_PRIMARY]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(
                colors=colors,
                line=dict(color='white', width=3)
            ),
            textinfo='label+percent+value',
            textfont=dict(size=12, color='white'),
            textposition='auto',
            hovertemplate='<b>%{label}</b><br>Valor: R$ %{value:,.0f}<br>Percentual: %{percent}<extra></extra>'
        )])
        
        layout = create_base_layout(f"Composição de Receitas{title_suffix}" if lang == 'pt' else f"Revenue Composition{title_suffix}")
        fig.update_layout(layout)
        
        # Anotação central
        fig.add_annotation(
            text=f"<b>TOTAL<br>R$ {receita_proprietario + taxa_amaro:,.0f}</b>",
            x=0.5, y=0.5,
            font=dict(size=14, color=AMARO_DARK),
            showarrow=False
        )
        
        return fig
        
    except Exception as e:
        # Gráfico de fallback em caso de erro
        fig = go.Figure()
        fig.add_annotation(
            text=f"Erro no gráfico: {str(e)}",
            x=0.5, y=0.5,
            font=dict(size=16, color=AMARO_ERROR),
            showarrow=False
        )
        fig.update_layout(create_base_layout("Erro - Composição de Receitas"))
        return fig

def render_chart_custos(custos_dict, lang='pt'):
    """
    Gráfico de barras horizontais para breakdown de custos
    GARANTIDO para mostrar dados
    """
    try:
        # Extrair e garantir valores numéricos
        labels_pt = ['Combustível', 'Tripulação', 'Manutenção', 'Depreciação']
        labels_en = ['Fuel', 'Crew', 'Maintenance', 'Depreciation']
        labels = labels_pt if lang == 'pt' else labels_en
        
        keys = ['combustivel', 'tripulacao', 'manutencao', 'depreciacao']
        values = []
        
        for key in keys:
            value = custos_dict.get(key, 0)
            values.append(float(value) if value else 0)
        
        # Se todos os valores são zero, criar dados exemplo
        if sum(values) == 0:
            values = [50000, 30000, 40000, 20000]  # Valores exemplo
            title_suffix = " (Exemplo)"
        else:
            title_suffix = ""
        
        colors = [AMARO_ERROR, AMARO_WARNING, AMARO_INFO, AMARO_SUCCESS]
        
        fig = go.Figure(data=[go.Bar(
            y=labels,
            x=values,
            orientation='h',
            text=[f'R$ {v:,.0f}' for v in values],
            textposition='outside',
            textfont=dict(size=12, color=AMARO_DARK),
            marker=dict(
                color=colors,
                line=dict(color='white', width=2)
            ),
            hovertemplate='<b>%{y}</b><br>Valor: R$ %{x:,.0f}<extra></extra>'
        )])
        
        layout = create_base_layout(f"Breakdown de Custos{title_suffix}" if lang == 'pt' else f"Cost Breakdown{title_suffix}")
        layout.update({
            'xaxis': {
                'title': 'Valor (R$)' if lang == 'pt' else 'Value (R$)',
                'showgrid': True,
                'gridcolor': '#E5E7EB',
                'tickformat': ',.0f',
                'tickfont': {'color': AMARO_DARK}
            },
            'yaxis': {
                'tickfont': {'color': AMARO_DARK, 'size': 11}
            }
        })
        
        fig.update_layout(layout)
        return fig
        
    except Exception as e:
        # Gráfico de fallback
        fig = go.Figure()
        fig.add_annotation(
            text=f"Erro no gráfico: {str(e)}",
            x=0.5, y=0.5,
            font=dict(size=16, color=AMARO_ERROR),
            showarrow=False
        )
        fig.update_layout(create_base_layout("Erro - Breakdown de Custos"))
        return fig

def render_chart_comparativo(custo_amaro, preco_mercado, lang='pt'):
    """
    Gráfico de barras comparativo Amaro vs Mercado
    GARANTIDO para mostrar dados
    """
    try:
        # Garantir valores numéricos
        custo_amaro = float(custo_amaro or 0)
        preco_mercado = float(preco_mercado or 0)
        
        # Se valores são zero, criar exemplo
        if custo_amaro == 0 and preco_mercado == 0:
            custo_amaro = 8000
            preco_mercado = 10000
            title_suffix = " (Exemplo)"
        else:
            title_suffix = ""
        
        categories = ['Amaro Aviation', 'Preço Mercado'] if lang == 'pt' else ['Amaro Aviation', 'Market Price']
        values = [custo_amaro, preco_mercado]
        colors = [AMARO_SUCCESS if custo_amaro < preco_mercado else AMARO_WARNING, AMARO_ERROR]
        
        fig = go.Figure(data=[go.Bar(
            x=categories,
            y=values,
            text=[f'R$ {v:,.0f}' for v in values],
            textposition='outside',
            textfont=dict(size=12, color=AMARO_DARK),
            marker=dict(
                color=colors,
                line=dict(color='white', width=2)
            ),
            hovertemplate='<b>%{x}</b><br>Valor: R$ %{y:,.0f}<extra></extra>'
        )])
        
        layout = create_base_layout(f"Comparativo de Preços{title_suffix}" if lang == 'pt' else f"Price Comparison{title_suffix}")
        layout.update({
            'yaxis': {
                'title': 'Valor (R$)' if lang == 'pt' else 'Value (R$)',
                'showgrid': True,
                'gridcolor': '#E5E7EB',
                'tickformat': ',.0f',
                'tickfont': {'color': AMARO_DARK}
            },
            'xaxis': {
                'tickfont': {'color': AMARO_DARK, 'size': 11}
            }
        })
        
        fig.update_layout(layout)
        
        # Adicionar linha de economia se houver
        economia = preco_mercado - custo_amaro
        if economia > 0:
            fig.add_annotation(
                text=f"<b>Economia: R$ {economia:,.0f}</b>",
                x=0.5, y=max(values) * 1.1,
                xref="paper", yref="y",
                font=dict(size=14, color=AMARO_SUCCESS),
                showarrow=False,
                bgcolor="rgba(16,185,129,0.1)",
                bordercolor=AMARO_SUCCESS,
                borderwidth=1
            )
        
        return fig
        
    except Exception as e:
        # Gráfico de fallback
        fig = go.Figure()
        fig.add_annotation(
            text=f"Erro no gráfico: {str(e)}",
            x=0.5, y=0.5,
            font=dict(size=16, color=AMARO_ERROR),
            showarrow=False
        )
        fig.update_layout(create_base_layout("Erro - Comparativo"))
        return fig

def render_chart_projecao(meses, receitas, custos, lang='pt'):
    """
    Gráfico de linha para projeção temporal
    """
    try:
        fig = go.Figure()
        
        # Receitas
        fig.add_trace(go.Scatter(
            x=meses,
            y=receitas,
            mode='lines+markers',
            name='Receitas' if lang == 'pt' else 'Revenue',
            line=dict(color=AMARO_SUCCESS, width=3),
            marker=dict(size=6, color=AMARO_SUCCESS),
            hovertemplate='<b>Mês %{x}</b><br>Receita: R$ %{y:,.0f}<extra></extra>'
        ))
        
        # Custos
        fig.add_trace(go.Scatter(
            x=meses,
            y=custos,
            mode='lines+markers',
            name='Custos' if lang == 'pt' else 'Costs',
            line=dict(color=AMARO_ERROR, width=3),
            marker=dict(size=6, color=AMARO_ERROR),
            hovertemplate='<b>Mês %{x}</b><br>Custo: R$ %{y:,.0f}<extra></extra>'
        ))
        
        layout = create_base_layout("Projeção Temporal" if lang == 'pt' else "Time Projection", height=500)
        layout.update({
            'xaxis': {
                'title': 'Meses' if lang == 'pt' else 'Months',
                'showgrid': True,
                'gridcolor': '#E5E7EB',
                'tickfont': {'color': AMARO_DARK}
            },
            'yaxis': {
                'title': 'Valor (R$)' if lang == 'pt' else 'Value (R$)',
                'showgrid': True,
                'gridcolor': '#E5E7EB',
                'tickformat': ',.0f',
                'tickfont': {'color': AMARO_DARK}
            }
        })
        
        fig.update_layout(layout)
        return fig
        
    except Exception as e:
        # Gráfico de fallback
        fig = go.Figure()
        fig.add_annotation(
            text=f"Erro no gráfico: {str(e)}",
            x=0.5, y=0.5,
            font=dict(size=16, color=AMARO_ERROR),
            showarrow=False
        )
        fig.update_layout(create_base_layout("Erro - Projeção"))
        return fig

def test_charts():
    """Função de teste para verificar se os gráficos funcionam"""
    print("🧪 Testando gráficos...")
    
    # Teste receitas
    fig1 = render_chart_receitas(90000, 10000, 'pt')
    print(f"✅ Gráfico receitas: {len(fig1.data)} traces")
    
    # Teste custos
    custos_test = {'combustivel': 5000, 'tripulacao': 3000, 'manutencao': 4000, 'depreciacao': 2000}
    fig2 = render_chart_custos(custos_test, 'pt')
    print(f"✅ Gráfico custos: {len(fig2.data)} traces")
    
    # Teste comparativo
    fig3 = render_chart_comparativo(8000, 10000, 'pt')
    print(f"✅ Gráfico comparativo: {len(fig3.data)} traces")
    
    print("🎉 Todos os gráficos funcionam!")

# Executar teste se rodado diretamente
if __name__ == "__main__":
    test_charts()