"""
Página 1: Estimativa de Lucro Mensal
Análise de rentabilidade com operação charter
"""

import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from config.theme import load_theme
from config.idiomas import get_text, detect_language_from_selection
from components.header import render_page_header
from components.sidebar import render_sidebar
from components.metrics import render_metric_card, render_kpi_grid
from components.status import render_calculation_status, render_system_status
from utils.params import load_params, format_currency, format_percentage
from utils.calculations import calcular_lucro_mensal_charter
from utils.export_manager import botao_download_inteligente, criar_relatorio_dados

lang = render_sidebar(current_lang="pt")
# Configuração da página
st.set_page_config(
    page_title="Estimativa de Lucro | Amaro Aviation",
    page_icon="📈",
    layout="wide"
)

from config.theme import load_theme
load_theme()

# Sidebar e idioma
lang = render_sidebar()

# Header da página
render_page_header(
    'page_profit',
    'Análise de rentabilidade mensal com operação charter' if lang == 'pt' 
    else 'Monthly profitability analysis with charter operation',
    lang
)

# Carregar parâmetros
try:
    params = load_params()
    if not render_system_status(params, lang):
        st.stop()
    
    modelos = params.get('modelos_disponiveis', [])
    
except Exception as e:
    st.error(f"❌ {get_text('system_load_error', lang)}: {e}")
    st.stop()

# Interface principal
st.markdown(f"### 💰 {get_text('page_profit', lang)}")

# Formulário de entrada
col1, col2, col3, col4 = st.columns(4)

with col1:
    modelo_selecionado = st.selectbox(
        get_text('aircraft_model', lang),
        modelos,
        key="modelo_lucro"
    )

with col2:
    horas_charter = st.number_input(
        get_text('monthly_hours', lang),
        min_value=10,
        max_value=200,
        value=80,
        step=10,
        help=get_text('monthly_hours', lang) if lang == 'pt' 
             else "Monthly hours available for charter"
    )

with col3:
    taxa_ocupacao = st.slider(
        get_text('occupancy_rate', lang),
        min_value=50,
        max_value=95,
        value=75,
        help=get_text('occupancy_rate', lang) if lang == 'pt'
             else "Percentage of occupied available hours"
    )

with col4:
    preco_hora_charter = st.number_input(
        get_text('charter_price', lang),
        value=float(params['preco_mercado_hora'].get(modelo_selecionado, 8000)),
        step=500.0,
        help=get_text('charter_price', lang) if lang == 'pt'
             else "Price charged per charter hour"
    )

