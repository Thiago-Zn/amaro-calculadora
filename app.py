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
from utils.params import load_params, save_params
from utils.calculations import calcula_custo_trecho, calcular_projecao_mensal
from utils.exportador_excel import criar_relatorio_dados, gerar_excel_simples
from utils.exportador_pdf import gerar_pdf

# ========================================================================
# CONFIGURAÇÃO DA PÁGINA
# ========================================================================
st.set_page_config(
    page_title="Amaro Aviation - Calculadora de Custos",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================================================
# SISTEMA DE IDIOMAS SIMPLIFICADO
# ========================================================================
@st.cache_data
def get_translations():
    """Sistema de traduções corporativo"""
    return {
        'pt': {
            'app_title': 'AMARO AVIATION',
            'app_subtitle': 'CALCULADORA DE CUSTOS OPERACIONAIS',
            'language': 'IDIOMA',
            'tab_profit': 'ESTIMATIVA DE LUCRO MENSAL',
            'tab_comparison': 'COMPARATIVO DE CUSTOS',
            'tab_settings': 'CONFIGURAÇÕES',
            'aircraft_model': 'Modelo da Aeronave',
            'monthly_hours': 'Horas de Voo por Mês',
            'occupancy_rate': 'Taxa de Ocupação (%)',
            'annual_hours': 'Horas de Voo por Ano',
            'fixed_costs': 'Custos Fixos Anuais (R$)',
            'include_charter': 'Incluir Receita de Charter',
            'calculate': 'CALCULAR',
            'gross_revenue': 'Receita Bruta',
            'owner_revenue': 'Receita do Proprietário',
            'amaro_fee': 'Taxa Amaro Aviation',
            'operational_costs': 'Custos Operacionais',
            'net_profit': 'Lucro Líquido',
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
            'save_settings': 'SALVAR CONFIGURAÇÕES',
            'system_operational': 'Sistema Operacional',
            'models_configured': 'modelos configurados',
            'profitable_operation': 'Operação Rentável',
            'operation_at_loss': 'Operação com Prejuízo',
            'settings_saved': 'Configurações salvas com sucesso',
            'calculation_error': 'Erro no cálculo',
            'export_excel': 'EXPORTAR EXCEL',
            'export_pdf': 'EXPORTAR PDF',
            'developed_with_love': 'Desenvolvido pela Amaro Aviation'
        },
        'en': {
            'app_title': 'AMARO AVIATION',
            'app_subtitle': 'OPERATING COST CALCULATOR',
            'language': 'LANGUAGE',
            'tab_profit': 'MONTHLY PROFIT ESTIMATION',
            'tab_comparison': 'COST COMPARISON',
            'tab_settings': 'SETTINGS',
            'aircraft_model': 'Aircraft Model',
            'monthly_hours': 'Flight Hours per Month',
            'occupancy_rate': 'Occupancy Rate (%)',
            'annual_hours': 'Annual Flight Hours',
            'fixed_costs': 'Annual Fixed Costs (R$)',
            'include_charter': 'Include Charter Revenue',
            'calculate': 'CALCULATE',
            'gross_revenue': 'Gross Revenue',
            'owner_revenue': 'Owner Revenue',
            'amaro_fee': 'Amaro Aviation Fee',
            'operational_costs': 'Operational Costs',
            'net_profit': 'Net Profit',
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
            'save_settings': 'SAVE SETTINGS',
            'system_operational': 'System Operational',
            'models_configured': 'models configured',
            'profitable_operation': 'Profitable Operation',
            'operation_at_loss': 'Operation at Loss',
            'settings_saved': 'Settings saved successfully',
            'calculation_error': 'Calculation error',
            'export_excel': 'EXPORT EXCEL',
            'export_pdf': 'EXPORT PDF',
            'developed_with_love': 'Developed by Amaro Aviation'
        }
    }

def t(key, lang='pt'):
    """Função de tradução"""
    translations = get_translations()
    return translations.get(lang, translations['pt']).get(key, key)

def format_currency(value, lang='pt'):
    """Formata valores monetários"""
    try:
        if lang == 'pt':
            return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            return f"R$ {value:,.2f}"
    except Exception:
        return str(value)

def format_percentage(value, lang='pt'):
    """Formata percentuais"""
    try:
        if lang == 'pt':
            return f"{value:.1f}%".replace(".", ",")
        else:
            return f"{value:.1f}%"
    except Exception:
        return str(value)

# ========================================================================
# CSS CORPORATIVO MINIMALISTA
# ========================================================================
def load_corporate_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', 'Helvetica Neue', 'Segoe UI', sans-serif;
        background-color: #FFFFFF;
        color: #333333;
    }
    
    .corporate-header {
        background-color: #FFFFFF;
        border-bottom: 2px solid #8C1D40;
        padding: 2rem 0;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .corporate-header h1 {
        color: #8C1D40;
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: 2px;
        margin: 0;
        text-transform: uppercase;
    }
    
    .corporate-header p {
        color: #333333;
        font-size: 1.1rem;
        font-weight: 400;
        margin: 0.5rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .corporate-card {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 4px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .corporate-card h3 {
        color: #8C1D40;
        font-size: 1.4rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-left: 4px solid #8C1D40;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #8C1D40;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #333333;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
        margin: 0;
    }
    
    .stButton > button {
        background-color: #8C1D40;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: background-color 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #6D1530;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: #FFFFFF;
        border-bottom: 1px solid #E0E0E0;
        padding: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #333333;
        font-weight: 500;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 1rem 2rem;
        border: none;
        border-bottom: 3px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #8C1D40;
        border-bottom: 3px solid #8C1D40;
        font-weight: 600;
    }
    
    .sidebar-header {
        background-color: #8C1D40;
        color: white;
        padding: 1.5rem;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
    }
    
    .sidebar-header h2 {
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stSlider > div > div > div {
        border: 1px solid #E0E0E0;
        border-radius: 4px;
    }
    
    .stSelectbox > label,
    .stNumberInput > label,
    .stSlider > label {
        font-weight: 500;
        color: #333333;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .success-highlight {
        background-color: rgba(76, 175, 80, 0.1);
        border: 1px solid #4CAF50;
        border-left: 4px solid #4CAF50;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    
    .warning-highlight {
        background-color: rgba(255, 193, 7, 0.1);
        border: 1px solid #FFC107;
        border-left: 4px solid #FFC107;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    
    .success-highlight h4,
    .warning-highlight h4 {
        margin: 0 0 0.5rem 0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stDeployButton {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# ========================================================================
# INICIALIZAÇÃO
# ========================================================================
load_corporate_css()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2>AMARO AVIATION</h2>
    </div>
    """, unsafe_allow_html=True)
    
    language_option = st.selectbox(
        "IDIOMA / LANGUAGE",
        ["Português", "English"],
        key="language_selector"
    )
    
    lang = 'pt' if language_option == 'Português' else 'en'

# Header Principal
st.markdown(f"""
<div class="corporate-header">
    <h1>{t('app_title', lang)}</h1>
    <p>{t('app_subtitle', lang)}</p>
</div>
""", unsafe_allow_html=True)

# Carregamento de dados
try:
    params = load_params()
    modelos = params.get('modelos_disponiveis', [])
    
    if not modelos:
        st.error("Nenhum modelo configurado. Verifique os dados em data/modelos.csv")
        st.stop()
        
except Exception as e:
    st.error(f"Erro ao carregar parâmetros: {e}")
    st.stop()

# ========================================================================
# TABS PRINCIPAIS
# ========================================================================
tab1, tab2, tab3 = st.tabs([
    t('tab_profit', lang),
    t('tab_comparison', lang),
    t('tab_settings', lang)
])

# ========================================================================
# TAB 1: ESTIMATIVA DE LUCRO MENSAL
# ========================================================================
with tab1:
    st.markdown(f"""
    <div class="corporate-card">
        <h3>{t('tab_profit', lang)}</h3>
        <p>Simule os lucros mensais estimados com a aeronave em voos fretados via Amaro Aviation</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        modelo_lucro = st.selectbox(
            t('aircraft_model', lang),
            modelos,
            key="modelo_lucro"
        )
    
    with col2:
        horas_mes = st.number_input(
            t('monthly_hours', lang),
            min_value=10,
            max_value=200,
            value=80,
            step=10,
            key="horas_mes"
        )
    
    with col3:
        ocupacao = st.slider(
            t('occupancy_rate', lang),
            min_value=50,
            max_value=95,
            value=75,
            key="ocupacao"
        )
    
    if st.button(t('calculate', lang), key="calc_lucro", type="primary"):
        try:
            resultado_hora = calcula_custo_trecho(modelo_lucro, 1.0, params)
            horas_efetivas = horas_mes * (ocupacao / 100)
            
            preco_hora_mercado = params['preco_mercado_hora'][modelo_lucro]
            receita_bruta = preco_hora_mercado * horas_efetivas
            custo_operacional = resultado_hora['total'] * horas_efetivas
            
            percentual_proprietario = 0.9
            percentual_amaro = 0.1
            
            receita_proprietario = receita_bruta * percentual_proprietario
            receita_amaro = receita_bruta * percentual_amaro
            lucro_liquido = receita_proprietario - custo_operacional
            
            roi_mensal = (lucro_liquido / custo_operacional * 100) if custo_operacional > 0 else 0
            
            st.markdown("### RESULTADOS DA SIMULAÇÃO")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{t('gross_revenue', lang)}</div>
                    <div class="metric-value">{format_currency(receita_bruta, lang)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{t('owner_revenue', lang)}</div>
                    <div class="metric-value">{format_currency(receita_proprietario, lang)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{t('operational_costs', lang)}</div>
                    <div class="metric-value">{format_currency(custo_operacional, lang)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                cor_lucro = '#4CAF50' if lucro_liquido > 0 else '#F44336'
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{t('net_profit', lang)}</div>
                    <div class="metric-value" style="color: {cor_lucro}">{format_currency(lucro_liquido, lang)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            fig_breakdown = go.Figure(data=[go.Pie(
                labels=[
                    t('owner_revenue', lang),
                    t('amaro_fee', lang),
                    t('operational_costs', lang)
                ],
                values=[
                    receita_proprietario - custo_operacional,
                    receita_amaro,
                    custo_operacional
                ],
                hole=0.4,
                marker=dict(colors=['#4CAF50', '#8C1D40', '#F44336']),
                textinfo='label+percent+value',
                texttemplate='<b>%{label}</b><br>%{percent}<br>%{value:,.0f}',
                textfont=dict(size=12)
            )])
            
            fig_breakdown.update_layout(
                title='BREAKDOWN FINANCEIRO MENSAL',
                font=dict(family='Inter, sans-serif', size=12),
                height=500,
                template='plotly_white',
                title_font=dict(size=16, color='#333333')
            )
            
            st.plotly_chart(fig_breakdown, use_container_width=True)
            
            if lucro_liquido > 0:
                st.markdown(f"""
                <div class="success-highlight">
                    <h4>{t('profitable_operation', lang)}</h4>
                    <p><strong>{t('net_profit', lang)}:</strong> {format_currency(lucro_liquido, lang)}</p>
                    <p><strong>{t('monthly_roi', lang)}:</strong> {format_percentage(roi_mensal, lang)}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="warning-highlight">
                    <h4>{t('operation_at_loss', lang)}</h4>
                    <p>Prejuízo mensal: {format_currency(abs(lucro_liquido), lang)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            dados_lucro = {
                "Análise": "Estimativa de Lucro Mensal",
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
                "Estimativa de Lucro Mensal",
                {"modelo": modelo_lucro, "horas": horas_mes, "ocupacao": ocupacao},
                dados_lucro
            )
            
            with col1:
                try:
                    excel_buffer = gerar_excel_simples(relatorio_lucro)
                    if excel_buffer:
                        st.download_button(
                            t('export_excel', lang),
                            data=excel_buffer.getvalue(),
                            file_name=f"amaro_lucro_mensal_{datetime.now().strftime('%Y%m%d')}.xlsx",
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
                            t('export_pdf', lang),
                            data=pdf_buffer.getvalue(),
                            file_name=f"amaro_lucro_mensal_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Erro ao gerar PDF: {e}")
                    
        except Exception as e:
            st.error(f"{t('calculation_error', lang)}: {e}")

# ========================================================================
# TAB 2: COMPARATIVO DE CUSTOS
# ========================================================================
with tab2:
    st.markdown(f"""
    <div class="corporate-card">
        <h3>{t('tab_comparison', lang)}</h3>
        <p>Compare os custos totais de gestão própria versus gestão com a Amaro Aviation</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        modelo_comp = st.selectbox(
            t('aircraft_model', lang),
            modelos,
            key="modelo_comp"
        )
        
        horas_anuais = st.number_input(
            t('annual_hours', lang),
            min_value=50,
            max_value=800,
            value=300,
            step=25,
            key="horas_anuais"
        )
    
    with col2:
        custos_fixos_anuais = st.number_input(
            t('fixed_costs', lang),
            min_value=50000,
            max_value=2000000,
            value=500000,
            step=25000,
            key="custos_fixos"
        )
        
        include_charter = st.checkbox(
            t('include_charter', lang),
            value=True,
            key="include_charter"
        )
    
    if st.button(t('calculate', lang), key="calc_comp", type="primary"):
        try:
            resultado_ano = calcula_custo_trecho(modelo_comp, horas_anuais, params)
            custo_operacional_ano = resultado_ano['total']
            custo_total_proprio = custo_operacional_ano + custos_fixos_anuais
            
            custo_amaro_ano = custo_operacional_ano
            
            receita_charter = 0
            if include_charter:
                preco_hora = params['preco_mercado_hora'][modelo_comp]
                receita_charter = preco_hora * horas_anuais * 0.6
            
            custo_liquido_proprio = custo_total_proprio - receita_charter
            custo_liquido_amaro = custo_amaro_ano - receita_charter
            
            economia_anual = custo_liquido_proprio - custo_liquido_amaro
            percentual_economia = (economia_anual / custo_liquido_proprio * 100) if custo_liquido_proprio > 0 else 0
            
            st.markdown("### COMPARATIVO ANUAL DE CUSTOS")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="corporate-card" style="background: #FFF8E1; border-left: 4px solid #FFC107;">
                    <h4 style="color: #FF8F00; margin: 0 0 1rem 0;">{t('own_management', lang)}</h4>
                    <div class="metric-value" style="color: #FF8F00;">{format_currency(custo_liquido_proprio, lang)}</div>
                    <hr style="border-color: #E0E0E0;">
                    <p><strong>{t('operational_costs', lang)}:</strong> {format_currency(custo_operacional_ano, lang)}</p>
                    <p><strong>Custos Fixos:</strong> {format_currency(custos_fixos_anuais, lang)}</p>
                    {f"<p><strong>Receita Charter:</strong> -{format_currency(receita_charter, lang)}</p>" if include_charter else ""}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="corporate-card" style="background: #E8F5E8; border-left: 4px solid #4CAF50;">
                    <h4 style="color: #2E7D32; margin: 0 0 1rem 0;">{t('amaro_management', lang)}</h4>
                    <div class="metric-value" style="color: #2E7D32;">{format_currency(custo_liquido_amaro, lang)}</div>
                    <hr style="border-color: #E0E0E0;">
                    <p><strong>{t('operational_costs', lang)}:</strong> {format_currency(custo_amaro_ano, lang)}</p>
                    <p><strong>Custos Fixos:</strong> {format_currency(0, lang)}</p>
                    {f"<p><strong>Receita Charter:</strong> -{format_currency(receita_charter, lang)}</p>" if include_charter else ""}
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                cor_economia = '#4CAF50' if economia_anual > 0 else '#F44336'
                st.markdown(f"""
                <div class="corporate-card" style="background: {'#E8F5E8' if economia_anual > 0 else '#FFEBEE'}; border-left: 4px solid {cor_economia};">
                    <h4 style="color: {cor_economia}; margin: 0 0 1rem 0;">{t('annual_savings', lang)}</h4>
                    <div class="metric-value" style="color: {cor_economia};">{format_currency(abs(economia_anual), lang)}</div>
                    <hr style="border-color: #E0E0E0;">
                    <p><strong>{t('savings_percentage', lang)}:</strong> {format_percentage(percentual_economia, lang)}</p>
                    <p><strong>Economia Mensal:</strong> {format_currency(economia_anual/12, lang)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            fig_comp = go.Figure()
            
            categorias = [t('own_management', lang), t('amaro_management', lang)]
            valores = [custo_liquido_proprio, custo_liquido_amaro]
            cores = ['#FFC107', '#8C1D40']
            
            fig_comp.add_trace(go.Bar(
                x=categorias,
                y=valores,
                marker_color=cores,
                text=[format_currency(v, lang) for v in valores],
                textposition='outside',
                textfont=dict(size=14, color='#333333')
            ))
            
            if economia_anual > 0:
                fig_comp.add_annotation(
                    x=0.5, y=max(valores) * 0.8,
                    text=f"{t('annual_savings', lang)}<br><b>{format_currency(economia_anual, lang)}</b>",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor='#4CAF50',
                    font=dict(size=14, color='#4CAF50')
                )
            
            fig_comp.update_layout(
                title='COMPARATIVO ANUAL DE CUSTOS',
                yaxis_title='Custo Anual (R$)' if lang == 'pt' else 'Annual Cost (R$)',
                template='plotly_white',
                height=500,
                font=dict(family='Inter, sans-serif', size=12),
                title_font=dict(size=16, color='#333333')
            )
            
            st.plotly_chart(fig_comp, use_container_width=True)
            
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
                            t('export_excel', lang),
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
                            t('export_pdf', lang),
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
# TAB 3: CONFIGURAÇÕES
# ========================================================================
with tab3:
    st.markdown(f"""
    <div class="corporate-card">
        <h3>{t('tab_settings', lang)}</h3>
        <p>Ajuste os parâmetros de cálculo e salve as configurações</p>
    </div>
    """, unsafe_allow_html=True)
    
    config_tab1, config_tab2 = st.tabs([
        "PARÂMETROS" if lang == 'pt' else "PARAMETERS",
        "FÓRMULAS" if lang == 'pt' else "FORMULAS"
    ])
    
    with config_tab1:
        st.markdown("### PARÂMETROS OPERACIONAIS" if lang == 'pt' else "### OPERATIONAL PARAMETERS")
        
        col1, col2 = st.columns(2)
        
        with col1:
            preco_combustivel = st.number_input(
                t('fuel_price', lang),
                min_value=1.0,
                max_value=50.0,
                value=float(params['preco_combustivel']),
                step=0.1,
                format="%.2f"
            )
            
            custo_piloto = st.number_input(
                t('pilot_cost', lang),
                min_value=500.0,
                max_value=5000.0,
                value=float(params['custo_piloto_hora']),
                step=50.0,
                format="%.0f"
            )
            
            depreciacao = st.number_input(
                t('depreciation', lang),
                min_value=1.0,
                max_value=20.0,
                value=float(params['depreciacao_anual_pct']),
                step=0.5,
                format="%.1f"
            )
        
        with col2:
            manut_turboprop = st.number_input(
                t('maintenance_turboprop', lang),
                min_value=500.0,
                max_value=5000.0,
                value=float(params['custo_manutencao_hora']['turboprop']),
                step=100.0,
                format="%.0f"
            )
            
            manut_jato = st.number_input(
                t('maintenance_jet', lang),
                min_value=1000.0,
                max_value=10000.0,
                value=float(params['custo_manutencao_hora']['jato']),
                step=200.0,
                format="%.0f"
            )
            
            mercado_turboprop = st.number_input(
                t('market_price_turboprop', lang),
                min_value=3000.0,
                max_value=15000.0,
                value=float(params['preco_mercado']['turboprop']),
                step=500.0,
                format="%.0f"
            )
            
            mercado_jato = st.number_input(
                t('market_price_jet', lang),
                min_value=8000.0,
                max_value=30000.0,
                value=float(params['preco_mercado']['jato']),
                step=1000.0,
                format="%.0f"
            )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(t('save_settings', lang), type="primary", use_container_width=True):
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
                        st.success(t('settings_saved', lang))
                        st.rerun()
                    else:
                        st.error("Erro ao salvar configurações")
                        
                except Exception as e:
                    st.error(f"Erro ao processar dados: {e}")
    
    with config_tab2:
        st.markdown("### FÓRMULAS UTILIZADAS" if lang == 'pt' else "### FORMULAS USED")
        
        st.markdown(f"""
        <div class="corporate-card">
            <h4>CÁLCULO DE CUSTO POR HORA</h4>
            <div style="background: #F5F5F5; padding: 1rem; border-radius: 4px; margin: 1rem 0; border-left: 4px solid #8C1D40;">
                <code style="font-family: 'Courier New', monospace; color: #333333;">
                {'Custo Total/Hora = Combustível + Piloto + Manutenção + Depreciação' if lang == 'pt' else 'Total Cost/Hour = Fuel + Pilot + Maintenance + Depreciation'}
                <br><br>
                {'Onde:' if lang == 'pt' else 'Where:'}<br>
                • {'Combustível = Consumo (L/h) × Preço Combustível (R$/L)' if lang == 'pt' else 'Fuel = Consumption (L/h) × Fuel Price (R$/L)'}<br>
                • {'Piloto = Custo Piloto (R$/h)' if lang == 'pt' else 'Pilot = Pilot Cost (R$/h)'}<br>
                • {'Manutenção = Custo Manutenção por tipo (R$/h)' if lang == 'pt' else 'Maintenance = Maintenance Cost per type (R$/h)'}<br>
                • {'Depreciação = (Valor Aeronave × % Depreciação Anual) ÷ Horas Anuais' if lang == 'pt' else 'Depreciation = (Aircraft Value × Annual Depreciation %) ÷ Annual Hours'}
                </code>
            </div>
        </div>
        
        <div class="corporate-card">
            <h4>CÁLCULO DE ECONOMIA</h4>
            <div style="background: #F5F5F5; padding: 1rem; border-radius: 4px; margin: 1rem 0; border-left: 4px solid #8C1D40;">
                <code style="font-family: 'Courier New', monospace; color: #333333;">
                {'Economia = Preço Mercado - Custo Amaro' if lang == 'pt' else 'Savings = Market Price - Amaro Cost'}
                <br><br>
                {'Percentual Economia = (Economia ÷ Preço Mercado) × 100' if lang == 'pt' else 'Savings Percentage = (Savings ÷ Market Price) × 100'}
                </code>
            </div>
        </div>
        
        <div class="corporate-card">
            <h4>MODELO DE RECEITA AMARO AVIATION</h4>
            <div style="background: #F5F5F5; padding: 1rem; border-radius: 4px; margin: 1rem 0; border-left: 4px solid #8C1D40;">
                <code style="font-family: 'Courier New', monospace; color: #333333;">
                {'Receita do Proprietário = Receita Bruta × 90%' if lang == 'pt' else 'Owner Revenue = Gross Revenue × 90%'}<br>
                {'Taxa Amaro Aviation = Receita Bruta × 10%' if lang == 'pt' else 'Amaro Aviation Fee = Gross Revenue × 10%'}<br>
                {'Lucro Líquido = Receita do Proprietário - Custos Operacionais' if lang == 'pt' else 'Net Profit = Owner Revenue - Operational Costs'}
                </code>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ========================================================================
# SIDEBAR - INFORMAÇÕES E STATUS
# ========================================================================
with st.sidebar:
    st.markdown("---")
    st.markdown("### STATUS DO SISTEMA" if lang == 'pt' else "### SYSTEM STATUS")
    
    st.success(f"""
    **{t('system_operational', lang)}**
    - {'Modelos' if lang == 'pt' else 'Models'}: {len(modelos)} {t('models_configured', lang)}
    - {'Parâmetros' if lang == 'pt' else 'Parameters'}: {'Carregados' if lang == 'pt' else 'Loaded'}
    - {'Idioma' if lang == 'pt' else 'Language'}: {language_option}
    """)
    
    st.markdown("### FUNCIONALIDADES" if lang == 'pt' else "### FEATURES")
    st.info(f"""
    **LUCRO MENSAL:**
    {'Simula receitas e custos mensais' if lang == 'pt' else 'Simulates monthly revenues and costs'}
    
    **COMPARATIVO:**
    {'Compara gestão própria vs. Amaro' if lang == 'pt' else 'Compares own management vs. Amaro'}
    
    **CONFIGURAÇÕES:**
    {'Ajusta parâmetros e visualiza fórmulas' if lang == 'pt' else 'Adjusts parameters and shows formulas'}
    """)
    
    st.markdown("### INSTRUÇÕES DE USO" if lang == 'pt' else "### USAGE INSTRUCTIONS")
    if lang == 'pt':
        st.markdown("""
        - Use ocupação de 70-80% para projeções realistas
        - Considere custos fixos reais (hangar, seguro, etc.)
        - Revise parâmetros periodicamente
        - Exporte relatórios para apresentações
        """)
    else:
        st.markdown("""
        - Use 70-80% occupancy for realistic projections
        - Consider real fixed costs (hangar, insurance, etc.)
        - Review parameters periodically
        - Export reports for presentations
        """)
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #333333; font-size: 0.8rem; font-weight: 400;">
        <p><strong>AMARO AVIATION CALCULATOR</strong></p>
        <p>VERSÃO 3.0</p>
        <p>{t('developed_with_love', lang)}</p>
    </div>
    """, unsafe_allow_html=True)