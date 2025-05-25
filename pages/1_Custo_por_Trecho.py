import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from utils.params import load_params
from utils.calculations import calcula_custo_trecho
from utils.charts import grafico_composicao, grafico_comparativo
from utils.exportador_excel import gerar_excel
from utils.exportador_pdf import gerar_pdf
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="Custo por Trecho - Amaro Aviation", 
    layout="wide",
    page_icon="✈️"
)

# CSS Premium específico para esta página
st.markdown("""
<style>
.metric-premium {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 15px;
    padding: 1.5rem;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    border-left: 5px solid #8c1d40;
    margin: 1rem 0;
}

.calculation-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border: 1px solid #e9ecef;
    margin: 1rem 0;
}

.result-highlight {
    background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    margin: 1rem 0;
}

.export-section {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 1rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header da página
st.markdown("""
<div class="result-highlight">
    <h1 style="margin: 0;">✈️ Análise de Custo por Trecho</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Cálculo detalhado para rotas específicas</p>
</div>
""", unsafe_allow_html=True)

# Carregamento de dados com tratamento de erro
try:
    params = load_params()
    modelos = params.get('modelos_disponiveis', [])
    
    # Carregamento de rotas com fallback
    rotas_file = Path("data/rotas.csv")
    if rotas_file.exists():
        rotas_df = pd.read_csv(rotas_file)
    else:
        # Rotas padrão se arquivo não existir
        rotas_df = pd.DataFrame([
            {"origem": "GRU", "destino": "SDU", "duracao_h": 1.0},
            {"origem": "GRU", "destino": "CGH", "duracao_h": 0.5},
            {"origem": "CGH", "destino": "BSB", "duracao_h": 1.4},
            {"origem": "BSB", "destino": "SDU", "duracao_h": 1.7}
        ])
        st.info("📋 Usando rotas padrão. Adicione 'data/rotas.csv' para rotas personalizadas.")

except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.stop()

# Interface de entrada elegante
st.markdown("## 🎯 Configuração do Voo")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="calculation-card">
        <h4>🛩️ Seleção da Aeronave</h4>
    """, unsafe_allow_html=True)
    
    modelo = st.selectbox(
        "Modelo da Aeronave",
        modelos,
        help="Selecione o modelo para análise de custos"
    )
    
    # Informações do modelo selecionado
    if modelo in params['consumo_modelos']:
        consumo = params['consumo_modelos'][modelo]
        tipo_aeronave = "Jato" if params['preco_mercado_hora'][modelo] > 10000 else "Turboprop"
        
        st.info(f"""
        **{modelo}**
        - Tipo: {tipo_aeronave}
        - Consumo: {consumo} L/h
        - Preço mercado: R$ {params['preco_mercado_hora'][modelo]:,.0f}/h
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="calculation-card">
        <h4>🗺️ Definição da Rota</h4>
    """, unsafe_allow_html=True)
    
    # Seleção de rota
    rota_opcoes = [f"{row['origem']} → {row['destino']} ({row['duracao_h']}h)" 
                   for _, row in rotas_df.iterrows()]
    
    rota_selecionada = st.selectbox(
        "Rota Pré-definida",
        rota_opcoes,
        help="Selecione uma rota ou configure manualmente abaixo"
    )
    
    # Opção manual
    usar_manual = st.checkbox("✏️ Configuração Manual", help="Ative para inserir rota personalizada")
    
    if usar_manual:
        col_orig, col_dest, col_dur = st.columns(3)
        with col_orig:
            origem = st.text_input("Origem", value="GRU", placeholder="Ex: GRU")
        with col_dest:
            destino = st.text_input("Destino", value="SDU", placeholder="Ex: SDU")
        with col_dur:
            duracao = st.number_input("Duração (h)", min_value=0.1, max_value=20.0, 
                                    value=1.0, step=0.1, help="Duração do voo em horas")
    else:
        # Extrair dados da rota selecionada
        idx = rota_opcoes.index(rota_selecionada)
        row = rotas_df.iloc[idx]
        origem, destino, duracao = row['origem'], row['destino'], row['duracao_h']
        
        st.write(f"**Origem:** {origem}")
        st.write(f"**Destino:** {destino}")
        st.write(f"**Duração:** {duracao}h")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Botão de cálculo premium
