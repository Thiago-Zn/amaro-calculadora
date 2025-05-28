"""
CORREÇÃO DIRETA - Página sem HTML problemático
"""

import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config.theme import load_theme
from config.idiomas import get_text
from components.sidebar import render_sidebar
from components.status import render_system_status, render_calculation_status
from utils.params import load_params, format_currency, format_percentage
from utils.calculations import calcular_lucro_mensal_charter
from utils.export_manager import botao_download_inteligente, criar_relatorio_dados

# Configuração da página
st.set_page_config(
    page_title="Estimativa de Lucro | Amaro Aviation",
    page_icon="📈",
    layout="wide"
)

# Carregamento do tema
load_theme()

# Sidebar e idioma
lang = render_sidebar()

# Header SIMPLES sem HTML
st.markdown("# 📈 Estimativa de Lucro")
st.markdown("*Análise de rentabilidade mensal com operação charter*")
st.markdown("---")

# Carregar parâmetros
try:
    params = load_params()
    system_ok = render_system_status(params, lang)  # NÃO exibe mais nada
    
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

# Interface principal - SEM HTML
st.markdown("### 💰 Estimativa de Lucro")

# Formulário de entrada
col1, col2, col3, col4 = st.columns(4)

with col1:
    modelo_selecionado = st.selectbox(
        "Modelo da Aeronave",
        modelos,
        key="modelo_lucro"
    )

with col2:
    horas_charter = st.number_input(
        "Horas de Charter/mês",
        min_value=10,
        max_value=200,
        value=80,
        step=10
    )

with col3:
    taxa_ocupacao = st.slider(
        "Taxa de Ocupação (%)",
        min_value=50,
        max_value=95,
        value=75
    )

with col4:
    preco_hora_charter = st.number_input(
        "Preço Hora Charter (R$)",
        value=float(params['preco_mercado_hora'].get(modelo_selecionado, 8000)),
        step=500.0
    )

# Botão de cálculo
if st.button("🚀 Calcular", type="primary", use_container_width=True):
    try:
        resultado = calcular_lucro_mensal_charter(
            modelo=modelo_selecionado,
            horas_charter=horas_charter,
            taxa_ocupacao=taxa_ocupacao,
            preco_hora=preco_hora_charter,
            params=params
        )
        
        # Separador
        st.markdown("---")
        st.markdown("### 📊 Análise de Projeção")
        
        # KPIs usando métricas nativas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Receita Bruta Mensal",
                format_currency(resultado['receita_bruta'], lang)
            )
        
        with col2:
            st.metric(
                "Receita do Proprietário (90%)",
                format_currency(resultado['receita_proprietario'], lang)
            )
        
        with col3:
            delta_value = f"+{resultado['roi_mensal']:.1f}%" if resultado['lucro_liquido'] > 0 else None
            st.metric(
                "Lucro Líquido",
                format_currency(resultado['lucro_liquido'], lang),
                delta=delta_value
            )
        
        with col4:
            st.metric(
                "ROI Mensal",
                format_percentage(resultado['roi_mensal'], lang)
            )
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Composição de Receitas")
            
            fig_receita = go.Figure(data=[go.Pie(
                labels=["Receita do Proprietário", "Taxa Amaro (10%)"],
                values=[resultado['receita_proprietario'], resultado['taxa_amaro']],
                hole=0.5,
                marker=dict(colors=['#10B981', '#8C1D40']),
                textinfo='label+percent',
                textfont=dict(size=12)
            )])
            
            fig_receita.update_layout(
                height=300,
                showlegend=True,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(color='#1F2937')
            )
            
            st.plotly_chart(fig_receita, use_container_width=True)
        
        with col2:
            st.markdown("#### 💸 Breakdown de Custos Operacionais")
            
            custos_labels = ["Combustível", "Tripulação", "Manutenção", "Depreciação"]
            custos_values = [
                resultado['breakdown_custos']['combustivel'],
                resultado['breakdown_custos']['tripulacao'],
                resultado['breakdown_custos']['manutencao'],
                resultado['breakdown_custos']['depreciacao']
            ]
            
            fig_custos = go.Figure(data=[go.Bar(
                y=custos_labels,
                x=custos_values,
                orientation='h',
                text=[format_currency(v, lang) for v in custos_values],
                textposition='auto',
                marker_color=['#EF4444', '#F59E0B', '#3B82F6', '#10B981']
            )])
            
            fig_custos.update_layout(
                height=300,
                xaxis_title="Valor (R$)",
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(color='#1F2937')
            )
            
            st.plotly_chart(fig_custos, use_container_width=True)
        
        # Status da operação
        render_calculation_status(
            is_profitable=resultado['lucrativo'],
            profit_value=resultado['lucro_liquido'],
            message="O proprietário terá um lucro líquido de" if resultado['lucrativo'] and lang == 'pt'
                    else "The owner will have a net profit of" if resultado['lucrativo']
                    else "A operação apresenta déficit de" if lang == 'pt'
                    else "The operation shows a deficit of",
            lang=lang
        )
        
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
        
        # Botão de exportação
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        
        with col2:
            botao_download_inteligente(
                relatorio_dados,
                "📊 Exportar",
                'excel',
                'estimativa_lucro_mensal'
            )
        
    except Exception as e:
        st.error(f"❌ Erro no cálculo: {e}")
        st.info("💡 Verifique se todos os parâmetros estão configurados corretamente")

# Informações adicionais
with st.expander("💡 Dicas e Informações"):
    st.markdown("""
    **Como interpretar os resultados:**
    
    - **Receita Bruta**: Total faturado com as horas de charter
    - **Receita do Proprietário**: 90% da receita bruta (padrão Amaro)
    - **Taxa Amaro**: 10% da receita bruta para gestão
    - **ROI Mensal**: Retorno sobre o investimento operacional
    
    **Dicas para otimização:**
    
    - Mantenha taxa de ocupação acima de 70%
    - Ajuste preços conforme demanda sazonal
    - Monitore custos de combustível regularmente
    - Considere rotas mais eficientes
    """)

# Footer simples
st.markdown("---")
st.markdown("**📈 Estimativa de Lucro** - Análise detalhada de rentabilidade")