import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
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
    page_title="Amaro Aviation - Calculadora de Custos",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================================================
# SISTEMA DE IDIOMAS SIMPLIFICADO
# ========================================================================
@st.cache_data
def get_translations():
    return {
        'pt': {
            'app_title': 'Amaro Aviation',
            'app_subtitle': 'Análise Estratégica de Custos Operacionais',
            'language': 'Idioma',
            'tab_profit': 'Estimativa de Receita Mensal',
            'tab_comparison': 'Análise Comparativa de Custos',
            'tab_settings': 'Configurações do Sistema',
            'aircraft_model': 'Modelo da Aeronave',
            'monthly_hours': 'Horas de Voo Mensais',
            'occupancy_rate': 'Taxa de Ocupação (%)',
            'annual_hours': 'Horas de Voo Anuais',
            'fixed_costs': 'Custos Fixos Anuais (R$)',
            'include_charter': 'Incluir Receita de Charter',
            'calculate': 'Calcular Análise',
            'gross_revenue': 'Receita Bruta',
            'owner_revenue': 'Receita do Proprietário (90%)',
            'amaro_fee': 'Taxa de Administração (10%)',
            'operational_costs': 'Custos Operacionais',
            'net_profit': 'Resultado Líquido',
            'monthly_roi': 'ROI Mensal',
            'own_management': 'Gestão Própria',
            'amaro_management': 'Gestão Amaro Aviation',
            'annual_savings': 'Economia Anual',
            'savings_percentage': 'Percentual de Economia',
            'fuel_price': 'Preço do Combustível (R$/L)',
            'pilot_cost': 'Custo Piloto (R$/h)',
            'depreciation': 'Depreciação Anual (%)',
            'maintenance_turboprop': 'Manutenção Turboprop (R$/h)',
            'maintenance_jet': 'Manutenção Jato (R$/h)',
            'market_price_turboprop': 'Preço Mercado Turboprop (R$/h)',
            'market_price_jet': 'Preço Mercado Jato (R$/h)',
            'save_settings': 'Salvar Configurações',
            'system_operational': 'Sistema Operacional',
            'models_configured': 'modelos configurados',
            'profitable_operation': 'Operação Rentável',
            'operation_at_loss': 'Operação em Déficit',
            'settings_saved': 'Configurações salvas com sucesso',
            'calculation_error': 'Erro no cálculo',
            'export_excel': 'Exportar para Excel',
            'export_pdf': 'Exportar para PDF',
            'developed_with_love': 'Desenvolvido para excelência operacional'
        },
        'en': {
            'app_title': 'Amaro Aviation',
            'app_subtitle': 'Strategic Operational Cost Analysis',
            'language': 'Language',
            'tab_profit': 'Monthly Revenue Estimation',
            'tab_comparison': 'Comparative Cost Analysis',
            'tab_settings': 'System Settings',
            'aircraft_model': 'Aircraft Model',
            'monthly_hours': 'Monthly Flight Hours',
            'occupancy_rate': 'Occupancy Rate (%)',
            'annual_hours': 'Annual Flight Hours',
            'fixed_costs': 'Annual Fixed Costs (R$)',
            'include_charter': 'Include Charter Revenue',
            'calculate': 'Calculate Analysis',
            'gross_revenue': 'Gross Revenue',
            'owner_revenue': 'Owner Revenue (90%)',
            'amaro_fee': 'Management Fee (10%)',
            'operational_costs': 'Operational Costs',
            'net_profit': 'Net Result',
            'monthly_roi': 'Monthly ROI',
            'own_management': 'Own Management',
            'amaro_management': 'Amaro Aviation Management',
            'annual_savings': 'Annual Savings',
            'savings_percentage': 'Savings Percentage',
            'fuel_price': 'Fuel Price (R$/L)',
            'pilot_cost': 'Pilot Cost (R$/h)',
            'depreciation': 'Annual Depreciation (%)',
            'maintenance_turboprop': 'Turboprop Maintenance (R$/h)',
            'maintenance_jet': 'Jet Maintenance (R$/h)',
            'market_price_turboprop': 'Turboprop Market Price (R$/h)',
            'market_price_jet': 'Jet Market Price (R$/h)',
            'save_settings': 'Save Settings',
            'system_operational': 'System Operational',
            'models_configured': 'models configured',
            'profitable_operation': 'Profitable Operation',
            'operation_at_loss': 'Deficit Operation',
            'settings_saved': 'Settings saved successfully',
            'calculation_error': 'Calculation error',
            'export_excel': 'Export to Excel',
            'export_pdf': 'Export to PDF',
            'developed_with_love': 'Developed for operational excellence'
        }
    }

