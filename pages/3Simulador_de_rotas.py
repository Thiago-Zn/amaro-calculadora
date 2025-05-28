"""
Página 3: Simulador de Rotas - VERSÃO DEFINITIVA 100% FUNCIONANDO
- Dropdowns persistentes (Origem, Destino, Modelo) FUNCIONAM
- Gráficos de Custos e Comparativo FUNCIONAM
- Tradução FUNCIONA
- Cálculos de rota FUNCIONAM
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

# Imports dos sistemas corrigidos
from config.theme import load_theme
from config.idiomas import get_text
from components.sidebar import render_sidebar
from components.status import render_system_status, render_status_box
from utils.params import load_params, format_currency
from utils.calculations import calcular_custo_rota
from utils.export_manager import botao_download_inteligente, criar_relatorio_dados
from utils.session_state import persistent_selectbox
from utils.charts_fixed import render_chart_custos, render_chart_comparativo

# ========================================================================
# CONFIGURAÇÃO DA PÁGINA
# ========================================================================
st.set_page_config(
    page_title="Simulador de Rotas | Amaro Aviation",
    page_icon="✈️",
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
        lang = 'pt'
except Exception:
    lang = 'pt'

# ========================================================================
# HEADER DA PÁGINA
# ========================================================================
st.markdown(f"# ✈️ {get_text('page_simulator', lang)}")
st.markdown("*Simulação de custos por rota específica origem-destino*")
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
# CARREGAMENTO DE ROTAS
# ========================================================================
try:
    df_rotas = pd.read_csv('data/rotas.csv')
    
    # Validar estrutura do CSV
    required_columns = ['origem', 'destino', 'duracao_h']
    if not all(col in df_rotas.columns for col in required_columns):
        raise ValueError(f"CSV deve ter colunas: {required_columns}")
    
    rotas_disponiveis = df_rotas.to_dict('records')
    
    if not rotas_disponiveis:
        raise ValueError("Nenhuma rota encontrada no arquivo")
        
except Exception as e:
    st.warning(f"⚠️ Problema com arquivo de rotas: {e}")
    
    # Rotas padrão como fallback
    rotas_disponiveis = [
        {"origem": "GRU", "destino": "SDU", "duracao_h": 1.0},
        {"origem": "GRU", "destino": "CGH", "duracao_h": 0.5},
        {"origem": "CGH", "destino": "BSB", "duracao_h": 1.4},
        {"origem": "BSB", "destino": "SDU", "duracao_h": 1.7},
        {"origem": "GRU", "destino": "CNF", "duracao_h": 1.0}
    ]
    
    st.info("ℹ️ Usando rotas padrão. Configure rotas personalizadas na página de Configurações.")

# ========================================================================
# INTERFACE PRINCIPAL - SELEÇÃO DE ROTA
# ========================================================================
st.markdown(f"### ✈️ {get_text('page_simulator', lang)}")

# Verificar se há rotas disponíveis
if not rotas_disponiveis:
    st.error(f"❌ {get_text('no_data', lang)} - Rotas")
    st.info(f"💡 Configure rotas na página de {get_text('page_settings', lang)}")
    st.stop()

# Formulário de seleção com persistência GARANTIDA
col1, col2, col3 = st.columns(3)

with col1:
    # Obter origens únicas e ordenadas
    try:
        origens_disponiveis = sorted(list(set([
            str(r['origem']).strip().upper() 
            for r in rotas_disponiveis 
            if r.get('origem') and str(r.get('origem')).strip()
        ])))
        
        if not origens_disponiveis:
            st.error("❌ Nenhuma origem válida encontrada nos dados")
            st.stop()
            
        # Selectbox persistente para origem
        origem = persistent_selectbox(
            get_text('origin_airport', lang),
            options=origens_disponiveis,
            key="origem_rota_persist",
            help="Aeroporto de origem (código IATA)"
        )
        
    except Exception as e:
        st.error(f"❌ Erro ao processar origens: {e}")
        st.stop()

with col2:
    # Filtrar destinos baseado na origem selecionada
    try:
        if origem:
            destinos_validos = sorted([
                str(r['destino']).strip().upper() 
                for r in rotas_disponiveis 
                if (r.get('origem', '').strip().upper() == origem and 
                    r.get('destino') and 
                    str(r.get('destino')).strip())
            ])
            
            # Remover duplicatas mantendo ordem
            destinos_validos = list(dict.fromkeys(destinos_validos))
            
            if not destinos_validos:
                destinos_validos = ["Sem destinos disponíveis"]
                
        else:
            destinos_validos = ["Selecione origem primeiro"]
            
        # Selectbox persistente para destino
        destino = persistent_selectbox(
            get_text('destination_airport', lang),
            options=destinos_validos,
            key="destino_rota_persist",
            help="Aeroporto de destino (código IATA)"
        )
        
    except Exception as e:
        st.error(f"❌ Erro ao processar destinos: {e}")
        destino = "Erro"

with col3:
    # Selectbox persistente para modelo
    modelo_rota = persistent_selectbox(
        get_text('aircraft_model', lang),
        options=modelos,
        key="modelo_rota_persist",
        help="Modelo da aeronave para simulação"
    )

# ========================================================================
# INFORMAÇÕES DA ROTA SELECIONADA
# ========================================================================
try:
    # Buscar informações da rota selecionada
    rota_info = None
    if origem and destino and destino not in ["Sem destinos disponíveis", "Selecione origem primeiro", "Erro"]:
        for r in rotas_disponiveis:
            if (str(r.get('origem', '')).strip().upper() == origem and 
                str(r.get('destino', '')).strip().upper() == destino):
                rota_info = r
                break
    
    # Exibir informações da rota
    if rota_info:
        st.success(f"""
        📍 **Rota Selecionada**: {origem} → {destino}  
        ⏱️ **Duração**: {rota_info['duracao_h']:.1f}h  
        ✈️ **Modelo**: {modelo_rota}
        """)
        rota_valida = True
    elif destino in ["Sem destinos disponíveis", "Selecione origem primeiro"]:
        st.info(f"ℹ️ {destino}")
        rota_valida = False
    else:
        st.warning(f"⚠️ Rota {origem} → {destino} não encontrada nos dados")
        rota_valida = False
        
except Exception as e:
    st.error(f"❌ Erro ao processar informações da rota: {e}")
    rota_valida = False

# ========================================================================
# BOTÃO DE SIMULAÇÃO E PROCESSAMENTO
# ========================================================================
if st.button(f"✈️ {get_text('simulate_route', lang)}", type="primary", use_container_width=True):
    
    # Validações antes da simulação
    if not rota_valida or not rota_info:
        st.error("❌ Selecione uma rota válida para simulação")
        st.stop()
    
    if not modelo_rota:
        st.error(f"❌ Selecione um {get_text('aircraft_model', lang).lower()}")
        st.stop()
    
    try:
        with st.spinner(f"{get_text('loading', lang)}..."):
            # Realizar cálculo da rota
            resultado_rota = calcular_custo_rota(
                origem=origem,
                destino=destino,
                modelo=modelo_rota,
                params=params,
                rotas_disponiveis=rotas_disponiveis
            )
        
        # ============================================================
        # EXIBIÇÃO DOS RESULTADOS
        # ============================================================
        st.markdown("---")
        st.markdown(f"### 📊 {get_text('route_analysis', lang)}: {origem} → {destino}")
        
        # KPIs da rota usando métricas nativas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                get_text('flight_duration', lang),
                f"{resultado_rota['duracao_horas']:.1f}h",
                help="Tempo de voo estimado para a rota"
            )
        
        with col2:
            st.metric(
                get_text('total_cost_amaro', lang),
                format_currency(resultado_rota['custo_amaro'], lang),
                help="Custo total da operação com Amaro Aviation"
            )
        
        with col3:
            st.metric(
                get_text('market_price', lang),
                format_currency(resultado_rota['preco_mercado'], lang),
                help="Preço típico de mercado para esta rota"
            )
        
        with col4:
            delta_symbol = "+" if resultado_rota['economia'] > 0 else ""
            delta_color = "normal" if resultado_rota['economia'] > 0 else "inverse"
            st.metric(
                get_text('savings', lang),
                format_currency(resultado_rota['economia'], lang),
                delta=f"{delta_symbol}{resultado_rota['economia_percentual']:.1f}%",
                help="Economia em relação ao preço de mercado"
            )
        
        # ============================================================
        # ANÁLISE VISUAL GARANTIDA
        # ============================================================
        st.markdown("#### 📊 Análise Visual")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"##### 💸 {get_text('cost_composition', lang)}")
            try:
                # Preparar dados dos custos de forma robusta
                custos_dict = {
                    'combustivel': resultado_rota.get('breakdown_custos', {}).get('combustivel', 0),
                    'tripulacao': resultado_rota.get('breakdown_custos', {}).get('tripulacao', 0),
                    'manutencao': resultado_rota.get('breakdown_custos', {}).get('manutencao', 0),
                    'depreciacao': resultado_rota.get('breakdown_custos', {}).get('depreciacao', 0)
                }
                
                fig_custos = render_chart_custos(custos_dict, lang)
                st.plotly_chart(fig_custos, use_container_width=True, key="chart_custos_rota")
                
            except Exception as e:
                st.error(f"Erro no gráfico de custos: {e}")
                st.info("🔍 Debug: Verifique os dados de breakdown_custos")
        
        with col2:
            st.markdown(f"##### 📊 {get_text('visual_comparison', lang)}")
            try:
                fig_comparativo = render_chart_comparativo(
                    resultado_rota['custo_amaro'], 
                    resultado_rota['preco_mercado'], 
                    lang
                )
                st.plotly_chart(fig_comparativo, use_container_width=True, key="chart_comparativo_rota")
                
            except Exception as e:
                st.error(f"Erro no gráfico comparativo: {e}")
                st.info("🔍 Debug: Verifique os dados de comparativo")
        
        # ============================================================
        # STATUS DA ANÁLISE
        # ============================================================
        if resultado_rota.get('viavel', False):
            render_status_box(
                'success',
                get_text('advantageous_route', lang),
                f"A gestão Amaro oferece economia de {format_currency(resultado_rota['economia'], lang)} ({resultado_rota['economia_percentual']:.1f}%) em relação ao preço de mercado para esta rota."
            )
        else:
            render_status_box(
                'warning',
                get_text('route_attention', lang),
                f"O custo operacional está acima do preço de mercado. Considere otimizações operacionais para esta rota."
            )
        
        # ============================================================
        # ANÁLISE DE SENSIBILIDADE
        # ============================================================
        with st.expander("📈 Análise de Sensibilidade"):
            st.markdown("**Impacto de variações nos custos:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                variacao_combustivel = st.slider(
                    "Variação Preço Combustível (%)",
                    -20, 20, 0, 5,
                    key="var_combustivel_rota",
                    help="Simule variações no preço do combustível"
                )
            
            with col2:
                variacao_manutencao = st.slider(
                    "Variação Custo Manutenção (%)",
                    -20, 20, 0, 5,
                    key="var_manutencao_rota",
                    help="Simule variações no custo de manutenção"
                )
            
            # Recalcular com variações
            try:
                breakdown = resultado_rota.get('breakdown_custos', {})
                custo_combustivel_ajustado = breakdown.get('combustivel', 0) * (1 + variacao_combustivel/100)
                custo_manutencao_ajustado = breakdown.get('manutencao', 0) * (1 + variacao_manutencao/100)
                
                custo_total_ajustado = (
                    custo_combustivel_ajustado + 
                    custo_manutencao_ajustado +
                    breakdown.get('tripulacao', 0) +
                    breakdown.get('depreciacao', 0)
                )
                
                economia_ajustada = resultado_rota['preco_mercado'] - custo_total_ajustado
                diferenca_custo = custo_total_ajustado - resultado_rota['custo_amaro']
                diferenca_economia = economia_ajustada - resultado_rota['economia']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        "Custo Total Ajustado",
                        format_currency(custo_total_ajustado, lang),
                        delta=f"{diferenca_custo:+.0f}" if diferenca_custo != 0 else None
                    )
                
                with col2:
                    st.metric(
                        "Economia Ajustada",
                        format_currency(economia_ajustada, lang),
                        delta=f"{diferenca_economia:+.0f}" if diferenca_economia != 0 else None
                    )
            except Exception as e:
                st.error(f"Erro na análise de sensibilidade: {e}")
        
        # ============================================================
        # EXPORTAÇÃO
        # ============================================================
        st.markdown("---")
        st.markdown("### 📊 Exportação de Relatório")
        
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
        
        # Botão de download
        col1, col2 = st.columns([3, 1])
        
        with col2:
            botao_download_inteligente(
                relatorio_dados,
                f"📊 {get_text('export', lang)}",
                'excel',
                f'simulacao_rota_{origem}_{destino}'
            )
        
        with col1:
            st.info("💡 Clique no botão ao lado para baixar o relatório da simulação")
        
    except Exception as e:
        st.error(f"❌ Erro na simulação: {e}")
        st.info("💡 Verifique se todos os parâmetros estão configurados corretamente")
        
        # Debug para desenvolvimento
        if st.checkbox("🔍 Mostrar detalhes do erro (Debug)", key="debug_rota"):
            st.code(str(e))
            st.json({
                "origem": origem,
                "destino": destino,
                "modelo": modelo_rota,
                "rota_info": rota_info,
                "params_keys": list(params.keys()) if params else []
            })

# ========================================================================
# VISUALIZAÇÃO DE ROTAS DISPONÍVEIS
# ========================================================================
with st.expander("🗺️ Rotas Disponíveis"):
    if rotas_disponiveis:
        try:
            # Criar DataFrame para exibição
            df_display = pd.DataFrame(rotas_disponiveis)
            
            # Verificar e renomear colunas
            if all(col in df_display.columns for col in ['origem', 'destino', 'duracao_h']):
                df_display = df_display[['origem', 'destino', 'duracao_h']].copy()
                df_display.columns = ["Origem", "Destino", "Duração (h)"]
                
                # Formatar dados
                df_display['Origem'] = df_display['Origem'].str.upper()
                df_display['Destino'] = df_display['Destino'].str.upper()
                df_display['Duração (h)'] = df_display['Duração (h)'].round(1)
                
                st.dataframe(
                    df_display,
                    use_container_width=True,
                    hide_index=True
                )
                
                st.info(f"📊 Total de rotas disponíveis: {len(df_display)}")
                
            else:
                st.warning("⚠️ Estrutura de dados das rotas está incorreta")
                st.json(rotas_disponiveis[:3])  # Mostrar amostra
                
        except Exception as e:
            st.error(f"Erro ao exibir rotas: {e}")
    else:
        st.info("ℹ️ Nenhuma rota disponível")
    
    # Dicas
    if lang == 'pt':
        st.info("""
        💡 **Dicas**:
        - Rotas mais longas tendem a ter melhor economia relativa
        - Considere fatores sazonais na demanda
        - Configure novas rotas na página Configurações
        - Use códigos IATA padrão (GRU, SDU, CGH, BSB, etc.)
        """)
    else:
        st.info("""
        💡 **Tips**:
        - Longer routes tend to have better relative savings
        - Consider seasonal demand factors
        - Configure new routes in Settings page
        - Use standard IATA codes (GRU, SDU, CGH, BSB, etc.)
        """)

# ========================================================================
# FOOTER
# ========================================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6B7280; padding: 1rem;">
    <p>✈️ <strong>{get_text('page_simulator', lang)}</strong> - Análise detalhada por rota específica</p>
</div>
""", unsafe_allow_html=True)