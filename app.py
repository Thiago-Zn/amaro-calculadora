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
    page_title="Amaro Aviation - Calculadora Premium",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================================================
# SISTEMA DE IDIOMAS SIMPLIFICADO
# ========================================================================
@st.cache_data
def get_translations():
    """Sistema de traduções integrado"""
    return {
        'pt': {
            # Interface Principal
            'app_title': 'Amaro Aviation',
            'app_subtitle': 'Calculadora Inteligente de Custos Operacionais',
            'language': 'Idioma',
            
            # Abas
            'tab_profit': '📈 Estimativa de Lucro Mensal',
            'tab_comparison': '⚖️ Comparativo de Custos',
            'tab_settings': '⚙️ Configurações e Fórmulas',
            
            # Campos
            'aircraft_model': 'Modelo da Aeronave',
            'monthly_hours': 'Horas de Voo por Mês',
            'occupancy_rate': 'Taxa de Ocupação (%)',
            'annual_hours': 'Horas de Voo por Ano',
            'fixed_costs': 'Custos Fixos Anuais (R$)',
            'include_charter': 'Incluir Receita de Charter',
            'calculate': '🚀 Calcular',
            
            # Resultados
            'gross_revenue': 'Receita Bruta',
            'owner_revenue': 'Receita do Proprietário (90%)',
            'amaro_fee': 'Taxa Amaro (10%)',
            'operational_costs': 'Custos Operacionais',
            'net_profit': 'Lucro Líquido',
            'monthly_roi': 'ROI Mensal',
            'own_management': 'Gestão Própria',
            'amaro_management': 'Gestão Amaro Aviation',
            'annual_savings': 'Economia Anual',
            'savings_percentage': 'Percentual de Economia',
            
            # Configurações
            'fuel_price': 'Preço do Combustível (R$/L)',
            'pilot_cost': 'Custo Piloto (R$/h)',
            'depreciation': 'Depreciação Anual (%)',
            'maintenance_turboprop': 'Manutenção Turboprop (R$/h)',
            'maintenance_jet': 'Manutenção Jato (R$/h)',
            'market_price_turboprop': 'Preço Mercado Turboprop (R$/h)',
            'market_price_jet': 'Preço Mercado Jato (R$/h)',
            'save_settings': '💾 Salvar Configurações',
            
            # Status
            'system_operational': 'Sistema Operacional',
            'models_configured': 'modelos configurados',
            'profitable_operation': 'Operação Rentável',
            'operation_at_loss': 'Atenção: Operação no Prejuízo',
            'settings_saved': 'Configurações salvas com sucesso!',
            'calculation_error': 'Erro no cálculo',
            
            # Exportação
            'export_excel': '📊 Baixar Excel',
            'export_pdf': '📄 Baixar PDF',
            'developed_with_love': 'Desenvolvido com ❤️ para excelência comercial'
        },
        'en': {
            # Main Interface
            'app_title': 'Amaro Aviation',
            'app_subtitle': 'Smart Operating Cost Calculator',
            'language': 'Language',
            
            # Tabs
            'tab_profit': '📈 Monthly Profit Estimation',
            'tab_comparison': '⚖️ Cost Comparison',
            'tab_settings': '⚙️ Settings & Formulas',
            
            # Fields
            'aircraft_model': 'Aircraft Model',
            'monthly_hours': 'Flight Hours per Month',
            'occupancy_rate': 'Occupancy Rate (%)',
            'annual_hours': 'Annual Flight Hours',
            'fixed_costs': 'Annual Fixed Costs (R$)',
            'include_charter': 'Include Charter Revenue',
            'calculate': '🚀 Calculate',
            
            # Results
            'gross_revenue': 'Gross Revenue',
            'owner_revenue': 'Owner Revenue (90%)',
            'amaro_fee': 'Amaro Fee (10%)',
            'operational_costs': 'Operational Costs',
            'net_profit': 'Net Profit',
            'monthly_roi': 'Monthly ROI',
            'own_management': 'Own Management',
            'amaro_management': 'Amaro Aviation Management',
            'annual_savings': 'Annual Savings',
            'savings_percentage': 'Savings Percentage',
            
            # Settings  
            'fuel_price': 'Fuel Price (R$/L)',
            'pilot_cost': 'Pilot Cost (R$/h)',
            'depreciation': 'Annual Depreciation (%)',
            'maintenance_turboprop': 'Turboprop Maintenance (R$/h)',
            'maintenance_jet': 'Jet Maintenance (R$/h)',
            'market_price_turboprop': 'Turboprop Market Price (R$/h)',
            'market_price_jet': 'Jet Market Price (R$/h)',
            'save_settings': '💾 Save Settings',
            
            # Status
            'system_operational': 'System Operational',
            'models_configured': 'models configured',
            'profitable_operation': 'Profitable Operation',
            'operation_at_loss': 'Warning: Operation at Loss',
            'settings_saved': 'Settings saved successfully!',
            'calculation_error': 'Calculation error',
            
            # Export
            'export_excel': '📊 Download Excel',
            'export_pdf': '📄 Download PDF', 
            'developed_with_love': 'Developed with ❤️ for commercial excellence'
        }
    }

