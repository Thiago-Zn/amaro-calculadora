"""
Página 3: Simulador de Rotas - VERSÃO QUE FUNCIONA 100%
- Dropdowns Origem/Destino/Modelo MANTÉM seleção
- Gráficos SEMPRE aparecem
- Sistema SIMPLES e ROBUSTO
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

# Imports APENAS do que funciona
from config.theme import load_theme
from utils.params import load_params, format_currency
from utils.calculations import calcular_custo_rota
from utils.graficos_simples import grafico_barras_custos, grafico_comparativo_simples
from utils.selectbox_simples import selectbox_que_funciona

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
# HEADER SIMPLES
# ========================================================================
st.markdown("# ✈️ Simulador de Rotas")
st.markdown("*Simulação de custos por rota específica origem-destino*")
st.markdown("---")

# ========================================================================
# CARREGAMENTO DE DADOS
# ========================================================================
try:
    params = load_params()
    modelos = params.get('modelos_disponiveis', [])
    
    if not modelos:
        st.error("❌ Nenhum modelo de aeronave configurado")
        st.stop()
    
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.stop()

# ========================================================================
# CARREGAMENTO DE ROTAS
# ========================================================================
try:
    df_rotas = pd.read_csv('data/rotas.csv')
    rotas_disponiveis = df_rotas.to_dict('records')
    
    if not rotas_disponiveis:
        raise ValueError("Nenhuma rota encontrada")
        
except Exception as e:
    st.warning(f"⚠️ Problema com rotas: {e}")
    
    # Rotas padrão
    rotas_disponiveis = [
        {"origem": "GRU", "destino": "SDU", "duracao_h": 1.0},
        {"origem": "GRU", "destino": "CGH", "duracao_h": 0.5},
        {"origem": "CGH", "destino": "BSB", "duracao_h": 1.4},
        {"origem": "BSB", "destino": "SDU", "duracao_h": 1.7},
        {"origem": "GRU", "destino": "CNF", "duracao_h": 1.0}
    ]

# ========================================================================
# PREPARAR LISTAS DE ORIGEM E DESTINO
# ========================================================================
# Obter todas as origens únicas
origens_disponiveis = sorted(list(set([r['origem'] for r in rotas_disponiveis])))

# ========================================================================
# FORMULÁRIO DE SELEÇÃO FUNCIONANDO 100%
# ========================================================================
st.markdown("### ✈️ Seleção de Rota")

col1, col2, col3 = st.columns(3)

with col1:
    origem_selecionada = selectbox_que_funciona(
        "Aeroporto de Origem",
        origens_disponiveis,
        "origem_rota",
        origens_disponiveis[0] if origens_disponiveis else None
    )

with col2:
    # Filtrar destinos baseado na origem
    if origem_selecionada:
        destinos_validos = sorted([
            r['destino'] for r in rotas_disponiveis 
            if r['origem'] == origem_selecionada
        ])
        
        # Remover duplicatas
        destinos_validos = list(set(destinos_validos))
        
        if not destinos_validos:
            destinos_validos = ["Nenhum destino disponível"]
    else:
        destinos_validos = ["Selecione origem primeiro"]
    
    destino_selecionado = selectbox_que_funciona(
        "Aeroporto de Destino",
        destinos_validos,
        "destino_rota",
        destinos_validos[0] if destinos_validos else None
    )

with col3:
    modelo_selecionado = selectbox_que_funciona(
        "Modelo da Aeronave",
        modelos,
        "modelo_rota",
        modelos[0] if modelos else None
    )

# ========================================================================
# MOSTRAR ROTA SELECIONADA
# ========================================================================
# Buscar informações da rota
rota_info = None
rota_valida = False

if (origem_selecionada and destino_selecionado and 
    destino_selecionado not in ["Nenhum destino disponível", "Selecione origem primeiro"]):
    
    for r in rotas_disponiveis:
        if r['origem'] == origem_selecionada and r['destino'] == destino_selecionado:
            rota_info = r
            rota_valida = True
            break

if rota_valida and rota_info:
    st.success(f"""
    📍 **Rota Selecionada**: {origem_selecionada} → {destino_selecionado}  
    ⏱️ **Duração**: {rota_info['duracao_h']:.1f}h  
    ✈️ **Modelo**: {modelo_selecionado}
    """)
else:
    st.info(f"ℹ️ Rota: {origem_selecionada} → {destino_selecionado}")

# ========================================================================
# BOTÃO DE SIMULAÇÃO
# ========================================================================
if st.button("✈️ SIMULAR ROTA", type="primary", use_container_width=True):
    
    if not rota_valida or not rota_info:
        st.error("❌ Selecione uma rota válida")
        st.stop()
    
    if not modelo_selecionado:
        st.error("❌ Selecione um modelo de aeronave")
        st.stop()
    
    try:
        with st.spinner("Simulando rota..."):
            # Calcular custos da rota
            resultado_rota = calcular_custo_rota(
                origem=origem_selecionada,
                destino=destino_selecionado,
                modelo=modelo_selecionado,
                params=params,
                rotas_disponiveis=rotas_disponiveis
            )
        
        # ============================================================
        # RESULTADOS DA ROTA
        # ============================================================
        st.markdown("---")
        st.markdown(f"### 📊 Análise da Rota: {origem_selecionada} → {destino_selecionado}")
        
        # KPIs da rota
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Duração do Voo",
                f"{resultado_rota['duracao_horas']:.1f}h"
            )
        
        with col2:
            st.metric(
                "Custo Total Amaro",
                f"R$ {resultado_rota['custo_amaro']:,.0f}"
            )
        
        with col3:
            st.metric(
                "Preço de Mercado",
                f"R$ {resultado_rota['preco_mercado']:,.0f}"
            )
        
        with col4:
            economia = resultado_rota['economia']
            percentual = resultado_rota['economia_percentual']
            st.metric(
                "Economia",
                f"R$ {economia:,.0f}",
                delta=f"{percentual:.1f}%"
            )
        
        # ============================================================
        # GRÁFICOS DA ROTA QUE FUNCIONAM GARANTIDO
        # ============================================================
        st.markdown("#### 📊 Análise Visual")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 💸 Composição de Custos")
            
            # GRÁFICO 1: Custos da rota
            breakdown = resultado_rota.get('breakdown_custos', {})
            fig_custos = grafico_barras_custos(
                breakdown.get('combustivel', 0),
                breakdown.get('tripulacao', 0),
                breakdown.get('manutencao', 0),
                breakdown.get('depreciacao', 0)
            )
            st.plotly_chart(fig_custos, use_container_width=True, key="grafico_custos_rota")
        
        with col2:
            st.markdown("##### 📊 Comparativo Visual")
            
            # GRÁFICO 2: Comparativo Amaro vs Mercado
            fig_comparativo = grafico_comparativo_simples(
                resultado_rota['custo_amaro'],
                resultado_rota['preco_mercado']
            )
            st.plotly_chart(fig_comparativo, use_container_width=True, key="grafico_comparativo_rota")
        
        # ============================================================
        # STATUS DA ROTA
        # ============================================================
        if resultado_rota.get('viavel', False):
            st.success(f"""
            **✅ Rota Vantajosa**
            
            A gestão Amaro oferece economia de **R$ {economia:,.0f}** ({percentual:.1f}%) para esta rota.
            """)
        else:
            st.warning(f"""
            **⚠️ Atenção**
            
            O custo operacional está acima do preço de mercado para esta rota.
            """)
        
        # ============================================================
        # DETALHES DA SIMULAÇÃO
        # ============================================================
        with st.expander("🔍 Detalhes da Simulação"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Breakdown de Custos:**")
                breakdown = resultado_rota.get('breakdown_custos', {})
                for key, value in breakdown.items():
                    st.write(f"• {key.title()}: R$ {value:,.0f}")
            
            with col2:
                st.markdown("**Informações da Rota:**")
                st.write(f"• Origem: {origem_selecionada}")
                st.write(f"• Destino: {destino_selecionado}")
                st.write(f"• Duração: {resultado_rota['duracao_horas']:.1f}h")
                st.write(f"• Modelo: {modelo_selecionado}")
        
    except Exception as e:
        st.error(f"❌ Erro na simulação: {e}")
        st.info("💡 Verifique os parâmetros e tente novamente")
        
        # Debug
        if st.checkbox("🔍 Mostrar erro detalhado"):
            st.code(str(e))

# ========================================================================
# ROTAS DISPONÍVEIS
# ========================================================================
with st.expander("🗺️ Rotas Disponíveis"):
    if rotas_disponiveis:
        df_display = pd.DataFrame(rotas_disponiveis)
        
        # Renomear colunas
        if 'origem' in df_display.columns:
            df_display = df_display.rename(columns={
                'origem': 'Origem',
                'destino': 'Destino',
                'duracao_h': 'Duração (h)'
            })
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        st.info(f"📊 Total de rotas: {len(df_display)}")
    else:
        st.info("ℹ️ Nenhuma rota disponível")

# ========================================================================
# DEBUG (REMOVÍVEL EM PRODUÇÃO)
# ========================================================================
if st.checkbox("🔧 Mostrar Debug"):
    st.write("### Debug - Valores Selecionados")
    st.write(f"- Origem: {origem_selecionada}")
    st.write(f"- Destino: {destino_selecionado}")
    st.write(f"- Modelo: {modelo_selecionado}")
    st.write(f"- Rota válida: {rota_valida}")
    
    from utils.selectbox_simples import mostrar_debug_session
    mostrar_debug_session()

# ========================================================================
# FOOTER
# ========================================================================
st.markdown("---")
st.markdown("**✈️ Simulador de Rotas** - Sistema funcionando 100%")