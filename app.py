import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
from io import BytesIO

# Imports locais
from utils.params import load_params, save_params
from utils.calculations import calcula_custo_trecho
from utils.exportador_excel import criar_relatorio_dados, gerar_excel_simples
from utils.exportador_pdf import gerar_pdf

# ========================================================================
# CONFIGURAÇÃO DA PÁGINA
# ========================================================================
st.set_page_config(
    page_title="Amaro Aviation - Calculadora Corporativa",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================================================
# SISTEMA DE TRADUÇÃO CORPORATIVO
# ========================================================================
@st.cache_data
def get_translations():
    return {
        'pt': {
            'app_title': 'AMARO AVIATION',
            'app_subtitle': 'CALCULADORA DE CUSTOS OPERACIONAIS',
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
            'operational_costs': 'Custos Operacionais',
            'net_profit': 'Lucro Líquido',
            'own_management': 'Gestão Própria',
            'amaro_management': 'Gestão Amaro Aviation',
            'annual_savings': 'Economia Anual',
            'fuel_price': 'Preço do Combustível (R$/L)',
            'pilot_cost': 'Custo Piloto (R$/h)',
            'depreciation': 'Depreciação Anual (%)',
            'maintenance_turboprop': 'Manutenção Turboprop (R$/h)',
            'maintenance_jet': 'Manutenção Jato (R$/h)',
            'market_price_turboprop': 'Preço Mercado Turboprop (R$/h)',
            'market_price_jet': 'Preço Mercado Jato (R$/h)',
            'save_settings': 'SALVAR CONFIGURAÇÕES',
            'profitable_operation': 'OPERAÇÃO RENTÁVEL',
            'operation_at_loss': 'OPERAÇÃO COM PREJUÍZO',
            'settings_saved': 'Configurações salvas com sucesso',
            'export_excel': 'EXPORTAR EXCEL',
            'export_pdf': 'EXPORTAR PDF'
        },
        'en': {
            'app_title': 'AMARO AVIATION',
            'app_subtitle': 'OPERATING COST CALCULATOR',
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
            'operational_costs': 'Operational Costs',
            'net_profit': 'Net Profit',
            'own_management': 'Own Management',
            'amaro_management': 'Amaro Aviation Management',
            'annual_savings': 'Annual Savings',
            'fuel_price': 'Fuel Price (R$/L)',
            'pilot_cost': 'Pilot Cost (R$/h)',
            'depreciation': 'Annual Depreciation (%)',
            'maintenance_turboprop': 'Turboprop Maintenance (R$/h)',
            'maintenance_jet': 'Jet Maintenance (R$/h)',
            'market_price_turboprop': 'Turboprop Market Price (R$/h)',
            'market_price_jet': 'Jet Market Price (R$/h)',
            'save_settings': 'SAVE SETTINGS',
            'profitable_operation': 'PROFITABLE OPERATION',
            'operation_at_loss': 'OPERATION AT LOSS',
            'settings_saved': 'Settings saved successfully',
            'export_excel': 'EXPORT EXCEL',
            'export_pdf': 'EXPORT PDF'
        }
    }

def t(key, lang='pt'):
    translations = get_translations()
    return translations.get(lang, translations['pt']).get(key, key)

def format_currency(value, lang='pt'):
    try:
        if lang == 'pt':
            return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            return f"R$ {value:,.2f}"
    except:
        return str(value)

def format_percentage(value, lang='pt'):
    try:
        if lang == 'pt':
            return f"{value:.1f}%".replace(".", ",")
        else:
            return f"{value:.1f}%"
    except:
        return str(value)

# ========================================================================
# CSS CORPORATIVO
# ========================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.stApp {
    font-family: 'Inter', 'Helvetica Neue', sans-serif;
    background-color: #FFFFFF;
    color: #333333;
}

.corporate-header {
    background-color: #8C1D40;
    color: white;
    padding: 3rem;
    text-align: center;
    margin-bottom: 2rem;
}

