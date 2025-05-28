import plotly.graph_objects as go

def render_chart_receitas(receita_proprietario, taxa_amaro, lang='pt'):
    values = [receita_proprietario, taxa_amaro]
    labels = ['Receita do Proprietário (90%)', 'Taxa Amaro (10%)']
    colors = ['#10B981', '#8C1D40']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.4,
        marker=dict(colors=colors, line=dict(color='white', width=3)),
        textinfo='label+percent', textfont=dict(size=12, color='white')
    )])
    
    fig.update_layout(
        title={'text': 'Composição de Receitas', 'x': 0.5},
        height=400, paper_bgcolor='white', plot_bgcolor='white'
    )
    return fig

def render_chart_custos(custos_dict, lang='pt'):
    labels = ['Combustível', 'Tripulação', 'Manutenção', 'Depreciação']
    values = [custos_dict.get('combustivel', 0), custos_dict.get('tripulacao', 0), 
              custos_dict.get('manutencao', 0), custos_dict.get('depreciacao', 0)]
    colors = ['#EF4444', '#F59E0B', '#3B82F6', '#10B981']
    
    fig = go.Figure(data=[go.Bar(
        y=labels, x=values, orientation='h',
        text=[f'R$ {v:,.0f}' for v in values], textposition='outside',
        marker=dict(color=colors)
    )])
    
    fig.update_layout(
        title={'text': 'Breakdown de Custos', 'x': 0.5},
        height=400, paper_bgcolor='white', plot_bgcolor='white',
        xaxis={'title': 'Valor (R$)'}
    )
    return fig