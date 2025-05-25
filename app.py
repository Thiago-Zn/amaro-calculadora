import streamlit as st
import plotly.express as px
import pandas as pd
from pathlib import Path
from utils.params import load_params
from utils.charts import grafico_comparativo

# Page configuration
st.set_page_config(
    page_title="Amaro Aviation - Calculadora",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    css_file = Path(__file__).parent / "assets" / "style.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Header
col1, col2 = st.columns([1, 4])
with col1:
    # Try to load logo
    logo_path = Path(__file__).parent / "assets" / "logo_amaro.png"
    if logo_path.exists():
        st.image(str(logo_path), width=120)
    else:
        st.markdown("### ✈️")

with col2:
    st.title('Amaro Aviation')
    st.subheader('Calculadora de Custos & Economia em Aviação Executiva')

st.markdown("---")

# Load parameters for overview
try:
    params = load_params()
    modelos = list(params['consumo_modelos'].keys())
except Exception as e:
    st.error(f"Erro ao carregar parâmetros: {e}")
    st.stop()

# Main dashboard
st.markdown("## 📊 Visão Geral do Sistema")

# Key metrics row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🛩️ Modelos Disponíveis",
        value=len(modelos),
        help="Quantidade de aeronaves disponíveis para simulação"
    )

with col2:
    avg_fuel_consumption = sum(params['consumo_modelos'].values()) / len(params['consumo_modelos'])
    st.metric(
        label="⛽ Consumo Médio",
        value=f"{avg_fuel_consumption:.0f} L/h",
        help="Consumo médio de combustível por hora"
    )

with col3:
    st.metric(
        label="💰 Preço Combustível",
        value=f"R$ {params['preco_combustivel']:.2f}/L",
        help="Preço atual do combustível por litro"
    )

with col4:
    avg_market_price = sum(params['preco_mercado_hora'].values()) / len(params['preco_mercado_hora'])
    st.metric(
        label="📈 Preço Médio Mercado",
        value=f"R$ {avg_market_price:,.0f}/h",
        help="Preço médio de mercado por hora de voo"
    )

st.markdown("---")

# Quick comparison section
st.markdown("## 🔍 Comparação Rápida por Modelo")

# Create comparison dataframe
comparison_data = []
for modelo in modelos:
    consumo = params['consumo_modelos'][modelo]
    custo_combustivel = consumo * params['preco_combustivel']
    custo_manutencao = params['custo_manutencao'][modelo]
    custo_piloto = params['custo_piloto_hora'][modelo]
    depreciacao = params['depreciacao_hora'][modelo]
    custo_total_hora = custo_combustivel + custo_manutencao + custo_piloto + depreciacao
    preco_mercado = params['preco_mercado_hora'][modelo]
    economia_hora = preco_mercado - custo_total_hora
    
    comparison_data.append({
        'Modelo': modelo,
        'Custo Total/h (R$)': custo_total_hora,
        'Preço Mercado/h (R$)': preco_mercado,
        'Economia/h (R$)': economia_hora,
        'Economia (%)': (economia_hora / preco_mercado) * 100 if preco_mercado > 0 else 0
    })

df_comparison = pd.DataFrame(comparison_data)

# Display comparison table
st.dataframe(
    df_comparison.style.format({
        'Custo Total/h (R$)': 'R$ {:,.2f}',
        'Preço Mercado/h (R$)': 'R$ {:,.2f}',
        'Economia/h (R$)': 'R$ {:,.2f}',
        'Economia (%)': '{:.1f}%'
    }),
    use_container_width=True
)

# Charts section
col1, col2 = st.columns(2)

with col1:
    # Cost breakdown chart
    fig_costs = px.bar(
        df_comparison,
        x='Modelo',
        y=['Custo Total/h (R$)', 'Preço Mercado/h (R$)'],
        title='Comparativo de Custos por Modelo',
        barmode='group'
    )
    fig_costs.update_layout(
        yaxis_tickprefix='R$ ',
        yaxis_tickformat=',.0f'
    )
    st.plotly_chart(fig_costs, use_container_width=True)

with col2:
    # Savings percentage chart
    fig_savings = px.bar(
        df_comparison,
        x='Modelo',
        y='Economia (%)',
        title='Percentual de Economia por Modelo',
        color='Economia (%)',
        color_continuous_scale='RdYlGn'
    )
    fig_savings.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    st.plotly_chart(fig_savings, use_container_width=True)

st.markdown("---")

# Navigation guide
st.markdown("## 🧭 Como Usar o Sistema")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📍 Para Cálculos Específicos
    - **Custo por Trecho**: Calcule o custo de uma rota específica
    - **Lucros Mensais**: Projete a rentabilidade mensal
    - **Meta de Receita**: Defina estratégias para atingir metas
    """)

with col2:
    st.markdown("""
    ### 📊 Para Análises
    - **Comparativo Economia**: Compare economia anual
    - **Modo Cliente**: Simulações para apresentações
    - **Configurações**: Ajuste parâmetros (uso interno)
    """)

with col3:
    st.markdown("""
    ### 💡 Dicas
    - Use o menu lateral para navegar
    - Todos os cálculos são em tempo real
    - Gráficos são interativos
    - Valores podem ser exportados
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🛩️ <strong>Amaro Aviation</strong> - Calculadora de Custos & Economia</p>
    <p>Ferramenta desenvolvida para análise de viabilidade econômica em aviação executiva</p>
</div>
""", unsafe_allow_html=True)

# Sidebar information
with st.sidebar:
    st.markdown("### ℹ️ Informações do Sistema")
    st.info(f"""
    **Modelos Disponíveis:** {len(modelos)}
    
    **Última Atualização:** Parâmetros carregados com sucesso
    
    **Funcionalidades:**
    - ✅ Cálculo por trecho
    - ✅ Projeções mensais
    - ✅ Análise de metas
    - ✅ Comparativos
    - ✅ Modo cliente
    - ⚙️ Configurações
    """)
    
    st.markdown("### 🚀 Navegação Rápida")
    st.markdown("""
    Use as páginas do menu acima para:
    - Fazer cálculos específicos
    - Gerar relatórios
    - Configurar parâmetros
    - Apresentar para clientes
    """)