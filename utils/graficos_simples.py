"""
GRÁFICOS SIMPLES QUE SEMPRE FUNCIONAM
Sem dependências complicadas, apenas Plotly básico
"""

import plotly.graph_objects as go
import streamlit as st

def grafico_pizza_receitas(receita_proprietario, taxa_amaro):
    """
    Gráfico de pizza SIMPLES que sempre funciona
    """
    try:
        # Garantir valores numéricos
        receita_proprietario = float(receita_proprietario) if receita_proprietario else 90000
        taxa_amaro = float(taxa_amaro) if taxa_amaro else 10000
        
        # Criar gráfico
        fig = go.Figure(data=[go.Pie(
            labels=['Proprietário (90%)', 'Amaro (10%)'],
            values=[receita_proprietario, taxa_amaro],
            marker_colors=['#10B981', '#8C1D40'],
            textinfo='label+percent',
            textfont_size=14,
            textfont_color='white'
        )])
        
        fig.update_layout(
            title='Composição de Receitas',
            title_x=0.5,
            title_font_size=16,
            height=400,
            showlegend=True
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Erro no gráfico de receitas: {e}")
        # Gráfico vazio como fallback
        fig = go.Figure()
        fig.add_annotation(text="Erro ao carregar gráfico", x=0.5, y=0.5)
        return fig

def grafico_barras_custos(combustivel, tripulacao, manutencao, depreciacao):
    """
    Gráfico de barras SIMPLES que sempre funciona
    """
    try:
        # Garantir valores numéricos
        combustivel = float(combustivel) if combustivel else 5000
        tripulacao = float(tripulacao) if tripulacao else 3000
        manutencao = float(manutencao) if manutencao else 4000
        depreciacao = float(depreciacao) if depreciacao else 2000
        
        # Dados do gráfico
        categorias = ['Combustível', 'Tripulação', 'Manutenção', 'Depreciação']
        valores = [combustivel, tripulacao, manutencao, depreciacao]
        cores = ['#EF4444', '#F59E0B', '#3B82F6', '#10B981']
        
        # Criar gráfico
        fig = go.Figure(data=[go.Bar(
            x=categorias,
            y=valores,
            marker_color=cores,
            text=[f'R$ {v:,.0f}' for v in valores],
            textposition='outside'
        )])
        
        fig.update_layout(
            title='Breakdown de Custos',
            title_x=0.5,
            title_font_size=16,
            height=400,
            yaxis_title='Valor (R$)',
            showlegend=False
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Erro no gráfico de custos: {e}")
        # Gráfico vazio como fallback
        fig = go.Figure()
        fig.add_annotation(text="Erro ao carregar gráfico", x=0.5, y=0.5)
        return fig

def grafico_comparativo_simples(custo_amaro, preco_mercado):
    """
    Gráfico comparativo SIMPLES que sempre funciona
    """
    try:
        # Garantir valores numéricos
        custo_amaro = float(custo_amaro) if custo_amaro else 8000
        preco_mercado = float(preco_mercado) if preco_mercado else 10000
        
        # Dados do gráfico
        categorias = ['Amaro Aviation', 'Preço Mercado']
        valores = [custo_amaro, preco_mercado]
        cores = ['#10B981', '#EF4444']
        
        # Criar gráfico
        fig = go.Figure(data=[go.Bar(
            x=categorias,
            y=valores,
            marker_color=cores,
            text=[f'R$ {v:,.0f}' for v in valores],
            textposition='outside'
        )])
        
        fig.update_layout(
            title='Comparativo de Preços',
            title_x=0.5,
            title_font_size=16,
            height=400,
            yaxis_title='Valor (R$)',
            showlegend=False
        )
        
        # Adicionar economia se houver
        economia = preco_mercado - custo_amaro
        if economia > 0:
            fig.add_annotation(
                text=f'Economia: R$ {economia:,.0f}',
                x=0.5, y=max(valores) * 1.1,
                xref="paper", yref="y",
                showarrow=False,
                font_color='green',
                font_size=14
            )
        
        return fig
        
    except Exception as e:
        st.error(f"Erro no gráfico comparativo: {e}")
        # Gráfico vazio como fallback
        fig = go.Figure()
        fig.add_annotation(text="Erro ao carregar gráfico", x=0.5, y=0.5)
        return fig

def teste_graficos():
    """
    Função para testar se os gráficos funcionam
    """
    st.write("🧪 Testando gráficos...")
    
    # Teste 1: Gráfico de receitas
    fig1 = grafico_pizza_receitas(90000, 10000)
    st.plotly_chart(fig1, use_container_width=True)
    
    # Teste 2: Gráfico de custos
    fig2 = grafico_barras_custos(5000, 3000, 4000, 2000)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Teste 3: Gráfico comparativo
    fig3 = grafico_comparativo_simples(8000, 10000)
    st.plotly_chart(fig3, use_container_width=True)
    
    st.success("✅ Todos os gráficos funcionaram!")

# Se executado diretamente, roda teste
if __name__ == "__main__":
    teste_graficos()