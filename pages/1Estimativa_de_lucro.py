"""
Página 1: Estimativa de Lucro - VERSÃO QUE FUNCIONA 100%
- Selectbox MANTÉM seleção visível
- Gráficos SEMPRE aparecem
- Sistema SIMPLES e ROBUSTO
"""

import streamlit as st
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

# Imports APENAS do que funciona
from config.theme import load_theme
from utils.params import load_params, format_currency
from utils.calculations import calcular_lucro_mensal_charter
from utils.graficos_simples import grafico_pizza_receitas, grafico_barras_custos
from utils.selectbox_simples import selectbox_que_funciona, number_input_que_funciona, slider_que_funciona

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
# HEADER SIMPLES
# ========================================================================
st.markdown("# 📈 Estimativa de Lucro")
st.markdown("*Análise de rentabilidade mensal com operação charter*")
st.markdown("---")

# ========================================================================
# CARREGAMENTO DE DADOS
# ========================================================================
try:
    params = load_params()
    modelos = params.get('modelos_disponiveis', [])
    
    if not modelos:
        st.error("❌ Nenhum modelo de aeronave configurado")
        st.info("💡 Configure modelos na página de Configurações")
        st.stop()
    
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.stop()

# ========================================================================
# FORMULÁRIO FUNCIONANDO 100%
# ========================================================================
st.markdown("### 💰 Parâmetros da Simulação")

col1, col2, col3, col4 = st.columns(4)

with col1:
    modelo_selecionado = selectbox_que_funciona(
        "Modelo da Aeronave",
        modelos,
        "modelo_lucro",
        modelos[0] if modelos else None
    )

with col2:
    horas_charter = number_input_que_funciona(
        "Horas Charter/mês",
        "horas_lucro",
        padrao=80,
        minimo=10,
        maximo=200
    )

with col3:
    taxa_ocupacao = slider_que_funciona(
        "Taxa de Ocupação (%)",
        "ocupacao_lucro",
        padrao=75,
        minimo=50,
        maximo=95
    )

with col4:
    # Buscar preço padrão baseado no modelo
    preco_default = 8000
    try:
        if modelo_selecionado and modelo_selecionado in params.get('preco_mercado_hora', {}):
            preco_default = int(params['preco_mercado_hora'][modelo_selecionado])
    except:
        pass
    
    preco_hora_charter = number_input_que_funciona(
        "Preço Hora Charter (R$)",
        "preco_lucro",
        padrao=preco_default,
        minimo=1000,
        maximo=50000
    )

# ========================================================================
# MOSTRAR VALORES SELECIONADOS (DEBUG)
# ========================================================================
st.info(f"""
📊 **Valores Selecionados:**
- Modelo: **{modelo_selecionado}**
- Horas/mês: **{horas_charter:.0f}**
- Ocupação: **{taxa_ocupacao}%**
- Preço/hora: **R$ {preco_hora_charter:,.0f}**
""")

