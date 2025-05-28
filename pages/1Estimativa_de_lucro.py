"""
Página 1: Estimativa de Lucro - VERSÃO DEFINITIVA 100% FUNCIONANDO
- Selectbox persistente FUNCIONA
- Gráficos FUNCIONAM e aparecem
- Tradução FUNCIONA
- Cálculos FUNCIONAM
"""

import streamlit as st
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

# Imports dos sistemas corrigidos
from config.theme_fix import load_theme
from config.idiomas import get_text, detect_language_from_selection, get_language_options, get_current_language_display
from components.sidebar import render_sidebar
from components.status import render_system_status, render_calculation_status
from utils.params import load_params, format_currency, format_percentage
from utils.calculations import calcular_lucro_mensal_charter
from utils.export_manager import botao_download_inteligente, criar_relatorio_dados
from utils.session_state import persistent_selectbox, persistent_number_input, persistent_slider
from utils.graficos_garantidos import criar_grafico_pizza as render_chart_receitas, criar_grafico_barras as render_chart_custos


# ========================================================================
# CONFIGURAÇÃO DA PÁGINA
# ========================================================================
st.set_page_config(
    page_title="Estimativa de Lucro | Amaro Aviation",
    page_icon="📈",
    layout="wide"
)

# Carregar tema
load_theme()

# ========================================================================
# SIDEBAR E DETECÇÃO DE IDIOMA
# ========================================================================
try:
    lang = render_sidebar()
    if not lang:
        lang = 'pt'  # Fallback
except Exception:
    lang = 'pt'  # Fallback se sidebar falhar

# ========================================================================
# HEADER DA PÁGINA
# ========================================================================
st.markdown(f"# 📈 {get_text('page_profit', lang)}")
st.markdown(f"*{get_text('cost_breakdown', lang)} com operação charter*")
st.markdown("---")

# ========================================================================
# CARREGAMENTO DE DADOS E VALIDAÇÃO
# ========================================================================
try:
    params = load_params()
    system_ok = render_system_status(params, lang)
    
    if not system_ok:
        st.error(f"❌ {get_text('system_error', lang)}")
        st.info(f"💡 Configure o sistema na página de {get_text('page_settings', lang)}")
        st.stop()
    
    modelos = params.get('modelos_disponiveis', [])
    
    if not modelos:
        st.error(f"❌ {get_text('no_data', lang)} - Modelos de aeronaves")
        st.stop()
    
except Exception as e:
    st.error(f"❌ {get_text('system_error', lang)}: {e}")
    st.stop()

# ========================================================================
# INTERFACE PRINCIPAL - FORMULÁRIO DE ENTRADA
# ========================================================================
st.markdown(f"### 💰 {get_text('page_profit', lang)}")

# Formulário com persistência GARANTIDA
col1, col2, col3, col4 = st.columns(4)

with col1:
    modelo_selecionado = persistent_selectbox(
        get_text('aircraft_model', lang),
        options=modelos,
        key="modelo_persist",
        help="Selecione o modelo da aeronave para análise"
    )

with col2:
    horas_charter = persistent_number_input(
        get_text('monthly_hours', lang),
        key="horas_persist",
        default_value=80.0,
        min_value=10.0,
        max_value=200.0,
        step=5.0,
        help="Horas disponíveis para charter por mês"
    )

with col3:
    taxa_ocupacao = persistent_slider(
        get_text('occupancy_rate', lang),
        key="taxa_ocupacao_persist",
        min_value=50,
        max_value=95,
        default_value=75,
        help="Percentual de ocupação das horas disponíveis"
    )

with col4:
    # Buscar preço padrão baseado no modelo
    preco_default = 8000.0
    try:
        if modelo_selecionado and modelo_selecionado in params.get('preco_mercado_hora', {}):
            preco_default = float(params['preco_mercado_hora'][modelo_selecionado])
    except:
        pass
    
    preco_hora_charter = persistent_number_input(
        get_text('charter_price', lang),
        key="preco_charter_persist",
        default_value=preco_default,
        min_value=1000.0,
        max_value=50000.0,
        step=500.0,
        help="Preço por hora de charter"
    )

