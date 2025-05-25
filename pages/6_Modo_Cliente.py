import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.params import load_params
from utils.calculations import calcula_custo_trecho
from utils.charts import grafico_comparativo
from utils.exportador_pdf import gerar_pdf
from io import BytesIO
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Modo Apresentação - Amaro Aviation", 
    layout="wide",
    page_icon="🎨"
)

# CSS para modo apresentação
st.markdown("""
<style>
.presentation-header {
    background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%);
    color: white;
    padding: 3rem 2rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(140, 29, 64, 0.3);
}

.presentation-card {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.1);
    margin: 1.5rem 0;
}

.savings-highlight {
    background: linear-gradient(135deg, #27AE60 0%, #2ECC71 100%);
    color: white;
    padding: 2.5rem;
    border-radius: 15px;
    text-align: center;
    margin: 2rem 0;
    box-shadow: 0 8px 25px rgba(39, 174, 96, 0.3);
}

.metric-presentation {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    border-left: 5px solid #8c1d40;
    margin: 1rem 0;
    text-align: center;
}

.value-prop-box {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 2rem;
    margin: 1rem 0;
    border: 2px solid #8c1d40;
}

.simple-form {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 6px 25px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

/* Esconder elementos desnecessários no modo apresentação */
.css-1y4p8pa {
    padding-top: 1rem;
}

/* Fontes maiores para apresentação */
.big-number {
    font-size: 3rem;
    font-weight: bold;
    color: #8c1d40;
}
</style>
""", unsafe_allow_html=True)

# Header de apresentação
st.markdown("""
<div class="presentation-header">
    <h1 style="margin: 0; font-size: 3.5rem;">✈️ Amaro Aviation</h1>
    <h2 style="margin: 1rem 0; font-size: 2rem; font-weight: 300;">Análise de Economia em Aviação Executiva</h2>
</div>
""", unsafe_allow_html=True)

# Carregamento de parâmetros
try:
    params = load_params()
    modelos = params.get('modelos_disponiveis', [])
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# Configuração simplificada
st.markdown("## 🎯 Simulação de Economia")

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
    <div class="simple-form">
        <h3>📋 Parâmetros da Simulação</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        modelo = st.selectbox(
            "🛩️ Modelo da Aeronave",
            modelos,
            help="Selecione o modelo para análise"
        )
    
    with col_b:
        # Rotas simplificadas
        rotas_exemplo = {
            "São Paulo → Rio": 1.0,
            "São Paulo → Brasília": 1.4,
            "Rio → Brasília": 1.7,
            "São Paulo → Belo Horizonte": 1.0,
            "Personalizada": 0
        }
        
        rota = st.selectbox("🗺️ Rota", list(rotas_exemplo.keys()))
        
        if rota == "Personalizada":
            duracao = st.number_input("Duração (h)", 0.5, 10.0, 1.5, 0.5)
        else:
            duracao = rotas_exemplo[rota]
    
    with col_c:
        frequencia = st.selectbox(
            "📅 Frequência",
            ["4 voos/mês", "8 voos/mês", "12 voos/mês", "20 voos/mês"],
            index=1
        )
        voos_mes = int(frequencia.split()[0])

with col2:
    if modelo in params['consumo_modelos']:
        st.markdown("""
        <div class="presentation-card">
            <h4>✈️ {}</h4>
            <p><strong>Tipo:</strong> {}</p>
            <p><strong>Consumo:</strong> {} L/h</p>
        </div>
        """.format(
            modelo,
            "Jato" if params['preco_mercado_hora'][modelo] > 10000 else "Turboprop",
            params['consumo_modelos'][modelo]
        ), unsafe_allow_html=True)

# Botão de cálculo grande
st.markdown("<br>", unsafe_allow_html=True)
calcular = st.button("🚀 CALCULAR ECONOMIA", type="primary", use_container_width=True, 
                    help="Clique para ver a análise completa")

