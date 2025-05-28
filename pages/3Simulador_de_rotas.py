"""
Página 3: Simulador de Trechos Origem-Destino - VERSÃO CORRIGIDA
Análise de custo ponto-a-ponto por rota específica
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
from components.metrics import render_metric_card, render_kpi_grid
from components.status import render_system_status, render_status_box
from utils.params import load_params, format_currency
from utils.calculations import calcular_custo_rota
from utils.export_manager import botao_download_inteligente, criar_relatorio_dados

# Configuração da página
st.set_page_config(
    page_title="Simulador de Rotas | Amaro Aviation",
    page_icon="✈️",
    layout="wide"
)

# Carregamento de tema
load_theme()

# Sidebar e idioma
lang = render_sidebar()

# Header da página
render_page_header(
    'page_simulator',
    'Simulação de custos por rota específica origem-destino' if lang == 'pt' 
    else 'Cost simulation per specific origin-destination route',
    lang
)

# Carregar parâmetros - SEM exibir o quadro verde irritante
try:
    params = load_params()
    system_ok = render_system_status(params, lang)  # Agora não exibe nada
    
    if not system_ok:
        st.error("❌ Sistema não configurado adequadamente")
        st.stop()
    
    modelos = params.get('modelos_disponiveis', [])
    
    if not modelos:
        st.error("❌ Nenhum modelo de aeronave configurado")
        st.stop()
    
except Exception as e:
    st.error(f"❌ {get_text('system_load_error', lang)}: {e}")
    st.stop()

# Carregar rotas disponíveis
try:
    df_rotas = pd.read_csv('data/rotas.csv')
    rotas_disponiveis = df_rotas.to_dict('records')
    
    if not rotas_disponiveis:
        st.warning("⚠️ Nenhuma rota encontrada no arquivo")
        rotas_disponiveis = []
        
except Exception as e:
    st.warning(f"⚠️ {get_text('routes_not_found', lang)}: {e}")
    rotas_disponiveis = [
        {"origem": "GRU", "destino": "SDU", "duracao_h": 1.0},
        {"origem": "CGH", "destino": "BSB", "duracao_h": 1.4},
        {"origem": "BSB", "destino": "SDU", "duracao_h": 1.7},
        {"origem": "GRU", "destino": "CNF", "duracao_h": 1.0}
    ]

# Interface principal
st.markdown(f"### ✈️ {get_text('page_simulator', lang)}")

# Verificar se há rotas disponíveis
if not rotas_disponiveis:
    st.error("❌ Nenhuma rota disponível para simulação")
    st.info("💡 Configure rotas na página de Configurações")
    st.stop()

# Formulário de seleção de rota
col1, col2, col3 = st.columns(3)

with col1:
    # Buscar origens únicas
    try:
        origens_disponiveis = sorted(list(set([r['origem'] for r in rotas_disponiveis if 'origem' in r])))
        
        if not origens_disponiveis:
            st.error("❌ Nenhuma origem válida encontrada")
            st.stop()
            
        origem = st.selectbox(
            get_text('origin_airport', lang),
            options=origens_disponiveis,
            key="origem_rota"
        )
    except Exception as e:
        st.error(f"❌ Erro ao carregar origens: {e}")
        st.stop()

with col2:
    # Filtrar destinos baseado na origem
    try:
        destinos_validos = sorted([r['destino'] for r in rotas_disponiveis 
                                  if r.get('origem') == origem and 'destino' in r])
        
        if not destinos_validos:
            st.warning(f"⚠️ Nenhum destino disponível para origem {origem}")
            destinos_validos = ["Sem destinos"]
            
        destino = st.selectbox(
            get_text('destination_airport', lang),
            options=destinos_validos,
            key="destino_rota"
        )
    except Exception as e:
        st.error(f"❌ Erro ao carregar destinos: {e}")
        st.stop()

with col3:
    modelo_rota = st.selectbox(
        get_text('aircraft_model', lang),
        modelos,
        key="modelo_rota"
    )

# Informações da rota selecionada
try:
    rota_info = next((r for r in rotas_disponiveis 
                     if r.get('origem') == origem and r.get('destino') == destino), None)
    
    if rota_info and destino != "Sem destinos":
        st.info(f"""
        📍 **Rota Selecionada**: {origem} → {destino}  
        ⏱️ **Duração**: {rota_info['duracao_h']:.1f}h  
        ✈️ **Modelo**: {modelo_rota}
        """)
    elif destino == "Sem destinos":
        st.warning("⚠️ Selecione uma origem com destinos disponíveis")
    else:
        st.warning(f"⚠️ Rota {origem} → {destino} não encontrada nos dados")
        
except Exception as e:
    st.error(f"❌ Erro ao processar rota: {e}")

# Botão de simulação
if st.button(f"✈️ {get_text('simulate_route', lang)}", type="primary", use_container_width=True):
    
    if destino == "Sem destinos":
        st.error("❌ Selecione uma rota válida para simulação")
        st.stop()
    
    if not rota_info:
        st.error(f"❌ Rota {origem} → {destino} não encontrada")
        st.stop()
    
    try:
        # Realizar cálculo da rota
        resultado_rota = calcular_custo_rota(
            origem=origem,
            destino=destino,
            modelo=modelo_rota,
            params=params,
            rotas_disponiveis=rotas_disponiveis
        )
        
        # Exibir resultados
        st.markdown("---")
        st.markdown(f"### 📊 {get_text('route_analysis', lang)}: {origem} → {destino}")
        
        # KPIs da rota
        kpis = [
            {
                'label': get_text('flight_duration', lang),
                'value': f"{resultado_rota['duracao_horas']:.1f}h",
                'format_type': 'text'
            },
            {
                'label': get_text('total_cost_amaro', lang),
                'value': resultado_rota['custo_amaro'],
                'format_type': 'currency'
            },
            {
                'label': get_text('market_price', lang),
                'value': resultado_rota['preco_mercado'],
                'format_type': 'currency'
            },
            {
                'label': get_text('savings', lang),
                'value': resultado_rota['economia'],
                'format_type': 'currency',
                'delta': resultado_rota['economia_percentual'] if resultado_rota['economia'] > 0 else None
            }
        ]
        
        render_kpi_grid(kpis, columns=4, lang=lang)
        
        # Análise visual da rota
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### 💸 {get_text('cost_composition', lang)}")
            
            custos_labels = [
                get_text('fuel', lang),
                get_text('crew', lang),
                get_text('maintenance', lang),
                get_text('depreciation', lang)
            ]
            
            custos_values = [
                resultado_rota['breakdown_custos']['combustivel'],
                resultado_rota['breakdown_custos']['tripulacao'],
                resultado_rota['breakdown_custos']['manutencao'],
                resultado_rota['breakdown_custos']['depreciacao']
            ]
            
            # Gráfico de pizza com fundo branco
            fig_custos_rota = go.Figure(data=[go.Pie(
                labels=custos_labels,
                values=custos_values,
                hole=0.5,
                marker=dict(colors=['#EF4444', '#F59E0B', '#3B82F6', '#10B981']),
                textinfo='label+percent',
                textfont=dict(size=12),
                hovertemplate='<b>%{label}</b><br>Valor: R$ %{value:,.2f}<br>Percentual: %{percent}<extra></extra>'
            )])
            
            fig_custos_rota.update_layout(
                height=350,
                showlegend=True,
                margin=dict(l=0, r=0, t=20, b=0),
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(color='#1F2937')
            )
            
            st.plotly_chart(fig_custos_rota, use_container_width=True)
        
        with col2:
            st.markdown(f"#### 📊 {get_text('visual_comparison', lang)}")
            
            # Gráfico de barras comparativo
            fig_comp_rota = go.Figure()
            
            categorias = [get_text('amaro_cost', lang), get_text('market_price_label', lang)]
            valores = [resultado_rota['custo_amaro'], resultado_rota['preco_mercado']]
            cores = ['#8C1D40', '#6B7280']
            
            fig_comp_rota.add_trace(go.Bar(
                x=categorias,
                y=valores,
                text=[format_currency(v, lang) for v in valores],
                textposition='outside',
                marker_color=cores,
                hovertemplate='<b>%{x}</b><br>Valor: R$ %{y:,.2f}<extra></extra>'
            ))
            
            # Anotação de economia se positiva
            if resultado_rota['economia'] > 0:
                fig_comp_rota.add_annotation(
                    x=0.5, 
                    y=max(valores) * 0.8,
                    text=f"💰 {get_text('savings', lang)}<br>{format_currency(resultado_rota['economia'], lang)}<br>({resultado_rota['economia_percentual']:.1f}%)",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor="#10B981",
                    font=dict(color="#10B981", size=12),
                    bgcolor="rgba(16, 185, 129, 0.1)",
                    bordercolor="#10B981",
                    borderwidth=1
                )
            
            fig_comp_rota.update_layout(
                height=350,
                showlegend=False,
                yaxis_title=f"Valor (R$)",
                margin=dict(l=0, r=0, t=20, b=0),
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(color='#1F2937'),
                yaxis=dict(tickformat=',.0f')
            )
            
            st.plotly_chart(fig_comp_rota, use_container_width=True)
        
        # Status da análise
        if resultado_rota['viavel']:
            render_status_box(
                'success',
                get_text('advantageous_route', lang),
                f"{get_text('amaro_savings_message', lang)} {format_currency(resultado_rota['economia'], lang)} ({resultado_rota['economia_percentual']:.1f}%) em relação ao preço de mercado para esta rota." if lang == 'pt'
                else f"{get_text('amaro_savings_message', lang)} {format_currency(resultado_rota['economia'], lang)} ({resultado_rota['economia_percentual']:.1f}%) compared to market price for this route."
            )
        else:
            render_status_box(
                'warning',
                get_text('route_attention', lang),
                f"{get_text('cost_above_market', lang)}. {get_text('consider_optimizations', lang)}."
            )
        
        # Análise de sensibilidade
        with st.expander("📈 Análise de Sensibilidade" if lang == 'pt' else "📈 Sensitivity Analysis"):
            st.markdown("**Impacto de variações nos custos:**" if lang == 'pt' else "**Impact of cost variations:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                variacao_combustivel = st.slider(
                    "Variação Preço Combustível (%)" if lang == 'pt' else "Fuel Price Variation (%)",
                    -20, 20, 0, 5
                )
            
            with col2:
                variacao_manutencao = st.slider(
                    "Variação Custo Manutenção (%)" if lang == 'pt' else "Maintenance Cost Variation (%)",
                    -20, 20, 0, 5
                )
            
            # Recalcular com variações
            custo_combustivel_ajustado = resultado_rota['breakdown_custos']['combustivel'] * (1 + variacao_combustivel/100)
            custo_manutencao_ajustado = resultado_rota['breakdown_custos']['manutencao'] * (1 + variacao_manutencao/100)
            
            custo_total_ajustado = (
                custo_combustivel_ajustado + 
                custo_manutencao_ajustado +
                resultado_rota['breakdown_custos']['tripulacao'] +
                resultado_rota['breakdown_custos']['depreciacao']
            )
            
            economia_ajustada = resultado_rota['preco_mercado'] - custo_total_ajustado
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    "Custo Total Ajustado" if lang == 'pt' else "Adjusted Total Cost",
                    format_currency(custo_total_ajustado, lang),
                    f"{custo_total_ajustado - resultado_rota['custo_amaro']:+.0f}"
                )
            
            with col2:
                st.metric(
                    "Economia Ajustada" if lang == 'pt' else "Adjusted Savings",
                    format_currency(economia_ajustada, lang),
                    f"{economia_ajustada - resultado_rota['economia']:+.0f}"
                )
        
        # Preparar dados para exportação
        dados_entrada = {
            'rota': f"{origem} → {destino}",
            'modelo': modelo_rota,
            'duracao_horas': resultado_rota['duracao_horas']
        }
        
        relatorio_dados = criar_relatorio_dados(
            "Simulação de Rota",
            dados_entrada,
            resultado_rota,
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
                f'simulacao_rota_{origem}_{destino}'
            )
        
    except Exception as e:
        st.error(f"❌ Erro na simulação: {e}")
        st.info("💡 Verifique se todos os parâmetros estão configurados corretamente")

# Visualização de rotas disponíveis
with st.expander("🗺️ Rotas Disponíveis" if lang == 'pt' else "🗺️ Available Routes"):
    if rotas_disponiveis:
        df_rotas_display = pd.DataFrame(rotas_disponiveis)
        
        # Verificar se as colunas existem
        if all(col in df_rotas_display.columns for col in ['origem', 'destino', 'duracao_h']):
            df_rotas_display.columns = [
                get_text('origin', lang),
                get_text('destination', lang), 
                get_text('duration', lang)
            ]
            
            st.dataframe(
                df_rotas_display,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("⚠️ Estrutura de dados das rotas está incorreta")
            st.json(rotas_disponiveis[:3])  # Mostrar amostra
    else:
        st.info("ℹ️ Nenhuma rota disponível")
    
    st.info(f"""
    💡 **Dicas** {'(Tips)' if lang == 'en' else ''}:
    - {'Rotas mais longas tendem a ter melhor economia relativa' if lang == 'pt' else 'Longer routes tend to have better relative savings'}
    - {'Considere fatores sazonais na demanda' if lang == 'pt' else 'Consider seasonal demand factors'}
    - {'Configure novas rotas na página Configurações' if lang == 'pt' else 'Configure new routes in Settings page'}
    """)

# Footer da página
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6B7280; padding: 1rem;">
    <p>✈️ <strong>{get_text('page_simulator', lang)}</strong> - Análise detalhada por rota específica</p>
</div>
""", unsafe_allow_html=True)