def t(key, lang='pt'):
    translations = get_translations()
    return translations.get(lang, translations['pt']).get(key, key)

# ========================================================================
# CSS CORPORATIVO PROFISSIONAL
# ========================================================================
def load_professional_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset e configurações globais */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background-color: #FFFFFF;
        color: #333333;
    }
    
    /* Remover padding padrão */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }
    
    /* Header corporativo */
    .corporate-header {
        background: linear-gradient(135deg, #8C1D40 0%, #A02050 100%);
        color: white;
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        border-bottom: 3px solid #8C1D40;
    }
    
    .corporate-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .corporate-header p {
        font-size: 1.1rem;
        font-weight: 400;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        letter-spacing: 0.01em;
    }
    
    /* Cards profissionais */
    .professional-card {
        background: #FFFFFF;
        border: 1px solid #E5E5E5;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    .professional-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border-color: #8C1D40;
    }
    
    /* Métricas corporativas */
    .metric-container {
        background: #F8F9FA;
        border-left: 4px solid #8C1D40;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 0 6px 6px 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #8C1D40;
        margin: 0;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666666;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    /* Botões corporativos */
    .stButton > button {
        background-color: #8C1D40;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.02em;
        transition: all 0.2s ease;
        text-transform: uppercase;
        min-height: 48px;
    }
    
    .stButton > button:hover {
        background-color: #A02050;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(140, 29, 64, 0.3);
    }
    
    .stButton > button:focus {
        box-shadow: 0 0 0 3px rgba(140, 29, 64, 0.2);
    }
    
    /* Tabs corporativas */
    .stTabs [data-baseweb="tab-list"] {
        background: #F8F9FA;
        border-radius: 8px;
        padding: 0.25rem;
        margin-bottom: 2rem;
        border: 1px solid #E5E5E5;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 6px;
        color: #666666;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #8C1D40;
        color: white;
    }
    
    /* Inputs profissionais */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stSlider > div > div > div {
        border-radius: 6px;
        border: 1px solid #D1D5DB;
        font-size: 0.95rem;
    }
    
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div:focus-within {
        border-color: #8C1D40;
        box-shadow: 0 0 0 3px rgba(140, 29, 64, 0.1);
    }
    
    /* Labels */
    .stSelectbox label,
    .stNumberInput label,
    .stSlider label {
        font-weight: 500;
        color: #374151;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }
    
    /* Sidebar profissional */
    .css-1d391kg {
        background-color: #F8F9FA;
        border-right: 1px solid #E5E5E5;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #8C1D40 0%, #A02050 100%);
        color: white;
        padding: 1.5rem;
        margin: -1rem -1rem 1.5rem -1rem;
        text-align: center;
    }
    
    /* Status boxes */
    .status-success {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 6px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        padding: 1rem;
        border-radius: 6px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .status-info {
        background: #F0F9FF;
        color: #0C4A6E;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #0EA5E9;
        margin: 1rem 0;
    }
    
    /* Tabelas */
    .dataframe {
        border: 1px solid #E5E5E5;
        border-radius: 6px;
        overflow: hidden;
    }
    
    .dataframe th {
        background-color: #8C1D40;
        color: white;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.02em;
        font-size: 0.85rem;
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        background-color: #10B981;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }
    
    .stDownloadButton > button:hover {
        background-color: #059669;
    }
    
    /* Logo container */
    .logo-container {
        text-align: center;
        margin: -1rem 0 2rem 0;
        padding: 1rem;
        background: #F8F9FA;
        border-bottom: 1px solid #E5E5E5;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Typography refinements */
    h1, h2, h3, h4, h5, h6 {
        color: #1F2937;
        font-weight: 600;
        letter-spacing: -0.01em;
    }
    
    p {
        color: #4B5563;
        line-height: 1.6;
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #E5E5E5, transparent);
        margin: 2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ========================================================================
# COMPONENTES PROFISSIONAIS
# ========================================================================
def render_corporate_header(title, subtitle, lang='pt'):
    """Renderiza cabeçalho corporativo"""
    st.markdown(f"""
    <div class="corporate-header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(label, value, format_type="currency", lang='pt'):
    """Renderiza card de métrica profissional"""
    if format_type == "currency":
        formatted_value = format_currency(value, lang)
    elif format_type == "percentage":
        formatted_value = format_percentage(value, lang)
    else:
        formatted_value = str(value)
    
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-value">{formatted_value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

def render_status_box(message, status_type="info"):
    """Renderiza caixa de status profissional"""
    st.markdown(f"""
    <div class="status-{status_type}">
        {message}
    </div>
    """, unsafe_allow_html=True)

# ========================================================================
# CARREGAMENTO E INICIALIZAÇÃO
# ========================================================================
load_professional_css()

# Sidebar corporativa
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h3 style="margin: 0; font-weight: 600;">Amaro Aviation</h3>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">Sistema de Análise</p>
    </div>
    """, unsafe_allow_html=True)
    
    language_option = st.selectbox(
        "IDIOMA / LANGUAGE",
        ["🇧🇷 Português", "🇺🇸 English"],
        key="language_selector"
    )
    
    lang = 'pt' if '🇧🇷' in language_option else 'en'

# Header principal
render_corporate_header(
    t('app_title', lang),
    t('app_subtitle', lang),
    lang
)

# Carregamento de dados com tratamento robusto
try:
    params = load_params()
    modelos = params.get('modelos_disponiveis', [])
    
    if not modelos:
        st.error("Sistema não configurado. Verifique os dados em data/modelos.csv")
        st.stop()
        
except Exception as e:
    st.error(f"Erro crítico no sistema: {e}")
    st.stop()

# ========================================================================
# INTERFACE PRINCIPAL
# ========================================================================
tab1, tab2, tab3 = st.tabs([
    t('tab_profit', lang),
    t('tab_comparison', lang), 
    t('tab_settings', lang)
])

# ========================================================================
# TAB 1: ESTIMATIVA DE RECEITA MENSAL
# ========================================================================
with tab1:
    st.markdown(f"""
    <div class="professional-card">
        <h3 style="margin-top: 0; color: #1F2937;">Análise de Receita Mensal</h3>
        <p style="color: #6B7280;">Configure os parâmetros operacionais para análise de viabilidade econômica mensal.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        modelo_lucro = st.selectbox(
            t('aircraft_model', lang).upper(),
            modelos,
            key="modelo_lucro"
        )
    
    with col2:
        horas_mes = st.number_input(
            t('monthly_hours', lang).upper(),
            min_value=10,
            max_value=200,
            value=80,
            step=10,
            key="horas_mes"
        )
    
    with col3:
        ocupacao = st.slider(
            t('occupancy_rate', lang).upper(),
            min_value=50,
            max_value=95,
            value=75,
            key="ocupacao"
        )
    
    if st.button(t('calculate', lang).upper(), key="calc_lucro", type="primary"):
        try:
            # Cálculos
            resultado_hora = calcula_custo_trecho(modelo_lucro, 1.0, params)
            horas_efetivas = float(horas_mes) * (float(ocupacao) / 100.0)
            
            # Receitas e custos
            preco_hora_mercado = float(params['preco_mercado_hora'][modelo_lucro])
            receita_bruta = preco_hora_mercado * horas_efetivas
            custo_operacional = float(resultado_hora['total']) * horas_efetivas
            
            # Cálculos financeiros
            percentual_proprietario = 0.9
            percentual_amaro = 0.1
            
            receita_proprietario = receita_bruta * percentual_proprietario
            receita_amaro = receita_bruta * percentual_amaro
            lucro_liquido = receita_proprietario - custo_operacional
            
            roi_mensal = (lucro_liquido / custo_operacional * 100.0) if custo_operacional > 0 else 0.0
            
            # Exibição profissional dos resultados
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("### Resultados da Análise Financeira")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                render_metric_card(t('gross_revenue', lang), receita_bruta, "currency", lang)
            
            with col2:
                render_metric_card(t('owner_revenue', lang), receita_proprietario, "currency", lang)
            
            with col3:
                render_metric_card(t('operational_costs', lang), custo_operacional, "currency", lang)
            
            with col4:
                render_metric_card(t('net_profit', lang), lucro_liquido, "currency", lang)
            
            # Gráfico profissional
            fig_breakdown = go.Figure(data=[go.Pie(
                labels=[
                    'Resultado Líquido',
                    'Taxa de Administração',
                    'Custos Operacionais'
                ],
                values=[
                    max(0, receita_proprietario - custo_operacional),
                    receita_amaro,
                    custo_operacional
                ],
                hole=0.5,
                marker=dict(colors=['#10B981', '#8C1D40', '#F59E0B']),
                textinfo='label+percent',
                textfont=dict(size=12, color='white'),
                hovertemplate='<b>%{label}</b><br>%{value:,.0f} R$<br>%{percent}<extra></extra>'
            )])
            
            fig_breakdown.update_layout(
                title={
                    'text': 'Composição Financeira Mensal',
                    'x': 0.5,
                    'font': {'size': 16, 'color': '#1F2937'}
                },
                font=dict(family="Inter, sans-serif", size=11),
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                ),
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            
            st.plotly_chart(fig_breakdown, use_container_width=True)
            
            # Status da operação
            if lucro_liquido > 0:
                render_status_box(
                    f"<strong>OPERAÇÃO RENTÁVEL</strong><br>"
                    f"Resultado líquido: {format_currency(lucro_liquido, lang)}<br>"
                    f"ROI mensal: {format_percentage(roi_mensal, lang)}",
                    "success"
                )
            else:
                render_status_box(
                    f"<strong>ATENÇÃO: OPERAÇÃO EM DÉFICIT</strong><br>"
                    f"Déficit mensal: {format_currency(abs(lucro_liquido), lang)}",
                    "warning"
                )
            
            # Exportação
            col1, col2 = st.columns(2)
            
            dados_lucro = {
                "Análise": "Estimativa de Receita Mensal",
                "Modelo": modelo_lucro,
                "Horas Mensais": horas_mes,
                "Taxa Ocupação": f"{ocupacao}%",
                "Receita Bruta": receita_bruta,
                "Receita Proprietário": receita_proprietario,
                "Custos Operacionais": custo_operacional,
                "Lucro Líquido": lucro_liquido,
                "ROI Mensal": f"{roi_mensal:.1f}%"
            }
            
            relatorio_lucro = criar_relatorio_dados(
                "Estimativa de Receita Mensal",
                {"modelo": modelo_lucro, "horas": horas_mes, "ocupacao": ocupacao},
                dados_lucro
            )
            
            with col1:
                try:
                    excel_buffer = gerar_excel_simples(relatorio_lucro)
                    if excel_buffer:
                        st.download_button(
                            t('export_excel', lang).upper(),
                            data=excel_buffer.getvalue(),
                            file_name=f"amaro_receita_mensal_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Erro ao gerar Excel: {e}")
            
            with col2:
                try:
                    pdf_buffer = BytesIO()
                    if gerar_pdf(pdf_buffer, dados_lucro):
                        pdf_buffer.seek(0)
                        st.download_button(
                            t('export_pdf', lang).upper(),
                            data=pdf_buffer.getvalue(),
                            file_name=f"amaro_receita_mensal_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Erro ao gerar PDF: {e}")
                    
        except Exception as e:
            st.error(f"{t('calculation_error', lang)}: {e}")

# ========================================================================
# TAB 2: ANÁLISE COMPARATIVA
# ========================================================================
with tab2:
    st.markdown(f"""
    <div class="professional-card">
        <h3 style="margin-top: 0; color: #1F2937;">Análise Comparativa de Custos</h3>
        <p style="color: #6B7280;">Compare os custos totais entre gestão própria e gestão Amaro Aviation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        modelo_comp = st.selectbox(
            t('aircraft_model', lang).upper(),
            modelos,
            key="modelo_comp"
        )
        
        horas_anuais = st.number_input(
            t('annual_hours', lang).upper(),
            min_value=50,
            max_value=800,
            value=300,
            step=25,
            key="horas_anuais"
        )
    
    with col2:
        custos_fixos_anuais = st.number_input(
            t('fixed_costs', lang).upper(),
            min_value=50000,
            max_value=2000000,
            value=500000,
            step=25000,
            key="custos_fixos"
        )
        
        include_charter = st.checkbox(
            t('include_charter', lang).upper(),
            value=True,
            key="include_charter"
        )
    
    if st.button(t('calculate', lang).upper(), key="calc_comp", type="primary"):
        try:
            # Cálculos comparativos
            resultado_ano = calcula_custo_trecho(modelo_comp, float(horas_anuais), params)
            custo_operacional_ano = float(resultado_ano['total'])
            custo_total_proprio = custo_operacional_ano + float(custos_fixos_anuais)
            
            # Gestão Amaro (sem custos fixos)
            custo_amaro_ano = custo_operacional_ano
            
            # Receita de charter
            receita_charter = 0.0
            if include_charter:
                preco_hora = float(params['preco_mercado_hora'][modelo_comp])
                receita_charter = preco_hora * float(horas_anuais) * 0.6
            
            # Custos líquidos
            custo_liquido_proprio = custo_total_proprio - receita_charter
            custo_liquido_amaro = custo_amaro_ano - receita_charter
            
            economia_anual = custo_liquido_proprio - custo_liquido_amaro
            percentual_economia = (economia_anual / custo_liquido_proprio * 100.0) if custo_liquido_proprio > 0 else 0.0
            
            # Exibição profissional
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("### Comparativo Anual de Custos")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="professional-card" style="background: #FEF3C7; border-left: 4px solid #F59E0B;">
                    <h4 style="color: #92400E; margin-top: 0;">GESTÃO PRÓPRIA</h4>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #92400E; margin: 1rem 0;">
                        {format_currency(custo_liquido_proprio, lang)}
                    </div>
                    <div style="font-size: 0.85rem; color: #78350F;">
                        <strong>Custos Operacionais:</strong> {format_currency(custo_operacional_ano, lang)}<br>
                        <strong>Custos Fixos:</strong> {format_currency(custos_fixos_anuais, lang)}
                        {f"<br><strong>Receita Charter:</strong> -{format_currency(receita_charter, lang)}" if include_charter else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="professional-card" style="background: #D1FAE5; border-left: 4px solid #10B981;">
                    <h4 style="color: #047857; margin-top: 0;">GESTÃO AMARO AVIATION</h4>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #047857; margin: 1rem 0;">
                        {format_currency(custo_liquido_amaro, lang)}
                    </div>
                    <div style="font-size: 0.85rem; color: #065F46;">
                        <strong>Custos Operacionais:</strong> {format_currency(custo_amaro_ano, lang)}<br>
                        <strong>Custos Fixos:</strong> {format_currency(0, lang)}
                        {f"<br><strong>Receita Charter:</strong> -{format_currency(receita_charter, lang)}" if include_charter else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                cor_economia = '#047857' if economia_anual > 0 else '#DC2626'
                bg_economia = '#D1FAE5' if economia_anual > 0 else '#FEE2E2'
                st.markdown(f"""
                <div class="professional-card" style="background: {bg_economia}; border-left: 4px solid {cor_economia};">
                    <h4 style="color: {cor_economia}; margin-top: 0;">ECONOMIA ANUAL</h4>
                    <div style="font-size: 1.5rem; font-weight: 700; color: {cor_economia}; margin: 1rem 0;">
                        {format_currency(abs(economia_anual), lang)}
                    </div>
                    <div style="font-size: 0.85rem; color: {cor_economia};">
                        <strong>Percentual:</strong> {format_percentage(percentual_economia, lang)}<br>
                        <strong>Economia Mensal:</strong> {format_currency(economia_anual/12, lang)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Gráfico comparativo profissional
            fig_comp = go.Figure()
            
            categorias = ['Gestão Própria', 'Gestão Amaro Aviation']
            valores = [custo_liquido_proprio, custo_liquido_amaro]
            cores = ['#F59E0B', '#8C1D40']
            
            fig_comp.add_trace(go.Bar(
                x=categorias,
                y=valores,
                marker_color=cores,
                text=[format_currency(v, lang) for v in valores],
                textposition='outside',
                textfont=dict(size=14, color='#1F2937'),
                hovertemplate='<b>%{x}</b><br>Custo: %{text}<extra></extra>'
            ))
            
            if economia_anual > 0:
                fig_comp.add_annotation(
                    x=0.5, y=max(valores) * 0.8,
                    text=f"ECONOMIA ANUAL<br><b>{format_currency(economia_anual, lang)}</b>",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor='#10B981',
                    font=dict(size=14, color='#10B981'),
                    bgcolor='white',
                    bordercolor='#10B981',
                    borderwidth=1
                )
            
            fig_comp.update_layout(
                title={
                    'text': 'Análise Comparativa Anual',
                    'x': 0.5,
                    'font': {'size': 16, 'color': '#1F2937'}
                },
                yaxis_title='Custo Anual (R$)',
                font=dict(family="Inter, sans-serif"),
                plot_bgcolor='white',
                paper_bgcolor='white',
                height=500,
                showlegend=False
            )
            
            st.plotly_chart(fig_comp, use_container_width=True)
            
            # Exportação
            col1, col2 = st.columns(2)
            
            dados_comp = {
                "Análise": "Comparativo de Custos",
                "Modelo": modelo_comp,
                "Horas Anuais": horas_anuais,
                "Custos Fixos": custos_fixos_anuais,
                "Custo Gestão Própria": custo_liquido_proprio,
                "Custo Gestão Amaro": custo_liquido_amaro,
                "Economia Anual": economia_anual,
                "Percentual Economia": f"{percentual_economia:.1f}%"
            }
            
            relatorio_comp = criar_relatorio_dados(
                "Comparativo de Custos",
                {"modelo": modelo_comp, "horas": horas_anuais, "fixos": custos_fixos_anuais},
                dados_comp
            )
            
            with col1:
                try:
                    excel_buffer = gerar_excel_simples(relatorio_comp)
                    if excel_buffer:
                        st.download_button(
                            t('export_excel', lang).upper(),
                            data=excel_buffer.getvalue(),
                            file_name=f"amaro_comparativo_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Erro ao gerar Excel: {e}")
            
            with col2:
                try:
                    pdf_buffer = BytesIO()
                    if gerar_pdf(pdf_buffer, dados_comp):
                        pdf_buffer.seek(0)
                        st.download_button(
                            t('export_pdf', lang).upper(),
                            data=pdf_buffer.getvalue(),
                            file_name=f"amaro_comparativo_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Erro ao gerar PDF: {e}")
                    
        except Exception as e:
            st.error(f"{t('calculation_error', lang)}: {e}")

# ========================================================================
# TAB 3: CONFIGURAÇÕES DO SISTEMA
# ========================================================================
with tab3:
    st.markdown(f"""
    <div class="professional-card">
        <h3 style="margin-top: 0; color: #1F2937;">Configurações do Sistema</h3>
        <p style="color: #6B7280;">Ajuste os parâmetros operacionais do sistema de análise.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### PARÂMETROS OPERACIONAIS")
        
        preco_combustivel = st.number_input(
            t('fuel_price', lang).upper(),
            value=float(params['preco_combustivel']),
            min_value=1.0,
            max_value=50.0,
            step=0.1,
            format="%.2f"
        )
        
        custo_piloto = st.number_input(
            t('pilot_cost', lang).upper(),
            value=float(params['custo_piloto_hora']),
            min_value=500,
            max_value=5000,
            step=50
        )
        
        depreciacao = st.number_input(
            t('depreciation', lang).upper(),
            value=float(params['depreciacao_anual_pct']),
            min_value=1.0,
            max_value=20.0,
            step=0.5,
            format="%.1f"
        )
    
    with col2:
        st.markdown("#### CUSTOS DE MANUTENÇÃO E MERCADO")
        
        manut_turboprop = st.number_input(
            t('maintenance_turboprop', lang).upper(),
            value=float(params['custo_manutencao_hora']['turboprop']),
            min_value=500,
            max_value=5000,
            step=100
        )
        
        manut_jato = st.number_input(
            t('maintenance_jet', lang).upper(),
            value=float(params['custo_manutencao_hora']['jato']),
            min_value=1000,
            max_value=10000,
            step=200
        )
        
        mercado_turboprop = st.number_input(
            t('market_price_turboprop', lang).upper(),
            value=float(params['preco_mercado']['turboprop']),
            min_value=3000,
            max_value=15000,
            step=500
        )
        
        mercado_jato = st.number_input(
            t('market_price_jet', lang).upper(),
            value=float(params['preco_mercado']['jato']),
            min_value=8000,
            max_value=30000,
            step=1000
        )
    
    # Botão de salvar centralizado
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(t('save_settings', lang).upper(), type="primary", use_container_width=True):
            try:
                novos_params = {
                    'preco_combustivel': preco_combustivel,
                    'custo_piloto_hora': custo_piloto,
                    'depreciacao_anual_pct': depreciacao,
                    'custo_manutencao_hora': {
                        'turboprop': manut_turboprop,
                        'jato': manut_jato
                    },
                    'percentual_proprietario': params.get('percentual_proprietario', 0.9),
                    'preco_mercado': {
                        'turboprop': mercado_turboprop,
                        'jato': mercado_jato
                    }
                }
                
                if save_params(novos_params):
                    render_status_box(t('settings_saved', lang), "success")
                    st.rerun()
                else:
                    st.error("Erro ao salvar configurações")
                    
            except Exception as e:
                st.error(f"Erro ao processar dados: {e}")

# ========================================================================
# SIDEBAR - STATUS E INFORMAÇÕES
# ========================================================================
with st.sidebar:
    st.markdown("<hr>", unsafe_allow_html=True)
    
    render_status_box(
        f"<strong>{t('system_operational', lang).upper()}</strong><br>"
        f"Modelos: {len(modelos)} {t('models_configured', lang)}<br>"
        f"Parâmetros: Carregados<br>"
        f"Idioma: {language_option}",
        "info"
    )
    
    st.markdown("#### RECURSOS DO SISTEMA")
    st.markdown("""
    **ANÁLISE DE RECEITA:**  
    Simulação de receitas e custos mensais
    
    **ANÁLISE COMPARATIVA:**  
    Comparação entre gestão própria e Amaro Aviation
    
    **CONFIGURAÇÕES:**  
    Ajuste de parâmetros operacionais
    """)
    
    st.markdown("#### ORIENTAÇÕES DE USO")
    if lang == 'pt':
        st.markdown("""
        • Use ocupação de 70-80% para projeções realistas
        • Considere custos fixos reais (hangar, seguro, etc.)
        • Revise parâmetros periodicamente
        • Exporte relatórios para apresentações
        """)
    else:
        st.markdown("""
        • Use 70-80% occupancy for realistic projections
        • Consider real fixed costs (hangar, insurance, etc.)
        • Review parameters periodically
        • Export reports for presentations
        """)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align: center; color: #6B7280; font-size: 0.8rem;">
        <p><strong>Amaro Aviation Calculator</strong></p>
        <p>Sistema Corporativo v3.0</p>
        <p>{t('developed_with_love', lang)}</p>
    </div>
    """, unsafe_allow_html=True)