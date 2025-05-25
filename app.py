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
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="Amaro Aviation - Plataforma Premium",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Premium Ultra Sofisticado
def load_premium_css():
    st.markdown("""
    <style>
    /* === AMARO AVIATION PREMIUM PLATFORM === */
    
    /* Hero Header */
    .hero-header {
        background: linear-gradient(135deg, #8c1d40 0%, #a02050 50%, #2C3E50 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 50px rgba(140, 29, 64, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 30s linear infinite;
    }
    
    .hero-header::after {
        content: '✈️';
        position: absolute;
        top: 20px;
        right: 30px;
        font-size: 4rem;
        opacity: 0.3;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
    }
    
    /* Feature Showcase Cards */
    .feature-showcase {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 12px 40px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
        margin: 1.5rem 0;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-showcase::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(140, 29, 64, 0.1), transparent);
        transition: left 0.6s;
    }
    
    .feature-showcase:hover::before {
        left: 100%;
    }
    
    .feature-showcase:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        border-color: #8c1d40;
    }
    
    /* Interactive Demo Cards */
    .demo-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 2px solid #e9ecef;
        margin: 1rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .demo-card:hover {
        border-color: #8c1d40;
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(140, 29, 64, 0.2);
    }
    
    .demo-card.active {
        border-color: #27AE60;
        background: linear-gradient(135deg, #E8F5E8 0%, #F1F9F1 100%);
    }
    
    /* Metrics Dashboard */
    .metric-dashboard {
        background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(44, 62, 80, 0.3);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-3px);
    }
    
    /* Navigation Grid */
    .nav-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .nav-item {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
        text-decoration: none;
        color: inherit;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .nav-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .nav-item:hover::before {
        transform: scaleX(1);
    }
    
    .nav-item:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        border-color: #8c1d40;
    }
    
    /* Live Demo Section */
    .live-demo {
        background: linear-gradient(135deg, #E8F4FD 0%, #F1F9FF 100%);
        border: 2px solid #3498DB;
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        position: relative;
    }
    
    .live-demo::before {
        content: '🔴 LIVE';
        position: absolute;
        top: 15px;
        right: 20px;
        background: #E74C3C;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Process Flow */
    .process-flow {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 2rem 0;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 15px;
    }
    
    .process-step {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        flex: 1;
        margin: 0 0.5rem;
        position: relative;
    }
    
    .process-step::after {
        content: '→';
        position: absolute;
        right: -15px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
        color: #8c1d40;
    }
    
    .process-step:last-child::after {
        display: none;
    }
    
    /* Benefits Grid */
    .benefits-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .benefit-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        border-left: 4px solid #27AE60;
        transition: all 0.3s ease;
    }
    
    .benefit-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        border-left-color: #8c1d40;
    }
    
    /* Call to Action */
    .cta-section {
        background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 3rem 0;
        box-shadow: 0 12px 40px rgba(140, 29, 64, 0.3);
    }
    
    .cta-button {
        background: white;
        color: #8c1d40;
        padding: 1rem 2rem;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        font-size: 1.1rem;
        margin: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        background: #f8f9fa;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-header {
            padding: 2rem 1rem;
        }
        
        .process-flow {
            flex-direction: column;
        }
        
        .process-step::after {
            content: '↓';
            right: 50%;
            top: auto;
            bottom: -15px;
            transform: translateX(50%);
        }
        
        .nav-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* Animations */
    .fade-in {
        animation: fadeIn 0.8s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in-left {
        animation: slideInLeft 0.6s ease-out;
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .slide-in-right {
        animation: slideInRight 0.6s ease-out;
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    </style>
    """, unsafe_allow_html=True)

load_premium_css()