def t(key, lang='pt'):
    """Função de tradução"""
    translations = get_translations()
    return translations.get(lang, translations['pt']).get(key, key)

# ========================================================================
# CSS MODERNO E ELEGANTE
# ========================================================================
def load_premium_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(140, 29, 64, 0.2);
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.3rem;
        font-weight: 300;
        margin: 1rem 0 0 0;
        opacity: 0.9;
    }
    
    .premium-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        margin: 1.5rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .premium-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.12);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border-left: 4px solid #8c1d40;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #8c1d40;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(140, 29, 64, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(140, 29, 64, 0.4);
        background: linear-gradient(135deg, #9e2148 0%, #b02356 100%);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.9);
        border-radius: 12px;
        padding: 0.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #495057;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(140, 29, 64, 0.3);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .success-highlight {
        background: linear-gradient(135deg, #27AE60 0%, #2ECC71 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .warning-highlight {
        background: linear-gradient(135deg, #F39C12 0%, #E67E22 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ========================================================================
# CARREGAMENTO DE DADOS E INICIALIZAÇÃO
# ========================================================================
load_premium_css()

# Sidebar - Seleção de idioma
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2 style="margin: 0;">✈️</h2>
        <p style="margin: 0.5rem 0 0 0; font-weight: 600;">Amaro Aviation</p>
    </div>
    """, unsafe_allow_html=True)
    
    language_option = st.selectbox(
        "🌐 Language / Idioma",
        ["🇧🇷 Português", "🇺🇸 English"],
        key="language_selector"
    )
    
    lang = 'pt' if '🇧🇷' in language_option else 'en'

# Header Principal
st.markdown(f"""
<div class="main-header">
    <h1>{t('app_title', lang)}</h1>
    <p>{t('app_subtitle', lang)}</p>
</div>
""", unsafe_allow_html=True)

# Carregamento de dados
try:
    params = load_params()
    modelos = params.get('modelos_disponiveis', [])
    
    if not modelos:
        st.error("⚠️ Nenhum modelo configurado. Verifique os dados em data/modelos.csv")
        st.stop()
        
except Exception as e:
    st.error(f"❌ Erro ao carregar parâmetros: {e}")
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
    <div class="premium-card">
        <h3>📊 {t('tab_profit', lang)}</h3>
        <p>Simule os lucros mensais estimados com a aeronave em voos fretados via Amaro Aviation</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        modelo_lucro = st.selectbox(
            f"✈️ {t('aircraft_model', lang)}",
            modelos,
            key="modelo_lucro"
        )
    
    with col2:
        horas_mes = st.number_input(
            f"⏰ {t('monthly_hours', lang)}",
            min_value=10,
            max_value=200,
            value=80,
            step=10,
            key="horas_mes"
        )
    
    with col3:
        ocupacao = st.slider(
            f"📊 {t('occupancy_rate', lang)}",
            min_value=50,
            max_value=95,
            value=75,
            key="ocupacao"
        )
    
    if st.button(f"{t('calculate', lang)}", key="calc_lucro", type="primary"):
        try:
            # Cálculos base
            resultado_hora = calcula_custo_trecho(modelo_lucro, 1.0, params)
            horas_efetivas = horas_mes * (ocupacao / 100)
            
            # Receitas e custos
            preco_hora_mercado = params['preco_mercado_hora'][modelo_lucro]
            receita_bruta = preco_hora_mercado * horas_efetivas
            custo_operacional = resultado_hora['total'] * horas_efetivas
            
            # Percentuais Amaro Aviation
            percentual_proprietario = 0.9  # 90% para proprietário
            percentual_amaro = 0.1  # 10% para Amaro
            
            receita_proprietario = receita_bruta * percentual_proprietario
            receita_amaro = receita_bruta * percentual_amaro
            lucro_liquido = receita_proprietario - custo_operacional
            
            # Métricas avançadas
            roi_mensal = (lucro_liquido / custo_operacional * 100) if custo_operacional > 0 else 0
            
            # Exibição dos resultados
            st.markdown("### 💰 Resultados da Simulação")
            
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
                cor_lucro = '#27AE60' if lucro_liquido > 0 else '#E74C3C'
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{t('net_profit', lang)}</div>
                    <div class="metric-value" style="color: {cor_lucro}">{format_currency(lucro_liquido, lang)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Gráfico de breakdown
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
                marker=dict(colors=['#27AE60', '#8c1d40', '#E74C3C']),
                textinfo='label+percent+value',
                texttemplate='<b>%{label}</b><br>%{percent}<br>%{value:,.0f}'
            )])
            
            fig_breakdown.update_layout(
                title='📊 Breakdown Financeiro Mensal',
                font=dict(size=12),
                height=500,
                template='plotly_white'
            )
            
            st.plotly_chart(fig_breakdown, use_container_width=True)
            
            # Insights
            if lucro_liquido > 0:
                st.markdown(f"""
                <div class="success-highlight">
                    <h4>✅ {t('profitable_operation', lang)}</h4>
                    <p><strong>{t('net_profit', lang)}:</strong> {format_currency(lucro_liquido, lang)}</p>
                    <p><strong>{t('monthly_roi', lang)}:</strong> {format_percentage(roi_mensal, lang)}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="warning-highlight">
                    <h4>⚠️ {t('operation_at_loss', lang)}</h4>
                    <p>Prejuízo mensal: {format_currency(abs(lucro_liquido), lang)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Exportação
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
    <div class="premium-card">
        <h3>⚖️ {t('tab_comparison', lang)}</h3>
        <p>Compare os custos totais de gestão própria versus gestão com a Amaro Aviation</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        modelo_comp = st.selectbox(
            f"✈️ {t('aircraft_model', lang)}",
            modelos,
            key="modelo_comp"
        )
        
        horas_anuais = st.number_input(
            f"⏰ {t('annual_hours', lang)}",
            min_value=50,
            max_value=800,
            value=300,
            step=25,
            key="horas_anuais"
        )
    
    with col2:
        custos_fixos_anuais = st.number_input(
            f"💰 {t('fixed_costs', lang)}",
            min_value=50000,
            max_value=2000000,
            value=500000,
            step=25000,
            key="custos_fixos"
        )
        
        include_charter = st.checkbox(
            f"📈 {t('include_charter', lang)}",
            value=True,
            key="include_charter"
        )
    
    if st.button(f"{t('calculate', lang)}", key="calc_comp", type="primary"):
        try:
            # Cálculos para gestão própria
            resultado_ano = calcula_custo_trecho(modelo_comp, horas_anuais, params)
            custo_operacional_ano = resultado_ano['total']
            custo_total_proprio = custo_operacional_ano + custos_fixos_anuais
            
            # Cálculos para gestão Amaro (sem custos fixos)
            custo_amaro_ano = custo_operacional_ano
            
            # Receita de charter (se incluída)
            receita_charter = 0
            if include_charter:
                preco_hora = params['preco_mercado_hora'][modelo_comp]
                receita_charter = preco_hora * horas_anuais * 0.6  # 60% ocupação estimada
            
            # Custos líquidos
            custo_liquido_proprio = custo_total_proprio - receita_charter
            custo_liquido_amaro = custo_amaro_ano - receita_charter
            
            economia_anual = custo_liquido_proprio - custo_liquido_amaro
            percentual_economia = (economia_anual / custo_liquido_proprio * 100) if custo_liquido_proprio > 0 else 0
            
            # Exibição comparativa
            st.markdown("### 📊 Comparativo Anual de Custos")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="premium-card" style="background: linear-gradient(135deg, #fff3cd 0%, #fce8b2 100%);">
                    <h4>🏠 {t('own_management', lang)}</h4>
                    <div class="metric-value" style="color: #856404;">{format_currency(custo_liquido_proprio, lang)}</div>
                    <hr>
                    <p><strong>{t('operational_costs', lang)}:</strong> {format_currency(custo_operacional_ano, lang)}</p>
                    <p><strong>Custos Fixos:</strong> {format_currency(custos_fixos_anuais, lang)}</p>
                    {f"<p><strong>Receita Charter:</strong> -{format_currency(receita_charter, lang)}</p>" if include_charter else ""}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="premium-card" style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);">
                    <h4>✈️ {t('amaro_management', lang)}</h4>
                    <div class="metric-value" style="color: #155724;">{format_currency(custo_liquido_amaro, lang)}</div>
                    <hr>
                    <p><strong>{t('operational_costs', lang)}:</strong> {format_currency(custo_amaro_ano, lang)}</p>
                    <p><strong>Custos Fixos:</strong> {format_currency(0, lang)}</p>
                    {f"<p><strong>Receita Charter:</strong> -{format_currency(receita_charter, lang)}</p>" if include_charter else ""}
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                cor_economia = '#27AE60' if economia_anual > 0 else '#E74C3C'
                st.markdown(f"""
                <div class="premium-card" style="background: linear-gradient(135deg, {'#d4edda' if economia_anual > 0 else '#f8d7da'} 0%, {'#c3e6cb' if economia_anual > 0 else '#f5c6cb'} 100%);">
                    <h4>💎 {t('annual_savings', lang)}</h4>
                    <div class="metric-value" style="color: {cor_economia};">{format_currency(abs(economia_anual), lang)}</div>
                    <hr>
                    <p><strong>{t('savings_percentage', lang)}:</strong> {format_percentage(percentual_economia, lang)}</p>
                    <p><strong>Economia Mensal:</strong> {format_currency(economia_anual/12, lang)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Gráfico comparativo
            fig_comp = go.Figure()
            
            categorias = [t('own_management', lang), t('amaro_management', lang)]
            valores = [custo_liquido_proprio, custo_liquido_amaro]
            cores = ['#FFC107', '#8c1d40']
            
            fig_comp.add_trace(go.Bar(
                x=categorias,
                y=valores,
                marker_color=cores,
                text=[format_currency(v, lang) for v in valores],
                textposition='outside'
            ))
            
            # Adicionar anotação de economia
            if economia_anual > 0:
                fig_comp.add_annotation(
                    x=0.5, y=max(valores) * 0.8,
                    text=f"{t('annual_savings', lang)}<br><b>{format_currency(economia_anual, lang)}</b>",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor='#27AE60',
                    font=dict(size=14, color='#27AE60')
                )
            
            fig_comp.update_layout(
                title='⚖️ Comparativo Anual de Custos',
                yaxis_title='Custo Anual (R$)' if lang == 'pt' else 'Annual Cost (R$)',
                template='plotly_white',
                height=500
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
# TAB 3: CONFIGURAÇÕES E FÓRMULAS
# ========================================================================
with tab3:
    st.markdown(f"""
    <div class="premium-card">
        <h3>⚙️ {t('tab_settings', lang)}</h3>
        <p>Ajuste os parâmetros de cálculo e visualize as fórmulas utilizadas</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sub-tabs para organizar configurações
    config_tab1, config_tab2 = st.tabs([
        f"💰 {'Parâmetros' if lang == 'pt' else 'Parameters'}", 
        f"📐 {'Fórmulas' if lang == 'pt' else 'Formulas'}"
    ])
    
    with config_tab1:
        st.markdown(f"### {'Parâmetros Operacionais' if lang == 'pt' else 'Operational Parameters'}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            preco_combustivel = st.number_input(
                f"⛽ {t('fuel_price', lang)}",
                value=float(params['preco_combustivel']),
                min_value=1.0,
                max_value=50.0,
                step=0.1,
                format="%.2f"
            )
            
            custo_piloto = st.number_input(
                f"👨‍✈️ {t('pilot_cost', lang)}",
                value=float(params['custo_piloto_hora']),
                min_value=500,
                max_value=5000,
                step=50
            )
            
            depreciacao = st.number_input(
                f"📉 {t('depreciation', lang)}",
                value=float(params['depreciacao_anual_pct']),
                min_value=1.0,
                max_value=20.0,
                step=0.5,
                format="%.1f"
            )
        
        with col2:
            manut_turboprop = st.number_input(
                f"🛩️ {t('maintenance_turboprop', lang)}",
                value=float(params['custo_manutencao_hora']['turboprop']),
                min_value=500,
                max_value=5000,
                step=100
            )
            
            manut_jato = st.number_input(
                f"✈️ {t('maintenance_jet', lang)}",
                value=float(params['custo_manutencao_hora']['jato']),
                min_value=1000,
                max_value=10000,
                step=200
            )
            
            mercado_turboprop = st.number_input(
                f"🛩️ {t('market_price_turboprop', lang)}",
                value=float(params['preco_mercado']['turboprop']),
                min_value=3000,
                max_value=15000,
                step=500
            )
            
            mercado_jato = st.number_input(
                f"✈️ {t('market_price_jet', lang)}",
                value=float(params['preco_mercado']['jato']),
                min_value=8000,
                max_value=30000,
                step=1000
            )
        
        # Botão de salvar
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"{t('save_settings', lang)}", type="primary", use_container_width=True):
                try:
                    # Atualizar parâmetros
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
                        st.success(f"✅ {t('settings_saved', lang)}")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao salvar configurações")
                        
                except Exception as e:
                    st.error(f"❌ Erro ao processar dados: {e}")
    
    with config_tab2:
        st.markdown(f"### {'Fórmulas Utilizadas' if lang == 'pt' else 'Formulas Used'}")
        
        st.markdown(f"""
        <div class="premium-card">
            <h4>🔧 {'Cálculo de Custo por Hora' if lang == 'pt' else 'Cost per Hour Calculation'}</h4>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <code>
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
        
        <div class="premium-card">
            <h4>💰 {'Cálculo de Economia' if lang == 'pt' else 'Savings Calculation'}</h4>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <code>
                {'Economia = Preço Mercado - Custo Amaro' if lang == 'pt' else 'Savings = Market Price - Amaro Cost'}
                <br><br>
                {'Percentual Economia = (Economia ÷ Preço Mercado) × 100' if lang == 'pt' else 'Savings Percentage = (Savings ÷ Market Price) × 100'}
                </code>
            </div>
        </div>
        
        <div class="premium-card">
            <h4>📊 {'Modelo de Receita Amaro Aviation' if lang == 'pt' else 'Amaro Aviation Revenue Model'}</h4>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <code>
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
    st.markdown(f"### 📊 {'Status do Sistema' if lang == 'pt' else 'System Status'}")
    
    st.success(f"""
    **✅ {t('system_operational', lang)}**
    - {'Modelos' if lang == 'pt' else 'Models'}: {len(modelos)} {t('models_configured', lang)}
    - {'Parâmetros' if lang == 'pt' else 'Parameters'}: {'Carregados' if lang == 'pt' else 'Loaded'}
    - {'Idioma' if lang == 'pt' else 'Language'}: {language_option}
    """)
    
    st.markdown(f"### 🎯 {'Funcionalidades' if lang == 'pt' else 'Features'}")
    st.info(f"""
    **📈 {'Lucro Mensal' if lang == 'pt' else 'Monthly Profit'}:**
    {'Simula receitas e custos mensais' if lang == 'pt' else 'Simulates monthly revenues and costs'}
    
    **⚖️ {'Comparativo' if lang == 'pt' else 'Comparison'}:**
    {'Compara gestão própria vs. Amaro' if lang == 'pt' else 'Compares own management vs. Amaro'}
    
    **⚙️ {'Configurações' if lang == 'pt' else 'Settings'}:**
    {'Ajusta parâmetros e visualiza fórmulas' if lang == 'pt' else 'Adjusts parameters and shows formulas'}
    """)
    
    st.markdown(f"### 💡 {'Dicas de Uso' if lang == 'pt' else 'Usage Tips'}")
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
    <div style="text-align: center; color: #6c757d; font-size: 0.8rem;">
        <p><strong>Amaro Aviation Calculator</strong></p>
        <p>v3.0 - {'Sistema Refatorado' if lang == 'pt' else 'Refactored System'}</p>
        <p>{t('developed_with_love', lang)}</p>
    </div>
    """, unsafe_allow_html=True)