st.markdown("---")
if st.button("🚀 Calcular Custos", type="primary", use_container_width=True):
    try:
        # Realizar cálculos
        resultado = calcula_custo_trecho(modelo, duracao, params)
        
        # Exibição dos resultados principais
        st.markdown("## 💰 Resultados da Análise")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💸 Custo Total",
                f"R$ {resultado['total']:,.2f}",
                help="Custo total da operação Amaro Aviation"
            )
        
        with col2:
            st.metric(
                "🏪 Preço Mercado",
                f"R$ {resultado['preco_mercado']:,.2f}",
                help="Preço cobrado no mercado para esta rota"
            )
        
        with col3:
            st.metric(
                "💎 Economia",
                f"R$ {resultado['economia']:,.2f}",
                delta=f"{resultado['percentual_economia']:.1f}%",
                help="Economia comparado ao mercado"
            )
        
        with col4:
            margem = (resultado['economia'] / resultado['preco_mercado'] * 100) if resultado['preco_mercado'] > 0 else 0
            st.metric(
                "📊 Margem",
                f"{margem:.1f}%",
                help="Margem de economia percentual"
            )
        
        # Breakdown detalhado dos custos
        st.markdown("---")
        st.markdown("## 📋 Breakdown de Custos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de composição
            fig_composicao = grafico_composicao({
                "Combustível": resultado['preco_comb'],
                "Piloto": resultado['piloto'],
                "Manutenção": resultado['manut'],
                "Depreciação": resultado['depr']
            })
            fig_composicao.update_layout(
                title="🥧 Composição dos Custos",
                height=400
            )
            st.plotly_chart(fig_composicao, use_container_width=True)
        
        with col2:
            # Gráfico comparativo
            fig_comparativo = grafico_comparativo(resultado['total'], resultado['preco_mercado'])
            fig_comparativo.update_layout(
                title="⚖️ Amaro vs. Mercado",
                height=400
            )
            st.plotly_chart(fig_comparativo, use_container_width=True)
        
        # Tabela detalhada
        st.markdown("### 📊 Detalhamento Completo")
        
        detalhes_df = pd.DataFrame([
            {"Componente": "🛢️ Combustível", "Valor": resultado['preco_comb'], "Descrição": f"{params['consumo_modelos'][modelo]} L/h × R$ {params['preco_combustivel']:.2f}/L"},
            {"Componente": "👨‍✈️ Piloto", "Valor": resultado['piloto'], "Descrição": f"R$ {params['custo_piloto_hora_modelo'][modelo]:,.0f}/h × {duracao}h"},
            {"Componente": "🔧 Manutenção", "Valor": resultado['manut'], "Descrição": f"R$ {params['custo_manutencao'][modelo]:,.0f}/h × {duracao}h"},
            {"Componente": "📉 Depreciação", "Valor": resultado['depr'], "Descrição": f"R$ {params['depreciacao_hora'][modelo]:,.0f}/h × {duracao}h"},
            {"Componente": "💰 **TOTAL AMARO**", "Valor": resultado['total'], "Descrição": "Soma de todos os custos"},
            {"Componente": "🏪 **PREÇO MERCADO**", "Valor": resultado['preco_mercado'], "Descrição": f"R$ {params['preco_mercado_hora'][modelo]:,.0f}/h × {duracao}h"},
            {"Componente": "💎 **ECONOMIA**", "Valor": resultado['economia'], "Descrição": f"Economia de {resultado['percentual_economia']:.1f}%"}
        ])
        
        st.dataframe(
            detalhes_df.style.format({"Valor": "R$ {:,.2f}"}).apply(
                lambda x: ['font-weight: bold' if '**' in str(x.name) else '' for i in x], axis=1
            ),
            use_container_width=True,
            hide_index=True
        )
        
        # Seção de exportação premium
        st.markdown("---")
        st.markdown("""
        <div class="export-section">
            <h3>📤 Exportar Relatórios</h3>
            <p>Baixe os resultados em formatos profissionais para apresentações e arquivo.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        # Preparar dados para exportação
        dados_exportacao = {
            "Análise": "Custo por Trecho",
            "Modelo": modelo,
            "Rota": f"{origem} → {destino}",
            "Duração": f"{duracao} horas",
            "Combustível": resultado['preco_comb'],
            "Piloto": resultado['piloto'],
            "Manutenção": resultado['manut'],
            "Depreciação": resultado['depr'],
            "Custo Total Amaro": resultado['total'],
            "Preço Mercado": resultado['preco_mercado'],
            "Economia": resultado['economia'],
            "Percentual Economia": f"{resultado['percentual_economia']:.1f}%"
        }
        
        with col1:
            # Exportação Excel
            try:
                excel_buffer = BytesIO()
                gerar_excel(excel_buffer, dados_exportacao)
                excel_buffer.seek(0)
                
                st.download_button(
                    "📊 Baixar Relatório Excel",
                    data=excel_buffer.getvalue(),
                    file_name=f"amaro_custo_trecho_{origem}_{destino}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Erro ao gerar Excel: {e}")
        
        with col2:
            # Exportação PDF
            try:
                pdf_buffer = BytesIO()
                gerar_pdf(pdf_buffer, dados_exportacao)
                pdf_buffer.seek(0)
                
                st.download_button(
                    "📄 Baixar Relatório PDF",
                    data=pdf_buffer.getvalue(),
                    file_name=f"amaro_custo_trecho_{origem}_{destino}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")
        
        # Insights e recomendações
        st.markdown("---")
        st.markdown("## 💡 Insights & Recomendações")
        
        if resultado['economia'] > 0:
            economia_anual = resultado['economia'] * 200  # Estimativa 200 voos/ano
            st.success(f"""
            ✅ **Economia Significativa Identificada**
            - Economia por voo: R$ {resultado['economia']:,.2f}
            - Potencial economia anual (200 voos): R$ {economia_anual:,.2f}
            - Percentual de economia: {resultado['percentual_economia']:.1f}%
            """)
        else:
            st.warning(f"""
            ⚠️ **Atenção: Custo Acima do Mercado**
            - Diferença: R$ {abs(resultado['economia']):,.2f}
            - Recomenda-se revisar parâmetros operacionais
            """)
            
    except Exception as e:
        st.error(f"❌ Erro no cálculo: {e}")
        st.info("🔧 Verifique os parâmetros e dados de entrada.")

# Informações adicionais na sidebar
with st.sidebar:
    st.markdown("""
    ### 📘 Como Usar
    
    1. **Selecione o modelo** da aeronave
    2. **Escolha a rota** ou configure manualmente
    3. **Clique em Calcular** para ver resultados
    4. **Exporte relatórios** em Excel ou PDF
    
    ### 🎯 Funcionalidades
    - Cálculo detalhado por componente
    - Comparação com preços de mercado
    - Gráficos interativos
    - Exportação profissional
    - Insights automáticos
    """)
    
    if 'resultado' in locals():
        st.markdown(f"""
        ### 📊 Resumo Rápido
        - **Economia:** R$ {resultado['economia']:,.0f}
        - **Margem:** {resultado['percentual_economia']:.1f}%
        - **Eficiência:** {"🟢 Excelente" if resultado['percentual_economia'] > 20 else "🟡 Boa" if resultado['percentual_economia'] > 10 else "🔴 Revisar"}
        """)