import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from utils.params import load_params
from utils.calculations import calcula_custo_trecho
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Amaro Aviation - Sistema de Análise de Custos",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Profissional
def load_professional_css():
    st.markdown("""
    <style>
    /* === AMARO AVIATION PROFESSIONAL PLATFORM === */
    
    /* Header Corporativo */
    .corporate-header {
        background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(140, 29, 64, 0.2);
    }
    
    /* Cards de Análise */
    .analysis-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .analysis-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.12);
    }
    
    /* Métricas */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        border-left: 4px solid #8c1d40;
        text-align: center;
    }
    
    /* Status System */
    .status-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #27AE60;
    }
    
    /* Navegação */
    .nav-button {
        background: white;
        border: 2px solid #8c1d40;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .nav-button:hover {
        background: #8c1d40;
        color: white;
    }
    
    /* Remover elementos desnecessários */
    .stAlert {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
    }
    
    /* Ajustes de espaçamento */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

load_professional_css()

# Header Corporativo
st.markdown("""
<div class="corporate-header">
    <h1 style="margin:0; font-size: 2.5rem;">✈️ Amaro Aviation</h1>
    <p style="margin:0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
        Sistema de Análise de Custos Operacionais
    </p>
</div>
""", unsafe_allow_html=True)

# Carregamento de dados
with st.spinner('Carregando sistema...'):
    try:
        params = load_params()
        modelos = list(params.get('modelos_disponiveis', []))
        
        if not modelos:
            st.error("⚠️ Nenhum modelo encontrado. Configure os modelos em data/modelos.csv")
            st.stop()
            
    except Exception as e:
        st.error(f"❌ Erro ao carregar parâmetros: {e}")
        st.stop()

# Status do Sistema
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="status-box">
        <h4 style="margin:0;">🟢 Sistema</h4>
        <p style="margin:0;">Operacional</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.metric("✈️ Modelos Ativos", len(modelos))

with col3:
    st.metric("⛽ Combustível", f"R$ {params['preco_combustivel']:.2f}/L")

with col4:
    st.metric("📅 Última Atualização", datetime.now().strftime('%d/%m %H:%M'))

# Módulos Disponíveis
st.markdown("## 📊 Módulos de Análise")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="analysis-card">
        <h3>✈️ Custo por Trecho</h3>
        <p>Análise detalhada de custos para rotas específicas com breakdown completo.</p>
        <ul>
            <li>Cálculo preciso por componente</li>
            <li>Comparação com mercado</li>
            <li>Exportação em PDF/Excel</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Acessar Análise de Trecho", use_container_width=True, key="btn_trecho"):
        st.switch_page("pages/1_Custo_por_Trecho.py")
    
    st.markdown("""
    <div class="analysis-card">
        <h3>📈 Projeções Mensais</h3>
        <p>Projeções de rentabilidade e análise de cenários operacionais.</p>
        <ul>
            <li>Simulação de lucros mensais</li>
            <li>Análise de sensibilidade</li>
            <li>ROI e break-even</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Acessar Projeções", use_container_width=True, key="btn_projecoes"):
        st.switch_page("pages/2_Lucros_Mensais.py")

with col2:
    st.markdown("""
    <div class="analysis-card">
        <h3>🎯 Planejamento de Metas</h3>
        <p>Definição e análise de viabilidade de metas de receita.</p>
        <ul>
            <li>Cálculo de horas necessárias</li>
            <li>Análise de viabilidade</li>
            <li>Estratégias de crescimento</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Acessar Planejamento", use_container_width=True, key="btn_metas"):
        st.switch_page("pages/3_Meta_de_Receita.py")
    
    st.markdown("""
    <div class="analysis-card">
        <h3>📊 Análise Comparativa</h3>
        <p>Comparação detalhada com mercado e análise de TCO.</p>
        <ul>
            <li>Benchmarking competitivo</li>
            <li>Análise de economia anual</li>
            <li>Cenários comparativos</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Acessar Comparativo", use_container_width=True, key="btn_comparativo"):
        st.switch_page("pages/4_Comparativo_Economia.py")

# Demonstração Rápida
st.markdown("---")
st.markdown("## 🚀 Demonstração Rápida")

demo_col1, demo_col2, demo_col3 = st.columns([1, 1, 1])

with demo_col1:
    modelo_demo = st.selectbox("Modelo", modelos)

with demo_col2:
    duracao_demo = st.number_input("Duração (h)", min_value=0.5, max_value=10.0, value=1.5, step=0.5)

with demo_col3:
    st.write("") # Espaçamento
    if st.button("Calcular", type="primary", use_container_width=True):
        resultado = calcula_custo_trecho(modelo_demo, duracao_demo, params)
        
        col_res1, col_res2, col_res3, col_res4 = st.columns(4)
        
        with col_res1:
            st.metric("Custo Amaro", f"R$ {resultado['total']:,.0f}")
        
        with col_res2:
            st.metric("Preço Mercado", f"R$ {resultado['preco_mercado']:,.0f}")
        
        with col_res3:
            st.metric("Economia", f"R$ {resultado['economia']:,.0f}")
        
        with col_res4:
            st.metric("Economia %", f"{resultado['percentual_economia']:.1f}%")

# Gráfico de Performance
if modelos:
    st.markdown("---")
    st.markdown("## 📊 Performance dos Modelos")
    
    # Criar dados para o gráfico
    performance_data = []
    for modelo in modelos[:5]:  # Limitar a 5 modelos para visualização
        if modelo in params.get('consumo_modelos', {}):
            resultado = calcula_custo_trecho(modelo, 1.0, params)
            performance_data.append({
                'Modelo': modelo,
                'Custo/Hora': resultado['total'],
                'Mercado/Hora': params['preco_mercado_hora'][modelo],
                'Economia/Hora': resultado['economia']
            })
    
    if performance_data:
        df_perf = pd.DataFrame(performance_data)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Custo Amaro',
            x=df_perf['Modelo'],
            y=df_perf['Custo/Hora'],
            marker_color='#8c1d40'
        ))
        
        fig.add_trace(go.Bar(
            name='Preço Mercado',
            x=df_perf['Modelo'],
            y=df_perf['Mercado/Hora'],
            marker_color='#95A5A6'
        ))
        
        fig.update_layout(
            title='Comparativo de Custos por Hora',
            barmode='group',
            yaxis_title='Valor (R$/hora)',
            template='plotly_white',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Sidebar - Navegação e Informações
with st.sidebar:
    # Logo ou identificação
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px; margin-bottom: 1rem;">
        <h2 style="margin: 0; color: #8c1d40;">✈️</h2>
        <p style="margin: 0; color: #8c1d40; font-weight: bold;">Amaro Aviation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navegação Rápida
    st.markdown("### 🗂️ Navegação Rápida")
    
    paginas = {
        "📊 Dashboard": "app.py",
        "✈️ Custo por Trecho": "pages/1_Custo_por_Trecho.py",
        "📈 Lucros Mensais": "pages/2_Lucros_Mensais.py",
        "🎯 Meta de Receita": "pages/3_Meta_de_Receita.py",
        "📊 Comparativo": "pages/4_Comparativo_Economia.py",
        "⚙️ Configurações": "pages/5_Configurações.py",
        "🎨 Modo Apresentação": "pages/6_Modo_Cliente.py"
    }
    
    for nome, pagina in paginas.items():
        if st.button(nome, use_container_width=True):
            if pagina != "app.py":
                st.switch_page(pagina)
    
    # Informações do Sistema
    st.markdown("---")
    st.markdown("### ℹ️ Informações")
    
    st.info(f"""
    **Versão:** 2.0  
    **Modelos:** {len(modelos)}  
    **Parâmetros:** Atualizados  
    **Build:** {hash(str(datetime.now().date())) % 10000}
    """)
    
    # Ações Rápidas
    st.markdown("### ⚡ Ações Rápidas")
    
    if st.button("🔄 Recarregar Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    if st.button("📥 Backup Parâmetros", use_container_width=True):
        st.info("Use a página de Configurações para backup completo")
    
    # Ajuda
    st.markdown("---")
    st.markdown("### 📘 Ajuda")
    st.markdown("""
    **Uso do Sistema:**
    1. Selecione o módulo desejado
    2. Configure os parâmetros
    3. Execute a análise
    4. Exporte os resultados
    
    **Para demonstrações:**
    Use o Modo Apresentação
    """)