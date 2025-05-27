import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from utils.params import load_params
from utils.calculations import calcula_custo_trecho

# Configuração da página
st.set_page_config(
    page_title="Amaro Aviation - Calculadora de Custos",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sistema de idiomas simplificado (fallback interno)
def get_translations():
    """Traduções básicas integradas"""
    return {
        'pt': {
            'title': 'Amaro Aviation',
            'subtitle': 'Calculadora Inteligente de Custos Operacionais',
            'language': 'Idioma',
            'monthly_profit': 'Estimativa de Lucro Mensal',
            'cost_comparison': 'Comparativo de Custos',
            'settings': 'Configurações e Fórmulas',
            'aircraft_model': 'Modelo da Aeronave',
            'flight_hours_month': 'Horas de Voo por Mês',
            'occupancy_rate': 'Taxa de Ocupação (%)',
            'annual_hours': 'Horas de Voo por Ano',
            'fixed_costs_annual': 'Custos Fixos Anuais (R$)',
            'include_charter_revenue': 'Incluir Receita de Charter',
            'calculate': 'Calcular',
            'gross_revenue': 'Receita Bruta',
            'owner_share': 'Receita do Proprietário',
            'operational_costs': 'Custos Operacionais',
            'net_profit': 'Lucro Líquido',
            'own_management': 'Gestão Própria',
            'amaro_management': 'Gestão Amaro Aviation',
            'annual_savings': 'Economia Anual',
            'monthly_savings': 'Economia Mensal',
            'savings_percentage': 'Percentual de Economia',
            'fixed_costs': 'Custos Fixos',
            'charter_revenue': 'Receita Charter',
            'fuel_price': 'Preço do Combustível (R$/L)',
            'pilot_cost_hour': 'Custo Piloto (R$/h)',
            'annual_depreciation': 'Depreciação Anual (%)',
            'maintenance_costs': 'Custos de Manutenção',
            'maintenance_turboprop': 'Manutenção Turboprop (R$/h)',
            'maintenance_jet': 'Manutenção Jato (R$/h)',
            'market_price_turboprop': 'Preço Mercado Turboprop (R$/h)',
            'market_price_jet': 'Preço Mercado Jato (R$/h)',
            'save_settings': 'Salvar Configurações',
            'system_status': 'Status do Sistema',
            'system_operational': 'Sistema Operacional',
            'models_configured': 'modelos configurados',
            'parameters_loaded': 'Parâmetros carregados',
            'features': 'Funcionalidades',
            'usage_tips': 'Dicas de Uso',
            'quick_actions': 'Ações Rápidas',
            'reload_data': 'Recarregar Dados',
            'presentation_mode': 'Modo Apresentação',
            'profitable_operation': 'Operação Rentável',
            'operation_at_loss': 'Atenção: Operação no Prejuízo',
            'monthly_deficit': 'Déficit mensal',
            'recommend_increase_occupancy': 'Recomenda-se aumentar ocupação ou revisar custos',
            'monthly_roi': 'ROI Mensal',
            'projected_annual_revenue': 'Receita Anual Projetada',
            'annual_cost_comparison': 'Comparativo Anual: Gestão Própria vs. Amaro Aviation',
            'calculation_error': 'Erro no cálculo',
            'settings_saved': 'Configurações salvas com sucesso!',
            'settings_save_error': 'Erro ao salvar configurações',
            'operational_costs_params': 'Parâmetros de Custos Operacionais',
            'market_reference_prices': 'Preços de Referência do Mercado',
            'formulas_used': 'Fórmulas Utilizadas',
            'impact_preview': 'Preview do Impacto',
            'current_parameters': 'Parâmetros Atuais',
            'cost_calculation_formula': 'Cálculo de Custo por Hora',
            'savings_calculation_formula': 'Cálculo de Economia',
            'roi_calculation_formula': 'Cálculo de ROI',
            'formula_where': 'Onde:',
            'formula_fuel': 'Combustível = Consumo (L/h) × Preço Combustível (R$/L)',
            'formula_pilot': 'Piloto = Custo Piloto (R$/h)',
            'formula_maintenance': 'Manutenção = Custo Manutenção por tipo (R$/h)',
            'formula_depreciation': 'Depreciação = (Valor Aeronave × % Depreciação Anual) ÷ Horas Anuais',
            'developed_with_love': 'Desenvolvido com ❤️ para excelência comercial',
            'version': 'v3.0',
            'refactored_system': 'Sistema Refatorado'
        },
        'en': {
            'title': 'Amaro Aviation',
            'subtitle': 'Smart Operating Cost Calculator',
            'language': 'Language',
            'monthly_profit': 'Monthly Profit Estimation',
            'cost_comparison': 'Cost Comparison',
            'settings': 'Settings & Formulas',
            'aircraft_model': 'Aircraft Model',
            'flight_hours_month': 'Flight Hours per Month',
            'occupancy_rate': 'Occupancy Rate (%)',
            'annual_hours': 'Annual Flight Hours',
            'fixed_costs_annual': 'Annual Fixed Costs (R$)',
            'include_charter_revenue': 'Include Charter Revenue',
            'calculate': 'Calculate',
            'gross_revenue': 'Gross Revenue',
            'owner_share': 'Owner Revenue',
            'operational_costs': 'Operational Costs',
            'net_profit': 'Net Profit',
            'own_management': 'Own Management',
            'amaro_management': 'Amaro Aviation Management',
            'annual_savings': 'Annual Savings',
            'monthly_savings': 'Monthly Savings',
            'savings_percentage': 'Savings Percentage',
            'fixed_costs': 'Fixed Costs',
            'charter_revenue': 'Charter Revenue',
            'fuel_price': 'Fuel Price (R$/L)',
            'pilot_cost_hour': 'Pilot Cost (R$/h)',
            'annual_depreciation': 'Annual Depreciation (%)',
            'maintenance_costs': 'Maintenance Costs',
            'maintenance_turboprop': 'Turboprop Maintenance (R$/h)',
            'maintenance_jet': 'Jet Maintenance (R$/h)',
            'market_price_turboprop': 'Turboprop Market Price (R$/h)',
            'market_price_jet': 'Jet Market Price (R$/h)',
            'save_settings': 'Save Settings',
            'system_status': 'System Status',
            'system_operational': 'System Operational',
            'models_configured': 'models configured',
            'parameters_loaded': 'Parameters loaded',
            'features': 'Features',
            'usage_tips': 'Usage Tips',
            'quick_actions': 'Quick Actions',
            'reload_data': 'Reload Data',
            'presentation_mode': 'Presentation Mode',
            'profitable_operation': 'Profitable Operation',
            'operation_at_loss': 'Warning: Operation at Loss',
            'monthly_deficit': 'Monthly deficit',
            'recommend_increase_occupancy': 'Recommend increasing occupancy or reviewing costs',
            'monthly_roi': 'Monthly ROI',
            'projected_annual_revenue': 'Projected Annual Revenue',
            'annual_cost_comparison': 'Annual Comparison: Own Management vs. Amaro Aviation',
            'calculation_error': 'Calculation error',
            'settings_saved': 'Settings saved successfully!',
            'settings_save_error': 'Error saving settings',
            'operational_costs_params': 'Operational Cost Parameters',
            'market_reference_prices': 'Market Reference Prices',
            'formulas_used': 'Formulas Used',
            'impact_preview': 'Impact Preview',
            'current_parameters': 'Current Parameters',
            'cost_calculation_formula': 'Cost per Hour Calculation',
            'savings_calculation_formula': 'Savings Calculation',
            'roi_calculation_formula': 'ROI Calculation',
            'formula_where': 'Where:',
            'formula_fuel': 'Fuel = Consumption (L/h) × Fuel Price (R$/L)',
            'formula_pilot': 'Pilot = Pilot Cost (R$/h)',
            'formula_maintenance': 'Maintenance = Maintenance Cost per type (R$/h)',
            'formula_depreciation': 'Depreciation = (Aircraft Value × Annual Depreciation %) ÷ Annual Hours',
            'developed_with_love': 'Developed with ❤️ for commercial excellence',
            'version': 'v3.0',
            'refactored_system': 'Refactored System'
        }
    }

def t(key, lang='pt'):
    """Função para obter textos traduzidos"""
    translations = get_translations()
    return translations.get(lang, translations['pt']).get(key, key)

def format_currency(value, lang='pt'):
    """Formata valores monetários de acordo com o idioma"""
    try:
        if lang == 'pt':
            return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            return f"R$ {value:,.2f}"
    except:
        return str(value)

def format_percentage(value, lang='pt'):
    """Formata percentuais de acordo com o idioma"""
    try:
        if lang == 'pt':
            return f"{value:.1f}%".replace(".", ",")
        else:
            return f"{value:.1f}%"
    except:
        return str(value)

# CSS Moderno e Elegante
def load_modern_css():
    st.markdown("""
    <style>
    /* Importar fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset e configurações base */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header principal */
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
    
    /* Cards modernos */
    .modern-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        margin: 1.5rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .modern-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.12);
    }
    
    /* Métricas elegantes */
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
    
    /* Botões modernos */
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
    
    /* Tabs modernos */
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
    
    /* Sidebar elegante */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        border-right: 1px solid rgba(140, 29, 64, 0.1);
    }
    
    /* Inputs modernos */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div:focus-within {
        border-color: #8c1d40;
        box-shadow: 0 0 0 3px rgba(140, 29, 64, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Inicialização
load_modern_css()

# Sidebar - Seleção de idioma
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%); border-radius: 12px; margin-bottom: 2rem;">
        <h2 style="margin: 0; color: white; font-size: 1.5rem;">✈️</h2>
        <p style="margin: 0.5rem 0 0 0; color: white; font-weight: 600;">Amaro Aviation</p>
    </div>
    """, unsafe_allow_html=True)
    
    language = st.selectbox(
        "🌐 Language / Idioma",
        ["🇧🇷 Português", "🇺🇸 English"],
        key="language_selector"
    )
    
    lang = 'pt' if '🇧🇷' in language else 'en'

# Header principal
st.markdown(f"""
<div class="main-header">
    <h1>{t('title', lang)}</h1>
    <p>{t('subtitle', lang)}</p>
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

# Tabs principais - Interface simplificada
tab1, tab2, tab3 = st.tabs([
    f"📈 {t('monthly_profit', lang)}", 
    f"⚖️ {t('cost_comparison', lang)}", 
    f"⚙️ {t('settings', lang)}"
])

# TAB 1: Estimativa de Lucro Mensal
with tab1:
    st.markdown(f"""
    <div class="modern-card">
        <h3>📊 {t('monthly_profit', lang)}</h3>
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
            f"⏰ {t('flight_hours_month', lang)}",
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
    
    if st.button(f"🚀 {t('calculate', lang)}", key="calc_lucro", type="primary"):
        try:
            # Cálculos base
            resultado_hora = calcula_custo_trecho(modelo_lucro, 1.0, params)
            horas_efetivas = horas_mes * (ocupacao / 100)
            
            # Receitas e custos
            preco_hora_mercado = params['preco_mercado_hora'][modelo_lucro]
            receita_bruta = preco_hora_mercado * horas_efetivas
            custo_operacional = resultado_hora['total'] * horas_efetivas
            
            # Percentuais
            percentual_amaro = 0.1  # 10% para Amaro
            percentual_proprietario = 0.9  # 90% para proprietário
            
            receita_proprietario = receita_bruta * percentual_proprietario
            receita_amaro = receita_bruta * percentual_amaro
            lucro_liquido = receita_proprietario - custo_operacional
            
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
                    <div class="metric-label">{t('owner_share', lang)}</div>
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
            
            # Gráfico de pizza - Breakdown
            fig_breakdown = go.Figure(data=[go.Pie(
                labels=['Receita Proprietário', 'Taxa Amaro', 'Custos Operacionais'],
                values=[receita_proprietario - custo_operacional, receita_amaro, custo_operacional],
                hole=0.4,
                marker=dict(colors=['#27AE60', '#8c1d40', '#E74C3C']),
                textinfo='label+percent+value',
                texttemplate='<b>%{label}</b><br>%{percent}<br>%{value:,.0f}'
            )])
            
            fig_breakdown.update_layout(
                title='📊 Breakdown Financeiro Mensal',
                font=dict(size=12),
                height=500
            )
            
            st.plotly_chart(fig_breakdown, use_container_width=True)
            
            # Insights
            if lucro_liquido > 0:
                roi_mensal = (lucro_liquido / custo_operacional * 100) if custo_operacional > 0 else 0
                st.success(f"""
                ✅ **{t('profitable_operation', lang)}**
                - {t('net_profit', lang)}: {format_currency(lucro_liquido, lang)}
                - {t('monthly_roi', lang)}: {format_percentage(roi_mensal, lang)}
                - {t('projected_annual_revenue', lang)}: {format_currency(receita_bruta * 12, lang)}
                """)
            else:
                st.warning(f"""
                ⚠️ **{t('operation_at_loss', lang)}**
                - {t('monthly_deficit', lang)}: {format_currency(abs(lucro_liquido), lang)}
                - {t('recommend_increase_occupancy', lang)}
                """)
                
        except Exception as e:
            st.error(f"{t('calculation_error', lang)}: {e}")

# TAB 2: Comparativo de Custos
with tab2:
    st.markdown(f"""
    <div class="modern-card">
        <h3>⚖️ {t('cost_comparison', lang)}</h3>
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
            f"💰 {t('fixed_costs_annual', lang)}",
            min_value=50000,
            max_value=2000000,
            value=500000,
            step=25000,
            key="custos_fixos"
        )
        
        include_charter = st.checkbox(
            f"📈 {t('include_charter_revenue', lang)}",
            value=True,
            key="include_charter"
        )
    
    if st.button(f"🚀 {t('calculate', lang)}", key="calc_comp", type="primary"):
        try:
            # Cálculos para gestão própria
            resultado_ano = calcula_custo_trecho(modelo_comp, horas_anuais, params)
            custo_operacional_ano = resultado_ano['total']
            custo_total_proprio = custo_operacional_ano + custos_fixos_anuais
            
            # Cálculos para gestão Amaro
            custo_amaro_ano = custo_operacional_ano
            
            # Receita de charter (se incluída)
            receita_charter = 0
            if include_charter:
                preco_hora = params['preco_mercado_hora'][modelo_comp]
                receita_charter = preco_hora * horas_anuais * 0.6  # 60% de ocupação estimada
            
            # Custos líquidos
            custo_liquido_proprio = custo_total_proprio - receita_charter
            custo_liquido_amaro = custo_amaro_ano - receita_charter
            
            economia_anual = custo_liquido_proprio - custo_liquido_amaro
            
            # Exibição comparativa
            st.markdown("### 📊 Comparativo Anual de Custos")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="modern-card" style="background: linear-gradient(135deg, #fff3cd 0%, #fce8b2 100%);">
                    <h4>🏠 {t('own_management', lang)}</h4>
                    <div class="metric-value" style="color: #856404;">{format_currency(custo_liquido_proprio, lang)}</div>
                    <hr>
                    <p><strong>{t('operational_costs', lang)}:</strong> {format_currency(custo_operacional_ano, lang)}</p>
                    <p><strong>{t('fixed_costs', lang)}:</strong> {format_currency(custos_fixos_anuais, lang)}</p>
                    {f"<p><strong>{t('charter_revenue', lang)}:</strong> -{format_currency(receita_charter, lang)}</p>" if include_charter else ""}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="modern-card" style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);">
                    <h4>✈️ {t('amaro_management', lang)}</h4>
                    <div class="metric-value" style="color: #155724;">{format_currency(custo_liquido_amaro, lang)}</div>
                    <hr>
                    <p><strong>{t('operational_costs', lang)}:</strong> {format_currency(custo_amaro_ano, lang)}</p>
                    <p><strong>{t('fixed_costs', lang)}:</strong> {format_currency(0, lang)}</p>
                    {f"<p><strong>{t('charter_revenue', lang)}:</strong> -{format_currency(receita_charter, lang)}</p>" if include_charter else ""}
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                cor_economia = '#27AE60' if economia_anual > 0 else '#E74C3C'
                st.markdown(f"""
                <div class="modern-card" style="background: linear-gradient(135deg, {'#d4edda' if economia_anual > 0 else '#f8d7da'} 0%, {'#c3e6cb' if economia_anual > 0 else '#f5c6cb'} 100%);">
                    <h4>💎 {t('annual_savings', lang)}</h4>
                    <div class="metric-value" style="color: {cor_economia};">{format_currency(abs(economia_anual), lang)}</div>
                    <hr>
                    <p><strong>{t('savings_percentage', lang)}:</strong> {format_percentage(economia_anual/custo_liquido_proprio*100 if custo_liquido_proprio > 0 else 0, lang)}</p>
                    <p><strong>{t('monthly_savings', lang)}:</strong> {format_currency(economia_anual/12, lang)}</p>
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
            
            # Adicionar linha de economia
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
                title=t('annual_cost_comparison', lang),
                yaxis_title='Custo Anual (R$)' if lang == 'pt' else 'Annual Cost (R$)',
                template='plotly_white',
                height=500
            )
            
            st.plotly_chart(fig_comp, use_container_width=True)
            
        except Exception as e:
            st.error(f"{t('calculation_error', lang)}: {e}")

# TAB 3: Configurações e Fórmulas
with tab3:
    st.markdown(f"""
    <div class="modern-card">
        <h3>⚙️ {t('settings', lang)}</h3>
        <p>Ajuste os parâmetros de cálculo e visualize as fórmulas utilizadas</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sub-tabs para organizar configurações
    config_tab1, config_tab2, config_tab3 = st.tabs([
        f"💰 Custos", 
        f"📊 Mercado", 
        f"📐 Fórmulas"
    ])
    
    with config_tab1:
        st.markdown(f"### {t('operational_costs_params', lang)}")
        
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
                f"👨‍✈️ {t('pilot_cost_hour', lang)}",
                value=float(params['custo_piloto_hora']),
                min_value=500,
                max_value=5000,
                step=50
            )
        
        with col2:
            depreciacao = st.number_input(
                f"📉 {t('annual_depreciation', lang)}",
                value=float(params['depreciacao_anual_pct']),
                min_value=1.0,
                max_value=20.0,
                step=0.5,
                format="%.1f"
            )
            
            st.markdown(f"**{t('maintenance_costs', lang)}:**")
            
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
    
    with config_tab2:
        st.markdown(f"### {t('market_reference_prices', lang)}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            mercado_turboprop = st.number_input(
                f"🛩️ {t('market_price_turboprop', lang)}",
                value=float(params['preco_mercado']['turboprop']),
                min_value=3000,
                max_value=15000,
                step=500
            )
        
        with col2:
            mercado_jato = st.number_input(
                f"✈️ {t('market_price_jet', lang)}",
                value=float(params['preco_mercado']['jato']),
                min_value=8000,
                max_value=30000,
                step=1000
            )
        
        # Preview do impacto das mudanças
        st.markdown(f"### 📊 {t('impact_preview', lang)}")
        
        if modelos:
            preview_data = []
            for modelo in modelos[:3]:  # Mostrar apenas os 3 primeiros
                # Calcular com parâmetros atuais
                resultado_atual = calcula_custo_trecho(modelo, 1.0, params)
                
                # Simular com novos parâmetros
                tipo_modelo = 'turboprop' if params['preco_mercado_hora'][modelo] < 12000 else 'jato'
                novo_custo_manut = manut_turboprop if tipo_modelo == 'turboprop' else manut_jato
                novo_preco_mercado = mercado_turboprop if tipo_modelo == 'turboprop' else mercado_jato
                
                # Calcular novo custo
                novo_custo = (
                    params['consumo_modelos'][modelo] * preco_combustivel +
                    custo_piloto +
                    novo_custo_manut +
                    params['depreciacao_hora'][modelo]  # Manter depreciação atual por simplicidade
                )
                
                nova_economia = novo_preco_mercado - novo_custo
                
                preview_data.append({
                    'Modelo' if lang == 'pt' else 'Model': modelo,
                    'Custo Atual' if lang == 'pt' else 'Current Cost': format_currency(resultado_atual['total'], lang),
                    'Novo Custo' if lang == 'pt' else 'New Cost': format_currency(novo_custo, lang),
                    'Economia' if lang == 'pt' else 'Savings': format_currency(nova_economia, lang),
                    'Variação' if lang == 'pt' else 'Change': f"{((novo_custo - resultado_atual['total'])/resultado_atual['total']*100):+.1f}%"
                })
            
            df_preview = pd.DataFrame(preview_data)
            st.dataframe(df_preview, use_container_width=True, hide_index=True)
    
    with config_tab3:
        st.markdown(f"### 📐 {t('formulas_used', lang)}")
        
        st.markdown(f"""
        <div class="modern-card">
            <h4>🔧 {t('cost_calculation_formula', lang)}</h4>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <code>
                {"Custo Total/Hora = Combustível + Piloto + Manutenção + Depreciação" if lang == 'pt' else "Total Cost/Hour = Fuel + Pilot + Maintenance + Depreciation"}
                <br><br>
                {t('formula_where', lang)}<br>
                • {t('formula_fuel', lang)}<br>
                • {t('formula_pilot', lang)}<br>
                • {t('formula_maintenance', lang)}<br>
                • {t('formula_depreciation', lang)}
                </code>
            </div>
        </div>
        
        <div class="modern-card">
            <h4>💰 {t('savings_calculation_formula', lang)}</h4>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <code>
                {"Economia = Preço Mercado - Custo Amaro" if lang == 'pt' else "Savings = Market Price - Amaro Cost"}
                <br><br>
                {"Percentual Economia = (Economia ÷ Preço Mercado) × 100" if lang == 'pt' else "Savings Percentage = (Savings ÷ Market Price) × 100"}
                </code>
            </div>
        </div>
        
        <div class="modern-card">
            <h4>📊 {t('roi_calculation_formula', lang)}</h4>
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <code>
                {"ROI Mensal = (Lucro Líquido ÷ Investimento) × 100" if lang == 'pt' else "Monthly ROI = (Net Profit ÷ Investment) × 100"}
                <br><br>
                {t('formula_where', lang)}<br>
                • {"Lucro Líquido = Receita Proprietário - Custos Operacionais" if lang == 'pt' else "Net Profit = Owner Revenue - Operational Costs"}<br>
                • {"Receita Proprietário = Receita Bruta × 90%" if lang == 'pt' else "Owner Revenue = Gross Revenue × 90%"}<br>
                • {"Receita Bruta = Preço Mercado × Horas Efetivas" if lang == 'pt' else "Gross Revenue = Market Price × Effective Hours"}
                </code>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar parâmetros atuais
        st.markdown(f"### 📋 {t('current_parameters', lang)}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **💰 {"Custos Operacionais" if lang == 'pt' else "Operational Costs"}:**
            - {"Combustível" if lang == 'pt' else "Fuel"}: {format_currency(params['preco_combustivel'], lang)}/L
            - {"Piloto" if lang == 'pt' else "Pilot"}: {format_currency(params['custo_piloto_hora'], lang)}/h
            - {"Depreciação" if lang == 'pt' else "Depreciation"}: {format_percentage(params['depreciacao_anual_pct'], lang)} {"ao ano" if lang == 'pt' else "per year"}
            """)
        
        with col2:
            st.info(f"""
            **🔧 {"Manutenção" if lang == 'pt' else "Maintenance"}:**
            - Turboprop: {format_currency(params['custo_manutencao_hora']['turboprop'], lang)}/h
            - {"Jato" if lang == 'pt' else "Jet"}: {format_currency(params['custo_manutencao_hora']['jato'], lang)}/h
            
            **📊 {"Preços de Mercado" if lang == 'pt' else "Market Prices"}:**
            - Turboprop: {format_currency(params['preco_mercado']['turboprop'], lang)}/h
            - {"Jato" if lang == 'pt' else "Jet"}: {format_currency(params['preco_mercado']['jato'], lang)}/h
            """)
    
    # Botão para salvar configurações
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button(f"💾 {t('save_settings', lang)}", type="primary", use_container_width=True):
            try:
                from utils.params import save_params
                
                # Preparar novos parâmetros
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
                    st.error(f"❌ {t('settings_save_error', lang)}")
                    
            except Exception as e:
                st.error(f"❌ {t('settings_save_error', lang)}: {e}")

# Informações na sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown(f"### 📊 {t('system_status', lang)}")
    
    st.success(f"""
    **✅ {t('system_operational', lang)}**
    - {"Modelos" if lang == 'pt' else "Models"}: {len(modelos)} {t('models_configured', lang)}
    - {"Parâmetros" if lang == 'pt' else "Parameters"}: {t('parameters_loaded', lang)}
    - {"Idioma" if lang == 'pt' else "Language"}: {language}
    """)
    
    st.markdown(f"### 🎯 {t('features', lang)}")
    st.info(f"""
    **📈 {t('monthly_profit', lang).replace('📈 ', '')}:**
    {"Simula receitas e custos mensais" if lang == 'pt' else "Simulates monthly revenues and costs"}
    
    **⚖️ {t('cost_comparison', lang).replace('⚖️ ', '')}:**
    {"Compara gestão própria vs. Amaro" if lang == 'pt' else "Compares own management vs. Amaro"}
    
    **⚙️ {t('settings', lang).replace('⚙️ ', '')}:**
    {"Ajusta parâmetros e visualiza fórmulas" if lang == 'pt' else "Adjusts parameters and shows formulas"}
    """)
    
    st.markdown(f"### 💡 {t('usage_tips', lang)}")
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
    st.markdown(f"### 🔄 {t('quick_actions', lang)}")
    
    if st.button(f"🔄 {t('reload_data', lang)}", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    if st.button(f"📱 {t('presentation_mode', lang)}", use_container_width=True):
        if lang == 'pt':
            st.info("💡 Use F11 para tela cheia durante apresentações")
        else:
            st.info("💡 Use F11 for fullscreen during presentations")
    
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #6c757d; font-size: 0.8rem;">
        <p><strong>Amaro Aviation Calculator</strong></p>
        <p>{t('version', lang)} - {t('refactored_system', lang)}</p>
        <p>{t('developed_with_love', lang)}</p>
    </div>
    """, unsafe_allow_html=True)