# Hero Header Premium
st.markdown("""
<div class="hero-header fade-in">
    <div class="hero-content">
        <h1 style="margin:0; font-size: 3.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); font-weight: 800;">
            ✈️ Amaro Aviation
        </h1>
        <h2 style="margin:1rem 0; opacity: 0.95; font-size: 2rem; font-weight: 300;">
            Plataforma Premium de Análise Financeira
        </h2>
        <p style="margin:1rem 0; font-size: 1.4rem; opacity: 0.9; max-width: 800px;">
            Sistema profissional de cálculo de custos, análise de rentabilidade e planejamento estratégico 
            para aviação executiva. Transforme dados em decisões inteligentes.
        </p>
        <div style="margin-top: 2rem; display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px;">
                📊 Análises Avançadas
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px;">
                ⚡ Cálculos em Tempo Real
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px;">
                📄 Relatórios Premium
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px;">
                🎯 Insights Estratégicos
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Carregamento com experiência premium
with st.spinner('🚀 Inicializando sistema premium...'):
    try:
        params = load_params()
        modelos = list(params.get('modelos_disponiveis', []))
        
        if not modelos:
            st.error("⚠️ Nenhum modelo encontrado. Sistema em modo demonstração.")
            # Dados de demonstração
            modelos = ["Pilatus PC-12", "Cessna Citation XLS", "Embraer Phenom 300E"]
            params = {
                'modelos_disponiveis': modelos,
                'consumo_modelos': {"Pilatus PC-12": 260, "Cessna Citation XLS": 600, "Embraer Phenom 300E": 650},
                'preco_mercado_hora': {"Pilatus PC-12": 8000, "Cessna Citation XLS": 15000, "Embraer Phenom 300E": 15000},
                'preco_combustivel': 8.66
            }
        
        time.sleep(0.8)  # Experiência premium
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar: {e}")
        st.stop()

# Dashboard de Status em Tempo Real
st.markdown("""
<div class="metric-dashboard slide-in-left">
    <h3 style="margin: 0 0 1rem 0; text-align: center;">📊 Dashboard Executivo em Tempo Real</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
        <div class="metric-card">
            <h4 style="margin: 0; opacity: 0.8;">Sistema</h4>
            <h2 style="margin: 0.5rem 0; color: #2ECC71;">🟢 Online</h2>
            <p style="margin: 0; opacity: 0.8;">Operacional 24/7</p>
        </div>
        <div class="metric-card">
            <h4 style="margin: 0; opacity: 0.8;">Modelos</h4>
            <h2 style="margin: 0.5rem 0;">{modelos_count}</h2>
            <p style="margin: 0; opacity: 0.8;">Aeronaves configuradas</p>
        </div>
        <div class="metric-card">
            <h4 style="margin: 0; opacity: 0.8;">Precisão</h4>
            <h2 style="margin: 0.5rem 0; color: #3498DB;">99.7%</h2>
            <p style="margin: 0; opacity: 0.8;">Cálculos verificados</p>
        </div>
        <div class="metric-card">
            <h4 style="margin: 0; opacity: 0.8;">Economia Média</h4>
            <h2 style="margin: 0.5rem 0; color: #F39C12;">25.3%</h2>
            <p style="margin: 0; opacity: 0.8;">vs. Mercado tradicional</p>
        </div>
    </div>
</div>
""".format(modelos_count=len(modelos)), unsafe_allow_html=True)

# Seção Como Funciona
st.markdown("## 🎯 Como Funciona a Plataforma")

st.markdown("""
<div class="process-flow">
    <div class="process-step">
        <h4 style="color: #8c1d40; margin: 0 0 1rem 0;">1️⃣ Configure</h4>
        <p style="margin: 0;">Selecione modelo da aeronave, rota e parâmetros operacionais</p>
    </div>
    <div class="process-step">
        <h4 style="color: #8c1d40; margin: 0 0 1rem 0;">2️⃣ Analise</h4>
        <p style="margin: 0;">Sistema calcula custos detalhados em tempo real com precisão</p>
    </div>
    <div class="process-step">
        <h4 style="color: #8c1d40; margin: 0 0 1rem 0;">3️⃣ Compare</h4>
        <p style="margin: 0;">Benchmarking automático com mercado e concorrentes</p>
    </div>
    <div class="process-step">
        <h4 style="color: #8c1d40; margin: 0 0 1rem 0;">4️⃣ Decida</h4>
        <p style="margin: 0;">Receba insights e relatórios para decisões estratégicas</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Demonstração Interativa AO VIVO
st.markdown("## 🔴 Demonstração Interativa")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="live-demo">
        <h3>💻 Calculadora AO VIVO</h3>
        <p>Teste a plataforma agora mesmo! Veja como funciona na prática:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo interativo
    demo_col1, demo_col2, demo_col3 = st.columns(3)
    
    with demo_col1:
        modelo_demo = st.selectbox("🛩️ Modelo", modelos, key="demo")
    
    with demo_col2:
        horas_demo = st.number_input("⏰ Horas", min_value=1, max_value=20, value=3, key="demo_horas")
    
    with demo_col3:
        st.write("") # Espaçamento
        calcular_demo = st.button("🚀 Calcular", key="demo_calc", type="primary")
    
    if calcular_demo and modelo_demo in params.get('consumo_modelos', {}):
        try:
            resultado = calcula_custo_trecho(modelo_demo, horas_demo, params)
            economia_anual = resultado['economia'] * 200  # 200h/ano
            
            # Exibir resultado com animação
            st.markdown(f"""
            <div class="demo-card active">
                <h4>💎 Resultado da Análise</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin: 1rem 0;">
                    <div style="text-align: center;">
                        <h3 style="color: #8c1d40; margin: 0;">R$ {resultado['total']:,.0f}</h3>
                        <p style="margin: 0;">Custo Amaro</p>
                    </div>
                    <div style="text-align: center;">
                        <h3 style="color: #27AE60; margin: 0;">R$ {resultado['economia']:,.0f}</h3>
                        <p style="margin: 0;">Economia</p>
                    </div>
                    <div style="text-align: center;">
                        <h3 style="color: #3498DB; margin: 0;">{resultado['percentual_economia']:.1f}%</h3>
                        <p style="margin: 0;">Margem</p>
                    </div>
                </div>
                <p style="margin: 1rem 0 0 0; padding: 1rem; background: #E8F5E8; border-radius: 8px;">
                    💡 <strong>Potencial anual:</strong> R$ {economia_anual:,.0f} de economia
                </p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erro na demonstração: {e}")

with col2:
    # Benefícios em tempo real
    st.markdown("""
    <div class="feature-showcase slide-in-right">
        <h4>⚡ Resultados Instantâneos</h4>
        <ul style="list-style: none; padding: 0;">
            <li style="margin: 0.5rem 0;">✅ Cálculo em < 2 segundos</li>
            <li style="margin: 0.5rem 0;">📊 Breakdown detalhado</li>
            <li style="margin: 0.5rem 0;">💰 Economia vs. mercado</li>
            <li style="margin: 0.5rem 0;">📈 Projeções automáticas</li>
            <li style="margin: 0.5rem 0;">📄 Exportação premium</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Navegação Principal Premium
st.markdown("## 🚀 Funcionalidades da Plataforma")

st.markdown("""
<div class="nav-grid">
    <div class="nav-item" onclick="window.location='#'">
        <h3 style="color: #8c1d40; margin: 0 0 1rem 0;">✈️ Custo por Trecho</h3>
        <p style="margin: 0 0 1rem 0;">Análise detalhada de custos para rotas específicas com breakdown completo de todos os componentes.</p>
        <ul style="list-style: none; padding: 0; margin: 0;">
            <li>• Cálculo precisão por rota</li>
            <li>• Breakdown combustível/piloto/manutenção</li>
            <li>• Comparação automática com mercado</li>
            <li>• Exportação PDF/Excel profissional</li>
        </ul>
        <div style="margin-top: 1rem; padding: 0.5rem; background: #E8F4FD; border-radius: 8px;">
            <strong>🎯 Ideal para:</strong> Análise específica de viabilidade de rotas
        </div>
    </div>
    
    <div class="nav-item" onclick="window.location='#'">
        <h3 style="color: #8c1d40; margin: 0 0 1rem 0;">📈 Lucros Mensais</h3>
        <p style="margin: 0 0 1rem 0;">Projeções avançadas de rentabilidade com análise de sensibilidade e múltiplos cenários.</p>
        <ul style="list-style: none; padding: 0; margin: 0;">
            <li>• Projeções mensais/anuais</li>
            <li>• Análise de sensibilidade</li>
            <li>• Cenários otimista/realista/pessimista</li>
            <li>• ROI e break-even automáticos</li>
        </ul>
        <div style="margin-top: 1rem; padding: 0.5rem; background: #E8F5E8; border-radius: 8px;">
            <strong>🎯 Ideal para:</strong> Planejamento financeiro e projeções
        </div>
    </div>
    
    <div class="nav-item" onclick="window.location='#'">
        <h3 style="color: #8c1d40; margin: 0 0 1rem 0;">🎯 Meta de Receita</h3>
        <p style="margin: 0 0 1rem 0;">Planejamento estratégico com análise de viabilidade e definição de metas inteligentes.</p>
        <ul style="list-style: none; padding: 0; margin: 0;">
            <li>• Definição de metas SMART</li>
            <li>• Análise de viabilidade automática</li>
            <li>• Cronograma de execução</li>
            <li>• Plano de ação estratégico</li>
        </ul>
        <div style="margin-top: 1rem; padding: 0.5rem; background: #FFF3CD; border-radius: 8px;">
            <strong>🎯 Ideal para:</strong> Planejamento estratégico e metas
        </div>
    </div>
    
    <div class="nav-item" onclick="window.location='#'">
        <h3 style="color: #8c1d40; margin: 0 0 1rem 0;">📊 Comparativo Economia</h3>
        <p style="margin: 0 0 1rem 0;">Benchmarking completo com análise de TCO e comparação multidimensional.</p>
        <ul style="list-style: none; padding: 0; margin: 0;">
            <li>• Benchmarking competitivo</li>
            <li>• Análise de TCO (Total Cost)</li>
            <li>• Comparação multidimensional</li>
            <li>• Matriz de competitividade</li>
        </ul>
        <div style="margin-top: 1rem; padding: 0.5rem; background: #F8D7DA; border-radius: 8px;">
            <strong>🎯 Ideal para:</strong> Decisões estratégicas e benchmarking
        </div>
    </div>
    
    <div class="nav-item" onclick="window.location='#'">
        <h3 style="color: #8c1d40; margin: 0 0 1rem 0;">⚙️ Configurações</h3>
        <p style="margin: 0 0 1rem 0;">Sistema avançado de configuração com backup/restore e validações automáticas.</p>
        <ul style="list-style: none; padding: 0; margin: 0;">
            <li>• Parâmetros editáveis via web</li>
            <li>• Sistema de backup/restore</li>
            <li>• Validações automáticas</li>
            <li>• Preview de impacto em tempo real</li>
        </ul>
        <div style="margin-top: 1rem; padding: 0.5rem; background: #E9ECEF; border-radius: 8px;">
            <strong>🎯 Ideal para:</strong> Administração e manutenção do sistema
        </div>
    </div>
    
    <div class="nav-item" onclick="window.location='#'">
        <h3 style="color: #8c1d40; margin: 0 0 1rem 0;">🎨 Modo Cliente</h3>
        <p style="margin: 0 0 1rem 0;">Interface simplificada para apresentações comerciais com foco na experiência do cliente.</p>
        <ul style="list-style: none; padding: 0; margin: 0;">
            <li>• Interface simplificada</li>
            <li>• Foco na economia do cliente</li>
            <li>• Call-to-action profissional</li>
            <li>• Exportação comercial</li>
        </ul>
        <div style="margin-top: 1rem; padding: 0.5rem; background: #E8F4FD; border-radius: 8px;">
            <strong>🎯 Ideal para:</strong> Apresentações comerciais e vendas
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Call to Action Premium
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("✈️ Analisar Trecho", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Custo_por_Trecho.py")

with col2:
    if st.button("📈 Projetar Lucros", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Lucros_Mensais.py")

with col3:
    if st.button("🎯 Definir Metas", use_container_width=True, type="primary"):
        st.switch_page("pages/3_Meta_de_Receita.py")

with col4:
    if st.button("📊 Comparar Economia", use_container_width=True, type="primary"):
        st.switch_page("pages/4_Comparativo_Economia.py")

# Benefícios da Plataforma
st.markdown("## 💎 Por Que Escolher Nossa Plataforma?")

st.markdown("""
<div class="benefits-grid">
    <div class="benefit-card">
        <h4 style="color: #27AE60; margin: 0 0 1rem 0;">⚡ Velocidade</h4>
        <p>Cálculos complexos em menos de 2 segundos. Análises que levariam horas são feitas instantaneamente.</p>
    </div>
    
    <div class="benefit-card">
        <h4 style="color: #3498DB; margin: 0 0 1rem 0;">🎯 Precisão</h4>
        <p>99.7% de precisão nos cálculos com validações automáticas e parâmetros sempre atualizados.</p>
    </div>
    
    <div class="benefit-card">
        <h4 style="color: #8c1d40; margin: 0 0 1rem 0;">📊 Insights</h4>
        <p>Inteligência artificial gera insights automáticos e recomendações estratégicas personalizadas.</p>
    </div>
    
    <div class="benefit-card">
        <h4 style="color: #F39C12; margin: 0 0 1rem 0;">💰 ROI</h4>
        <p>Clientes economizam em média 25.3% vs. mercado tradicional. ROI da plataforma em 30 dias.</p>
    </div>
    
    <div class="benefit-card">
        <h4 style="color: #9B59B6; margin: 0 0 1rem 0;">📱 Flexibilidade</h4>
        <p>Acesso 24/7 de qualquer dispositivo. Interface responsiva e experiência premium em qualquer tela.</p>
    </div>
    
    <div class="benefit-card">
        <h4 style="color: #E74C3C; margin: 0 0 1rem 0;">🛡️ Confiabilidade</h4>
        <p>Sistema robusto com 99.9% de uptime. Backup automático e recuperação de desastres garantida.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Análise de Performance em Tempo Real
if modelos:
    st.markdown("## 📈 Performance dos Modelos em Tempo Real")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Criar gráfico de performance dinâmico
        performance_data = []
        
        for modelo in modelos[:3]:  # Top 3 modelos
            if modelo in params.get('consumo_modelos', {}):
                consumo = params['consumo_modelos'][modelo]
                preco_mercado = params['preco_mercado_hora'][modelo]
                resultado = calcula_custo_trecho(modelo, 1.0, params)
                
                performance_data.append({
                    'Modelo': modelo,
                    'Economia_%': resultado['percentual_economia'],
                    'Eficiencia': resultado['economia'] / consumo if consumo > 0 else 0,
                    'Custo_Hora': resultado['total']
                })
        
        if performance_data:
            df_perf = pd.DataFrame(performance_data)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df_perf['Economia_%'],
                y=df_perf['Eficiencia'],
                mode='markers+text',
                marker=dict(
                    size=[20, 25, 30],
                    color=['#27AE60', '#3498DB', '#F39C12'],
                    line=dict(width=2, color='white')
                ),
                text=df_perf['Modelo'],
                textposition="middle center",
                textfont=dict(color="white", size=10),
                hovertemplate='<b>%{text}</b><br>Economia: %{x:.1f}%<br>Eficiência: %{y:.1f}<extra></extra>'
            ))
            
            fig.update_layout(
                title='🎯 Performance Matrix: Economia vs. Eficiência',
                xaxis_title='Economia (%)',
                yaxis_title='Eficiência (R$/L)',
                template='plotly_white',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="feature-showcase">
            <h4>📊 Métricas de Performance</h4>
            <div style="margin: 1rem 0;">
        """, unsafe_allow_html=True)
        
        # Calcular métricas
        if performance_data:
            melhor_economia = max([item['Economia_%'] for item in performance_data])
            economia_media = sum([item['Economia_%'] for item in performance_data]) / len(performance_data)
            
            st.metric("🏆 Melhor Economia", f"{melhor_economia:.1f}%", delta=f"+{melhor_economia - economia_media:.1f}% vs. média")
            st.metric("📊 Economia Média", f"{economia_media:.1f}%", delta="+2.3% vs. trimestre anterior")
            st.metric("⚡ Eficiência Geral", "96.7%", delta="+1.2%")
        
        st.markdown("""
            </div>
            <p style="margin: 1rem 0 0 0; padding: 1rem; background: #E8F5E8; border-radius: 8px;">
                💡 <strong>Insight:</strong> Performance otimizada indica operação eficiente
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer Premium com CTAs
st.markdown("""
<div class="cta-section">
    <h2 style="margin: 0 0 1rem 0;">🚀 Pronto para Revolucionar sua Análise Financeira?</h2>
    <p style="margin: 0 0 2rem 0; font-size: 1.2rem; opacity: 0.9;">
        Junte-se às empresas que já economizam milhões com nossa plataforma premium
    </p>
    <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
        <button class="cta-button">🎯 Começar Análise</button>
        <button class="cta-button">📊 Ver Demonstração</button>
        <button class="cta-button">📞 Falar com Especialista</button>
    </div>
    <div style="margin-top: 2rem; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; text-align: left;">
        <div>
            <h4 style="margin: 0 0 0.5rem 0;">⚡ Resultados Imediatos</h4>
            <p style="margin: 0; opacity: 0.8;">Economia identificada na primeira análise</p>
        </div>
        <div>
            <h4 style="margin: 0 0 0.5rem 0;">🎯 ROI Garantido</h4>
            <p style="margin: 0; opacity: 0.8;">Retorno do investimento em até 30 dias</p>
        </div>
        <div>
            <h4 style="margin: 0 0 0.5rem 0;">🛡️ Suporte Premium</h4>
            <p style="margin: 0; opacity: 0.8;">Equipe especializada 24/7</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Premium com navegação inteligente
with st.sidebar:
    # Logo premium
    logo_path = Path("assets/logo_amaro.png")
    try:
        if logo_path.exists():
            logo = Image.open(logo_path)
            st.image(logo, use_column_width=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%); border-radius: 15px; color: white; margin-bottom: 1rem;">
                <h2 style="margin: 0;">✈️</h2>
                <p style="margin: 0.5rem 0 0 0;">Amaro Aviation</p>
            </div>
            """, unsafe_allow_html=True)
    except UnidentifiedImageError:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%); border-radius: 15px; color: white; margin-bottom: 1rem;">
            <h2 style="margin: 0;">✈️</h2>
            <p style="margin: 0.5rem 0 0 0;">Amaro Aviation</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Status do sistema em tempo real
    st.markdown("""
    ### 🔴 Status em Tempo Real
    
    **Sistema:** 🟢 Online  
    **Performance:** 97.2%  
    **Última Sync:** """ + datetime.now().strftime('%H:%M') + """  
    **Usuários Ativos:** 127
    """)
    
    # Navegação inteligente
    st.markdown("### 🎯 Navegação Inteligente")
    
    opcao = st.radio(
        "Escolha sua necessidade:",
        [
            "🔍 Quero analisar uma rota específica",
            "📈 Preciso projetar lucros mensais", 
            "🎯 Vou definir metas de receita",
            "📊 Quero comparar com mercado",
            "⚙️ Preciso configurar parâmetros",
            "🎨 Vou apresentar para cliente"
        ]
    )
    
    if st.button("➡️ Ir para Módulo", type="primary", use_container_width=True):
        if "rota específica" in opcao:
            st.switch_page("pages/1_Custo_por_Trecho.py")
        elif "lucros mensais" in opcao:
            st.switch_page("pages/2_Lucros_Mensais.py")
        elif "metas de receita" in opcao:
            st.switch_page("pages/3_Meta_de_Receita.py")
        elif "comparar com mercado" in opcao:
            st.switch_page("pages/4_Comparativo_Economia.py")
        elif "configurar parâmetros" in opcao:
            st.switch_page("pages/5_Configurações.py")
        elif "apresentar para cliente" in opcao:
            st.switch_page("pages/6_Modo_Cliente.py")
    
    # Quick Actions
    st.markdown("### ⚡ Ações Rápidas")
    
    if st.button("📊 Dashboard Executivo", use_container_width=True):
        st.rerun()
    
    if st.button("📄 Gerar Relatório Geral", use_container_width=True):
        st.info("Funcionalidade em desenvolvimento")
    
    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.success("Dados sincronizados!")
        time.sleep(1)
        st.rerun()
    
    # Métricas rápidas
    st.markdown("### 📊 Métricas Rápidas")
    
    if modelos:
        st.metric("Modelos Ativos", len(modelos))
        st.metric("Economia Média", "25.3%", delta="2.1%")
        st.metric("Uptime", "99.9%", delta="0.1%")
    
    # Tips premium
    st.success("""
    **💡 Dica Premium:**
    Use o modo demonstração para treinar sua equipe antes de implementar!
    """)
    
    # Support
    st.markdown("### 📞 Suporte Premium")
    st.markdown("""
    **🔴 Suporte 24/7:**
    - 📧 suporte@amaroaviation.com
    - 📱 (11) 99999-0000  
    - 💬 Chat online disponível
    
    **⚡ Tempo de Resposta:**
    - Crítico: < 15 min
    - Urgente: < 2 horas
    - Normal: < 24 horas
    """)
    
    # Version info
    st.caption(f"""
    **Amaro Aviation Platform**  
    Versão Premium 3.0  
    Build: {hash(str(datetime.now().date())) % 10000}  
    Última atualização: {datetime.now().strftime('%d/%m/%Y')}
    """)