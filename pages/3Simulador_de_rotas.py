"""
Página 3: Simulador de Rotas - VERSÃO FINAL CORRIGIDA
Com selectbox persistente e gráficos funcionais
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from config.theme import load_theme
from config.idiomas import get_text
from components.sidebar import render_sidebar
from components.status import render_system_status, render_status_box
from utils.params import load_params, format_currency
from utils.calculations import calcular_custo_rota
from utils.export_manager import botao_download_inteligente, criar_relatorio_dados
from utils.session_state import persistent_selectbox
from utils.charts_fixed import render_chart_custos, render_chart_comparativo

# Configuração da página
st.set_page_config(
    page_title="Simulador de Rotas | Amaro Aviation",
    page_icon="✈️",
    layout="wide"
)

# Carregamento do tema
load_theme()

# Sidebar e idioma
lang = render_sidebar()

# Header da página
st.markdown("# ✈️ Simulador de Rotas")
st.markdown("*Simulação de custos por rota específica origem-destino*")
st.markdown("---")

# Carregar parâmetros
try:
    params = load_params()
    system_ok = render_system_status(params, lang)
    
    if not system_ok:
        st.error("❌ Sistema não configurado adequadamente")
        st.info("💡 Configure o sistema na página de Configurações")
        st.stop()
    
    modelos = params.get('modelos_disponiveis', [])
    
    if not modelos:
        st.error("❌ Nenhum modelo de aeronave configurado")
        st.stop()
    
except Exception as e:
    st.error(f"❌ Erro ao carregar sistema: {e}")
    st.stop()

# Carregar rotas disponíveis
try:
    df_rotas = pd.read_csv('data/rotas.csv')
    rotas_disponiveis = df_rotas.to_dict('records')
    
    if not rotas_disponiveis:
        st.warning("⚠️ Nenhuma rota encontrada no arquivo")
        rotas_disponiveis = []
        
except Exception as e:
    st.warning(f"⚠️ Arquivo de rotas não encontrado: {e}")
    rotas_disponiveis = [
        {"origem": "GRU", "destino": "SDU", "duracao_h": 1.0},
        {"origem": "CGH", "destino": "BSB", "duracao_h": 1.4},
        {"origem": "BSB", "destino": "SDU", "duracao_h": 1.7},
        {"origem": "GRU", "destino": "CNF", "duracao_h": 1.0}
    ]

# Interface principal
st.markdown("### ✈️ Simulador de Rotas")

# Verificar se há rotas disponíveis
if not rotas_disponiveis:
    st.error("❌ Nenhuma rota disponível para simulação")
    st.info("💡 Configure rotas na página de Configurações")
    st.stop()

# Formulário de seleção de rota com persistência
col1, col2, col3 = st.columns(3)

with col1:
    # Buscar origens únicas
    try:
        origens_disponiveis = sorted(list(set([r['origem'] for r in rotas_disponiveis if 'origem' in r])))
        
        if not origens_disponiveis:
            st.error("❌ Nenhuma origem válida encontrada")
            st.stop()
            
        # Selectbox persistente para origem
        origem = persistent_selectbox(
            "Aeroporto de Origem",
            options=origens_disponiveis,
            key="origem_rota_persist"
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
            
        # Selectbox persistente para destino
        destino = persistent_selectbox(
            "Aeroporto de Destino",
            options=destinos_validos,
            key="destino_rota_persist"
        )
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar destinos: {e}")
        st.stop()

with col3:
    # Selectbox persistente para modelo
    modelo_rota = persistent_selectbox(
        "Modelo da Aeronave",
        options=modelos,
        key="modelo_rota_persist"
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
if st.button("✈️ Simular Rota", type="primary", use_container_width=True):
    
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
        st.markdown(f"### 📊 Análise da Rota: {origem} → {destino}")
        
        # KPIs da rota usando métricas nativas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Duração do Voo",
                f"{resultado_rota['duracao_horas']:.1f}h"
            )
        
        with col2:
            st.metric(
                "Custo Total Amaro",
                format_currency(resultado_rota['custo_amaro'], lang)
            )
        
        with col3:
            st.metric(
                "Preço de Mercado",
                format_currency(resultado_rota['preco_mercado'], lang)
            )
        
        with col4:
            delta_value = f"+{resultado_rota['economia_percentual']:.1f}%" if resultado_rota['economia'] > 0 else f"{resultado_rota['economia_percentual']:.1f}%"
            st.metric(
                "Economia",
                format_currency(resultado_rota['economia'], lang),
                delta=delta_value
            )
        
        # Análise visual da rota
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💸 Composição de Custos")
            
            # Preparar dados dos custos para o gráfico
            custos_dict = {
                'combustivel': resultado_rota['breakdown_custos']['combustivel'],
                'tripulacao': resultado_rota['breakdown_custos']['tripulacao'],
                'manutencao': resultado_rota['breakdown_custos']['manutencao'],
                'depreciacao': resultado_rota['breakdown_custos']['depreciacao']
            }
            
            # Renderizar gráfico de custos
            fig_custos = render_chart_custos(custos_dict, lang)
            st.plotly_chart(fig_custos, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Comparativo Visual")
            
            # Renderizar gráfico comparativo
            fig_comparativo = render_chart_comparativo(
                resultado_rota['custo_amaro'], 
                resultado_rota['preco_mercado'], 
                lang
            )
            st.plotly_chart(fig_comparativo, use_container_width=True)
        
        # Status da análise
        if resultado_rota['viavel']:
            render_status_box(
                'success',
                'Rota Vantajosa',
                f"A gestão Amaro oferece economia de {format_currency(resultado_rota['economia'], lang)} ({resultado_rota['economia_percentual']:.1f}%) em relação ao preço de mercado para esta rota."
            )
        else:
            render_status_box(
                'warning',
                'Atenção',
                f"O custo operacional está acima do preço de mercado. Considere otimizações operacionais para esta rota."
            )
        
        # Análise de sensibilidade
        with st.expander("📈 Análise de Sensibilidade"):
            st.markdown("**Impacto de variações nos custos:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                variacao_combustivel = st.slider(
                    "Variação Preço Combustível (%)",
                    -20, 20, 0, 5,
                    key="var_combustivel"
                )
            
            with col2:
                variacao_manutencao = st.slider(
                    "Variação Custo Manutenção (%)",
                    -20, 20, 0, 5,
                    key="var_manutencao"
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
                    "Custo Total Ajustado",
                    format_currency(custo_total_ajustado, lang),
                    f"{custo_total_ajustado - resultado_rota['custo_amaro']:+.0f}"
                )
            
            with col2:
                st.metric(
                    "Economia Ajustada",
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
                "📊 Exportar",
                'excel',
                f'simulacao_rota_{origem}_{destino}'
            )
        
    except Exception as e:
        st.error(f"❌ Erro na simulação: {e}")
        st.info("💡 Verifique se todos os parâmetros estão configurados corretamente")

# Visualização de rotas disponíveis
with st.expander("🗺️ Rotas Disponíveis"):
    if rotas_disponiveis:
        df_rotas_display = pd.DataFrame(rotas_disponiveis)
        
        # Verificar se as colunas existem
        if all(col in df_rotas_display.columns for col in ['origem', 'destino', 'duracao_h']):
            df_rotas_display.columns = ["Origem", "Destino", "Duração (h)"]
            
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
    
    st.info("""
    💡 **Dicas**:
    - Rotas mais longas tendem a ter melhor economia relativa
    - Considere fatores sazonais na demanda
    - Configure novas rotas na página Configurações
    """)

# Footer da página
st.markdown("---")
st.markdown("**✈️ Simulador de Rotas** - Análise detalhada por rota específica")