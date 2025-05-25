"""charts.py - funções para gerar gráficos"""

import plotly.express as px

def grafico_composicao(custos):
    """
    Gera um gráfico de pizza mostrando a composição dos custos.

    Parâmetros:
    - custos: dict com labels como chaves e valores numéricos.

    Retorna:
    - figura Plotly Express de pizza.
    """
    labels = list(custos.keys())
    values = list(custos.values())
    fig = px.pie(
        names=labels,
        values=values,
        title='Composição de Custos',
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def grafico_comparativo(amaro, mercado):
    """
    Gera um gráfico de barras comparando custo Amaro vs Mercado.

    Parâmetros:
    - amaro: valor numérico do custo Amaro.
    - mercado: valor numérico do custo de mercado.

    Retorna:
    - figura Plotly Express de barras.
    """
    fig = px.bar(
        x=['Amaro', 'Mercado'],
        y=[amaro, mercado],
        title='Comparativo Amaro vs Mercado',
        text=[f"R$ {amaro:,.2f}", f"R$ {mercado:,.2f}"]
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(yaxis_tickprefix='R$ ')
    return fig
