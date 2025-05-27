"""
Página 2: Breakdown Comparativo de Custos
Comparação item a item: gestão própria vs Amaro Aviation
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from config.theme import load_theme
from config.idiomas import get_text, detect_language_from_selection
from components.header import render_page_header
from components.sidebar import render_sidebar
from components.metrics import render_comparison_metrics, render_highlight_metric
from components.status import render_system_status
from utils.params import load_params, format_currency
from utils.calculations import calcular_comparativo_gestao
from utils.export_manager import botao_download_inteligente, criar_relatorio_dados

lang = render_sidebar(current_lang="pt")

# Configuração da página
st.set_page_config(
    page_title="Breakdown de Custos | Amaro Aviation",
    page_icon="📊",
    layout="wide"
)

from config.theme import load_theme
load_theme()


# Sidebar e idioma
lang = render_sidebar()

# Header da página
render_page_header(
    'page_breakdown',
    'Comparação detalhada: gestão própria vs gestão Amaro Aviation' if lang == 'pt' 
    else 'Detailed comparison: own management vs Amaro Aviation management',
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
st.markdown(f"### ⚖️ {get_text('page_breakdown', lang)}")

# Formulário de entrada
col1, col2, col3 = st.columns(3)

with col1:
    modelo_comp = st.selectbox(
        get_text('aircraft_model', lang),
        modelos,
        key="modelo_breakdown"
    )

with col2:
    horas_anuais = st.number_input(
        get_text('annual_hours', lang),
        min_value=50,
        max_value=800,
        value=300,
        step=25,
        help=get_text('annual_hours', lang) if lang == 'pt'
             else "Total hours flown per year"
    )

with col3:
    incluir_charter = st.checkbox(
        get_text('include_charter', lang),
        value=True,
        help=get_text('include_charter', lang) if lang == 'pt'
             else "Consider charter revenue as cost reduction"
    )

# Custos fixos anuais
st.markdown(f"#### 💼 {get_text('fixed_costs', lang)}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    custo_hangar = st.number_input(
        get_text('hangar_cost', lang),
        value=120000,
        step=10000,
        help=get_text('hangar_cost', lang) if lang == 'pt'
             else "Annual hangar cost"
    )

with col2:
    custo_seguro = st.number_input(
        get_text('insurance_cost', lang),
        value=250000,
        step=10000,
        help=get_text('insurance_cost', lang) if lang == 'pt'
             else "Annual aeronautical insurance cost"
    )

with col3:
    custo_tripulacao = st.number_input(
        get_text('crew_cost', lang),
        value=300000,
        step=10000,
        help=get_text('crew_cost', lang) if lang == 'pt'
             else "Dedicated crew salaries and charges"
    )

with col4:
    custo_admin = st.number_input(
        get_text('admin_cost', lang),
        value=50000,
        step=5000,
        help=get_text('admin_cost', lang) if lang == 'pt'
             else "Administrative and planning costs"
    )

# Botão de comparação
if st.button(f"📊 {get_text('calculate', lang)}", type="primary", use_container_width=True):
    
    try:
        # Preparar custos fixos
        custos_fixos_externos = {
            'hangar': custo_hangar,
            'seguro': custo_seguro,
            'tripulacao': custo_tripulacao,
            'administracao': custo_admin
        }
        
        # Realizar comparação
        resultado = calcular_comparativo_gestao(
            modelo=modelo_comp,
            horas_anuais=horas_anuais,
            params=params,
            custos_fixos_externos=custos_fixos_externos
        )
        
        # Calcular receita de charter se incluída
        receita_charter = 0
        if incluir_charter:
            horas_charter_ano = horas_anuais * 0.3  # 30% das horas para charter
            preco_hora = params['preco_mercado_hora'][modelo_comp]
            receita_charter = horas_charter_ano * preco_hora * 0.75  # 75% ocupação
        
        # Ajustar totais com receita
        total_proprio_liquido = resultado['gestao_propria']['total'] - receita_charter
        total_amaro_liquido = resultado['gestao_amaro']['total'] - (receita_charter * 0.9)
        
        economia_final = total_proprio_liquido - total_amaro_liquido
        economia_percentual = (economia_final / total_proprio_liquido * 100) if total_proprio_liquido > 0 else 0
        
        # Exibir resultados
        st.markdown("---")
        st.markdown(f"### 📊 {get_text('detailed_breakdown', lang)}")
        
        # Comparação de totais
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="
                background: white;
                border: 2px solid #EF4444;
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
            ">
                <div style="color: #6B7280; font-size: 0.875rem; text-transform: uppercase;">
                    {get_text('own_management', lang)}
                </div>
                <div style="color: #EF4444; font-size: 1.8rem; font-weight: 700; margin: 0.5rem 0;">
                    {format_currency(total_proprio_liquido, lang)}
                </div>
                <div style="color: #6B7280; font-size: 0.75rem;">
                    {'Incluindo todos os custos fixos' if lang == 'pt' else 'Including all fixed costs'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="
                background: white;
                border: 2px solid #10B981;
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
            ">
                <div style="color: #6B7280; font-size: 0.875rem; text-transform: uppercase;">
                    {get_text('amaro_management', lang)}
                </div>
                <div style="color: #10B981; font-size: 1.8rem; font-weight: 700; margin: 0.5rem 0;">
                    {format_currency(total_amaro_liquido, lang)}
                </div>
                <div style="color: #6B7280; font-size: 0.75rem;">
                    {'Apenas custos operacionais' if lang == 'pt' else 'Only operational costs'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            render_highlight_metric(
                get_text('annual_savings', lang),
                economia_final,
                f"{economia_percentual:.1f}% {get_text('cost_reduction', lang)}",
                "#10B981",
                "currency",
                lang
            )
        
        # Tabela comparativa detalhada
        st.markdown(f"#### 📋 {get_text('detailed_breakdown', lang)}")
        
        # Criar dados da tabela
        items_custos = [
            get_text('hangar', lang),
            get_text('insurance', lang),
            get_text('crew', lang),
            get_text('administration', lang),
            get_text('fuel', lang),
            get_text('maintenance', lang),
            get_text('depreciation', lang),
            get_text('other_costs', lang)
        ]
        
        custos_proprio = [
            custo_hangar,
            custo_seguro,
            custo_tripulacao,
            custo_admin,
            resultado['gestao_propria']['breakdown_variaveis']['combustivel'],
            resultado['gestao_propria']['breakdown_variaveis']['manutencao'],
            resultado['gestao_propria']['breakdown_variaveis']['depreciacao'],
            resultado['gestao_propria']['breakdown_variaveis']['tripulacao_variavel']
        ]
        
        custos_amaro = [
            0, 0, 0, 0,  # Custos fixos zerados para Amaro
            resultado['gestao_amaro']['breakdown_variaveis']['combustivel'],
            resultado['gestao_amaro']['breakdown_variaveis']['manutencao'],
            resultado['gestao_amaro']['breakdown_variaveis']['depreciacao'],
            resultado['gestao_amaro']['breakdown_variaveis']['tripulacao_variavel']
        ]
        
        # Criar DataFrame
        df_comparativo = pd.DataFrame({
            'Item': items_custos,
            get_text('own_management', lang): [format_currency(v, lang) for v in custos_proprio],
            get_text('amaro_management', lang): [format_currency(v, lang) for v in custos_amaro],
            get_text('savings', lang): [format_currency(p - a, lang) for p, a in zip(custos_proprio, custos_amaro)],
            f"{get_text('savings', lang)} %": [f"{((p - a) / p * 100):.1f}%" if p > 0 else "0%" for p, a in zip(custos_proprio, custos_amaro)]
        })
        
        # Adicionar linha de receita charter se incluída
        if incluir_charter:
            receita_row = pd.DataFrame({
                'Item': [get_text('charter_revenue', lang)],
                get_text('own_management', lang): [format_currency(-receita_charter, lang)],
                get_text('amaro_management', lang): [format_currency(-receita_charter * 0.9, lang)],
                get_text('savings', lang): [''],
                f"{get_text('savings', lang)} %": ['']
            })
            df_comparativo = pd.concat([df_comparativo, receita_row], ignore_index=True)
        
        # Adicionar linha de total
        total_row = pd.DataFrame({
            'Item': [get_text('net_total', lang)],
            get_text('own_management', lang): [format_currency(total_proprio_liquido, lang)],
            get_text('amaro_management', lang): [format_currency(total_amaro_liquido, lang)],
            get_text('savings', lang): [format_currency(economia_final, lang)],
            f"{get_text('savings', lang)} %": [f"{economia_percentual:.1f}%"]
        })
        df_comparativo = pd.concat([df_comparativo, total_row], ignore_index=True)
        
        # Exibir tabela
        st.dataframe(
            df_comparativo,
            use_container_width=True,
            hide_index=True
        )
        
        # Gráficos de análise
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### 📊 {get_text('cost_distribution', lang)}")
            
            fig_proprio = go.Figure(data=[go.Pie(
                labels=[get_text('fixed_costs_label', lang), get_text('variable_costs_label', lang)],
                values=[resultado['gestao_propria']['custos_fixos'], resultado['gestao_propria']['custos_variaveis']],
                hole=0.5,
                marker=dict(colors=['#EF4444', '#F59E0B']),
                textinfo='label+percent'
            )])
            
            fig_proprio.update_layout(
                height=300,
                showlegend=True,
                margin=dict(l=0, r=0, t=20, b=0)
            )
            
            st.plotly_chart(fig_proprio, use_container_width=True)
        
        with col2:
            st.markdown(f"#### 📊 {get_text('accumulated_savings', lang)}")
            
            anos = list(range(1, 6))
            economia_acumulada = [economia_final * ano for ano in anos]
            
            fig_economia = go.Figure()
            fig_economia.add_trace(go.Bar(
                x=anos,
                y=economia_acumulada,
                text=[format_currency(v, lang) for v in economia_acumulada],
                textposition='outside',
                marker_color='#10B981'
            ))
            
            fig_economia.update_layout(
                height=300,
                xaxis_title='Anos' if lang == 'pt' else 'Years',
                yaxis_title=f"{get_text('accumulated_savings', lang)} ({format_currency(0, lang).split(' ')[0]})",
                showlegend=False,
                margin=dict(l=0, r=0, t=20, b=0)
            )
            
            st.plotly_chart(fig_economia, use_container_width=True)
        
        # Preparar dados para exportação
        dados_entrada = {
            'modelo': modelo_comp,
            'horas_anuais': horas_anuais,
            'incluir_charter': incluir_charter,
            'custo_hangar': custo_hangar,
            'custo_seguro': custo_seguro,
            'custo_tripulacao': custo_tripulacao,
            'custo_admin': custo_admin
        }
        
        resultados_export = {
            'total_gestao_propria': total_proprio_liquido,
            'total_gestao_amaro': total_amaro_liquido,
            'economia_anual': economia_final,
            'economia_percentual': economia_percentual,
            'economia_5_anos': economia_final * 5
        }
        
        relatorio_dados = criar_relatorio_dados(
            "Breakdown Comparativo de Custos",
            dados_entrada,
            resultados_export,
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
                'breakdown_custos'
            )
        
    except Exception as e:
        st.error(f"❌ Erro no cálculo: {e}")

# Informações adicionais
with st.expander("💡 Interpretação dos Resultados" if lang == 'pt' else "💡 Results Interpretation"):
    if lang == 'pt':
        st.markdown("""
        **Gestão Própria vs. Gestão Amaro:**
        
        - **Custos Fixos**: Hangar, seguro, tripulação dedicada e administração são absorvidos pela Amaro
        - **Custos Variáveis**: Combustível, manutenção e depreciação são mantidos em ambos os modelos
        - **Receita Charter**: Se incluída, considera 30% das horas para charter com 75% de ocupação
        - **Taxa Amaro**: 10% da receita de charter é retida pela Amaro como taxa de gestão
        
        **Benefícios da Gestão Amaro:**
        
        - Eliminação de custos fixos elevados
        - Flexibilidade operacional
        - Gestão profissional especializada
        - Redução de riscos administrativos
        """)
    else:
        st.markdown("""
        **Own Management vs. Amaro Management:**
        
        - **Fixed Costs**: Hangar, insurance, dedicated crew and administration are absorbed by Amaro
        - **Variable Costs**: Fuel, maintenance and depreciation are maintained in both models
        - **Charter Revenue**: If included, considers 30% of hours for charter with 75% occupancy
        - **Amaro Fee**: 10% of charter revenue is retained by Amaro as management fee
        
        **Amaro Management Benefits:**
        
        - Elimination of high fixed costs
        - Operational flexibility
        - Specialized professional management
        - Reduction of administrative risks
        """)

# Footer da página
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6B7280; padding: 1rem;">
    <p>📊 <strong>{get_text('page_breakdown', lang)}</strong> - Comparação detalhada de modelos de gestão</p>
</div>
""", unsafe_allow_html=True)