# ========================================================================
# BOTÃO DE CÁLCULO E PROCESSAMENTO
# ========================================================================
if st.button(f"🚀 {get_text('calculate', lang)}", type="primary", use_container_width=True):
    
    # Validar dados antes do cálculo
    if not modelo_selecionado:
        st.error(f"❌ Selecione um {get_text('aircraft_model', lang).lower()}")
        st.stop()
    
    if horas_charter <= 0:
        st.error(f"❌ {get_text('invalid_data', lang)} - Horas devem ser maior que zero")
        st.stop()
    
    try:
        with st.spinner(f"{get_text('loading', lang)}..."):
            # Realizar cálculo
            resultado = calcular_lucro_mensal_charter(
                modelo=modelo_selecionado,
                horas_charter=horas_charter,
                taxa_ocupacao=taxa_ocupacao,
                preco_hora=preco_hora_charter,
                params=params
            )
        
        # ============================================================
        # EXIBIÇÃO DOS RESULTADOS
        # ============================================================
        st.markdown("---")
        st.markdown(f"### 📊 {get_text('projection_analysis', lang)}")
        
        # KPIs principais usando métricas nativas do Streamlit
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                get_text('gross_revenue', lang),
                format_currency(resultado['receita_bruta'], lang),
                help="Receita total antes da divisão"
            )
        
        with col2:
            st.metric(
                get_text('owner_revenue', lang),
                format_currency(resultado['receita_proprietario'], lang),
                help="90% da receita vai para o proprietário"
            )
        
        with col3:
            delta_color = "normal" if resultado['lucro_liquido'] > 0 else "inverse"
            st.metric(
                get_text('net_profit', lang),
                format_currency(resultado['lucro_liquido'], lang),
                delta=f"{resultado['roi_mensal']:.1f}%",
                help="Lucro após descontar custos operacionais"
            )
        
        with col4:
            st.metric(
                get_text('monthly_roi', lang),
                format_percentage(resultado['roi_mensal'], lang),
                help="Retorno sobre investimento mensal"
            )
        
        # ============================================================
        # GRÁFICOS GARANTIDOS PARA FUNCIONAR
        # ============================================================
        st.markdown("#### 📊 Análise Visual")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"##### 💰 {get_text('revenue_composition', lang)}")
            try:
                fig_receita = render_chart_receitas(
                    resultado['receita_proprietario'], 
                    resultado['taxa_amaro'], 
                    lang
                )
                st.plotly_chart(fig_receita, use_container_width=True, key="chart_receitas")
            except Exception as e:
                st.error(f"Erro no gráfico de receitas: {e}")
                st.info("🔍 Debug: Verifique se os dados estão corretos")
        
        with col2:
            st.markdown(f"##### 💸 {get_text('cost_breakdown', lang)}")
            try:
                # Preparar dados dos custos de forma robusta
                custos_dict = {
                    'combustivel': resultado.get('breakdown_custos', {}).get('combustivel', 0),
                    'tripulacao': resultado.get('breakdown_custos', {}).get('tripulacao', 0),
                    'manutencao': resultado.get('breakdown_custos', {}).get('manutencao', 0),
                    'depreciacao': resultado.get('breakdown_custos', {}).get('depreciacao', 0)
                }
                
                fig_custos = render_chart_custos(custos_dict, lang)
                st.plotly_chart(fig_custos, use_container_width=True, key="chart_custos")
            except Exception as e:
                st.error(f"Erro no gráfico de custos: {e}")
                st.info("🔍 Debug: Verifique os dados de breakdown_custos")
        
        # ============================================================
        # STATUS DA OPERAÇÃO
        # ============================================================
        if resultado['lucrativo']:
            st.success(f"""
            **✅ {get_text('profitable_operation', lang)}**
            
            O proprietário terá um lucro líquido de **{format_currency(resultado['lucro_liquido'], lang)}** por mês.
            """)
        else:
            st.warning(f"""
            **⚠️ {get_text('operation_deficit', lang)}**
            
            A operação apresenta déficit de **{format_currency(abs(resultado['lucro_liquido']), lang)}** por mês.
            """)
        
        # ============================================================
        # DETALHAMENTO DOS CUSTOS
        # ============================================================
        with st.expander("🔍 Detalhamento dos Custos"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Custos Operacionais:**")
                for key, value in resultado.get('breakdown_custos', {}).items():
                    label = get_text(key, lang)
                    st.write(f"• {label}: {format_currency(value, lang)}")
            
            with col2:
                st.markdown("**Parâmetros da Simulação:**")
                st.write(f"• Horas disponíveis: {horas_charter}h/mês")
                st.write(f"• Horas efetivas: {resultado.get('horas_efetivas', 0):.1f}h/mês")
                st.write(f"• Taxa de ocupação: {taxa_ocupacao}%")
                st.write(f"• Preço por hora: {format_currency(preco_hora_charter, lang)}")
        
        # ============================================================
        # EXPORTAÇÃO
        # ============================================================
        st.markdown("---")
        st.markdown("### 📊 Exportação de Relatório")
        
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
        
        # Botão de download
        col1, col2 = st.columns([3, 1])
        
        with col2:
            botao_download_inteligente(
                relatorio_dados,
                f"📊 {get_text('export', lang)}",
                'excel',
                'estimativa_lucro_mensal'
            )
        
        with col1:
            st.info("💡 Clique no botão ao lado para baixar o relatório completo em Excel")
        
    except Exception as e:
        st.error(f"❌ Erro no cálculo: {e}")
        st.info("💡 Verifique se todos os parâmetros estão configurados corretamente na página de Configurações")
        
        # Debug para desenvolvimento
        if st.checkbox("🔍 Mostrar detalhes do erro (Debug)"):
            st.code(str(e))
            st.json({
                "modelo": modelo_selecionado,
                "horas": horas_charter,
                "ocupacao": taxa_ocupacao,
                "preco": preco_hora_charter,
                "params_keys": list(params.keys()) if params else []
            })

# ========================================================================
# INFORMAÇÕES ADICIONAIS
# ========================================================================
with st.expander("💡 Dicas e Informações"):
    if lang == 'pt':
        st.markdown("""
        **Como interpretar os resultados:**
        
        - **Receita Bruta**: Total faturado com as horas de charter efetivamente voadas
        - **Receita do Proprietário**: 90% da receita bruta (padrão de divisão Amaro Aviation)
        - **Taxa Amaro**: 10% da receita bruta destinada à gestão e operação
        - **Lucro Líquido**: Receita do proprietário menos custos operacionais totais
        - **ROI Mensal**: Percentual de retorno sobre os custos operacionais
        
        **Dicas para otimização:**
        
        - Mantenha a taxa de ocupação acima de 70% para maximizar receitas
        - Ajuste preços conforme demanda sazonal e mercado local
        - Monitore regularmente custos de combustível (maior componente variável)
        - Considere rotas mais eficientes para reduzir tempos de ferry
        - Analise a concorrência para precificação competitiva
        """)
    else:
        st.markdown("""
        **How to interpret results:**
        
        - **Gross Revenue**: Total billed for effectively flown charter hours
        - **Owner Revenue**: 90% of gross revenue (Amaro Aviation standard split)
        - **Amaro Fee**: 10% of gross revenue for management and operations
        - **Net Profit**: Owner revenue minus total operational costs
        - **Monthly ROI**: Percentage return on operational costs
        
        **Optimization tips:**
        
        - Keep occupancy rate above 70% to maximize revenue
        - Adjust prices according to seasonal demand and local market
        - Regularly monitor fuel costs (largest variable component)
        - Consider more efficient routes to reduce ferry times
        - Analyze competition for competitive pricing
        """)

# ========================================================================
# FOOTER
# ========================================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6B7280; padding: 1rem;">
    <p>📈 <strong>{get_text('page_profit', lang)}</strong> - Análise detalhada de rentabilidade mensal</p>
</div>
""", unsafe_allow_html=True)