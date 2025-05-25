import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.params import load_params
from utils.calculations import calcula_custo_trecho
from utils.exportador_pdf import gerar_pdf
from utils.exportador_excel import gerar_excel
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="Análise Comparativa - Amaro Aviation", 
    layout="wide",
    page_icon="📊"
)

# CSS Premium
st.markdown("""
<style>
.comparison-header {
    background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%);
    color: white;
    padding: 2.5rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(140, 29, 64, 0.3);
}

.comparison-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    border: 1px solid #e9ecef;
    margin: 1rem 0;
    transition: all 0.3s ease;
}

.winner-card {
    background: linear-gradient(135deg, #E8F5E8 0%, #F1F9F1 100%);
    border: 3px solid #27AE60;
    border-radius: 15px;
    padding: 2rem;
    margin: 1rem 0;
    position: relative;
}

.winner-card::before {
    content: "🏆";
    position: absolute;
    top: -15px;
    right: 20px;
    font-size: 2rem;
    background: #27AE60;
    border-radius: 50%;
    padding: 0.5rem;
}

.competitor-card {
    background: linear-gradient(135deg, #FFF3CD 0%, #FCF8E3 100%);
    border: 2px solid #F39C12;
    border-radius: 15px;
    padding: 2rem;
    margin: 1rem 0;
}

.disadvantage-card {
    background: linear-gradient(135deg, #F8D7DA 0%, #FDEAEA 100%);
    border: 2px solid #E74C3C;
    border-radius: 15px;
    padding: 2rem;
    margin: 1rem 0;
}

.savings-highlight {
    background: linear-gradient(135deg, #27AE60 0%, #2ECC71 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin: 2rem 0;
    box-shadow: 0 8px 25px rgba(39, 174, 96, 0.3);
}

.comparison-metric {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    border-left: 5px solid #3498DB;
    margin: 1rem 0;
    text-align: center;
}

.benchmark-box {
    background: linear-gradient(135deg, #E8F4FD 0%, #F1F9FF 100%);
    border: 2px solid #3498DB;
    border-radius: 15px;
    padding: 2rem;
    margin: 2rem 0;
}

.tco-analysis {
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
<div class="comparison-header">
    <h1 style="margin: 0; font-size: 2.5rem;">📊 Análise Comparativa de Economia</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.2rem;">Benchmarking Avançado e Análise de Custo Total de Propriedade (TCO)</p>
</div>
""", unsafe_allow_html=True)