# Botão de cálculo
if st.button(f"🚀 {get_text('calculate', lang)}", type="primary", use_container_width=True):
    
    # Realizar cálculos
    try:
        resultado = calcular_lucro_mensal_charter(
            modelo=modelo_selecionado,
            horas_charter=horas_charter,
            taxa_ocupacao=taxa_ocupacao,
            preco_hora=preco_hora_charter,
            params=params
        )
        
        # Exibir resultados
        st.markdown("---")
        st.markdown(f"### 📊 {get_text('projection_analysis', lang)}")
        
        # KPIs principais
        kpis = [
            {
                'label': get_text('gross_revenue', lang),
                'value': resultado['receita_bruta'],
                'format_type': 'currency'
            },
            {
                'label': get_text('owner_revenue', lang),
                'value': resultado['receita_proprietario'],
                'format_type': 'currency'
            },
            {
                'label': get_text('net_profit', lang),
                'value': resultado['lucro_liquido'],
                'format_type': 'currency',
                'delta': resultado['roi_mensal'] if resultado['lucro_liquido'] > 0 else None
            },
            {
                'label': get_text('monthly_roi', lang),
                'value': resultado['roi_mensal'],
                'format_type': 'percentage'
            }
        ]
        
        render_kpi_grid(kpis, columns=4, lang=lang)
        
        # Gráficos de análise
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### 📊 {get_text('revenue_composition', lang)}")
            
            fig_receita = go.Figure(data=[go.Pie(
                labels=[
                    get_text('owner_revenue', lang).replace(' (90%)', ''),
                    'Taxa Amaro (10%)' if lang == 'pt' else 'Amaro Fee (10%)'
                ],
                values=[resultado['receita_proprietario'], resultado['taxa_amaro']],
                hole=0.5,
                marker=dict(colors=['#10B981', '#8C1D40']),
                textinfo='label+value',
                texttemplate='<b>%{label}</b><br>' + format_currency(0, lang).replace('0,00', '%{value:,.0f}')
            )])
            
            fig_receita.update_layout(
                height=300,
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig_receita, use_container_width=True)
        
        with col2:
            st.markdown(f"#### 💸 {get_text('cost_breakdown', lang)}")
            
            custos_labels = [
                get_text('fuel', lang),
                get_text('crew', lang),
                get_text('maintenance', lang),
                get_text('depreciation', lang)
            ]
            
            custos_values = [
                resultado['breakdown_custos']['combustivel'],
                resultado['breakdown_custos']['tripulacao'],
                resultado['breakdown_custos']['manutencao'],
                resultado['breakdown_custos']['depreciacao']
            ]
            
            fig_custos = go.Figure(data=[go.Bar(
                y=custos_labels,
                x=custos_values,
                orientation='h',
                text=[format_currency(v, lang) for v in custos_values],
                textposition='inside',
                marker_color=['#EF4444', '#F59E0B', '#3B82F6', '#10B981']
            )])
            
            fig_custos.update_layout(
                height=300,
                xaxis_title=get_text('value_currency', lang),
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig_custos, use_container_width=True)
        
        # Status da operação
        render_calculation_status(
            is_profitable=resultado['lucrativo'],
            profit_value=resultado['lucro_liquido'],
            message="O proprietário terá um lucro líquido de" if lang == 'pt' and resultado['lucrativo']
                    else "The owner will have a net profit of" if resultado['lucrativo']
                    else "A operação apresenta déficit de" if lang == 'pt'
                    else "The operation shows a deficit of",
            lang=lang
        )
        
        # Preparar dados para exportação
        dados_entrada = {
            'modelo': modelo_selecionado,
            'horas_charter_mes': horas_charter,
            'taxa_ocupacao': taxa_ocupacao,
            'preco_hora_charter': preco_hora_charter
        }
        
        relatorio_dados = criar_relatorio_dados(
            "Estimativa de Lucro Mensal",
            dados_entrada,
            resultado,
            lang
        )
        
        # Botão de exportação
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        
        with col2:
            botao_download_inteligente(
                relatorio_dados,
                f"📊 {get_text('export', lang)}",
                'excel',
                'estimativa_lucro_mensal'
            )
        
    except Exception as e:
        st.error(f"❌ Erro no cálculo: {e}")

# Informações adicionais
with st.expander("💡 Dicas e Informações" if lang == 'pt' else "💡 Tips and Information"):
    if lang == 'pt':
        st.markdown("""
        **Como interpretar os resultados:**
        
        - **Receita Bruta**: Total faturado com as horas de charter
        - **Receita do Proprietário**: 90% da receita bruta (padrão Amaro)
        - **Taxa Amaro**: 10% da receita bruta para gestão
        - **ROI Mensal**: Retorno sobre o investimento operacional
        
        **Dicas para otimização:**
        
        - Mantenha taxa de ocupação acima de 70%
        - Ajuste preços conforme demanda sazonal
        - Monitore custos de combustível regularmente
        - Considere rotas mais eficientes
        """)
    else:
        st.markdown("""
        **How to interpret results:**
        
        - **Gross Revenue**: Total billed charter hours
        - **Owner Revenue**: 90% of gross revenue (Amaro standard)
        - **Amaro Fee**: 10% of gross revenue for management
        - **Monthly ROI**: Return on operational investment
        
        **Optimization tips:**
        
        - Keep occupancy rate above 70%
        - Adjust prices according to seasonal demand
        - Monitor fuel costs regularly
        - Consider more efficient routes
        """)

# Footer da página
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6B7280; padding: 1rem;">
    <p>📈 <strong>{get_text('page_profit', lang)}</strong> - Análise detalhada de rentabilidade</p>
</div>
""", unsafe_allow_html=True)