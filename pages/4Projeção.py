"""
Página 4: Projeção de Longo Prazo e Análise de Breakeven
Análise temporal de 12-60 meses com ponto de equilíbrio
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
from components.metrics import render_highlight_metric, render_kpi_grid
from components.status import render_system_status
from utils.params import load_params, format_currency
from utils.calculations import calcular_projecao_mensal
from utils.export_manager import botao_download_inteligente, criar_relatorio_dados

# Configuração da página
st.set_page_config(
    page_title="Projeção e Breakeven | Amaro Aviation",
    page_icon="📈",
    layout="wide"
)

# Carregar tema
load_theme()

# Sidebar e idioma
lang = render_sidebar()

# Header da página
render_page_header(
    'page_projection',
    'Análise temporal e determinação do ponto de equilíbrio financeiro' if lang == 'pt' 
    else 'Time analysis and financial breakeven point determination',
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
st.markdown(f"### 📈 {get_text('page_projection', lang)}")

# Parâmetros principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    modelo_proj = st.selectbox(
        get_text('aircraft_model', lang),
        modelos,
        key="modelo_proj"
    )

with col2:
    horas_mes_proj = st.number_input(
        get_text('monthly_hours', lang).replace('Charter/', 'Voo/'),
        min_value=20,
        max_value=150,
        value=60,
        step=10,
        key="horas_mes_proj"
    )

with col3:
    horizonte_meses = st.slider(
        get_text('projection_horizon', lang),
        min_value=12,
        max_value=60,
        value=36,
        step=12,
        key="horizonte_proj"
    )

with col4:
    taxa_crescimento = st.number_input(
        get_text('growth_rate', lang),
        min_value=0.0,
        max_value=20.0,
        value=5.0,
        step=1.0,
        help="Taxa de crescimento anual das horas voadas" if lang == 'pt'
             else "Annual growth rate of flight hours"
    )

# Parâmetros avançados
with st.expander(f"⚙️ {get_text('advanced_parameters', lang)}"):
    col1, col2 = st.columns(2)
    
    with col1:
        investimento_inicial = st.number_input(
            get_text('initial_investment', lang),
            value=0,
            step=100000,
            help="Valor de entrada ou investimento inicial" if lang == 'pt'
                 else "Initial investment or down payment"
        )
        
        taxa_ocupacao_proj = st.slider(
            get_text('occupancy_charter', lang),
            min_value=50,
            max_value=90,
            value=70,
            key="ocupacao_proj"
        )
    
    with col2:
        inflacao_custos = st.number_input(
            get_text('cost_inflation', lang),
            min_value=0.0,
            max_value=15.0,
            value=4.0,
            step=0.5
        )
        
        reajuste_charter = st.number_input(
            get_text('charter_adjustment', lang),
            min_value=0.0,
            max_value=15.0,
            value=5.0,
            step=0.5
        )

# Botão de geração da projeção
if st.button(f"📊 {get_text('generate_projection', lang)}", type="primary", use_container_width=True):
    
    try:
        # Realizar projeção
        resultado_projecao = calcular_projecao_mensal(
            modelo=modelo_proj,
            horas_mes=horas_mes_proj,
            num_meses=horizonte_meses,
            params=params,
            taxa_crescimento=taxa_crescimento,
            inflacao_custos=inflacao_custos,
            reajuste_preco=reajuste_charter,
            investimento_inicial=investimento_inicial
        )
        
        # Calcular totais
        receita_total = sum(resultado_projecao['receitas'])
        custo_total = sum(resultado_projecao['custos'])
        lucro_total = sum(resultado_projecao['lucros'])
        roi_total = (lucro_total / (investimento_inicial if investimento_inicial > 0 else custo_total)) * 100
        
        # Exibir resultados
        st.markdown("---")
        st.markdown(f"### 📊 {get_text('projection_analysis', lang)}")
        
        # KPIs principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            render_highlight_metric(
                get_text('total_revenue_projected', lang),
                receita_total,
                f"{horizonte_meses} meses",
                "#10B981",
                "currency",
                lang
            )
        
        with col2:
            render_highlight_metric(
                get_text('total_cost_projected', lang),
                custo_total,
                f"{horizonte_meses} meses",
                "#EF4444", 
                "currency",
                lang
            )
        
        with col3:
            render_highlight_metric(
                get_text('total_profit_projected', lang),
                lucro_total,
                f"ROI: {roi_total:.1f}%",
                "#8C1D40",
                "currency",
                lang
            )
        
        with col4:
            if resultado_projecao['breakeven_mes']:
                render_highlight_metric(
                    get_text('breakeven', lang),
                    resultado_projecao['breakeven_mes'],
                    get_text('return_investment', lang),
                    "#F59E0B",
                    "number",
                    lang
                )
            else:
                render_highlight_metric(
                    get_text('breakeven', lang),
                    f"> {horizonte_meses}",
                    get_text('outside_horizon', lang),
                    "#EF4444",
                    "text",
                    lang
                )
        
        # Gráfico de projeção temporal
        st.markdown(f"#### 📈 {get_text('long_term_projection', lang)}")
        
        fig_projecao = go.Figure()
        
        # Receitas acumuladas
        receitas_acc = [sum(resultado_projecao['receitas'][:i+1]) for i in range(len(resultado_projecao['receitas']))]
        fig_projecao.add_trace(go.Scatter(
            x=resultado_projecao['meses'],
            y=receitas_acc,
            name=get_text('accumulated_revenue', lang),
            mode='lines',
            line=dict(color='#10B981', width=3),
            fill='tonexty',
            fillcolor='rgba(16, 185, 129, 0.1)'
        ))
        
        # Custos acumulados
        custos_acc = [sum(resultado_projecao['custos'][:i+1]) for i in range(len(resultado_projecao['custos']))]
        fig_projecao.add_trace(go.Scatter(
            x=resultado_projecao['meses'],
            y=custos_acc,
            name=get_text('accumulated_cost', lang),
            mode='lines',
            line=dict(color='#EF4444', width=3)
        ))
        
        # Fluxo de caixa
        fig_projecao.add_trace(go.Scatter(
            x=resultado_projecao['meses'],
            y=resultado_projecao['fluxo_caixa'],
            name=get_text('cash_flow', lang),
            mode='lines',
            line=dict(color='#8C1D40', width=4),
            fill='tozeroy',
            fillcolor='rgba(140, 29, 64, 0.1)'
        ))
        
        # Linha de breakeven
        if resultado_projecao['breakeven_mes']:
            fig_projecao.add_vline(
                x=resultado_projecao['breakeven_mes'],
                line_dash="dash",
                line_color="#F59E0B",
                annotation_text=f"Breakeven: {resultado_projecao['breakeven_mes']} {get_text('months', lang).lower()}",
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
            title=get_text('long_term_projection', lang),
            xaxis_title=get_text('months', lang),
            yaxis_title=get_text('value_currency', lang),
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
        
        # Análise de marcos importantes
        st.markdown(f"#### 📊 {get_text('important_milestones', lang)}")
        
        marcos_data = []
        periodos = [6, 12, 24, 36, horizonte_meses] if horizonte_meses != 36 else [6, 12, 24, 36]
        
        for periodo in periodos:
            if periodo <= len(resultado_projecao['receitas']):
                marcos_data.append({
                    get_text('milestone', lang): f"{periodo} {get_text('months', lang).lower()}",
                    get_text('accumulated_revenue', lang): format_currency(sum(resultado_projecao['receitas'][:periodo]), lang),
                    get_text('accumulated_profit', lang): format_currency(sum(resultado_projecao['lucros'][:periodo]), lang),
                    get_text('cash_flow', lang): format_currency(resultado_projecao['fluxo_caixa'][periodo-1], lang)
                })
        
        df_marcos = pd.DataFrame(marcos_data)
        st.dataframe(df_marcos, use_container_width=True, hide_index=True)
        
        # Análise de cenários
        with st.expander("🔄 Análise de Cenários" if lang == 'pt' else "🔄 Scenario Analysis"):
            st.markdown("**Impacto de mudanças nos parâmetros:**" if lang == 'pt' else "**Impact of parameter changes:**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Cenário Otimista (+20%)**" if lang == 'pt' else "**Optimistic Scenario (+20%)**")
                lucro_otimista = lucro_total * 1.2
                breakeven_otimista = int(resultado_projecao['breakeven_mes'] * 0.8) if resultado_projecao['breakeven_mes'] else None
                
                st.metric("Lucro Total" if lang == 'pt' else "Total Profit", 
                         format_currency(lucro_otimista, lang),
                         f"+{format_currency(lucro_otimista - lucro_total, lang)}")
                
                if breakeven_otimista:
                    st.metric("Breakeven", f"{breakeven_otimista} meses",
                             f"-{resultado_projecao['breakeven_mes'] - breakeven_otimista} meses")
            
            with col2:
                st.markdown("**Cenário Base**" if lang == 'pt' else "**Base Scenario**")
                st.metric("Lucro Total" if lang == 'pt' else "Total Profit", 
                         format_currency(lucro_total, lang))
                
                if resultado_projecao['breakeven_mes']:
                    st.metric("Breakeven", f"{resultado_projecao['breakeven_mes']} meses")
                else:
                    st.metric("Breakeven", f"> {horizonte_meses} meses")
            
            with col3:
                st.markdown("**Cenário Pessimista (-20%)**" if lang == 'pt' else "**Pessimistic Scenario (-20%)**")
                lucro_pessimista = lucro_total * 0.8
                breakeven_pessimista = int(resultado_projecao['breakeven_mes'] * 1.2) if resultado_projecao['breakeven_mes'] else None
                
                st.metric("Lucro Total" if lang == 'pt' else "Total Profit", 
                         format_currency(lucro_pessimista, lang),
                         f"{format_currency(lucro_pessimista - lucro_total, lang)}")
                
                if breakeven_pessimista and breakeven_pessimista <= horizonte_meses:
                    st.metric("Breakeven", f"{breakeven_pessimista} meses",
                             f"+{breakeven_pessimista - resultado_projecao['breakeven_mes']} meses")
                else:
                    st.metric("Breakeven", f"> {horizonte_meses} meses")
        
        # Preparar dados para exportação
        dados_entrada = {
            'modelo': modelo_proj,
            'horas_mes_inicial': horas_mes_proj,
            'horizonte_meses': horizonte_meses,
            'taxa_crescimento': taxa_crescimento,
            'investimento_inicial': investimento_inicial,
            'inflacao_custos': inflacao_custos,
            'reajuste_charter': reajuste_charter
        }
        
        resultados_export = {
            'receita_total': receita_total,
            'custo_total': custo_total,
            'lucro_total': lucro_total,
            'roi_total': roi_total,
            'breakeven_mes': resultado_projecao['breakeven_mes'],
            'fluxo_caixa_final': resultado_projecao['fluxo_caixa'][-1]
        }
        
        relatorio_dados = criar_relatorio_dados(
            "Projeção de Longo Prazo",
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
                'projecao_longo_prazo'
            )
        
    except Exception as e:
        st.error(f"❌ Erro na projeção: {e}")

# Calculadora de breakeven rápida
with st.expander("⚡ Calculadora de Breakeven Rápida" if lang == 'pt' else "⚡ Quick Breakeven Calculator"):
    st.markdown("**Estimativa rápida de breakeven:**" if lang == 'pt' else "**Quick breakeven estimate:**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        investimento_rapido = st.number_input(
            "Investimento (R$)" if lang == 'pt' else "Investment (R$)",
            value=1000000,
            step=100000,
            key="inv_rapido"
        )
    
    with col2:
        lucro_mensal_estimado = st.number_input(
            "Lucro Mensal Estimado (R$)" if lang == 'pt' else "Estimated Monthly Profit (R$)",
            value=50000,
            step=5000,
            key="lucro_rapido"
        )
    
    with col3:
        if lucro_mensal_estimado > 0:
            breakeven_rapido = investimento_rapido / lucro_mensal_estimado
            st.metric(
                "Breakeven Estimado" if lang == 'pt' else "Estimated Breakeven",
                f"{breakeven_rapido:.1f} meses"
            )
        else:
            st.metric(
                "Breakeven Estimado" if lang == 'pt' else "Estimated Breakeven",
                "N/A"
            )

# Informações educativas
with st.expander("📚 Entendendo a Projeção" if lang == 'pt' else "📚 Understanding Projection"):
    if lang == 'pt':
        st.markdown("""
        **Conceitos Importantes:**
        
        - **Breakeven**: Ponto onde o fluxo de caixa acumulado torna-se positivo
        - **ROI**: Retorno sobre o investimento considerando o período total
        - **Fluxo de Caixa**: Diferença acumulada entre receitas e custos, considerando investimento inicial
        - **Cenários**: Variações dos parâmetros para análise de sensibilidade
        
        **Fatores que Aceleram o Breakeven:**
        
        - Maior taxa de ocupação
        - Preços de charter mais altos
        - Crescimento consistente das horas
        - Controle de inflação de custos
        - Menor investimento inicial
        
        **Fatores de Risco:**
        
        - Volatilidade do preço do combustível
        - Sazonalidade da demanda
        - Custos de manutenção imprevistos
        - Mudanças regulatórias
        """)
    else:
        st.markdown("""
        **Important Concepts:**
        
        - **Breakeven**: Point where accumulated cash flow becomes positive
        - **ROI**: Return on investment considering the total period
        - **Cash Flow**: Accumulated difference between revenues and costs, considering initial investment
        - **Scenarios**: Parameter variations for sensitivity analysis
        
        **Factors that Accelerate Breakeven:**
        
        - Higher occupancy rate
        - Higher charter prices
        - Consistent growth in hours
        - Cost inflation control
        - Lower initial investment
        
        **Risk Factors:**
        
        - Fuel price volatility
        - Demand seasonality
        - Unexpected maintenance costs
        - Regulatory changes
        """)

# Footer da página
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6B7280; padding: 1rem;">
    <p>📈 <strong>{get_text('page_projection', lang)}</strong> - Análise temporal completa com breakeven</p>
</div>
""", unsafe_allow_html=True)