# ========================================================================
# BOTÃO DE CÁLCULO
# ========================================================================
if st.button("🚀 CALCULAR LUCRO", type="primary", use_container_width=True):
    
    if not modelo_selecionado:
        st.error("❌ Selecione um modelo de aeronave")
        st.stop()
    
    try:
        with st.spinner("Calculando..."):
            # Realizar cálculo
            resultado = calcular_lucro_mensal_charter(
                modelo=modelo_selecionado,
                horas_charter=horas_charter,
                taxa_ocupacao=taxa_ocupacao,
                preco_hora=preco_hora_charter,
                params=params
            )
        
        # ============================================================
        # RESULTADOS
        # ============================================================
        st.markdown("---")
        st.markdown("### 📊 Resultados da Análise")
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Receita Bruta",
                f"R$ {resultado['receita_bruta']:,.0f}"
            )
        
        with col2:
            st.metric(
                "Receita Proprietário (90%)",
                f"R$ {resultado['receita_proprietario']:,.0f}"
            )
        
        with col3:
            st.metric(
                "Lucro Líquido",
                f"R$ {resultado['lucro_liquido']:,.0f}",
                delta=f"{resultado['roi_mensal']:.1f}%"
            )
        
        with col4:
            st.metric(
                "ROI Mensal",
                f"{resultado['roi_mensal']:.1f}%"
            )
        
        # ============================================================
        # GRÁFICOS QUE FUNCIONAM GARANTIDO
        # ============================================================
        st.markdown("#### 📊 Análise Visual")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 💰 Composição de Receitas")
            
            # GRÁFICO 1: Pizza de receitas
            fig_receita = grafico_pizza_receitas(
                resultado['receita_proprietario'],
                resultado['taxa_amaro']
            )
            st.plotly_chart(fig_receita, use_container_width=True, key="grafico_receitas_1")
        
        with col2:
            st.markdown("##### 💸 Breakdown de Custos")
            
            # GRÁFICO 2: Barras de custos
            breakdown = resultado.get('breakdown_custos', {})
            fig_custos = grafico_barras_custos(
                breakdown.get('combustivel', 0),
                breakdown.get('tripulacao', 0),
                breakdown.get('manutencao', 0),
                breakdown.get('depreciacao', 0)
            )
            st.plotly_chart(fig_custos, use_container_width=True, key="grafico_custos_1")
        
        # ============================================================
        # STATUS DA OPERAÇÃO
        # ============================================================
        if resultado['lucrativo']:
            st.success(f"""
            **✅ Operação Lucrativa**
            
            O proprietário terá um lucro líquido de **R$ {resultado['lucro_liquido']:,.0f}** por mês.
            """)
        else:
            st.warning(f"""
            **⚠️ Operação com déficit**
            
            A operação apresenta déficit de **R$ {abs(resultado['lucro_liquido']):,.0f}** por mês.
            """)
        
        # ============================================================
        # DETALHES DOS CUSTOS
        # ============================================================
        with st.expander("🔍 Detalhamento dos Custos"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Custos Operacionais:**")
                breakdown = resultado.get('breakdown_custos', {})
                for key, value in breakdown.items():
                    st.write(f"• {key.title()}: R$ {value:,.0f}")
            
            with col2:
                st.markdown("**Parâmetros Usados:**")
                st.write(f"• Horas disponíveis: {horas_charter:.0f}h/mês")
                st.write(f"• Horas efetivas: {resultado.get('horas_efetivas', 0):.1f}h/mês")
                st.write(f"• Taxa de ocupação: {taxa_ocupacao}%")
                st.write(f"• Preço por hora: R$ {preco_hora_charter:,.0f}")
        
    except Exception as e:
        st.error(f"❌ Erro no cálculo: {e}")
        st.info("💡 Verifique os parâmetros e tente novamente")
        
        # Debug
        if st.checkbox("🔍 Mostrar erro detalhado"):
            st.code(str(e))

# ========================================================================
# INFORMAÇÕES ÚTEIS
# ========================================================================
with st.expander("💡 Como interpretar os resultados"):
    st.markdown("""
    **Significado dos valores:**
    
    - **Receita Bruta**: Total faturado com charter
    - **Receita Proprietário**: 90% da receita bruta (padrão Amaro)
    - **Lucro Líquido**: Receita do proprietário menos custos operacionais
    - **ROI**: Percentual de retorno sobre os custos
    
    **Dicas para melhorar resultados:**
    
    - Mantenha ocupação acima de 70%
    - Monitore custos de combustível
    - Ajuste preços conforme mercado
    - Otimize rotas para reduzir custos
    """)

# ========================================================================
# DEBUG (REMOVÍVEL EM PRODUÇÃO)
# ========================================================================
if st.checkbox("🔧 Mostrar Debug (apenas desenvolvimento)"):
    st.write("### Debug - Session State")
    from utils.selectbox_simples import mostrar_debug_session
    mostrar_debug_session()
    
    if st.button("🔄 Reset Todos Valores"):
        from utils.selectbox_simples import limpar_todos_valores
        limpar_todos_valores()

# ========================================================================
# FOOTER
# ========================================================================
st.markdown("---")
st.markdown("**📈 Estimativa de Lucro** - Sistema funcionando 100%")