# Carregamento de parâmetros
try:
    params = load_params()
    modelos = params.get('modelos_disponiveis', [])
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# Configuração da análise comparativa
st.markdown("## 🔍 Configuração da Análise Comparativa")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="comparison-card">
        <h3>📋 Parâmetros de Comparação</h3>
        <p>Configure cenários para análise comparativa completa</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs para diferentes tipos de análise
    tab1, tab2, tab3, tab4 = st.tabs(["⚖️ Cenários", "🏢 Concorrentes", "💰 TCO", "📈 Benchmarking"])
    
    with tab1:
        st.markdown("### ⚖️ Cenários de Comparação")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            modelo_analise = st.selectbox(
                "🛩️ Modelo para Análise",
                modelos,
                help="Modelo principal para comparação"
            )
            
            horas_anuais = st.number_input(
                "⏰ Horas de Voo/Ano",
                min_value=50,
                max_value=1000,
                value=300,
                step=25,
                help="Horas anuais de utilização"
            )
            
            periodo_analise = st.selectbox(
                "📅 Período de Análise",
                ["1 ano", "3 anos", "5 anos", "10 anos"],
                index=2
            )
        
        with col_b:
            cenario_uso = st.selectbox(
                "🎯 Perfil de Uso",
                ["Executivo Pessoal", "Empresa Pequena", "Empresa Média", 
                 "Empresa Grande", "Charter/Táxi Aéreo"],
                index=1
            )
            
            sazonalidade = st.slider(
                "📊 Variação Sazonal (%)",
                min_value=0,
                max_value=50,
                value=20,
                help="Variação de demanda entre alta/baixa temporada"
            )
            
            crescimento_demanda = st.slider(
                "📈 Crescimento Anual (%)",
                min_value=-10,
                max_value=30,
                value=5,
                help="Crescimento esperado da demanda"
            )
        
        with col_c:
            inflacao_anual = st.slider(
                "📊 Inflação Anual (%)",
                min_value=2,
                max_value=15,
                value=6,
                help="Inflação esperada para ajuste de custos"
            )
            
            taxa_desconto = st.slider(
                "💰 Taxa de Desconto (%)",
                min_value=5,
                max_value=20,
                value=12,
                help="Taxa para valor presente líquido"
            )
            
            incluir_impostos = st.checkbox(
                "🏛️ Incluir Impostos",
                value=True,
                help="Considerar impostos na análise"
            )
    
    with tab2:
        st.markdown("### 🏢 Análise Competitiva")
        
        # Dados dos concorrentes (simulados baseados no mercado real)
        concorrentes_data = {
            "Flex": {"markup": 1.15, "qualidade": 8.5, "pontualidade": 85},
            "Avistar": {"markup": 1.10, "qualidade": 8.0, "pontualidade": 80},
            "Charter Premium": {"markup": 1.25, "qualidade": 9.0, "pontualidade": 90},
            "Operador Regional": {"markup": 0.95, "qualidade": 7.0, "pontualidade": 75}
        }
        
        col_comp1, col_comp2 = st.columns(2)
        
        with col_comp1:
            concorrentes_selecionados = st.multiselect(
                "🏆 Concorrentes para Comparação",
                list(concorrentes_data.keys()),
                default=["Flex", "Charter Premium"],
                help="Selecione concorrentes para benchmarking"
            )
            
            incluir_terceirizacao = st.checkbox(
                "🤝 Incluir Terceirização Completa",
                value=True,
                help="Comparar com terceirização total vs. operação própria"
            )
        
        with col_comp2:
            fatores_comparacao = st.multiselect(
                "📊 Fatores de Comparação",
                ["Preço", "Qualidade", "Pontualidade", "Flexibilidade", 
                 "Disponibilidade", "Suporte", "Tecnologia"],
                default=["Preço", "Qualidade", "Pontualidade"],
                help="Aspectos a serem comparados"
            )
            
            peso_preco = st.slider(
                "💰 Peso do Preço na Decisão (%)",
                min_value=20,
                max_value=80,
                value=60,
                help="Importância do preço na decisão final"
            )
    
    with tab3:
        st.markdown("### 💰 Análise de TCO (Total Cost of Ownership)")
        
        col_tco1, col_tco2 = st.columns(2)
        
        with col_tco1:
            incluir_aquisicao = st.checkbox(
                "✈️ Incluir Custo de Aquisição",
                value=False,
                help="Comparar compra vs. locação/charter"
            )
            
            if incluir_aquisicao:
                valor_aeronave = st.number_input(
                    "💵 Valor da Aeronave (R$)",
                    min_value=5000000,
                    max_value=100000000,
                    value=25000000,
                    step=1000000
                )
                
                financiamento_pct = st.slider(
                    "🏦 % Financiamento",
                    min_value=0,
                    max_value=80,
                    value=70
                )
                
                taxa_juros = st.slider(
                    "📈 Taxa de Juros (%)",
                    min_value=8,
                    max_value=20,
                    value=12
                )
        
        with col_tco2:
            custos_adicionais = st.multiselect(
                "💼 Custos Adicionais",
                ["Hangar", "Seguro Completo", "Tripulação Dedicada", 
                 "Manutenção Preventiva Plus", "Upgrade de Sistemas"],
                default=["Hangar", "Seguro Completo"]
            )
            
            valor_revenda_pct = st.slider(
                "💰 Valor de Revenda (% do original)",
                min_value=30,
                max_value=80,
                value=60,
                help="Valor residual após período de análise"
            ) if incluir_aquisicao else 0
    
    with tab4:
        st.markdown("### 📈 Benchmarking de Mercado")
        
        col_bench1, col_bench2 = st.columns(2)
        
        with col_bench1:
            referencias_mercado = st.multiselect(
                "📊 Referências de Mercado",
                ["ABAG (Associação Brasileira de Aviação Geral)",
                 "ANAC - Dados Setoriais", "Consultoria Especializada",
                 "Benchmarks Internacionais"],
                default=["ABAG (Associação Brasileira de Aviação Geral)"]
            )
            
            ajuste_regional = st.selectbox(
                "🌍 Ajuste Regional",
                ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"],
                help="Ajustar preços conforme região"
            )
        
        with col_bench2:
            nivel_servico = st.selectbox(
                "⭐ Nível de Serviço",
                ["Básico", "Executivo", "Premium", "Ultra Premium"],
                index=1
            )
            
            incluir_tendencias = st.checkbox(
                "📈 Incluir Tendências de Mercado",
                value=True,
                help="Considerar tendências e projeções do setor"
            )

