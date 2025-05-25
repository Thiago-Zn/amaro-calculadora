"""charts.py - funções para gráficos"""

import plotly.graph_objects as go

def grafico_composicao(itens: dict):
    labels = list(itens.keys())
    values = list(itens.values())

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
    fig.update_layout(title="Composição de Custos", legend_title="Categorias")
    return fig

def grafico_comparativo(custo_amaro, preco_mercado):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Amaro Aviation", "Preço de Mercado"],
        y=[custo_amaro, preco_mercado],
        marker_color=["#a80000", "#555555"]
    ))
    fig.update_layout(title="Comparativo de Custos", yaxis_title="Custo Total (R$)")
    return fig
