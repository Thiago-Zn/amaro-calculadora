import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.params import load_params
from utils.calculations import calcular_projecao_mensal, calcula_custo_trecho
from utils.charts import grafico_evolucao_mensal, grafico_breakdown_detalhado
from utils.exportador_pdf import gerar_pdf
from utils.exportador_excel import gerar_excel
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="Projeção de Lucros - Amaro Aviation", 
    layout="wide",
    page_icon="📈"
)

# CSS Premium
st.markdown("""
<style>
.profit-header {
    background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%);
    color: white;
    padding: 2.5rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(140, 29, 64, 0.3);
}

.scenario-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    border: 1px solid #e9ecef;
    margin: 1rem 0;
    transition: all 0.3s ease;
}

.scenario-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(0,0,0,0.15);
}

.profit-metric {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    border-left: 5px solid #27AE60;
    margin: 1rem 0;
    text-align: center;
}

.loss-metric {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    border-left: 5px solid #E74C3C;
    margin: 1rem 0;
    text-align: center;
}

.neutral-metric {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    border-left: 5px solid #F39C12;
    margin: 1rem 0;
    text-align: center;
}

.insights-box {
    background: linear-gradient(135deg, #E8F4FD 0%, #F1F9FF 100%);
    border: 2px solid #3498DB;
    border-radius: 15px;
    padding: 2rem;
    margin: 2rem 0;
}

.optimization-box {
    background: linear-gradient(135deg, #E8F5E8 0%, #F1F9F1 100%);
    border: 2px solid #27AE60;
    border-radius: 15px;
    padding: 2rem;
    margin: 2rem 0;
}

.simulation-controls {
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
<div class="profit-header">
    <h1 style="margin: 0; font-size: 2.5rem;">📈 Projeção de Lucros Mensais</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.2rem;">Análise Avançada de Rentabilidade e Planejamento Estratégico</p>
</div>
""", unsafe_allow_html=True)

# Carregamento de parâmetros
try:
    params = load_params()
    modelos = params.get('modelos_disponiveis', [])
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# Controles de simulação avançados
st.markdown("## 🎯 Configuração da Simulação")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="simulation-controls">
        <h3>📊 Parâmetros Operacionais</h3>
        <p>Configure os parâmetros para análise detalhada de rentabilidade</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs para diferentes tipos de análise
    tab1, tab2, tab3 = st.tabs(["📅 Análise Mensal", "📈 Cenários Múltiplos", "🎯 Metas Personalizadas"])
    
    with tab1:
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            modelo_base = st.selectbox(
                "🛩️ Modelo Principal",
                modelos,
                help="Modelo de aeronave para análise principal"
            )
            
            dias_operacao = st.slider(
                "📅 Dias de Operação/Mês",
                min_value=1,
                max_value=31,
                value=20,
                help="Dias úteis de operação por mês"
            )
        
        with col_b:
            horas_por_dia = st.number_input(
                "⏰ Horas/Dia",
                min_value=1.0,
                max_value=12.0,
                value=6.0,
                step=0.5,
                help="Horas de voo por dia de operação"
            )
            
            taxa_ocupacao = st.slider(
                "📊 Taxa de Ocupação (%)",
                min_value=30,
                max_value=100,
                value=75,
                help="Percentual de ocupação da aeronave"
            )
        
        with col_c:
            custo_fixo_mensal = st.number_input(
                "💰 Custos Fixos Mensais (R$)",
                min_value=0.0,
                value=50000.0,
                step=5000.0,
                help="Hangar, seguro, financiamento, etc."
            )
            
            margem_seguranca = st.slider(
                "🛡️ Margem de Segurança (%)",
                min_value=0,
                max_value=30,
                value=10,
                help="Margem para imprevistos"
            )
    
    with tab2:
        st.markdown("### 📊 Análise de Cenários")
        
        # Cenários predefinidos
        cenario_selecionado = st.selectbox(
            "Cenário de Análise",
            [
                "Operação Conservadora (50% ocupação)",
                "Operação Normal (75% ocupação)", 
                "Operação Otimizada (90% ocupação)",
                "Cenário Personalizado"
            ]
        )
        
        if cenario_selecionado == "Cenário Personalizado":
            col_cen1, col_cen2 = st.columns(2)
            with col_cen1:
                ocupacao_custom = st.slider("Taxa de Ocupação (%)", 30, 100, 80)
                dias_custom = st.slider("Dias de Operação", 10, 30, 22)
            with col_cen2:
                horas_custom = st.number_input("Horas por Dia", 2.0, 10.0, 5.0)
                fixos_custom = st.number_input("Custos Fixos (R$)", 20000.0, 200000.0, 60000.0)
    
    with tab3:
        st.markdown("### 🎯 Definição de Metas")
        
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            meta_lucro_mensal = st.number_input(
                "Meta de Lucro Mensal (R$)",
                min_value=0.0,
                value=200000.0,
                step=10000.0
            )
            
            meta_margem = st.slider(
                "Meta de Margem (%)",
                min_value=10,
                max_value=50,
                value=25
            )
        
        with col_meta2:
            meta_roi_anual = st.slider(
                "Meta ROI Anual (%)",
                min_value=10,
                max_value=100,
                value=30
            )
            
            periodo_retorno = st.selectbox(
                "Período de Retorno Desejado",
                ["12 meses", "18 meses", "24 meses", "36 meses"]
            )