with col2:
    # Resumo da configuração
    st.markdown("""
    <div class="comparison-card">
        <h4>📋 Resumo da Análise</h4>
    """, unsafe_allow_html=True)
    
    if modelo_analise:
        resultado_base = calcula_custo_trecho(modelo_analise, 1.0, params)
        custo_base_anual = resultado_base['total'] * horas_anuais
        mercado_base_anual = params['preco_mercado_hora'][modelo_analise] * horas_anuais
        economia_base_anual = mercado_base_anual - custo_base_anual
        
        st.write(f"**Modelo:** {modelo_analise}")
        st.write(f"**Horas/Ano:** {horas_anuais}")
        st.write(f"**Período:** {periodo_analise}")
        st.write(f"**Perfil:** {cenario_uso}")
        st.write(f"**Custo Anual Amaro:** R$ {custo_base_anual:,.0f}")
        st.write(f"**Preço Mercado:** R$ {mercado_base_anual:,.0f}")
        st.write(f"**Economia Anual:** R$ {economia_base_anual:,.0f}")
        
        # Indicador visual
        economia_pct = (economia_base_anual / mercado_base_anual * 100) if mercado_base_anual > 0 else 0
        if economia_pct > 20:
            st.success(f"✅ Economia: {economia_pct:.1f}%")
        elif economia_pct > 10:
            st.warning(f"⚠️ Economia: {economia_pct:.1f}%")
        else:
            st.error(f"❌ Economia: {economia_pct:.1f}%")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Execução da análise comparativa