.corporate-header h1 {
    font-size: 3rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.corporate-header p {
    font-size: 1.2rem;
    font-weight: 500;
    margin: 1rem 0 0 0;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.corporate-card {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.corporate-card h3 {
    color: #8C1D40;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 0 1rem 0;
    text-transform: uppercase;
    letter-spacing: 2px;
    border-bottom: 2px solid #8C1D40;
    padding-bottom: 0.5rem;
}

.metric-card {
    background-color: #FFFFFF;
    border: 2px solid #E0E0E0;
    border-left: 6px solid #8C1D40;
    padding: 2rem;
    margin: 1rem 0;
    text-align: center;
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: #8C1D40;
    margin: 1rem 0;
}

.metric-label {
    font-size: 0.9rem;
    color: #333333;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}

.stButton > button {
    background-color: #8C1D40;
    color: white;
    border: none;
    padding: 1rem 3rem;
    font-weight: 700;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    width: 100%;
}

.stButton > button:hover {
    background-color: #6D1530;
}

.stTabs [data-baseweb="tab-list"] {
    background-color: #F8F9FA;
    border-bottom: 2px solid #E0E0E0;
}

.stTabs [data-baseweb="tab"] {
    color: #333333;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 1.5rem 2rem;
}

.stTabs [aria-selected="true"] {
    background-color: #FFFFFF;
    color: #8C1D40;
    border-bottom: 4px solid #8C1D40;
    font-weight: 700;
}

.sidebar-header {
    background-color: #8C1D40;
    color: white;
    padding: 2rem;
    margin: -1rem -1rem 2rem -1rem;
    text-align: center;
}

.sidebar-header h2 {
    font-size: 1.3rem;
    font-weight: 700;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.stSelectbox > label,
.stNumberInput > label,
.stSlider > label,
.stCheckbox > label {
    font-weight: 600;
    color: #333333;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.success-highlight {
    background-color: #E8F5E8;
    border: 2px solid #4CAF50;
    border-left: 6px solid #4CAF50;
    padding: 2rem;
    margin: 2rem 0;
}

.warning-highlight {
    background-color: #FFF3E0;
    border: 2px solid #FF9800;
    border-left: 6px solid #FF9800;
    padding: 2rem;
    margin: 2rem 0;
}

.success-highlight h4,
.warning-highlight h4 {
    margin: 0 0 1rem 0;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
}
</style>
""", unsafe_allow_html=True)

# ========================================================================
# SIDEBAR
# ========================================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2>AMARO AVIATION</h2>
    </div>
    """, unsafe_allow_html=True)
    
    language_option = st.selectbox(
        "IDIOMA / LANGUAGE",
        ["Português", "English"]
    )
    
    lang = 'pt' if language_option == 'Português' else 'en'

# ========================================================================
# HEADER
# ========================================================================
st.markdown(f"""
<div class="corporate-header">
    <h1>{t('app_title', lang)}</h1>
    <p>{t('app_subtitle', lang)}</p>
</div>
""", unsafe_allow_html=True)

# ========================================================================
# CARREGAMENTO DE DADOS
# ========================================================================
try:
    params = load_params()
    modelos = params.get('modelos_disponiveis', [])
    
    if not modelos:
        st.error("ERRO: Nenhum modelo configurado")
        st.stop()
        
except Exception as e:
    st.error(f"ERRO ao carregar parâmetros: {e}")
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
            modelos
        )
    
    with col2:
        horas_mes = st.number_input(
            t('monthly_hours', lang),
            min_value=10,
            max_value=200,
            value=80,
            step=10
        )
    
    with col3:
        ocupacao = st.slider(
            t('occupancy_rate', lang),
            min_value=50,
            max_value=95,
            value=75
        )
    
    if st.button(t('calculate', lang), type="primary"):
        try:
            resultado_hora = calcula_custo_trecho(modelo_lucro, 1.0, params)
            horas_efetivas = horas_mes * (ocupacao / 100)
            
            preco_hora_mercado = params['preco_mercado_hora'][modelo_lucro]
            receita_bruta = preco_hora_mercado * horas_efetivas
            custo_operacional = resultado_hora['total'] * horas_efetivas
            
            receita_proprietario = receita_bruta * 0.9
            lucro_liquido = receita_proprietario - custo_operacional
            
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
            
            # Gráfico
            fig = go.Figure(data=[go.Pie(
                labels=['Lucro Proprietário', 'Taxa Amaro', 'Custos Operacionais'],
                values=[receita_proprietario - custo_operacional, receita_bruta * 0.1, custo_operacional],
                hole=0.4,
                marker_colors=['#4CAF50', '#8C1D40', '#F44336']
            )])
            
            fig.update_layout(
                title='BREAKDOWN FINANCEIRO MENSAL',
                height=500,
                font=dict(family='Inter', size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Status
            if lucro_liquido > 0:
                st.markdown(f"""
                <div class="success-highlight">
                    <h4>{t('profitable_operation', lang)}</h4>
                    <p><strong>{t('net_profit', lang)}:</strong> {format_currency(lucro_liquido, lang)}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="warning-highlight">
                    <h4>{t('operation_at_loss', lang)}</h4>
                    <p><strong>Prejuízo:</strong> {format_currency(abs(lucro_liquido), lang)}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Exportação
            st.markdown("### EXPORTAR RELATÓRIO")
            col1, col2 = st.columns(2)
            
            dados = {
                "Modelo": modelo_lucro,
                "Horas Mensais": horas_mes,
                "Taxa Ocupação": f"{ocupacao}%",
                "Receita Bruta": receita_bruta,
                "Lucro Líquido": lucro_liquido
            }
            
            relatorio = criar_relatorio_dados("Lucro Mensal", dados, dados)
            
            with col1:
                try:
                    excel_buffer = gerar_excel_simples(relatorio)
                    if excel_buffer:
                        st.download_button(
                            t('export_excel', lang),
                            data=excel_buffer.getvalue(),
                            file_name=f"amaro_lucro_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                except:
                    pass
            
            with col2:
                try:
                    pdf_buffer = BytesIO()
                    if gerar_pdf(pdf_buffer, dados):
                        st.download_button(
                            t('export_pdf', lang),
                            data=pdf_buffer.getvalue(),
                            file_name=f"amaro_lucro_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                except:
                    pass
                    
        except Exception as e:
            st.error(f"Erro no cálculo: {e}")

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
            key="comp_modelo"
        )
        
        horas_anuais = st.number_input(
            t('annual_hours', lang),
            min_value=50,
            max_value=800,
            value=300,
            step=25
        )
    
    with col2:
        custos_fixos = st.number_input(
            t('fixed_costs', lang),
            min_value=50000,
            max_value=2000000,
            value=500000,
            step=25000
        )
        
        include_charter = st.checkbox(
            t('include_charter', lang),
            value=True
        )
    
    if st.button(t('calculate', lang), key="calc_comp", type="primary"):
        try:
            resultado_ano = calcula_custo_trecho(modelo_comp, horas_anuais, params)
            custo_operacional = resultado_ano['total']
            custo_proprio = custo_operacional + custos_fixos
            custo_amaro = custo_operacional
            
            receita_charter = 0
            if include_charter:
                preco_hora = params['preco_mercado_hora'][modelo_comp]
                receita_charter = preco_hora * horas_anuais * 0.6
            
            custo_liquido_proprio = custo_proprio - receita_charter
            custo_liquido_amaro = custo_amaro - receita_charter
            economia = custo_liquido_proprio - custo_liquido_amaro
            
            st.markdown("### COMPARATIVO ANUAL")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="corporate-card" style="background: #FFF8E1; border-left: 6px solid #FF9800;">
                    <h4 style="color: #E65100;">{t('own_management', lang)}</h4>
                    <div class="metric-value" style="color: #E65100;">{format_currency(custo_liquido_proprio, lang)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="corporate-card" style="background: #E8F5E8; border-left: 6px solid #4CAF50;">
                    <h4 style="color: #2E7D32;">{t('amaro_management', lang)}</h4>
                    <div class="metric-value" style="color: #2E7D32;">{format_currency(custo_liquido_amaro, lang)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                cor = '#4CAF50' if economia > 0 else '#F44336'
                st.markdown(f"""
                <div class="corporate-card" style="background: {'#E8F5E8' if economia > 0 else '#FFEBEE'}; border-left: 6px solid {cor};">
                    <h4 style="color: {cor};">{t('annual_savings', lang)}</h4>
                    <div class="metric-value" style="color: {cor};">{format_currency(abs(economia), lang)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Gráfico comparativo
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[t('own_management', lang), t('amaro_management', lang)],
                y=[custo_liquido_proprio, custo_liquido_amaro],
                marker_color=['#FF9800', '#8C1D40']
            ))
            
            fig.update_layout(
                title='COMPARATIVO ANUAL DE CUSTOS',
                yaxis_title='Custo Anual (R$)',
                height=500,
                font=dict(family='Inter', size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro no cálculo: {e}")

# ========================================================================
# TAB 3: CONFIGURAÇÕES
# ========================================================================
with tab3:
    st.markdown(f"""
    <div class="corporate-card">
        <h3>{t('tab_settings', lang)}</h3>
        <p>Ajuste os parâmetros de cálculo</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### PARÂMETROS OPERACIONAIS")
    
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
    
    st.markdown("---")
    if st.button(t('save_settings', lang), type="primary", use_container_width=True):
        try:
            novos_params = {
                'preco_combustivel': float(preco_combustivel),
                'custo_piloto_hora': float(custo_piloto),
                'depreciacao_anual_pct': float(depreciacao),
                'custo_manutencao_hora': {
                    'turboprop': float(manut_turboprop),
                    'jato': float(manut_jato)
                },
                'percentual_proprietario': 0.9,
                'preco_mercado': {
                    'turboprop': float(mercado_turboprop),
                    'jato': float(mercado_jato)
                }
            }
            
            if save_params(novos_params):
                st.success(t('settings_saved', lang))
                st.rerun()
            else:
                st.error("Erro ao salvar")
                
        except Exception as e:
            st.error(f"Erro: {e}")

# ========================================================================
# SIDEBAR INFO
# ========================================================================
with st.sidebar:
    st.markdown("---")
    st.markdown("### STATUS DO SISTEMA")
    st.success(f"""
    **Sistema Operacional**
    - Modelos: {len(modelos)} configurados
    - Idioma: {language_option}
    """)
    
    st.markdown("### FUNCIONALIDADES")
    st.info("""
    **ESTIMATIVA DE LUCRO:**
    Simula receitas e custos mensais
    
    **COMPARATIVO:**
    Gestão própria vs. Amaro
    
    **CONFIGURAÇÕES:**
    Ajusta parâmetros
    """)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #333333; font-size: 0.8rem;">
        <p><strong>AMARO AVIATION CALCULATOR</strong></p>
        <p>VERSÃO 3.0 CORPORATIVA</p>
        <p>Desenvolvido pela Amaro Aviation</p>
    </div>
    """, unsafe_allow_html=True)