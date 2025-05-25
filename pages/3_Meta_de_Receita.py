import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.params import load_params
from utils.calculations import calcula_custo_trecho, calcular_horas_para_meta
from utils.exportador_pdf import gerar_pdf
from utils.exportador_excel import gerar_excel
from io import BytesIO
import calendar

# Configuração da página
st.set_page_config(
    page_title="Planejamento de Metas - Amaro Aviation", 
    layout="wide",
    page_icon="🎯"
)

# CSS Premium
st.markdown("""
<style>
.strategy-header {
    background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%);
    color: white;
    padding: 2.5rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(140, 29, 64, 0.3);
}

.goal-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    border: 1px solid #e9ecef;
    margin: 1rem 0;
    transition: all 0.3s ease;
}

.goal-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(0,0,0,0.15);
}

.achievable-goal {
    background: linear-gradient(135deg, #E8F5E8 0%, #F1F9F1 100%);
    border: 2px solid #27AE60;
    border-radius: 15px;
    padding: 2rem;
    margin: 1rem 0;
}

.challenging-goal {
    background: linear-gradient(135deg, #FFF3CD 0%, #FCF8E3 100%);
    border: 2px solid #F39C12;
    border-radius: 15px;
    padding: 2rem;
    margin: 1rem 0;
}

.unrealistic-goal {
    background: linear-gradient(135deg, #F8D7DA 0%, #FDEAEA 100%);
    border: 2px solid #E74C3C;
    border-radius: 15px;
    padding: 2rem;
    margin: 1rem 0;
}

.strategy-metric {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    border-left: 5px solid #3498DB;
    margin: 1rem 0;
    text-align: center;
}

.action-plan {
    background: linear-gradient(135deg, #E8F4FD 0%, #F1F9FF 100%);
    border: 2px solid #3498DB;
    border-radius: 15px;
    padding: 2rem;
    margin: 2rem 0;
}

.progress-tracker {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header Premium
st.markdown("""
<div class="strategy-header">
    <h1 style="margin: 0; font-size: 2.5rem;">🎯 Planejamento Estratégico de Metas</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.2rem;">Análise Avançada de Viabilidade e Estratégias de Crescimento</p>
</div>
""", unsafe_allow_html=True)

# Carregamento de parâmetros
try:
    params = load_params()
    modelos = params.get('modelos_disponiveis', [])
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# Configuração de metas
st.markdown("## 🎯 Definição de Metas Estratégicas")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="goal-card">
        <h3>📊 Configuração de Objetivos</h3>
        <p>Defina metas realistas baseadas em análise de mercado e capacidade operacional</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs para diferentes tipos de metas
    tab1, tab2, tab3, tab4 = st.tabs(["💰 Meta Financeira", "📈 Crescimento", "🎯 Operacional", "🏆 Competitividade"])
    
    with tab1:
        col_a, col_b = st.columns(2)
        
        with col_a:
            meta_receita_mensal = st.number_input(
                "🎯 Meta de Receita Mensal (R$)",
                min_value=50000.0,
                max_value=5000000.0,
                value=500000.0,
                step=25000.0,
                help="Meta de receita bruta mensal desejada"
            )
            
            meta_margem_liquida = st.slider(
                "📊 Meta de Margem Líquida (%)",
                min_value=10,
                max_value=50,
                value=25,
                help="Margem líquida desejada sobre a receita"
            )
            
            periodo_meta = st.selectbox(
                "📅 Período da Meta",
                ["1 mês", "3 meses", "6 meses", "12 meses"],
                index=2
            )
        
        with col_b:
            crescimento_mensal = st.slider(
                "📈 Crescimento Mensal (%)",
                min_value=0,
                max_value=20,
                value=5,
                help="Taxa de crescimento mensal esperada"
            )
            
            investimento_inicial = st.number_input(
                "💼 Investimento Disponível (R$)",
                min_value=0.0,
                value=1000000.0,
                step=50000.0,
                help="Capital disponível para investimento"
            )
            
            risco_tolerancia = st.select_slider(
                "⚖️ Tolerância ao Risco",
                options=["Conservador", "Moderado", "Agressivo"],
                value="Moderado"
            )
    
    with tab2:
        st.markdown("### 📈 Estratégia de Crescimento")
        
        col_grow1, col_grow2 = st.columns(2)
        
        with col_grow1:
            expansao_frota = st.checkbox("✈️ Expansão da Frota", value=False)
            if expansao_frota:
                novos_modelos = st.multiselect(
                    "Modelos para Expansão",
                    modelos,
                    help="Selecione modelos para expansão"
                )
                cronograma_expansao = st.selectbox(
                    "Cronograma de Expansão",
                    ["3 meses", "6 meses", "12 meses", "18 meses"]
                )
            
            novos_mercados = st.checkbox("🌍 Novos Mercados", value=False)
            if novos_mercados:
                regioes_alvo = st.multiselect(
                    "Regiões Alvo",
                    ["Sul", "Nordeste", "Norte", "Centro-Oeste", "Internacional"],
                    default=["Sul"]
                )
        
        with col_grow2:
            servicos_premium = st.checkbox("💎 Serviços Premium", value=False)
            if servicos_premium:
                premium_markup = st.slider(
                    "Markup Premium (%)",
                    min_value=10,
                    max_value=50,
                    value=25
                )
            
            parcerias_estrategicas = st.checkbox("🤝 Parcerias", value=False)
            if parcerias_estrategicas:
                tipo_parceria = st.selectbox(
                    "Tipo de Parceria",
                    ["Operadores", "Brokers", "Empresas", "Turismo"]
                )
    
    with tab3:
        st.markdown("### 🎯 Metas Operacionais")
        
        col_op1, col_op2 = st.columns(2)
        
        with col_op1:
            meta_ocupacao = st.slider(
                "📊 Meta de Ocupação (%)",
                min_value=60,
                max_value=95,
                value=80,
                help="Taxa de ocupação alvo da frota"
            )
            
            meta_pontualidade = st.slider(
                "⏰ Meta de Pontualidade (%)",
                min_value=85,
                max_value=100,
                value=95
            )
            
            eficiencia_combustivel = st.slider(
                "⛽ Eficiência de Combustível (%)",
                min_value=90,
                max_value=100,
                value=96,
                help="Meta de eficiência no consumo"
            )
        
        with col_op2:
            satisfacao_cliente = st.slider(
                "😊 Satisfação do Cliente",
                min_value=8.0,
                max_value=10.0,
                value=9.2,
                step=0.1,
                help="Nota média de satisfação (0-10)"
            )
            
            tempo_resposta = st.number_input(
                "📞 Tempo de Resposta (min)",
                min_value=5,
                max_value=60,
                value=15,
                help="Tempo máximo de resposta a solicitações"
            )
    
    with tab4:
        st.markdown("### 🏆 Análise Competitiva")
        
        col_comp1, col_comp2 = st.columns(2)
        
        with col_comp1:
            preco_competitivo = st.slider(
                "💰 Posicionamento de Preço",
                min_value=-20,
                max_value=20,
                value=-10,
                help="% acima/abaixo da média do mercado"
            )
            
            market_share_alvo = st.slider(
                "📊 Market Share Alvo (%)",
                min_value=1,
                max_value=25,
                value=5,
                help="Participação de mercado desejada"
            )
        
        with col_comp2:
            diferenciacao = st.multiselect(
                "🌟 Diferenciais Competitivos",
                ["Preço", "Qualidade", "Pontualidade", "Flexibilidade", 
                 "Tecnologia", "Atendimento", "Sustentabilidade"],
                default=["Preço", "Pontualidade"]
            )

with col2:
    # Análise de viabilidade em tempo real
    st.markdown("""
    <div class="goal-card">
        <h4>📊 Análise de Viabilidade</h4>
    """, unsafe_allow_html=True)
    
    # Calcular viabilidade básica
    modelo_principal = modelos[0] if modelos else None
    if modelo_principal:
        resultado_hora = calcula_custo_trecho(modelo_principal, 1.0, params)
        preco_hora = params['preco_mercado_hora'][modelo_principal]
        
        # Horas necessárias para meta
        horas_necessarias = meta_receita_mensal / preco_hora
        dias_necessarios = horas_necessarias / 8  # 8h por dia máximo
        
        # Análise de viabilidade
        if dias_necessarios <= 25:  # Viável
            viabilidade = "✅ Viável"
            cor_viabilidade = "#27AE60"
        elif dias_necessarios <= 35:  # Desafiador
            viabilidade = "⚠️ Desafiador"
            cor_viabilidade = "#F39C12"
        else:  # Irrealista
            viabilidade = "❌ Irrealista"
            cor_viabilidade = "#E74C3C"
        
        st.write(f"**Status:** {viabilidade}")
        st.write(f"**Horas Necessárias:** {horas_necessarias:.0f}/mês")
        st.write(f"**Dias Operação:** {dias_necessarios:.0f}")
        st.write(f"**Modelo Base:** {modelo_principal}")
        
        # Progresso visual
        progresso = min(100, (25 / dias_necessarios) * 100)
        st.progress(progresso / 100)
        
    st.markdown("</div>", unsafe_allow_html=True)

# Execução da análise
if st.button("🚀 Executar Análise Estratégica Completa", type="primary", use_container_width=True):
    try:
        # Análise detalhada por modelo
        st.markdown("---")
        st.markdown("## 📊 Análise Estratégica Detalhada")
        
        # Calcular estratégias para cada modelo
        estrategias = []
        
        for modelo in modelos:
            resultado_hora = calcula_custo_trecho(modelo, 1.0, params)
            preco_hora = params['preco_mercado_hora'][modelo]
            
            # Horas necessárias
            horas_meta = meta_receita_mensal / preco_hora
            dias_meta = horas_meta / 8
            
            # Análise de rentabilidade
            lucro_hora = resultado_hora['economia']
            lucro_meta = lucro_hora * horas_meta
            margem_real = (lucro_meta / meta_receita_mensal * 100) if meta_receita_mensal > 0 else 0
            
            # Classificação da estratégia
            if dias_meta <= 25 and margem_real >= meta_margem_liquida:
                classificacao = "Excelente"
                cor = "#27AE60"
            elif dias_meta <= 30 and margem_real >= meta_margem_liquida * 0.8:
                classificacao = "Boa"
                cor = "#3498DB"
            elif dias_meta <= 35:
                classificacao = "Desafiadora"
                cor = "#F39C12"
            else:
                classificacao = "Irrealista"
                cor = "#E74C3C"
            
            estrategias.append({
                'Modelo': modelo,
                'Preço/Hora': preco_hora,
                'Horas Necessárias': horas_meta,
                'Dias Operação': dias_meta,
                'Lucro/Hora': lucro_hora,
                'Lucro Meta': lucro_meta,
                'Margem Real': margem_real,
                'Classificação': classificacao,
                'Cor': cor
            })
        
        # Exibir análise por modelo
        st.markdown("### 🛩️ Análise por Modelo de Aeronave")
        
        for estrategia in estrategias:
            classificacao_class = estrategia['Classificação'].lower()
            if classificacao_class == "excelente":
                card_class = "achievable-goal"
            elif classificacao_class in ["boa", "desafiadora"]:
                card_class = "challenging-goal"
            else:
                card_class = "unrealistic-goal"
            
            st.markdown(f"""
            <div class="{card_class}">
                <h4>{estrategia['Modelo']} - {estrategia['Classificação']}</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 1rem;">
                    <div><strong>Preço/Hora:</strong><br>R$ {estrategia['Preço/Hora']:,.0f}</div>
                    <div><strong>Horas/Mês:</strong><br>{estrategia['Horas Necessárias']:.0f}h</div>
                    <div><strong>Dias Operação:</strong><br>{estrategia['Dias Operação']:.0f} dias</div>
                    <div><strong>Margem Real:</strong><br>{estrategia['Margem Real']:.1f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Estratégia recomendada
        melhor_estrategia = min(estrategias, key=lambda x: x['Dias Operação'])
        
        st.markdown("### 🏆 Estratégia Recomendada")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="strategy-metric">
                <h4>🛩️ Modelo Recomendado</h4>
                <h2>{melhor_estrategia['Modelo']}</h2>
                <p>Maior eficiência operacional</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="strategy-metric">
                <h4>⏰ Horas Necessárias</h4>
                <h2>{melhor_estrategia['Horas Necessárias']:.0f}h</h2>
                <p>Por mês para atingir meta</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="strategy-metric">
                <h4>💰 Lucro Estimado</h4>
                <h2>R$ {melhor_estrategia['Lucro Meta']:,.0f}</h2>
                <p>Margem: {melhor_estrategia['Margem Real']:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráfico comparativo de estratégias
        fig_estrategias = go.Figure()
        
        fig_estrategias.add_trace(go.Scatter(
            x=[e['Dias Operação'] for e in estrategias],
            y=[e['Margem Real'] for e in estrategias],
            mode='markers+text',
            marker=dict(
                size=[e['Lucro Meta']/10000 for e in estrategias],
                color=[e['Cor'] for e in estrategias],
                line=dict(width=2, color='white'),
                sizemode='diameter',
                sizemin=10
            ),
            text=[e['Modelo'] for e in estrategias],
            textposition="middle center",
            textfont=dict(color="white", size=10),
            hovertemplate='<b>%{text}</b><br>' +
                         'Dias: %{x:.0f}<br>' +
                         'Margem: %{y:.1f}%<br>' +
                         '<extra></extra>'
        ))
        
        # Linhas de referência
        fig_estrategias.add_hline(y=meta_margem_liquida, line_dash="dash", 
                                 line_color="green", annotation_text="Meta de Margem")
        fig_estrategias.add_vline(x=25, line_dash="dash", 
                                 line_color="blue", annotation_text="Limite Ideal (25 dias)")
        
        fig_estrategias.update_layout(
            title='🎯 Matriz Estratégica: Viabilidade vs. Rentabilidade',
            xaxis_title='Dias de Operação Necessários',
            yaxis_title='Margem Real (%)',
            template='plotly_white',
            height=500
        )
        
        st.plotly_chart(fig_estrategias, use_container_width=True)
        
        # Cronograma de execução
        st.markdown("### 📅 Cronograma de Execução")
        
        # Simular cronograma baseado no período da meta
        periodo_num = int(periodo_meta.split()[0])
        meses_cronograma = list(range(1, periodo_num + 1))
        
        # Calcular crescimento progressivo
        receita_base = meta_receita_mensal / (1 + crescimento_mensal/100)**(periodo_num-1)
        cronograma_data = []
        
        for mes in meses_cronograma:
            receita_mes = receita_base * (1 + crescimento_mensal/100)**(mes-1)
            horas_mes = receita_mes / melhor_estrategia['Preço/Hora']
            lucro_mes = (receita_mes * melhor_estrategia['Margem Real'] / 100)
            
            cronograma_data.append({
                'Mês': mes,
                'Meta Receita': receita_mes,
                'Horas Necessárias': horas_mes,
                'Lucro Estimado': lucro_mes,
                'Crescimento': ((receita_mes / receita_base) - 1) * 100
            })
        
        df_cronograma = pd.DataFrame(cronograma_data)
        
        # Gráfico de cronograma
        fig_cronograma = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Evolução da Receita', 'Horas de Operação', 
                           'Lucro Estimado', 'Taxa de Crescimento'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Receita
        fig_cronograma.add_trace(
            go.Scatter(x=df_cronograma['Mês'], y=df_cronograma['Meta Receita'],
                      mode='lines+markers', name='Receita', line=dict(color='#27AE60', width=3)),
            row=1, col=1
        )
        
        # Horas
        fig_cronograma.add_trace(
            go.Bar(x=df_cronograma['Mês'], y=df_cronograma['Horas Necessárias'],
                   name='Horas', marker_color='#3498DB'),
            row=1, col=2
        )
        
        # Lucro
        fig_cronograma.add_trace(
            go.Scatter(x=df_cronograma['Mês'], y=df_cronograma['Lucro Estimado'],
                      mode='lines+markers', name='Lucro', line=dict(color='#8c1d40', width=3),
                      fill='tonexty', fillcolor='rgba(140, 29, 64, 0.1)'),
            row=2, col=1
        )
        
        # Crescimento
        fig_cronograma.add_trace(
            go.Bar(x=df_cronograma['Mês'], y=df_cronograma['Crescimento'],
                   name='Crescimento %', marker_color='#F39C12'),
            row=2, col=2
        )
        
        fig_cronograma.update_layout(
            title='📊 Cronograma de Execução da Meta',
            template='plotly_white',
            height=600,
            showlegend=False
        )
        
        st.plotly_chart(fig_cronograma, use_container_width=True)
        
        # Plano de ação detalhado
        st.markdown(f"""
        <div class="action-plan">
            <h3>🎯 Plano de Ação Estratégico</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
                <div>
                    <h4>📋 Ações Imediatas (Próximos 30 dias)</h4>
                    <ul>
                        <li>🛩️ Otimizar operação do {melhor_estrategia['Modelo']}</li>
                        <li>📊 Implementar sistema de monitoramento de ocupação</li>
                        <li>💰 Negociar contratos com margem alvo de {meta_margem_liquida}%</li>
                        <li>📞 Intensificar prospecção comercial</li>
                        {"<li>✈️ Preparar expansão da frota</li>" if expansao_frota else ""}
                    </ul>
                    
                    <h4>📈 Metas Trimestrais</h4>
                    <ul>
                        <li>🎯 Atingir {meta_ocupacao}% de ocupação média</li>
                        <li>💼 Desenvolver {len(diferenciacao)} diferenciais competitivos</li>
                        <li>🤝 Estabelecer parcerias estratégicas</li>
                        <li>📊 Alcançar {satisfacao_cliente:.1f}/10 em satisfação</li>
                    </ul>
                </div>
                <div>
                    <h4>⚠️ Riscos e Mitigações</h4>
                    <ul>
                        <li><strong>Risco:</strong> Baixa ocupação<br><strong>Mitigação:</strong> Diversificar canais de venda</li>
                        <li><strong>Risco:</strong> Concorrência de preços<br><strong>Mitigação:</strong> Focar em qualidade e pontualidade</li>
                        <li><strong>Risco:</strong> Custos de combustível<br><strong>Mitigação:</strong> Hedging e eficiência operacional</li>
                        <li><strong>Risco:</strong> Sazonalidade<br><strong>Mitigação:</strong> Contratos anuais e flexibilidade</li>
                    </ul>
                    
                    <h4>📊 KPIs de Acompanhamento</h4>
                    <ul>
                        <li>📈 Receita mensal vs. meta</li>
                        <li>💰 Margem líquida realizada</li>
                        <li>⏰ Taxa de ocupação da frota</li>
                        <li>😊 NPS (Net Promoter Score)</li>
                    </ul>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Análise de sensibilidade
        st.markdown("### 🔄 Análise de Sensibilidade")
        
        # Cenários de análise
        cenarios = {
            'Pessimista': {'ocupacao': 0.7, 'preco': 0.9, 'custo': 1.1},
            'Realista': {'ocupacao': 0.8, 'preco': 1.0, 'custo': 1.0},
            'Otimista': {'ocupacao': 0.9, 'preco': 1.1, 'custo': 0.95}
        }
        
        sensibilidade_data = []
        for nome, params_cenario in cenarios.items():
            receita_cenario = meta_receita_mensal * params_cenario['preco'] * params_cenario['ocupacao']
            custo_cenario = (meta_receita_mensal - melhor_estrategia['Lucro Meta']) * params_cenario['custo']
            lucro_cenario = receita_cenario - custo_cenario
            margem_cenario = (lucro_cenario / receita_cenario * 100) if receita_cenario > 0 else 0
            
            sensibilidade_data.append({
                'Cenário': nome,
                'Receita': receita_cenario,
                'Lucro': lucro_cenario,
                'Margem': margem_cenario,
                'Viabilidade': 'Alta' if margem_cenario >= meta_margem_liquida else 'Média' if margem_cenario >= meta_margem_liquida * 0.7 else 'Baixa'
            })
        
        df_sensibilidade = pd.DataFrame(sensibilidade_data)
        
        fig_sens = go.Figure()
        
        cores_cenario = {'Pessimista': '#E74C3C', 'Realista': '#3498DB', 'Otimista': '#27AE60'}
        
        for _, row in df_sensibilidade.iterrows():
            fig_sens.add_trace(go.Bar(
                name=row['Cenário'],
                x=[row['Cenário']],
                y=[row['Margem']],
                marker_color=cores_cenario[row['Cenário']],
                text=f"{row['Margem']:.1f}%",
                textposition='outside',
                hovertemplate=f"<b>{row['Cenário']}</b><br>" +
                             f"Receita: R$ {row['Receita']:,.0f}<br>" +
                             f"Lucro: R$ {row['Lucro']:,.0f}<br>" +
                             f"Margem: {row['Margem']:.1f}%<br>" +
                             f"Viabilidade: {row['Viabilidade']}<extra></extra>"
            ))
        
        fig_sens.add_hline(y=meta_margem_liquida, line_dash="dash", 
                          line_color="orange", annotation_text="Meta de Margem")
        
        fig_sens.update_layout(
            title='🎲 Análise de Cenários - Margem Líquida',
            yaxis_title='Margem Líquida (%)',
            template='plotly_white',
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_sens, use_container_width=True)
        
        # Exportação
        st.markdown("---")
        st.markdown("## 📄 Exportar Plano Estratégico")
        
        col1, col2 = st.columns(2)
        
        # Preparar dados para exportação
        dados_estrategia = {
            "Análise": "Planejamento Estratégico de Metas",
            "Data": datetime.now().strftime("%d/%m/%Y"),
            "Meta Receita Mensal": meta_receita_mensal,
            "Meta Margem Líquida": f"{meta_margem_liquida}%",
            "Período": periodo_meta,
            "Modelo Recomendado": melhor_estrategia['Modelo'],
            "Horas Necessárias": f"{melhor_estrategia['Horas Necessárias']:.0f}",
            "Dias Operação": f"{melhor_estrategia['Dias Operação']:.0f}",
            "Lucro Estimado": melhor_estrategia['Lucro Meta'],
            "Margem Real": f"{melhor_estrategia['Margem Real']:.1f}%",
            "Classificação": melhor_estrategia['Classificação'],
            "Taxa Ocupação Meta": f"{meta_ocupacao}%",
            "Crescimento Mensal": f"{crescimento_mensal}%",
            "Investimento Disponível": investimento_inicial,
            "Tolerância Risco": risco_tolerancia,
            "Cenário Realista Margem": f"{df_sensibilidade.iloc[1]['Margem']:.1f}%",
            "Viabilidade Geral": df_sensibilidade.iloc[1]['Viabilidade']
        }
        
        with col1:
            try:
                pdf_buffer = BytesIO()
                if gerar_pdf(pdf_buffer, dados_estrategia):
                    pdf_buffer.seek(0)
                    st.download_button(
                        "📄 Plano Estratégico PDF",
                        data=pdf_buffer.getvalue(),
                        file_name=f"amaro_plano_estrategico_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")
        
        with col2:
            try:
                excel_buffer = BytesIO()
                if gerar_excel(excel_buffer, dados_estrategia):
                    excel_buffer.seek(0)
                    st.download_button(
                        "📊 Planilha Estratégica",
                        data=excel_buffer.getvalue(),
                        file_name=f"amaro_plano_estrategico_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Erro ao gerar Excel: {e}")
        
    except Exception as e:
        st.error(f"Erro na análise estratégica: {e}")

# Sidebar com orientações
with st.sidebar:
    st.markdown("### 🎯 Guia Estratégico")
    
    st.info("""
    **📋 Passo a Passo:**
    1. Defina meta financeira realista
    2. Configure parâmetros operacionais
    3. Analise cenários de crescimento
    4. Execute análise estratégica
    5. Implemente plano de ação
    
    **🎯 Metas SMART:**
    - **S**pecíficas: R$ valores exatos
    - **M**ensuráveis: KPIs definidos
    - **A**tingíveis: Baseadas em capacidade
    - **R**elevantes: Alinhadas ao negócio
    - **T**emporais: Prazo definido
    """)
    
    st.markdown("### 💡 Dicas Estratégicas")
    
    st.success("""
    **🚀 Para Sucesso:**
    - Foque em ocupação > 75%
    - Mantenha margem > 20%
    - Diversifique modelos/rotas
    - Monitore KPIs semanalmente
    - Ajuste estratégia conforme necessário
    """)
    
    st.warning("""
    **⚠️ Alertas:**
    - Metas irrealistas prejudicam moral
    - Considere sazonalidade
    - Prepare contingências
    - Invista em relacionamento cliente
    """)
    
    st.markdown("### 📞 Consultoria Estratégica")
    st.markdown("""
    Para planejamento personalizado:
    **Estratégia Amaro**
    📧 estrategia@amaroaviation.com
    📞 (11) 99999-8888
    """)