if st.button("🚀 Executar Análise Comparativa Completa", type="primary", use_container_width=True):
    try:
        # Cálculos base
        resultado_amaro = calcula_custo_trecho(modelo_analise, 1.0, params)
        preco_hora_amaro = resultado_amaro['total']
        preco_hora_mercado = params['preco_mercado_hora'][modelo_analise]
        
        st.markdown("---")
        st.markdown("## 📊 Análise Comparativa Detalhada")
        
        # 1. Comparação com Concorrentes
        st.markdown("### 🏆 Comparação com Concorrentes")
        
        # Preparar dados de comparação
        comparacao_data = []
        
        # Amaro Aviation
        comparacao_data.append({
            'Empresa': 'Amaro Aviation',
            'Preço/Hora': preco_hora_amaro,
            'Qualidade': 9.5,
            'Pontualidade': 95,
            'Flexibilidade': 90,
            'Tipo': 'Amaro',
            'Score_Total': 0  # Calculado depois
        })
        
        # Concorrentes
        for concorrente in concorrentes_selecionados:
            data = concorrentes_data[concorrente]
            preco_concorrente = preco_hora_mercado * data['markup']
            
            comparacao_data.append({
                'Empresa': concorrente,
                'Preço/Hora': preco_concorrente,
                'Qualidade': data['qualidade'],
                'Pontualidade': data['pontualidade'],
                'Flexibilidade': data['qualidade'] * 8,  # Estimativa
                'Tipo': 'Concorrente',
                'Score_Total': 0
            })
        
        # Terceirização completa
        if incluir_terceirizacao:
            preco_terceirizacao = preco_hora_mercado * 1.05  # 5% markup
            comparacao_data.append({
                'Empresa': 'Terceirização Total',
                'Preço/Hora': preco_terceirizacao,
                'Qualidade': 8.0,
                'Pontualidade': 85,
                'Flexibilidade': 70,
                'Tipo': 'Terceirização',
                'Score_Total': 0
            })
        
        # Calcular score total ponderado
        for item in comparacao_data:
            # Normalizar preço (menor é melhor)
            preco_min = min([d['Preço/Hora'] for d in comparacao_data])
            preco_max = max([d['Preço/Hora'] for d in comparacao_data])
            score_preco = (preco_max - item['Preço/Hora']) / (preco_max - preco_min) * 100 if preco_max > preco_min else 100
            
            # Score total ponderado
            item['Score_Total'] = (
                score_preco * (peso_preco / 100) +
                item['Qualidade'] * 10 * ((100 - peso_preco) / 300) +
                item['Pontualidade'] * ((100 - peso_preco) / 300) +
                item['Flexibilidade'] * ((100 - peso_preco) / 300)
            )
        
        df_comparacao = pd.DataFrame(comparacao_data)
        
        # Exibir comparação
        melhor_opcao = df_comparacao.loc[df_comparacao['Score_Total'].idxmax()]
        
        for _, row in df_comparacao.iterrows():
            if row['Empresa'] == melhor_opcao['Empresa']:
                card_class = "winner-card"
                badge = "🏆 MELHOR OPÇÃO"
            elif row['Tipo'] == 'Amaro':
                card_class = "comparison-card"
                badge = "🛩️ AMARO AVIATION"
            else:
                card_class = "competitor-card"
                badge = "🏢 CONCORRENTE"
            
            economia_vs_amaro = ((row['Preço/Hora'] - preco_hora_amaro) / preco_hora_amaro * 100) if preco_hora_amaro > 0 else 0
            economia_anual_vs_amaro = (row['Preço/Hora'] - preco_hora_amaro) * horas_anuais
            
            st.markdown(f"""
            <div class="{card_class}">
                <h4>{badge} - {row['Empresa']}</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr 1fr; gap: 1rem; margin: 1rem 0;">
                    <div><strong>Preço/Hora:</strong><br>R$ {row['Preço/Hora']:,.0f}</div>
                    <div><strong>Qualidade:</strong><br>{row['Qualidade']:.1f}/10</div>
                    <div><strong>Pontualidade:</strong><br>{row['Pontualidade']:.0f}%</div>
                    <div><strong>Score Total:</strong><br>{row['Score_Total']:.1f}</div>
                    <div><strong>vs. Amaro:</strong><br>{"+" if economia_vs_amaro > 0 else ""}{economia_vs_amaro:+.1f}%</div>
                </div>
                <p><strong>Impacto Anual vs. Amaro:</strong> {"R$ " if economia_anual_vs_amaro >= 0 else "-R$ "}{abs(economia_anual_vs_amaro):,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráfico radar de comparação
        fig_radar = go.Figure()
        
        categorias = ['Preço', 'Qualidade', 'Pontualidade', 'Flexibilidade']
        
        for _, row in df_comparacao.iterrows():
            # Normalizar valores para o radar
            valores_norm = [
                (max(df_comparacao['Preço/Hora']) - row['Preço/Hora']) / 
                (max(df_comparacao['Preço/Hora']) - min(df_comparacao['Preço/Hora'])) * 100 
                if max(df_comparacao['Preço/Hora']) > min(df_comparacao['Preço/Hora']) else 100,  # Preço (inverso)
                row['Qualidade'] * 10,  # Qualidade
                row['Pontualidade'],  # Pontualidade
                row['Flexibilidade']  # Flexibilidade
            ]
            
            cor = '#27AE60' if row['Tipo'] == 'Amaro' else '#3498DB' if row['Tipo'] == 'Concorrente' else '#F39C12'
            
            fig_radar.add_trace(go.Scatterpolar(
                r=valores_norm,
                theta=categorias,
                fill='toself',
                name=row['Empresa'],
                line_color=cor,
                fillcolor=cor,
                opacity=0.6 if row['Tipo'] == 'Amaro' else 0.3
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            title="🎯 Análise Multidimensional de Competitividade",
            template='plotly_white',
            height=500
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
        
        # 2. Análise de TCO (Total Cost of Ownership)
        st.markdown("### 💰 Análise de TCO - Total Cost of Ownership")
        
        periodo_anos = int(periodo_analise.split()[0])
        
        # Projeções de custo
        tco_data = []
        
        for ano in range(1, periodo_anos + 1):
            # Ajustes anuais
            fator_inflacao = (1 + inflacao_anual/100) ** ano
            fator_crescimento = (1 + crescimento_demanda/100) ** ano
            horas_ano_ajustado = horas_anuais * fator_crescimento
            
            # Custos Amaro
            custo_operacional_amaro = preco_hora_amaro * horas_ano_ajustado * fator_inflacao
            custos_adicionais_valor = 0
            
            if 'Hangar' in custos_adicionais:
                custos_adicionais_valor += 60000 * fator_inflacao
            if 'Seguro Completo' in custos_adicionais:
                custos_adicionais_valor += 80000 * fator_inflacao
            if 'Tripulação Dedicada' in custos_adicionais:
                custos_adicionais_valor += 200000 * fator_inflacao
            if 'Manutenção Preventiva Plus' in custos_adicionais:
                custos_adicionais_valor += 40000 * fator_inflacao
            if 'Upgrade de Sistemas' in custos_adicionais:
                custos_adicionais_valor += 30000 * fator_inflacao
            
            tco_amaro = custo_operacional_amaro + custos_adicionais_valor
            
            # Custos Mercado
            custo_mercado = preco_hora_mercado * horas_ano_ajustado * fator_inflacao
            
            # Custos Terceirização
            custo_terceirizacao = preco_hora_mercado * 1.05 * horas_ano_ajustado * fator_inflacao
            
            # Custo de Aquisição (se aplicável)
            custo_aquisicao = 0
            if incluir_aquisicao and ano == 1:
                valor_entrada = valor_aeronave * (1 - financiamento_pct/100)
                custo_aquisicao = valor_entrada
                
                # Financiamento
                if financiamento_pct > 0:
                    valor_financiado = valor_aeronave * (financiamento_pct/100)
                    # Parcela anual do financiamento (simplificado)
                    parcela_anual = valor_financiado * (taxa_juros/100) / (1 - (1 + taxa_juros/100)**(-periodo_anos))
                    tco_amaro += parcela_anual
            
            tco_data.append({
                'Ano': ano,
                'TCO_Amaro': tco_amaro,
                'TCO_Mercado': custo_mercado,
                'TCO_Terceirizacao': custo_terceirizacao,
                'Economia_vs_Mercado': custo_mercado - tco_amaro,
                'Economia_vs_Terceirizacao': custo_terceirizacao - tco_amaro,
                'Horas': horas_ano_ajustado
            })
        
        df_tco = pd.DataFrame(tco_data)
        
        # Valor presente líquido
        df_tco['VPL_Amaro'] = df_tco['TCO_Amaro'] / (1 + taxa_desconto/100) ** df_tco['Ano']
        df_tco['VPL_Mercado'] = df_tco['TCO_Mercado'] / (1 + taxa_desconto/100) ** df_tco['Ano']
        df_tco['VPL_Terceirizacao'] = df_tco['TCO_Terceirizacao'] / (1 + taxa_desconto/100) ** df_tco['Ano']
        
        # Totais
        vpl_total_amaro = df_tco['VPL_Amaro'].sum()
        vpl_total_mercado = df_tco['VPL_Mercado'].sum()
        vpl_total_terceirizacao = df_tco['VPL_Terceirizacao'].sum()
        
        # Valor residual (se houve aquisição)
        if incluir_aquisicao:
            valor_residual = valor_aeronave * (valor_revenda_pct/100)
            vpl_valor_residual = valor_residual / (1 + taxa_desconto/100) ** periodo_anos
            vpl_total_amaro -= vpl_valor_residual  # Diminui o custo
        
        # Exibir resultados TCO
        col1, col2, col3 = st.columns(3)
        
        with col1:
            economia_total_mercado = vpl_total_mercado - vpl_total_amaro
            st.markdown(f"""
            <div class="comparison-metric">
                <h4>🛩️ Amaro Aviation</h4>
                <h2>R$ {vpl_total_amaro:,.0f}</h2>
                <p>VPL {periodo_anos} anos</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="comparison-metric">
                <h4>🏪 Mercado Tradicional</h4>
                <h2>R$ {vpl_total_mercado:,.0f}</h2>
                <p>Economia: R$ {economia_total_mercado:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            economia_total_terceirizacao = vpl_total_terceirizacao - vpl_total_amaro
            st.markdown(f"""
            <div class="comparison-metric">
                <h4>🤝 Terceirização</h4>
                <h2>R$ {vpl_total_terceirizacao:,.0f}</h2>
                <p>Economia: R$ {economia_total_terceirizacao:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráfico de evolução TCO
        fig_tco = go.Figure()
        
        fig_tco.add_trace(go.Scatter(
            x=df_tco['Ano'],
            y=df_tco['TCO_Amaro'].cumsum(),
            mode='lines+markers',
            name='Amaro Aviation',
            line=dict(color='#27AE60', width=4),
            marker=dict(size=8),
            fill='tonexty',
            fillcolor='rgba(39, 174, 96, 0.1)'
        ))
        
        fig_tco.add_trace(go.Scatter(
            x=df_tco['Ano'],
            y=df_tco['TCO_Mercado'].cumsum(),
            mode='lines+markers',
            name='Mercado Tradicional',
            line=dict(color='#E74C3C', width=4),
            marker=dict(size=8)
        ))
        
        fig_tco.add_trace(go.Scatter(
            x=df_tco['Ano'],
            y=df_tco['TCO_Terceirizacao'].cumsum(),
            mode='lines+markers',
            name='Terceirização',
            line=dict(color='#F39C12', width=4),
            marker=dict(size=8)
        ))
        
        fig_tco.update_layout(
            title=f'📈 Evolução do TCO - Total Cost of Ownership ({periodo_anos} anos)',
            xaxis_title='Anos',
            yaxis_title='Custo Acumulado (R$)',
            template='plotly_white',
            height=500,
            yaxis_tickformat=',.0f'
        )
        
        st.plotly_chart(fig_tco, use_container_width=True)
        
        # 3. Análise de Break-even
        st.markdown("### ⚖️ Análise de Break-even")
        
        # Calcular ponto de equilíbrio
        economia_por_hora = preco_hora_mercado - preco_hora_amaro
        
        if incluir_aquisicao:
            investimento_inicial = valor_aeronave * (1 - financiamento_pct/100)
            break_even_horas = investimento_inicial / economia_por_hora if economia_por_hora > 0 else float('inf')
            break_even_anos = break_even_horas / horas_anuais if horas_anuais > 0 else float('inf')
        else:
            break_even_horas = 0
            break_even_anos = 0
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de break-even
            if break_even_anos < 20:  # Só mostrar se for viável
                anos_analise = list(range(0, min(int(break_even_anos) + 3, 20)))
                economia_acumulada = [ano * horas_anuais * economia_por_hora for ano in anos_analise]
                investimento_linha = [investimento_inicial if incluir_aquisicao else 0] * len(anos_analise)
                
                fig_break = go.Figure()
                
                fig_break.add_trace(go.Scatter(
                    x=anos_analise,
                    y=economia_acumulada,
                    mode='lines+markers',
                    name='Economia Acumulada',
                    line=dict(color='#27AE60', width=4),
                    fill='tonexty',
                    fillcolor='rgba(39, 174, 96, 0.1)'
                ))
                
                if incluir_aquisicao:
                    fig_break.add_trace(go.Scatter(
                        x=anos_analise,
                        y=investimento_linha,
                        mode='lines',
                        name='Investimento Inicial',
                        line=dict(color='#E74C3C', width=3, dash='dash')
                    ))
                    
                    # Ponto de break-even
                    fig_break.add_trace(go.Scatter(
                        x=[break_even_anos],
                        y=[investimento_inicial],
                        mode='markers',
                        name='Break-even',
                        marker=dict(size=15, color='#F39C12', symbol='star')
                    ))
                
                fig_break.update_layout(
                    title='⚖️ Análise de Break-even',
                    xaxis_title='Anos',
                    yaxis_title='Valor (R$)',
                    template='plotly_white',
                    height=400
                )
                
                st.plotly_chart(fig_break, use_container_width=True)
        
        with col2:
            st.markdown(f"""
            <div class="benchmark-box">
                <h4>📊 Métricas de Break-even</h4>
                <p><strong>Economia por Hora:</strong> R$ {economia_por_hora:,.0f}</p>
                <p><strong>Economia Anual:</strong> R$ {economia_por_hora * horas_anuais:,.0f}</p>
                {"<p><strong>Break-even:</strong> {:.1f} anos</p>".format(break_even_anos) if incluir_aquisicao and break_even_anos < 20 else ""}
                {"<p><strong>Horas Break-even:</strong> {:,.0f}h</p>".format(break_even_horas) if incluir_aquisicao and break_even_horas < 10000 else ""}
                <p><strong>ROI Anual:</strong> {:.1f}%</p>
            </div>
            """.format((economia_por_hora * horas_anuais / vpl_total_amaro * 100) if vpl_total_amaro > 0 else 0), 
            unsafe_allow_html=True)
        
        # 4. Resumo Executivo e Recomendações
        economia_percentual_total = (economia_total_mercado / vpl_total_mercado * 100) if vpl_total_mercado > 0 else 0
        
        if economia_percentual_total > 20:
            recomendacao = "🟢 ALTAMENTE RECOMENDADO"
            cor_recomendacao = "#27AE60"
            justificativa = "Economia significativa com excelente retorno sobre investimento"
        elif economia_percentual_total > 10:
            recomendacao = "🟡 RECOMENDADO COM RESSALVAS"
            cor_recomendacao = "#F39C12"
            justificativa = "Economia moderada, avaliar outros fatores estratégicos"
        else:
            recomendacao = "🔴 NÃO RECOMENDADO"
            cor_recomendacao = "#E74C3C"
            justificativa = "Economia insuficiente para justificar mudança"
        
        st.markdown(f"""
        <div class="savings-highlight">
            <h2 style="margin: 0;">{recomendacao}</h2>
            <h3 style="margin: 1rem 0;">Economia Total: R$ {economia_total_mercado:,.0f} ({economia_percentual_total:.1f}%)</h3>
            <p style="margin: 0; font-size: 1.1rem;">{justificativa}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabela resumo
        st.markdown("### 📋 Resumo Executivo")
        
        resumo_data = {
            "Métrica": [
                "Custo Hora Amaro Aviation",
                "Preço Hora Mercado Tradicional", 
                "Economia por Hora",
                "Economia Anual",
                f"VPL Total Amaro ({periodo_anos} anos)",
                f"VPL Total Mercado ({periodo_anos} anos)",
                "Economia Total (VPL)",
                "Percentual de Economia",
                "ROI Anual Médio",
                "Classificação"
            ],
            "Valor": [
                f"R$ {preco_hora_amaro:,.0f}",
                f"R$ {preco_hora_mercado:,.0f}",
                f"R$ {economia_por_hora:,.0f}",
                f"R$ {economia_por_hora * horas_anuais:,.0f}",
                f"R$ {vpl_total_amaro:,.0f}",
                f"R$ {vpl_total_mercado:,.0f}",
                f"R$ {economia_total_mercado:,.0f}",
                f"{economia_percentual_total:.1f}%",
                f"{(economia_por_hora * horas_anuais / vpl_total_amaro * 100):.1f}%" if vpl_total_amaro > 0 else "N/A",
                recomendacao.split()[1]
            ]
        }
        
        df_resumo = pd.DataFrame(resumo_data)
        
        st.dataframe(
            df_resumo.style.apply(
                lambda x: ['background-color: #E8F5E8' if 'Economia' in x['Métrica'] or 'ROI' in x['Métrica'] else '' for i in x], 
                axis=1
            ),
            use_container_width=True,
            hide_index=True
        )
        
        # Exportação
        st.markdown("---")
        st.markdown("## 📄 Exportar Análise Comparativa")
        
        col1, col2 = st.columns(2)
        
        # Preparar dados para exportação
        dados_comparacao = {
            "Análise": "Comparativo de Economia Completo",
            "Data": datetime.now().strftime("%d/%m/%Y"),
            "Modelo Analisado": modelo_analise,
            "Horas Anuais": horas_anuais,
            "Período Análise": periodo_analise,
            "Perfil Uso": cenario_uso,
            "Custo Hora Amaro": preco_hora_amaro,
            "Preço Hora Mercado": preco_hora_mercado,
            "Economia por Hora": economia_por_hora,
            "Economia Anual": economia_por_hora * horas_anuais,
            "VPL Total Amaro": vpl_total_amaro,
            "VPL Total Mercado": vpl_total_mercado,
            "Economia Total VPL": economia_total_mercado,
            "Percentual Economia": f"{economia_percentual_total:.1f}%",
            "Recomendação": recomendacao,
            "ROI Anual": f"{(economia_por_hora * horas_anuais / vpl_total_amaro * 100):.1f}%" if vpl_total_amaro > 0 else "N/A",
            "Break-even Anos": f"{break_even_anos:.1f}" if incluir_aquisicao and break_even_anos < 20 else "N/A",
            "Melhor Concorrente": melhor_opcao['Empresa'],
            "Score Melhor Opção": f"{melhor_opcao['Score_Total']:.1f}"
        }
        
        with col1:
            try:
                pdf_buffer = BytesIO()
                if gerar_pdf(pdf_buffer, dados_comparacao):
                    pdf_buffer.seek(0)
                    st.download_button(
                        "📄 Relatório Comparativo PDF",
                        data=pdf_buffer.getvalue(),
                        file_name=f"amaro_comparativo_economia_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Erro ao gerar PDF: {e}")
        
        with col2:
            try:
                excel_buffer = BytesIO()
                if gerar_excel(excel_buffer, dados_comparacao):
                    excel_buffer.seek(0)
                    st.download_button(
                        "📊 Planilha Comparativa",
                        data=excel_buffer.getvalue(),
                        file_name=f"amaro_comparativo_economia_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Erro ao gerar Excel: {e}")
        
    except Exception as e:
        st.error(f"Erro na análise comparativa: {e}")

# Sidebar com orientações
with st.sidebar:
    st.markdown("### 📊 Guia de Análise")
    
    st.info("""
    **🔍 Metodologia:**
    1. Configure cenários de comparação
    2. Selecione concorrentes relevantes
    3. Defina parâmetros de TCO
    4. Execute análise completa
    5. Analise recomendações
    
    **📈 Métricas Principais:**
    - **VPL**: Valor Presente Líquido
    - **TCO**: Total Cost of Ownership
    - **ROI**: Return on Investment
    - **Break-even**: Ponto de equilíbrio
    """)
    
    st.markdown("### 💡 Interpretação")
    
    st.success("""
    **🟢 Economia > 20%:**
    Altamente recomendado
    
    **🟡 Economia 10-20%:**
    Recomendado com análise
    
    **🔴 Economia < 10%:**
    Requer justificativa estratégica
    """)
    
    st.warning("""
    **⚠️ Considere Também:**
    - Qualidade do serviço
    - Pontualidade e confiabilidade
    - Flexibilidade operacional
    - Suporte técnico
    - Tendências de mercado
    """)
    
    st.markdown("### 📞 Consultoria")
    st.markdown("""
    Para análises personalizadas:
    **Análise Competitiva Amaro**
    📧 analise@amaroaviation.com
    📞 (11) 99999-7777
    """)