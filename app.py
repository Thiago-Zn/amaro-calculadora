import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
from pathlib import Path
import json
from io import BytesIO

# Imports locais
from utils.params import load_params, save_params, format_currency, format_percentage
from utils.calculations import calcula_custo_trecho, calcular_projecao_mensal
from utils.exportador_excel import criar_relatorio_dados, gerar_excel_simples
from utils.exportador_pdf import gerar_pdf

# ========================================================================
# CONFIGURAÇÃO DA PÁGINA
# ========================================================================
st.set_page_config(
    page_title="Amaro Aviation - Simulador Estratégico de Custos",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================================================
# ESTILOS CSS ALINHADOS À IDENTIDADE VISUAL AMARO
# ========================================================================
def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Configurações globais */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #FFFFFF;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #8C1D40 0%, #A02050 100%);
        color: white;
        padding: 3rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    /* Cards de métricas */
    .metric-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .metric-card-value {
        font-size: 2rem;
        font-weight: 700;
        color: #8C1D40;
        margin: 0.5rem 0;
    }
    
    .metric-card-label {
        font-size: 0.875rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Tabelas customizadas */
    .comparison-table {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .comparison-table th {
        background: #F3F4F6;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
        padding: 1rem;
    }
    
    .comparison-table td {
        padding: 1rem;
        border-bottom: 1px solid #E5E7EB;
    }
    
    /* Botões personalizados */
    .stButton > button {
        background: #8C1D40;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #A02050;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(140, 29, 64, 0.3);
    }
    
    /* Tabs estilizadas */
    .stTabs [data-baseweb="tab-list"] {
        background: #F9FAFB;
        border-radius: 12px;
        padding: 0.25rem;
        gap: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: #8C1D40;
        color: white;
    }
    
    /* Sidebar refinada */
    .css-1d391kg {
        background: #F9FAFB;
    }
    
    /* Métricas de destaque */
    .highlight-metric {
        background: linear-gradient(135deg, #8C1D40 0%, #A02050 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .highlight-metric h3 {
        font-size: 1.5rem;
        margin: 0;
    }
    
    .highlight-metric .value {
        font-size: 3rem;
        font-weight: 700;
        margin: 1rem 0;
    }
    
    /* Configurações do data editor */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Ocultar elementos Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ========================================================================
# FUNÇÕES AUXILIARES
# ========================================================================
def create_metric_card(label, value, delta=None, format_type="currency"):
    """Cria um card de métrica customizado"""
    formatted_value = format_currency(value) if format_type == "currency" else format_percentage(value)
    
    delta_html = ""
    if delta is not None:
        delta_color = "#10B981" if delta > 0 else "#EF4444"
        delta_symbol = "▲" if delta > 0 else "▼"
        delta_html = f'<div style="color: {delta_color}; font-size: 0.875rem;">{delta_symbol} {abs(delta):.1f}%</div>'
    
    return f"""
    <div class="metric-card">
        <div class="metric-card-label">{label}</div>
        <div class="metric-card-value">{formatted_value}</div>
        {delta_html}
    </div>
    """

def create_comparison_table(data_proprio, data_amaro, items):
    """Cria tabela comparativa lado a lado"""
    df = pd.DataFrame({
        'Item': items,
        'Gestão Própria': data_proprio,
        'Gestão Amaro': data_amaro,
        'Economia': [p - a for p, a in zip(data_proprio, data_amaro)],
        'Economia %': [(p - a) / p * 100 if p > 0 else 0 for p, a in zip(data_proprio, data_amaro)]
    })
    
    # Formatação
    for col in ['Gestão Própria', 'Gestão Amaro', 'Economia']:
        df[col] = df[col].apply(lambda x: format_currency(x))
    df['Economia %'] = df['Economia %'].apply(lambda x: f"{x:.1f}%")
    
    return df

# ========================================================================
# CARREGAMENTO DE DADOS
# ========================================================================
load_custom_css()

# Sidebar com configurações
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h3 style="color: #8C1D40; margin: 0;">✈️ Amaro Aviation</h3>
        <p style="color: #6B7280; font-size: 0.875rem; margin-top: 0.5rem;">Simulador Estratégico de Custos</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Seleção de idioma
    idioma = st.selectbox(
        "🌐 Idioma / Language",
        ["🇧🇷 Português", "🇺🇸 English"],
        key="language"
    )
    lang = 'pt' if '🇧🇷' in idioma else 'en'

# Header principal
st.markdown("""
<div class="main-header">
    <h1>Simulador Estratégico de Custos Operacionais</h1>
    <p>Demonstre o valor da gestão Amaro Aviation com dados reais e personalizados</p>
</div>
""", unsafe_allow_html=True)

# Carregamento de parâmetros
try:
    params = load_params()
    modelos = params.get('modelos_disponiveis', [])
    
    if not modelos:
        st.error("⚠️ Sistema não configurado. Execute o setup inicial.")
        st.stop()
        
except Exception as e:
    st.error(f"❌ Erro ao carregar sistema: {e}")
    st.stop()

# ========================================================================
# INTERFACE PRINCIPAL - TABS
# ========================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💰 Estimativa de Lucro Mensal",
    "⚖️ Comparativo de Custos", 
    "✈️ Simulador de Rotas",
    "📈 Projeção de Longo Prazo",
    "⚙️ Configurações"
])

# ========================================================================
# TAB 1: ESTIMATIVA DE LUCRO MENSAL
# ========================================================================
with tab1:
    st.markdown("### 💰 Análise de Rentabilidade Mensal com Charter")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        modelo_lucro = st.selectbox(
            "Modelo da Aeronave",
            modelos,
            key="modelo_lucro_tab1"
        )
    
    with col2:
        horas_charter = st.number_input(
            "Horas Disponíveis para Charter/mês",
            min_value=10,
            max_value=200,
            value=80,
            step=10,
            help="Quantidade de horas mensais disponíveis para charter"
        )
    
    with col3:
        taxa_ocupacao = st.slider(
            "Taxa de Ocupação (%)",
            min_value=50,
            max_value=95,
            value=75,
            help="Percentual de ocupação das horas disponíveis"
        )
    
    with col4:
        preco_hora_charter = st.number_input(
            "Preço por Hora Charter (R$)",
            value=float(params['preco_mercado_hora'].get(modelo_lucro, 8000)),
            step=500.0,
            help="Valor cobrado por hora de charter"
        )
    
    if st.button("🚀 Calcular Projeção Mensal", type="primary", use_container_width=True):
        # Cálculos
        horas_efetivas = horas_charter * (taxa_ocupacao / 100)
        receita_bruta = preco_hora_charter * horas_efetivas
        
        # Divisão Amaro (90/10)
        receita_proprietario = receita_bruta * 0.9
        taxa_amaro = receita_bruta * 0.1
        
        # Custos operacionais detalhados
        resultado_hora = calcula_custo_trecho(modelo_lucro, 1.0, params)
        
        custo_combustivel = float(resultado_hora['preco_comb']) * horas_efetivas
        custo_piloto = float(resultado_hora['piloto']) * horas_efetivas
        custo_manutencao = float(resultado_hora['manut']) * horas_efetivas
        custo_depreciacao = float(resultado_hora['depr']) * horas_efetivas
        
        custo_total = custo_combustivel + custo_piloto + custo_manutencao + custo_depreciacao
        lucro_liquido = receita_proprietario - custo_total
        roi_mensal = (lucro_liquido / custo_total * 100) if custo_total > 0 else 0
        
        # Display de resultados
        st.markdown("---")
        st.markdown("### 📊 Resultados da Análise Mensal")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card("Receita Bruta Mensal", receita_bruta), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card("Receita do Proprietário (90%)", receita_proprietario), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card("Lucro Líquido", lucro_liquido, 
                                         delta=roi_mensal if lucro_liquido > 0 else None), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card("ROI Mensal", roi_mensal, format_type="percentage"), unsafe_allow_html=True)
        
        # Breakdown de custos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Composição de Receitas")
            
            fig_receita = go.Figure(data=[go.Pie(
                labels=['Proprietário (90%)', 'Taxa Amaro (10%)'],
                values=[receita_proprietario, taxa_amaro],
                hole=0.5,
                marker=dict(colors=['#10B981', '#8C1D40']),
                textinfo='label+value',
                texttemplate='<b>%{label}</b><br>R$ %{value:,.0f}'
            )])
            
            fig_receita.update_layout(
                height=300,
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig_receita, use_container_width=True)
        
        with col2:
            st.markdown("#### 💸 Breakdown de Custos Operacionais")
            
            custos_detalhados = pd.DataFrame({
                'Item': ['Combustível', 'Piloto', 'Manutenção', 'Depreciação'],
                'Valor': [custo_combustivel, custo_piloto, custo_manutencao, custo_depreciacao],
                'Percentual': [
                    custo_combustivel/custo_total*100,
                    custo_piloto/custo_total*100,
                    custo_manutencao/custo_total*100,
                    custo_depreciacao/custo_total*100
                ]
            })
            
            fig_custos = go.Figure(data=[go.Bar(
                x=custos_detalhados['Percentual'],
                y=custos_detalhados['Item'],
                orientation='h',
                text=[f'R$ {v:,.0f} ({p:.1f}%)' for v, p in zip(custos_detalhados['Valor'], custos_detalhados['Percentual'])],
                textposition='inside',
                marker_color=['#EF4444', '#F59E0B', '#3B82F6', '#10B981']
            )])
            
            fig_custos.update_layout(
                height=300,
                xaxis_title='Percentual do Custo Total',
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig_custos, use_container_width=True)
        
        # Análise de viabilidade
        if lucro_liquido > 0:
            st.success(f"""
            ✅ **Operação Lucrativa**: O proprietário terá um lucro líquido de {format_currency(lucro_liquido)} por mês, 
            representando um ROI de {roi_mensal:.1f}% sobre os custos operacionais.
            """)
        else:
            st.warning(f"""
            ⚠️ **Atenção**: A operação apresenta déficit de {format_currency(abs(lucro_liquido))} mensalmente. 
            Considere ajustar o preço da hora ou aumentar a taxa de ocupação.
            """)

# ========================================================================
# TAB 2: COMPARATIVO DE CUSTOS
# ========================================================================
with tab2:
    st.markdown("### ⚖️ Comparativo: Gestão Própria vs. Gestão Amaro")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        modelo_comp = st.selectbox(
            "Modelo da Aeronave",
            modelos,
            key="modelo_comp_tab2"
        )
    
    with col2:
        horas_anuais = st.number_input(
            "Horas de Voo Anuais",
            min_value=50,
            max_value=800,
            value=300,
            step=25,
            help="Total de horas voadas por ano"
        )
    
    with col3:
        incluir_charter_comp = st.checkbox(
            "Incluir Receita de Charter na Comparação",
            value=True,
            help="Considera a receita de charter como redução de custos"
        )
    
    # Parâmetros de custos fixos
    st.markdown("#### 💼 Custos Fixos Anuais (Gestão Própria)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        custo_hangar = st.number_input(
            "Hangaragem (R$/ano)",
            value=120000,
            step=10000,
            help="Custo anual de hangaragem"
        )
    
    with col2:
        custo_seguro = st.number_input(
            "Seguro (R$/ano)",
            value=250000,
            step=10000,
            help="Custo anual de seguro aeronáutico"
        )
    
    with col3:
        custo_tripulacao = st.number_input(
            "Tripulação Fixa (R$/ano)",
            value=300000,
            step=10000,
            help="Salários e encargos de tripulação dedicada"
        )
    
    with col4:
        custo_admin = st.number_input(
            "Administração (R$/ano)",
            value=50000,
            step=5000,
            help="Custos administrativos e planejamento"
        )
    
    if st.button("📊 Comparar Cenários", type="primary", use_container_width=True):
        # Custos variáveis
        resultado_ano = calcula_custo_trecho(modelo_comp, float(horas_anuais), params)
        
        # GESTÃO PRÓPRIA
        custos_fixos_proprio = custo_hangar + custo_seguro + custo_tripulacao + custo_admin
        custos_variaveis_proprio = float(resultado_ano['total'])
        custo_total_proprio = custos_fixos_proprio + custos_variaveis_proprio
        
        # GESTÃO AMARO
        custos_fixos_amaro = 0  # Amaro assume custos fixos
        custos_variaveis_amaro = float(resultado_ano['total'])
        custo_total_amaro = custos_variaveis_amaro
        
        # Receita de charter (se aplicável)
        receita_charter = 0
        if incluir_charter_comp:
            horas_charter_ano = horas_anuais * 0.3  # 30% das horas para charter
            preco_hora = float(params['preco_mercado_hora'][modelo_comp])
            receita_charter = horas_charter_ano * preco_hora * 0.75  # 75% ocupação
        
        # Custos líquidos
        custo_liquido_proprio = custo_total_proprio - receita_charter
        custo_liquido_amaro = custo_total_amaro - (receita_charter * 0.9)  # Proprietário recebe 90%
        
        economia_anual = custo_liquido_proprio - custo_liquido_amaro
        economia_percentual = (economia_anual / custo_liquido_proprio * 100) if custo_liquido_proprio > 0 else 0
        
        # Display de resultados
        st.markdown("---")
        st.markdown("### 📊 Análise Comparativa Detalhada")
        
        # Cards de resumo
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid #EF4444;">
                <div class="metric-card-label">Custo Total - Gestão Própria</div>
                <div class="metric-card-value" style="color: #EF4444;">{format_currency(custo_liquido_proprio)}</div>
                <div style="font-size: 0.875rem; color: #6B7280;">Incluindo todos os custos fixos e variáveis</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid #10B981;">
                <div class="metric-card-label">Custo Total - Gestão Amaro</div>
                <div class="metric-card-value" style="color: #10B981;">{format_currency(custo_liquido_amaro)}</div>
                <div style="font-size: 0.875rem; color: #6B7280;">Apenas custos operacionais</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="highlight-metric">
                <h3>Economia Anual</h3>
                <div class="value">{format_currency(economia_anual)}</div>
                <div>{economia_percentual:.1f}% de redução de custos</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Tabela comparativa detalhada
        st.markdown("#### 📋 Breakdown Detalhado de Custos")
        
        # Preparar dados para tabela
        items_custos = [
            'Hangaragem',
            'Seguro Aeronáutico',
            'Tripulação Dedicada',
            'Administração/Planejamento',
            'Combustível',
            'Manutenção',
            'Depreciação',
            'Outros Custos Variáveis'
        ]
        
        custos_proprio = [
            custo_hangar,
            custo_seguro,
            custo_tripulacao,
            custo_admin,
            float(resultado_ano['preco_comb']),
            float(resultado_ano['manut']),
            float(resultado_ano['depr']),
            float(resultado_ano['piloto'])
        ]
        
        custos_amaro = [
            0,  # Hangar
            0,  # Seguro
            0,  # Tripulação
            0,  # Admin
            float(resultado_ano['preco_comb']),
            float(resultado_ano['manut']),
            float(resultado_ano['depr']),
            float(resultado_ano['piloto'])
        ]
        
        df_comparativo = create_comparison_table(custos_proprio, custos_amaro, items_custos)
        
        # Adicionar linha de receita de charter
        if incluir_charter_comp:
            receita_row = pd.DataFrame({
                'Item': ['Receita Charter (compensação)'],
                'Gestão Própria': [format_currency(-receita_charter)],
                'Gestão Amaro': [format_currency(-receita_charter * 0.9)],
                'Economia': [''],
                'Economia %': ['']
            })
            df_comparativo = pd.concat([df_comparativo, receita_row], ignore_index=True)
        
        # Adicionar linha de total
        total_row = pd.DataFrame({
            'Item': ['TOTAL LÍQUIDO'],
            'Gestão Própria': [format_currency(custo_liquido_proprio)],
            'Gestão Amaro': [format_currency(custo_liquido_amaro)],
            'Economia': [format_currency(economia_anual)],
            'Economia %': [f"{economia_percentual:.1f}%"]
        })
        df_comparativo = pd.concat([df_comparativo, total_row], ignore_index=True)
        
        # Estilizar dataframe
        st.dataframe(
            df_comparativo,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Item": st.column_config.TextColumn("Item de Custo", width="medium"),
                "Gestão Própria": st.column_config.TextColumn("Gestão Própria", width="small"),
                "Gestão Amaro": st.column_config.TextColumn("Gestão Amaro", width="small"),
                "Economia": st.column_config.TextColumn("Economia", width="small"),
                "Economia %": st.column_config.TextColumn("Economia %", width="small"),
            }
        )
        
        # Gráfico comparativo visual
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Distribuição de Custos - Gestão Própria")
            
            fig_proprio = go.Figure(data=[go.Pie(
                labels=['Custos Fixos', 'Custos Variáveis'],
                values=[custos_fixos_proprio, custos_variaveis_proprio],
                hole=0.5,
                marker=dict(colors=['#EF4444', '#F59E0B']),
                textinfo='label+percent',
                texttemplate='<b>%{label}</b><br>%{percent}'
            )])
            
            fig_proprio.update_layout(
                height=300,
                showlegend=True,
                margin=dict(l=0, r=0, t=20, b=0)
            )
            
            st.plotly_chart(fig_proprio, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Economia Acumulada em 5 Anos")
            
            anos = list(range(1, 6))
            economia_acumulada = [economia_anual * ano for ano in anos]
            
            fig_economia = go.Figure()
            fig_economia.add_trace(go.Bar(
                x=anos,
                y=economia_acumulada,
                text=[format_currency(v) for v in economia_acumulada],
                textposition='outside',
                marker_color='#10B981'
            ))
            
            fig_economia.update_layout(
                height=300,
                xaxis_title='Anos',
                yaxis_title='Economia Acumulada (R$)',
                showlegend=False,
                margin=dict(l=0, r=0, t=20, b=0)
            )
            
            st.plotly_chart(fig_economia, use_container_width=True)

# ========================================================================
# TAB 3: SIMULADOR DE ROTAS
# ========================================================================
with tab3:
    st.markdown("### ✈️ Simulador de Custos por Rota")
    
    # Carregar rotas
    try:
        df_rotas = pd.read_csv('data/rotas.csv')
        rotas_disponiveis = df_rotas.to_dict('records')
    except:
        st.warning("⚠️ Arquivo de rotas não encontrado. Usando rotas padrão.")
        rotas_disponiveis = [
            {"origem": "GRU", "destino": "SDU", "duracao_h": 1.0},
            {"origem": "CGH", "destino": "BSB", "duracao_h": 1.4}
        ]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        origem = st.selectbox(
            "Aeroporto de Origem",
            options=list(set([r['origem'] for r in rotas_disponiveis])),
            key="origem_rota"
        )
    
    with col2:
        # Filtrar destinos baseado na origem
        destinos_validos = [r['destino'] for r in rotas_disponiveis if r['origem'] == origem]
        destino = st.selectbox(
            "Aeroporto de Destino",
            options=destinos_validos,
            key="destino_rota"
        )
    
    with col3:
        modelo_rota = st.selectbox(
            "Modelo da Aeronave",
            modelos,
            key="modelo_rota"
        )
    
    if st.button("✈️ Simular Rota", type="primary", use_container_width=True):
        # Buscar duração da rota
        rota_info = next((r for r in rotas_disponiveis if r['origem'] == origem and r['destino'] == destino), None)
        
        if rota_info:
            duracao = float(rota_info['duracao_h'])
            
            # Calcular custos
            resultado_rota = calcula_custo_trecho(modelo_rota, duracao, params)
            
            # Preço de mercado
            preco_mercado = float(params['preco_mercado_hora'][modelo_rota]) * duracao
            
            # Display de resultados
            st.markdown("---")
            st.markdown(f"### 📊 Análise da Rota: {origem} → {destino}")
            
            # Informações da rota
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(create_metric_card("Duração do Voo", f"{duracao:.1f}h", format_type="text"), unsafe_allow_html=True)
            
            with col2:
                st.markdown(create_metric_card("Custo Total Amaro", float(resultado_rota['total'])), unsafe_allow_html=True)
            
            with col3:
                st.markdown(create_metric_card("Preço de Mercado", preco_mercado), unsafe_allow_html=True)
            
            with col4:
                economia_rota = preco_mercado - float(resultado_rota['total'])
                economia_pct = (economia_rota / preco_mercado * 100) if preco_mercado > 0 else 0
                st.markdown(create_metric_card("Economia", economia_rota, delta=economia_pct), unsafe_allow_html=True)
            
            # Breakdown detalhado
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 💸 Composição de Custos")
                
                custos_rota = {
                    'Combustível': float(resultado_rota['preco_comb']),
                    'Piloto': float(resultado_rota['piloto']),
                    'Manutenção': float(resultado_rota['manut']),
                    'Depreciação': float(resultado_rota['depr'])
                }
                
                fig_custos_rota = go.Figure(data=[go.Pie(
                    labels=list(custos_rota.keys()),
                    values=list(custos_rota.values()),
                    hole=0.5,
                    marker=dict(colors=['#EF4444', '#F59E0B', '#3B82F6', '#10B981']),
                    textinfo='label+value',
                    texttemplate='<b>%{label}</b><br>R$ %{value:,.0f}'
                )])
                
                fig_custos_rota.update_layout(
                    height=350,
                    showlegend=True,
                    margin=dict(l=0, r=0, t=20, b=0)
                )
                
                st.plotly_chart(fig_custos_rota, use_container_width=True)
            
            with col2:
                st.markdown("#### 📊 Comparativo Visual")
                
                fig_comp_rota = go.Figure()
                
                fig_comp_rota.add_trace(go.Bar(
                    x=['Custo Amaro', 'Preço Mercado'],
                    y=[float(resultado_rota['total']), preco_mercado],
                    text=[format_currency(float(resultado_rota['total'])), format_currency(preco_mercado)],
                    textposition='outside',
                    marker_color=['#8C1D40', '#6B7280']
                ))
                
                # Adicionar linha de economia
                fig_comp_rota.add_shape(
                    type="line",
                    x0=-0.4, y0=float(resultado_rota['total']),
                    x1=1.4, y1=float(resultado_rota['total']),
                    line=dict(color="#10B981", width=2, dash="dash")
                )
                
                fig_comp_rota.add_annotation(
                    x=0.5, y=(float(resultado_rota['total']) + preco_mercado) / 2,
                    text=f"Economia: {format_currency(economia_rota)}<br>({economia_pct:.1f}%)",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor="#10B981",
                    font=dict(color="#10B981", size=12, family="Inter")
                )
                
                fig_comp_rota.update_layout(
                    height=350,
                    showlegend=False,
                    yaxis_title="Valor (R$)",
                    margin=dict(l=0, r=0, t=20, b=0)
                )
                
                st.plotly_chart(fig_comp_rota, use_container_width=True)
            
            # Análise de viabilidade
            if economia_rota > 0:
                st.success(f"""
                ✅ **Rota Vantajosa**: A gestão Amaro oferece economia de {format_currency(economia_rota)} ({economia_pct:.1f}%) 
                em relação ao preço de mercado para esta rota.
                """)
            else:
                st.warning(f"""
                ⚠️ **Atenção**: O custo operacional está {format_currency(abs(economia_rota))} acima do preço de mercado. 
                Considere otimizações operacionais para esta rota.
                """)

# ========================================================================
# TAB 4: PROJEÇÃO DE LONGO PRAZO
# ========================================================================
with tab4:
    st.markdown("### 📈 Projeção de Longo Prazo e Análise de Breakeven")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        modelo_proj = st.selectbox(
            "Modelo da Aeronave",
            modelos,
            key="modelo_proj"
        )
    
    with col2:
        horas_mes_proj = st.number_input(
            "Horas de Voo/mês",
            min_value=20,
            max_value=150,
            value=60,
            step=10,
            key="horas_mes_proj"
        )
    
    with col3:
        horizonte_meses = st.slider(
            "Horizonte de Projeção (meses)",
            min_value=12,
            max_value=60,
            value=36,
            step=12,
            key="horizonte_proj"
        )
    
    with col4:
        taxa_crescimento = st.number_input(
            "Crescimento Anual (%)",
            min_value=0.0,
            max_value=20.0,
            value=5.0,
            step=1.0,
            help="Taxa de crescimento anual das horas voadas"
        )
    
    # Parâmetros adicionais
    with st.expander("⚙️ Parâmetros Avançados"):
        col1, col2 = st.columns(2)
        
        with col1:
            investimento_inicial = st.number_input(
                "Investimento Inicial (R$)",
                value=0,
                step=100000,
                help="Valor de entrada ou investimento inicial"
            )
            
            taxa_ocupacao_proj = st.slider(
                "Taxa de Ocupação Charter (%)",
                min_value=50,
                max_value=90,
                value=70,
                key="ocupacao_proj"
            )
        
        with col2:
            inflacao_custos = st.number_input(
                "Inflação de Custos (%/ano)",
                min_value=0.0,
                max_value=15.0,
                value=4.0,
                step=0.5
            )
            
            reajuste_charter = st.number_input(
                "Reajuste Preço Charter (%/ano)",
                min_value=0.0,
                max_value=15.0,
                value=5.0,
                step=0.5
            )
    
    if st.button("📊 Gerar Projeção", type="primary", use_container_width=True):
        # Preparar dados para projeção
        meses = list(range(1, horizonte_meses + 1))
        
        # Arrays para armazenar valores
        receitas_acumuladas = []
        custos_acumulados = []
        lucros_acumulados = []
        fluxo_caixa = []
        
        # Valores iniciais
        horas_mes_atual = horas_mes_proj
        preco_hora_atual = float(params['preco_mercado_hora'][modelo_proj])
        resultado_hora_base = calcula_custo_trecho(modelo_proj, 1.0, params)
        custo_hora_atual = float(resultado_hora_base['total'])
        
        # Considerar investimento inicial
        saldo_acumulado = -investimento_inicial if investimento_inicial > 0 else 0
        
        # Calcular mês a mês
        for mes in meses:
            # Aplicar crescimento anual
            if mes % 12 == 0:
                horas_mes_atual *= (1 + taxa_crescimento / 100)
                preco_hora_atual *= (1 + reajuste_charter / 100)
                custo_hora_atual *= (1 + inflacao_custos / 100)
            
            # Receita mensal
            horas_charter = horas_mes_atual * 0.5  # 50% para charter
            horas_efetivas = horas_charter * (taxa_ocupacao_proj / 100)
            receita_mensal = preco_hora_atual * horas_efetivas * 0.9  # 90% para proprietário
            
            # Custo mensal total
            custo_mensal = custo_hora_atual * horas_mes_atual
            
            # Lucro mensal
            lucro_mensal = receita_mensal - custo_mensal
            
            # Acumulados
            saldo_acumulado += lucro_mensal
            
            receitas_acumuladas.append(receita_mensal)
            custos_acumulados.append(custo_mensal)
            lucros_acumulados.append(lucro_mensal)
            fluxo_caixa.append(saldo_acumulado)
        
        # Encontrar breakeven
        breakeven_mes = None
        for i, valor in enumerate(fluxo_caixa):
            if valor > 0:
                breakeven_mes = i + 1
                break
        
        # Display de resultados
        st.markdown("---")
        st.markdown("### 📊 Análise de Projeção")
        
        # Métricas resumidas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            receita_total = sum(receitas_acumuladas)
            st.markdown(create_metric_card("Receita Total Projetada", receita_total), unsafe_allow_html=True)
        
        with col2:
            custo_total = sum(custos_acumulados)
            st.markdown(create_metric_card("Custo Total Projetado", custo_total), unsafe_allow_html=True)
        
        with col3:
            lucro_total = sum(lucros_acumulados)
            roi_total = (lucro_total / (investimento_inicial if investimento_inicial > 0 else custo_total)) * 100
            st.markdown(create_metric_card("Lucro Total Projetado", lucro_total, delta=roi_total), unsafe_allow_html=True)
        
        with col4:
            if breakeven_mes:
                st.markdown(f"""
                <div class="highlight-metric" style="background: #10B981;">
                    <h3>Breakeven</h3>
                    <div class="value">{breakeven_mes} meses</div>
                    <div>Retorno do investimento</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="highlight-metric" style="background: #EF4444;">
                    <h3>Breakeven</h3>
                    <div class="value">> {horizonte_meses} meses</div>
                    <div>Fora do horizonte</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Gráfico de projeção
        fig_projecao = go.Figure()
        
        # Receitas acumuladas
        receitas_acc = [sum(receitas_acumuladas[:i+1]) for i in range(len(receitas_acumuladas))]
        fig_projecao.add_trace(go.Scatter(
            x=meses,
            y=receitas_acc,
            name='Receita Acumulada',
            mode='lines',
            line=dict(color='#10B981', width=3),
            fill='tonexty',
            fillcolor='rgba(16, 185, 129, 0.1)'
        ))
        
        # Custos acumulados
        custos_acc = [sum(custos_acumulados[:i+1]) for i in range(len(custos_acumulados))]
        fig_projecao.add_trace(go.Scatter(
            x=meses,
            y=custos_acc,
            name='Custo Acumulado',
            mode='lines',
            line=dict(color='#EF4444', width=3)
        ))
        
        # Fluxo de caixa
        fig_projecao.add_trace(go.Scatter(
            x=meses,
            y=fluxo_caixa,
            name='Fluxo de Caixa',
            mode='lines',
            line=dict(color='#8C1D40', width=4),
            fill='tozeroy',
            fillcolor='rgba(140, 29, 64, 0.1)'
        ))
        
        # Linha de breakeven
        if breakeven_mes:
            fig_projecao.add_vline(
                x=breakeven_mes,
                line_dash="dash",
                line_color="#F59E0B",
                annotation_text=f"Breakeven: {breakeven_mes} meses",
                annotation_position="top"
            )
        
        # Linha zero
        fig_projecao.add_hline(
            y=0,
            line_dash="solid",
            line_color="#6B7280",
            line_width=1
        )
        
        fig_projecao.update_layout(
            title="Projeção Financeira de Longo Prazo",
            xaxis_title="Meses",
            yaxis_title="Valor (R$)",
            height=500,
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_projecao, use_container_width=True)
        
        # Tabela de marcos
        st.markdown("#### 📊 Marcos Importantes da Projeção")
        
        marcos_df = pd.DataFrame({
            'Marco': ['6 meses', '12 meses', '24 meses', '36 meses', str(horizonte_meses) + ' meses'],
            'Receita Acumulada': [
                format_currency(sum(receitas_acumuladas[:6])) if len(receitas_acumuladas) >= 6 else 'N/A',
                format_currency(sum(receitas_acumuladas[:12])) if len(receitas_acumuladas) >= 12 else 'N/A',
                format_currency(sum(receitas_acumuladas[:24])) if len(receitas_acumuladas) >= 24 else 'N/A',
                format_currency(sum(receitas_acumuladas[:36])) if len(receitas_acumuladas) >= 36 else 'N/A',
                format_currency(sum(receitas_acumuladas))
            ],
            'Lucro Acumulado': [
                format_currency(sum(lucros_acumulados[:6])) if len(lucros_acumulados) >= 6 else 'N/A',
                format_currency(sum(lucros_acumulados[:12])) if len(lucros_acumulados) >= 12 else 'N/A',
                format_currency(sum(lucros_acumulados[:24])) if len(lucros_acumulados) >= 24 else 'N/A',
                format_currency(sum(lucros_acumulados[:36])) if len(lucros_acumulados) >= 36 else 'N/A',
                format_currency(sum(lucros_acumulados))
            ],
            'Fluxo de Caixa': [
                format_currency(fluxo_caixa[5]) if len(fluxo_caixa) > 5 else 'N/A',
                format_currency(fluxo_caixa[11]) if len(fluxo_caixa) > 11 else 'N/A',
                format_currency(fluxo_caixa[23]) if len(fluxo_caixa) > 23 else 'N/A',
                format_currency(fluxo_caixa[35]) if len(fluxo_caixa) > 35 else 'N/A',
                format_currency(fluxo_caixa[-1])
            ]
        })
        
        st.dataframe(marcos_df, use_container_width=True, hide_index=True)

# ========================================================================
# TAB 5: CONFIGURAÇÕES
# ========================================================================
with tab5:
    st.markdown("### ⚙️ Configurações e Parâmetros do Sistema")
    
    st.info("""
    💡 **Dica**: Ajuste os parâmetros abaixo para personalizar as simulações de acordo com a realidade 
    do seu mercado e operação. As alterações serão aplicadas em todos os cálculos.
    """)
    
    # Organizar em abas para melhor organização
    config_tab1, config_tab2, config_tab3 = st.tabs([
        "💰 Parâmetros Financeiros",
        "✈️ Modelos de Aeronaves",
        "🗺️ Rotas Disponíveis"
    ])
    
    with config_tab1:
        st.markdown("#### 💰 Parâmetros Financeiros e Operacionais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Custos Operacionais")
            
            preco_combustivel = st.number_input(
                "Preço do Combustível (R$/litro)",
                value=float(params['preco_combustivel']),
                min_value=1.0,
                max_value=20.0,
                step=0.1,
                format="%.2f",
                help="Preço médio do QAV-1 (querosene de aviação)"
            )
            
            custo_piloto = st.number_input(
                "Custo Hora Piloto (R$)",
                value=float(params['custo_piloto_hora']),
                min_value=500.0,
                max_value=5000.0,
                step=100.0,
                help="Custo médio por hora de voo do piloto"
            )
            
            depreciacao = st.number_input(
                "Depreciação Anual (%)",
                value=float(params['depreciacao_anual_pct']),
                min_value=1.0,
                max_value=20.0,
                step=0.5,
                help="Taxa de depreciação anual da aeronave"
            )
        
        with col2:
            st.markdown("##### Custos de Manutenção por Tipo")
            
            manut_turboprop = st.number_input(
                "Manutenção Turboprop (R$/hora)",
                value=float(params['custo_manutencao_hora']['turboprop']),
                min_value=500.0,
                max_value=5000.0,
                step=100.0,
                help="Custo médio de manutenção para turboprops"
            )
            
            manut_jato = st.number_input(
                "Manutenção Jato (R$/hora)",
                value=float(params['custo_manutencao_hora']['jato']),
                min_value=1000.0,
                max_value=10000.0,
                step=200.0,
                help="Custo médio de manutenção para jatos"
            )
        
        st.markdown("##### Preços de Mercado (Charter)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            mercado_turboprop = st.number_input(
                "Preço Charter Turboprop (R$/hora)",
                value=float(params['preco_mercado']['turboprop']),
                min_value=3000.0,
                max_value=15000.0,
                step=500.0,
                help="Preço médio de mercado para charter de turboprops"
            )
        
        with col2:
            mercado_jato = st.number_input(
                "Preço Charter Jato (R$/hora)",
                value=float(params['preco_mercado']['jato']),
                min_value=8000.0,
                max_value=30000.0,
                step=1000.0,
                help="Preço médio de mercado para charter de jatos"
            )
        
        if st.button("💾 Salvar Configurações Financeiras", type="primary"):
            novos_params = {
                'preco_combustivel': preco_combustivel,
                'custo_piloto_hora': custo_piloto,
                'depreciacao_anual_pct': depreciacao,
                'custo_manutencao_hora': {
                    'turboprop': manut_turboprop,
                    'jato': manut_jato
                },
                'percentual_proprietario': 0.9,
                'preco_mercado': {
                    'turboprop': mercado_turboprop,
                    'jato': mercado_jato
                }
            }
            
            if save_params(novos_params):
                st.success("✅ Configurações salvas com sucesso!")
                st.rerun()
            else:
                st.error("❌ Erro ao salvar configurações")
    
    with config_tab2:
        st.markdown("#### ✈️ Gerenciamento de Modelos de Aeronaves")
        
        # Carregar modelos atuais
        try:
            df_modelos = pd.read_csv('data/modelos.csv')
        except:
            df_modelos = pd.DataFrame({
                'modelo': ['Pilatus PC-12'],
                'consumo_l_por_h': [260],
                'manut_tipo': ['turboprop'],
                'tipo': ['turboprop']
            })
        
        # Editor de dados
        st.markdown("##### Editar Modelos Existentes")
        df_editado = st.data_editor(
            df_modelos,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "modelo": st.column_config.TextColumn("Modelo", help="Nome do modelo da aeronave"),
                "consumo_l_por_h": st.column_config.NumberColumn("Consumo (L/h)", help="Consumo de combustível em litros por hora"),
                "manut_tipo": st.column_config.SelectboxColumn("Tipo Manutenção", options=["turboprop", "jato"]),
                "tipo": st.column_config.SelectboxColumn("Tipo Aeronave", options=["turboprop", "jato"])
            }
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Salvar Alterações nos Modelos", type="primary"):
                try:
                    df_editado.to_csv('data/modelos.csv', index=False)
                    st.success("✅ Modelos atualizados com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao salvar modelos: {e}")
        
        with col2:
            # Download do template
            csv = df_modelos.to_csv(index=False)
            st.download_button(
                "📥 Baixar Template CSV",
                csv,
                "modelos_template.csv",
                "text/csv",
                help="Baixe o template para editar externamente"
            )
    
    with config_tab3:
        st.markdown("#### 🗺️ Gerenciamento de Rotas")
        
        # Carregar rotas atuais
        try:
            df_rotas = pd.read_csv('data/rotas.csv')
        except:
            df_rotas = pd.DataFrame({
                'origem': ['GRU'],
                'destino': ['SDU'],
                'duracao_h': [1.0]
            })
        
        # Editor de dados
        st.markdown("##### Editar Rotas Disponíveis")
        df_rotas_editado = st.data_editor(
            df_rotas,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "origem": st.column_config.TextColumn("Origem", help="Código IATA do aeroporto de origem"),
                "destino": st.column_config.TextColumn("Destino", help="Código IATA do aeroporto de destino"),
                "duracao_h": st.column_config.NumberColumn("Duração (h)", help="Duração do voo em horas", format="%.1f")
            }
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Salvar Alterações nas Rotas", type="primary"):
                try:
                    df_rotas_editado.to_csv('data/rotas.csv', index=False)
                    st.success("✅ Rotas atualizadas com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao salvar rotas: {e}")
        
        with col2:
            # Download do template
            csv_rotas = df_rotas.to_csv(index=False)
            st.download_button(
                "📥 Baixar Template CSV",
                csv_rotas,
                "rotas_template.csv",
                "text/csv",
                help="Baixe o template para editar externamente"
            )

# ========================================================================
# FOOTER
# ========================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 2rem;">
    <p>✈️ <strong>Amaro Aviation</strong> - Excelência em Gestão de Aviação Executiva</p>
    <p style="font-size: 0.875rem;">Simulador desenvolvido para demonstrar o valor agregado da gestão profissional Amaro</p>
</div>
""", unsafe_allow_html=True)