with col2:
    # Informações do modelo selecionado
    if modelo_base in params['consumo_modelos']:
        st.markdown("""
        <div class="scenario-card">
            <h4>📋 Perfil da Aeronave</h4>
        """, unsafe_allow_html=True)
        
        consumo = params['consumo_modelos'][modelo_base]
        preco_mercado_hora = params['preco_mercado_hora'][modelo_base]
        tipo_aeronave = "Jato Executivo" if preco_mercado_hora > 10000 else "Turboprop"
        
        # Calcular custo operacional por hora
        resultado_hora = calcula_custo_trecho(modelo_base, 1.0, params)
        
        st.write(f"**{modelo_base}**")
        st.write(f"**Categoria:** {tipo_aeronave}")
        st.write(f"**Consumo:** {consumo} L/h")
        st.write(f"**Custo Operacional:** R$ {resultado_hora['total']:,.0f}/h")
        st.write(f"**Preço Mercado:** R$ {preco_mercado_hora:,.0f}/h")
        st.write(f"**Margem Bruta:** R$ {resultado_hora['economia']:,.0f}/h")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Botão de cálculo principal
if st.button("🚀 Executar Análise Completa", type="primary", use_container_width=True):
    try:
        # Cálculos base
        resultado_hora = calcula_custo_trecho(modelo_base, 1.0, params)
        
        # Aplicar parâmetros de operação
        horas_totais_mes = dias_operacao * horas_por_dia * (taxa_ocupacao / 100)
        
        # Custos e receitas
        custo_operacional_mes = resultado_hora['total'] * horas_totais_mes
        receita_bruta_mes = params['preco_mercado_hora'][modelo_base] * horas_totais_mes
        margem_bruta = receita_bruta_mes - custo_operacional_mes
        
        # Custos adicionais
        custo_total_mes = custo_operacional_mes + custo_fixo_mensal
        lucro_liquido = receita_bruta_mes - custo_total_mes
        
        # Margem de segurança
        lucro_com_seguranca = lucro_liquido * (1 - margem_seguranca / 100)
        
        # Métricas avançadas
        roi_mensal = (lucro_liquido / custo_total_mes * 100) if custo_total_mes > 0 else 0
        margem_liquida = (lucro_liquido / receita_bruta_mes * 100) if receita_bruta_mes > 0 else 0
        ponto_equilibrio_horas = custo_fixo_mensal / resultado_hora['economia'] if resultado_hora['economia'] > 0 else 0
        
        # Exibição dos resultados
        st.markdown("---")
        st.markdown("## 💰 Análise Financeira Detalhada")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if lucro_liquido > 0:
                st.markdown(f"""
                <div class="profit-metric">
                    <h4>💰 Lucro Líquido</h4>
                    <h2>R$ {lucro_liquido:,.0f}</h2>
                    <p>Margem: {margem_liquida:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="loss-metric">
                    <h4>⚠️ Prejuízo</h4>
                    <h2>R$ {abs(lucro_liquido):,.0f}</h2>
                    <p>Revisar operação</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="neutral-metric">
                <h4>📊 ROI Mensal</h4>
                <h2>{roi_mensal:.1f}%</h2>
                <p>ROI Anual: {roi_mensal * 12:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="neutral-metric">
                <h4>⏰ Horas Voadas</h4>
                <h2>{horas_totais_mes:.0f}h</h2>
                <p>Ocupação: {taxa_ocupacao}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="neutral-metric">
                <h4>⚖️ Ponto Equilíbrio</h4>
                <h2>{ponto_equilibrio_horas:.0f}h</h2>
                <p>Por mês para cobrir fixos</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Breakdown detalhado
        st.markdown("### 📊 Breakdown Financeiro Completo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de composição de custos
            fig_custos = go.Figure()
            
            categorias = ['Custos Operacionais', 'Custos Fixos']
            valores = [custo_operacional_mes, custo_fixo_mensal]
            cores = ['#8c1d40', '#a02050']
            
            fig_custos.add_trace(go.Pie(
                labels=categorias,
                values=valores,
                hole=0.4,
                marker=dict(colors=cores, line=dict(color='white', width=3)),
                textinfo='label+percent+value',
                texttemplate='<b>%{label}</b><br>%{percent}<br>R$ %{value:,.0f}',
                hovertemplate='<b>%{label}</b><br>Valor: R$ %{value:,.0f}<br>Percentual: %{percent}<extra></extra>'
            ))
            
            fig_custos.add_annotation(
                text=f"<b>Total</b><br>R$ {custo_total_mes:,.0f}",
                x=0.5, y=0.5,
                font=dict(size=16, color='#2C3E50'),
                showarrow=False
            )
            
            fig_custos.update_layout(
                title='💸 Composição de Custos Mensais',
                template='plotly_white',
                height=400
            )
            
            st.plotly_chart(fig_custos, use_container_width=True)
        
        with col2:
            # Gráfico de receita vs custos
            fig_resultado = go.Figure()
            
            fig_resultado.add_trace(go.Bar(
                name='Receita Bruta',
                x=['Mensal'],
                y=[receita_bruta_mes],
                marker_color='#27AE60',
                text=f'R$ {receita_bruta_mes:,.0f}',
                textposition='outside'
            ))
            
            fig_resultado.add_trace(go.Bar(
                name='Custo Total',
                x=['Mensal'],
                y=[custo_total_mes],
                marker_color='#E74C3C',
                text=f'R$ {custo_total_mes:,.0f}',
                textposition='outside'
            ))
            
            fig_resultado.add_trace(go.Bar(
                name='Lucro Líquido',
                x=['Mensal'],
                y=[lucro_liquido],
                marker_color='#3498DB' if lucro_liquido > 0 else '#E67E22',
                text=f'R$ {lucro_liquido:,.0f}',
                textposition='outside'
            ))
            
            fig_resultado.update_layout(
                title='📈 Resultado Financeiro Mensal',
                yaxis_title='Valor (R$)',
                template='plotly_white',
                height=400,
                barmode='group'
            )
            
            st.plotly_chart(fig_resultado, use_container_width=True)
        
        # Projeção anual
        st.markdown("### 📅 Projeção Anual")
        
        # Simular variações mensais
        meses = list(range(1, 13))
        projecao_anual = []
        
        for mes in meses:
            # Simular sazonalidade (maior demanda em dez-fev e jun-jul)
            if mes in [12, 1, 2, 6, 7]:
                fator_sazonalidade = 1.2
            elif mes in [3, 4, 9, 10]:
                fator_sazonalidade = 0.9
            else:
                fator_sazonalidade = 1.0
            
            lucro_mes = lucro_liquido * fator_sazonalidade
            projecao_anual.append({
                'Mês': f'{mes:02d}',
                'Lucro': lucro_mes,
                'Acumulado': sum([projecao_anual[i]['Lucro'] for i in range(len(projecao_anual))]) + lucro_mes
            })
        
        df_projecao = pd.DataFrame(projecao_anual)
        
        fig_anual = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Lucro Mensal', 'Lucro Acumulado'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Lucro mensal
        fig_anual.add_trace(
            go.Bar(
                x=df_projecao['Mês'],
                y=df_projecao['Lucro'],
                name='Lucro Mensal',
                marker_color='#27AE60',
                hovertemplate='Mês %{x}<br>Lucro: R$ %{y:,.0f}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Lucro acumulado
        fig_anual.add_trace(
            go.Scatter(
                x=df_projecao['Mês'],
                y=df_projecao['Acumulado'],
                mode='lines+markers',
                name='Lucro Acumulado',
                line=dict(color='#3498DB', width=4),
                marker=dict(size=8),
                fill='tonexty',
                fillcolor='rgba(52, 152, 219, 0.1)',
                hovertemplate='Mês %{x}<br>Acumulado: R$ %{y:,.0f}<extra></extra>'
            ),
            row=1, col=2
        )
        
        fig_anual.update_layout(
            title='📊 Projeção de Lucros - 12 Meses',
            template='plotly_white',
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_anual, use_container_width=True)
        
        # Insights automáticos
        lucro_anual_projetado = sum([item['Lucro'] for item in projecao_anual])
        
        st.markdown(f"""
        <div class="insights-box">
            <h3>💡 Insights Estratégicos</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
                <div>
                    <h4>📊 Performance Financeira</h4>
                    <p>• <strong>Lucro Anual Projetado:</strong> R$ {lucro_anual_projetado:,.0f}</p>
                    <p>• <strong>ROI Anual:</strong> {roi_mensal * 12:.1f}%</p>
                    <p>• <strong>Margem Líquida:</strong> {margem_liquida:.1f}%</p>
                    <p>• <strong>Ponto de Equilíbrio:</strong> {ponto_equilibrio_horas:.0f}h/mês</p>
                </div>
                <div>
                    <h4>🎯 Recomendações</h4>
                    {"<p>• <strong style='color: #27AE60;'>Operação Rentável:</strong> Continue com esta estratégia</p>" if lucro_liquido > 0 else "<p>• <strong style='color: #E74C3C;'>Revisar Operação:</strong> Ajustes necessários</p>"}
                    <p>• <strong>Otimização:</strong> Aumentar ocupação para {min(100, taxa_ocupacao + 10)}%</p>
                    <p>• <strong>Expansão:</strong> {"Considerar segundo modelo" if roi_mensal > 3 else "Focar na eficiência atual"}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Análise de sensibilidade
        st.markdown("### 🔄 Análise de Sensibilidade")
        
        sensibilidade_data = []
        for ocupacao in [50, 60, 70, 80, 90, 100]:
            horas_sens = dias_operacao * horas_por_dia * (ocupacao / 100)
            custo_op_sens = resultado_hora['total'] * horas_sens
            receita_sens = params['preco_mercado_hora'][modelo_base] * horas_sens
            lucro_sens = receita_sens - custo_op_sens - custo_fixo_mensal
            
            sensibilidade_data.append({
                'Ocupação': f"{ocupacao}%",
                'Horas': horas_sens,
                'Lucro': lucro_sens,
                'ROI': (lucro_sens / (custo_op_sens + custo_fixo_mensal) * 100) if (custo_op_sens + custo_fixo_mensal) > 0 else 0
            })
        
        df_sensibilidade = pd.DataFrame(sensibilidade_data)
        
        fig_sens = go.Figure()
        
        fig_sens.add_trace(go.Scatter(
            x=df_sensibilidade['Ocupação'],
            y=df_sensibilidade['Lucro'],
            mode='lines+markers',
            name='Lucro',
            line=dict(color='#27AE60', width=4),
            marker=dict(size=10, color='#27AE60'),
            hovertemplate='Ocupação: %{x}<br>Lucro: R$ %{y:,.0f}<extra></extra>'
        ))
        
        # Linha de break-even
        fig_sens.add_hline(y=0, line_dash="dash", line_color="red", 
                          annotation_text="Break-even")
        
        fig_sens.update_layout(
            title='🎯 Sensibilidade: Lucro vs. Taxa de Ocupação',
            xaxis_title='Taxa de Ocupação',
            yaxis_title='Lucro Mensal (R$)',
            template='plotly_white',
            height=400
        )
        
        st.plotly_chart(fig_sens, use_container_width=True)
        
        # Exportação de relatórios
        st.markdown("---")
        st.markdown("## 📄 Exportar Análise")
        
        col1, col2 = st.columns(2)
        
        # Preparar dados para exportação
        dados_relatorio = {
            "Análise": "Projeção de Lucros Mensais",
            "Data": datetime.now().strftime("%d/%m/%Y"),
            "Modelo": modelo_base,
            "Dias Operação": dias_operacao,
            "Horas por Dia": horas_por_dia,
            "Taxa Ocupação": f"{taxa_ocupacao}%",
            "Horas Totais Mês": f"{horas_totais_mes:.0f}",
            "Receita Bruta": receita_bruta_mes,
            "Custo Operacional": custo_operacional_mes,
            "Custos Fixos": custo_fixo_mensal,
            "Custo Total": custo_total_mes,
            "Lucro Líquido": lucro_liquido,
            "Margem Líquida": f"{margem_liquida:.1f}%",
            "ROI Mensal": f"{roi_mensal:.1f}%",
            "ROI Anual Projetado": f"{roi_mensal * 12:.1f}%",
            "Ponto Equilíbrio": f"{ponto_equilibrio_horas:.0f} horas/mês",
            "Lucro Anual Projetado": lucro_anual_projetado
        }
        
        with col1:
            try:
                pdf_buffer = BytesIO()
                if gerar_pdf(pdf_buffer, dados_relatorio):
                    pdf_buffer.seek(0)
                    st.download_button(
                        "📄 Relatório PDF",
                        data=pdf_buffer.getvalue(),
                        file_name=f"amaro_lucros_mensais_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")
        
        with col2:
            try:
                excel_buffer = BytesIO()
                if gerar_excel(excel_buffer, dados_relatorio):
                    excel_buffer.seek(0)
                    st.download_button(
                        "📊 Planilha Excel",
                        data=excel_buffer.getvalue(),
                        file_name=f"amaro_lucros_mensais_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Erro ao gerar Excel: {e}")
        
    except Exception as e:
        st.error(f"Erro na análise: {e}")

# Sidebar com informações
with st.sidebar:
    st.markdown("### 📊 Guia de Análise")
    
    st.info("""
    **🎯 Como Usar:**
    1. Configure parâmetros operacionais
    2. Escolha cenário de análise
    3. Execute análise completa
    4. Revise insights e recomendações
    5. Exporte relatórios
    
    **📈 Métricas Principais:**
    - **ROI**: Retorno sobre investimento
    - **Margem Líquida**: Lucro/Receita
    - **Ponto Equilíbrio**: Horas para cobrir custos fixos
    - **Ocupação**: % de utilização da aeronave
    """)
    
    st.markdown("### 💡 Dicas Estratégicas")
    
    st.success("""
    **🚀 Otimização:**
    - Mantenha ocupação > 70%
    - ROI mensal > 2%
    - Margem líquida > 15%
    - Monitore sazonalidade
    """)
    
    if 'lucro_liquido' in locals():
        if lucro_liquido > 0:
            st.success(f"✅ **Operação Rentável**\nLucro: R$ {lucro_liquido:,.0f}")
        else:
            st.warning(f"⚠️ **Revisar Estratégia**\nPrejuízo: R$ {abs(lucro_liquido):,.0f}")
    
    st.markdown("### 📞 Suporte")
    st.markdown("""
    Para otimização operacional:
    **Equipe Técnica Amaro**
    📧 operacoes@amaroaviation.com
    """)