if calcular:
    # Cálculos
    resultado = calcula_custo_trecho(modelo, duracao, params)
    
    # Valores
    economia_voo = resultado['economia']
    economia_mensal = economia_voo * voos_mes
    economia_anual = economia_mensal * 12
    
    # Exibição destacada da economia
    if economia_voo > 0:
        st.markdown(f"""
        <div class="savings-highlight">
            <h2 style="margin: 0; font-size: 2.5rem;">💎 ECONOMIA COM AMARO AVIATION</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 2rem; margin-top: 2rem;">
                <div>
                    <h3 style="margin: 0; opacity: 0.8;">Por Voo</h3>
                    <div class="big-number" style="color: white;">R$ {economia_voo:,.0f}</div>
                </div>
                <div>
                    <h3 style="margin: 0; opacity: 0.8;">Por Mês</h3>
                    <div class="big-number" style="color: white;">R$ {economia_mensal:,.0f}</div>
                </div>
                <div>
                    <h3 style="margin: 0; opacity: 0.8;">Por Ano</h3>
                    <div class="big-number" style="color: white;">R$ {economia_anual:,.0f}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Métricas detalhadas
    st.markdown("## 📊 Análise Detalhada")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-presentation">
            <h4>💰 Custo Amaro</h4>
            <div class="big-number">R$ {resultado['total']:,.0f}</div>
            <p>por voo</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-presentation">
            <h4>🏢 Preço Mercado</h4>
            <div class="big-number">R$ {resultado['preco_mercado']:,.0f}</div>
            <p>por voo</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-presentation">
            <h4>💎 Economia</h4>
            <div class="big-number">{resultado['percentual_economia']:.0f}%</div>
            <p>de redução</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-presentation">
            <h4>⏱️ Duração</h4>
            <div class="big-number">{duracao}h</div>
            <p>de voo</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráficos de apresentação
    st.markdown("## 📈 Visualização Comparativa")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras comparativo
        fig_comp = go.Figure()
        
        fig_comp.add_trace(go.Bar(
            x=['Amaro Aviation', 'Mercado Tradicional'],
            y=[resultado['total'], resultado['preco_mercado']],
            marker_color=['#8c1d40', '#95A5A6'],
            text=[f'R$ {resultado["total"]:,.0f}', f'R$ {resultado["preco_mercado"]:,.0f}'],
            textposition='outside',
            textfont=dict(size=16)
        ))
        
        fig_comp.add_annotation(
            x=0.5, y=resultado['total'] + (resultado['preco_mercado'] - resultado['total'])/2,
            text=f"Economia<br><b>R$ {economia_voo:,.0f}</b>",
            showarrow=True,
            arrowhead=2,
            arrowcolor='#27AE60',
            ax=40,
            ay=-40,
            font=dict(size=14, color='#27AE60')
        )
        
        fig_comp.update_layout(
            title='Comparação de Custos por Voo',
            yaxis_title='Valor (R$)',
            template='plotly_white',
            height=400,
            font=dict(size=14)
        )
        
        st.plotly_chart(fig_comp, use_container_width=True)
    
    with col2:
        # Gráfico de composição
        fig_comp = go.Figure(data=[go.Pie(
            labels=['Combustível', 'Piloto', 'Manutenção', 'Depreciação'],
            values=[resultado['preco_comb'], resultado['piloto'], 
                   resultado['manut'], resultado['depr']],
            hole=0.4,
            marker=dict(colors=['#8c1d40', '#a02050', '#3498DB', '#F39C12'])
        )])
        
        fig_comp.add_annotation(
            text=f"<b>Total</b><br>R$ {resultado['total']:,.0f}",
            x=0.5, y=0.5,
            font=dict(size=16),
            showarrow=False
        )
        
        fig_comp.update_layout(
            title='Composição dos Custos Amaro',
            template='plotly_white',
            height=400,
            font=dict(size=14)
        )
        
        st.plotly_chart(fig_comp, use_container_width=True)
    
    # Projeção anual
    st.markdown("## 📊 Projeção Anual de Economia")
    
    meses = list(range(1, 13))
    economia_acumulada = [economia_mensal * mes for mes in meses]
    
    fig_proj = go.Figure()
    
    fig_proj.add_trace(go.Scatter(
        x=meses,
        y=economia_acumulada,
        mode='lines+markers',
        line=dict(color='#27AE60', width=4),
        marker=dict(size=10),
        fill='tonexty',
        fillcolor='rgba(39, 174, 96, 0.2)',
        name='Economia Acumulada'
    ))
    
    # Adicionar anotação no último ponto
    fig_proj.add_annotation(
        x=12, y=economia_anual,
        text=f"<b>R$ {economia_anual:,.0f}</b><br>economia anual",
        showarrow=True,
        arrowhead=2,
        ax=-40,
        ay=-40,
        font=dict(size=14, color='#27AE60')
    )
    
    fig_proj.update_layout(
        title='Projeção de Economia Acumulada',
        xaxis_title='Mês',
        yaxis_title='Economia Acumulada (R$)',
        template='plotly_white',
        height=400,
        font=dict(size=14),
        yaxis_tickformat=',.0f'
    )
    
    st.plotly_chart(fig_proj, use_container_width=True)
    
    # Proposta de valor
    st.markdown("## 🎯 Proposta de Valor Amaro Aviation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="value-prop-box">
            <h3>💰 Eficiência Financeira</h3>
            <ul>
                <li>Economia média de {}% vs. mercado</li>
                <li>Transparência total nos custos</li>
                <li>Sem taxas ocultas ou surpresas</li>
                <li>Relatórios detalhados mensais</li>
            </ul>
        </div>
        """.format(int(resultado['percentual_economia'])), unsafe_allow_html=True)
        
        st.markdown("""
        <div class="value-prop-box">
            <h3>🛡️ Segurança e Confiabilidade</h3>
            <ul>
                <li>Frota moderna e bem mantida</li>
                <li>Pilotos altamente qualificados</li>
                <li>Manutenção preventiva rigorosa</li>
                <li>Certificações internacionais</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="value-prop-box">
            <h3>📊 Gestão Profissional</h3>
            <ul>
                <li>Controle total de custos</li>
                <li>Análises mensais detalhadas</li>
                <li>Otimização contínua</li>
                <li>Suporte técnico especializado</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="value-prop-box">
            <h3>✈️ Excelência Operacional</h3>
            <ul>
                <li>Disponibilidade garantida</li>
                <li>Pontualidade superior a 95%</li>
                <li>Flexibilidade de horários</li>
                <li>Aeronaves de última geração</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Exportação
    st.markdown("---")
    st.markdown("## 📄 Exportar Análise")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        dados_apresentacao = {
            "Análise": "Demonstração de Economia",
            "Data": datetime.now().strftime("%d/%m/%Y"),
            "Modelo": modelo,
            "Rota": rota,
            "Duração": f"{duracao} horas",
            "Frequência": frequencia,
            "Custo Amaro": resultado['total'],
            "Preço Mercado": resultado['preco_mercado'],
            "Economia por Voo": economia_voo,
            "Economia Mensal": economia_mensal,
            "Economia Anual": economia_anual,
            "Percentual Economia": f"{resultado['percentual_economia']:.1f}%"
        }
        
        try:
            pdf_buffer = BytesIO()
            if gerar_pdf(pdf_buffer, dados_apresentacao):
                pdf_buffer.seek(0)
                
                st.download_button(
                    "📄 Baixar Apresentação em PDF",
                    data=pdf_buffer.getvalue(),
                    file_name=f"amaro_apresentacao_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    type="secondary",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")

# Sidebar minimalista
with st.sidebar:
    st.markdown("""
    ### 🎨 Modo Apresentação
    
    Interface simplificada para demonstrações com clientes e parceiros.
    
    **Dicas para apresentação:**
    - Use tela cheia (F11)
    - Prepare os parâmetros antes
    - Tenha os dados do cliente em mãos
    
    ---
    
    ### ⚡ Ações Rápidas
    """)
    
    if st.button("🏠 Voltar ao Dashboard", use_container_width=True):
        st.switch_page("app.py")
    
    if st.button("⚙️ Configurações", use_container_width=True):
        st.switch_page("pages/5_Configurações.py")
    
    st.markdown("---")
    st.info("""
    **Modo Apresentação v2.0**
    
    Sistema interno Amaro Aviation
    """)