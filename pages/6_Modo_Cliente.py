import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.params import load_params
from utils.calculations import calcula_custo_trecho, calcular_projecao_mensal
from utils.charts import grafico_comparativo, grafico_composicao
from utils.exportador_pdf import gerar_pdf
from io import BytesIO
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Apresentação Cliente - Amaro Aviation", 
    layout="wide",
    page_icon="🎨"
)

# CSS Premium para modo cliente
st.markdown("""
<style>
.client-header {
    background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%);
    color: white;
    padding: 3rem 2rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(140, 29, 64, 0.3);
}

.client-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 30px rgba(0,0,0,0.1);
    border: 1px solid #e9ecef;
    margin: 1.5rem 0;
    transition: transform 0.3s ease;
}

.client-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.15);
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

.client-metric {
    background: white;
    border-radius: 15px;
    padding: 1.5rem;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    border-left: 5px solid #8c1d40;
    margin: 1rem 0;
    text-align: center;
}

.value-proposition {
    background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
    border: 2px solid #8c1d40;
    border-radius: 15px;
    padding: 2rem;
    margin: 2rem 0;
}

.cta-section {
    background: linear-gradient(135deg, #2C3E50 0%, #34495E 100%);
    color: white;
    padding: 3rem 2rem;
    border-radius: 20px;
    text-align: center;
    margin: 3rem 0;
}

.simple-form {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 6px 25px rgba(0,0,0,0.1);
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header cliente premium
st.markdown("""
<div class="client-header">
    <h1 style="margin: 0; font-size: 3rem;">✈️ Amaro Aviation</h1>
    <h2 style="margin: 1rem 0; opacity: 0.9;">Calculadora de Economia em Aviação Executiva</h2>
    <p style="margin: 0; font-size: 1.2rem; opacity: 0.8;">Descubra quanto você pode economizar conosco</p>
</div>
""", unsafe_allow_html=True)

# Carregamento de parâmetros
try:
    params = load_params()
    modelos = params.get('modelos_disponiveis', [])
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# Seção de entrada simplificada
st.markdown("## 🎯 Simule Sua Economia")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="simple-form">
        <h3>📋 Configure Sua Simulação</h3>
        <p>Preencha os dados abaixo para calcularmos sua economia personalizada</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Formulário simplificado
    col_a, col_b = st.columns(2)
    
    with col_a:
        modelo = st.selectbox(
            "🛩️ Tipo de Aeronave",
            modelos,
            help="Selecione o modelo que melhor atende suas necessidades"
        )
        
        # Rotas pré-definidas simplificadas
        rotas_populares = {
            "São Paulo → Rio de Janeiro": {"duracao": 1.0, "descricao": "Rota mais popular"},
            "São Paulo → Brasília": {"duracao": 1.4, "descricao": "Conexão executiva"},
            "Rio de Janeiro → Brasília": {"duracao": 1.7, "descricao": "Rota governamental"},
            "São Paulo → Campinas": {"duracao": 0.5, "descricao": "Voo regional"},
            "Rota Personalizada": {"duracao": 1.0, "descricao": "Configure manualmente"}
        }
        
        rota_selecionada = st.selectbox(
            "🗺️ Rota",
            list(rotas_populares.keys()),
            help="Escolha sua rota ou configure uma personalizada"
        )
    
    with col_b:
        # Duração baseada na rota ou personalizada
        if rota_selecionada == "Rota Personalizada":
            duracao = st.number_input(
                "⏱️ Duração do Voo (horas)",
                min_value=0.1,
                max_value=10.0,
                value=1.0,
                step=0.1,
                help="Tempo total de voo"
            )
        else:
            duracao = rotas_populares[rota_selecionada]["duracao"]
            st.metric(
                "⏱️ Duração do Voo",
                f"{duracao} horas",
                help=rotas_populares[rota_selecionada]["descricao"]
            )
        
        voos_mes = st.number_input(
            "📅 Voos por Mês",
            min_value=1,
            max_value=50,
            value=4,
            step=1,
            help="Quantidade estimada de voos mensais"
        )

with col2:
    # Informações do modelo selecionado
    if modelo in params['consumo_modelos']:
        st.markdown("""
        <div class="client-card">
            <h4>📋 Informações da Aeronave</h4>
        """, unsafe_allow_html=True)
        
        consumo = params['consumo_modelos'][modelo]
        preco_mercado_hora = params['preco_mercado_hora'][modelo]
        tipo_aeronave = "Jato Executivo" if preco_mercado_hora > 10000 else "Turboprop"
        
        st.write(f"**Modelo:** {modelo}")
        st.write(f"**Categoria:** {tipo_aeronave}")
        st.write(f"**Consumo:** {consumo} L/h")
        st.write(f"**Preço Mercado:** R$ {preco_mercado_hora:,.0f}/h")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Botão de cálculo premium
if st.button("🚀 Calcular Minha Economia", type="primary", use_container_width=True):
    try:
        # Realizar cálculos
        resultado_voo = calcula_custo_trecho(modelo, duracao, params)
        
        # Resultados principais com destaque
        st.markdown("---")
        
        # Economia destacada
        economia_voo = resultado_voo['economia']
        economia_mensal = economia_voo * voos_mes
        economia_anual = economia_mensal * 12
        
        if economia_voo > 0:
            st.markdown(f"""
            <div class="savings-highlight">
                <h2 style="margin: 0;">💎 SUA ECONOMIA COM AMARO AVIATION</h2>
                <div style="display: flex; justify-content: space-around; margin-top: 2rem;">
                    <div>
                        <h3 style="margin: 0;">Por Voo</h3>
                        <h1 style="margin: 0.5rem 0;">R$ {economia_voo:,.0f}</h1>
                    </div>
                    <div>
                        <h3 style="margin: 0;">Por Mês</h3>
                        <h1 style="margin: 0.5rem 0;">R$ {economia_mensal:,.0f}</h1>
                    </div>
                    <div>
                        <h3 style="margin: 0;">Por Ano</h3>
                        <h1 style="margin: 0.5rem 0;">R$ {economia_anual:,.0f}</h1>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(f"""
            ⚠️ **Análise Personalizada Necessária**
            
            Para esta configuração específica, recomendamos uma análise detalhada. 
            Nossa equipe pode otimizar a operação para garantir a melhor relação custo-benefício.
            """)
        
        # Métricas comparativas
        st.markdown("## 📊 Comparativo Detalhado")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="client-metric">
                <h4>💰 Custo Amaro</h4>
            """, unsafe_allow_html=True)
            st.metric("", f"R$ {resultado_voo['total']:,.0f}", help="Custo total por voo")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="client-metric">
                <h4>🏪 Preço Mercado</h4>
            """, unsafe_allow_html=True)
            st.metric("", f"R$ {resultado_voo['preco_mercado']:,.0f}", help="Preço típico do mercado")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="client-metric">
                <h4>💎 Economia</h4>
            """, unsafe_allow_html=True)
            st.metric("", f"R$ {economia_voo:,.0f}", f"{resultado_voo['percentual_economia']:.1f}%")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="client-metric">
                <h4>📈 Margem</h4>
            """, unsafe_allow_html=True)
            margem = (economia_voo / resultado_voo['preco_mercado'] * 100) if resultado_voo['preco_mercado'] > 0 else 0
            st.metric("", f"{margem:.1f}%", help="Percentual de economia")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Gráficos visuais simplificados
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de comparação simples
            fig_comp = go.Figure()
            
            fig_comp.add_trace(go.Bar(
                name='Amaro Aviation',
                x=[''],
                y=[resultado_voo['total']],
                marker_color='#8c1d40',
                text=f'R$ {resultado_voo["total"]:,.0f}',
                textposition='outside',
                width=0.4
            ))
            
            fig_comp.add_trace(go.Bar(
                name='Mercado Tradicional',
                x=[''],
                y=[resultado_voo['preco_mercado']],
                marker_color='#95A5A6',
                text=f'R$ {resultado_voo["preco_mercado"]:,.0f}',
                textposition='outside',
                width=0.4
            ))
            
            fig_comp.update_layout(
                title='💰 Comparação de Preços por Voo',
                showlegend=True,
                height=400,
                template='plotly_white',
                yaxis_title='Valor (R$)',
                bargap=0.6
            )
            
            st.plotly_chart(fig_comp, use_container_width=True)
        
        with col2:
            # Projeção anual
            meses = list(range(1, 13))
            economia_acumulada = [economia_mensal * mes for mes in meses]
            
            fig_proj = go.Figure()
            
            fig_proj.add_trace(go.Scatter(
                x=meses,
                y=economia_acumulada,
                mode='lines+markers',
                name='Economia Acumulada',
                line=dict(color='#27AE60', width=4),
                marker=dict(size=8, color='#27AE60'),
                fill='tonexty',
                fillcolor='rgba(39, 174, 96, 0.1)'
            ))
            
            fig_proj.update_layout(
                title='📈 Projeção de Economia Anual',
                xaxis_title='Mês',
                yaxis_title='Economia Acumulada (R$)',
                height=400,
                template='plotly_white',
                yaxis_tickformat=',.0f'
            )
            
            st.plotly_chart(fig_proj, use_container_width=True)
        
        # Proposta de valor
        if economia_voo > 0:
            st.markdown(f"""
            <div class="value-proposition">
                <h3>🎯 Por Que Escolher a Amaro Aviation?</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 1.5rem;">
                    <div>
                        <h4>💡 Transparência Total</h4>
                        <p>Todos os custos são apresentados de forma clara e detalhada, sem surpresas ou taxas ocultas.</p>
                        
                        <h4>🛡️ Confiabilidade</h4>
                        <p>Operação com os mais altos padrões de segurança e pontualidade do mercado.</p>
                    </div>
                    <div>
                        <h4>💰 Economia Garantida</h4>
                        <p>Economia de até {resultado_voo['percentual_economia']:.1f}% comparado ao mercado tradicional.</p>
                        
                        <h4>✈️ Frota Moderna</h4>
                        <p>Aeronaves de última geração com máxima eficiência e conforto.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Exportação do relatório cliente
        st.markdown("---")
        st.markdown("## 📄 Leve Esta Análise Com Você")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Preparar dados para relatório cliente
            dados_cliente = {
                "Análise": "Simulação Cliente",
                "Cliente": "Prospecto",
                "Data": datetime.now().strftime("%d/%m/%Y"),
                "Modelo": modelo,
                "Rota": rota_selecionada,
                "Duração": f"{duracao} horas",
                "Voos Mensais": voos_mes,
                "Custo Amaro por Voo": resultado_voo['total'],
                "Preço Mercado por Voo": resultado_voo['preco_mercado'],
                "Economia por Voo": economia_voo,
                "Economia Mensal": economia_mensal,
                "Economia Anual": economia_anual,
                "Percentual Economia": f"{resultado_voo['percentual_economia']:.1f}%"
            }
            
            try:
                pdf_buffer = BytesIO()
                if gerar_pdf(pdf_buffer, dados_cliente):
                    pdf_buffer.seek(0)
                    
                    st.download_button(
                        "📄 Baixar Relatório de Economia (PDF)",
                        data=pdf_buffer.getvalue(),
                        file_name=f"amaro_economia_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
                else:
                    st.error("Erro ao gerar relatório PDF")
            except Exception as e:
                st.error(f"Erro na exportação: {e}")
    
    except Exception as e:
        st.error(f"Erro nos cálculos: {e}")

# Call-to-Action premium
st.markdown("""
<div class="cta-section">
    <h2 style="margin: 0;">🤝 Pronto Para Começar?</h2>
    <p style="margin: 1rem 0; font-size: 1.2rem;">Entre em contato conosco e descubra como a Amaro Aviation pode transformar sua experiência em aviação executiva</p>
    <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem;">
        <div>
            <h4 style="margin: 0;">📞 Telefone</h4>
            <p style="margin: 0.5rem 0;">(11) 9999-9999</p>
        </div>
        <div>
            <h4 style="margin: 0;">📧 E-mail</h4>
            <p style="margin: 0.5rem 0;">contato@amaroaviation.com</p>
        </div>
        <div>
            <h4 style="margin: 0;">🌐 Website</h4>
            <p style="margin: 0.5rem 0;">www.amaroaviation.com</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Seção de diferenciais
st.markdown("## 🌟 Nossos Diferenciais")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="client-card">
        <div style="text-align: center;">
            <h3>🛡️ Segurança</h3>
            <p>Certificações internacionais e rigorosos protocolos de segurança</p>
            <ul style="text-align: left;">
                <li>Pilotos certificados</li>
                <li>Manutenção preventiva</li>
                <li>Seguro completo</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="client-card">
        <div style="text-align: center;">
            <h3>💰 Economia</h3>
            <p>Transparência total e economia real comprovada</p>
            <ul style="text-align: left;">
                <li>Sem taxas ocultas</li>
                <li>Preços competitivos</li>
                <li>Relatórios detalhados</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="client-card">
        <div style="text-align: center;">
            <h3>🕐 Flexibilidade</h3>
            <p>Disponibilidade 24/7 e atendimento personalizado</p>
            <ul style="text-align: left;">
                <li>Horários flexíveis</li>
                <li>Rotas personalizadas</li>
                <li>Suporte dedicado</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Testemunhos e cases (simulados)
st.markdown("---")
st.markdown("## 💬 O Que Nossos Clientes Dizem")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="client-card">
        <div style="border-left: 4px solid #8c1d40; padding-left: 1rem;">
            <p style="font-style: italic;">"A economia com a Amaro Aviation superou nossas expectativas. Além da transparência nos custos, a qualidade do serviço é excepcional."</p>
            <p><strong>- CEO, Empresa de Tecnologia</strong></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="client-card">
        <div style="border-left: 4px solid #8c1d40; padding-left: 1rem;">
            <p style="font-style: italic;">"Pontualidade, segurança e economia. A Amaro Aviation entrega exatamente o que promete. Recomendo sem hesitação."</p>
            <p><strong>- Diretor Executivo, Grupo Empresarial</strong></p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# FAQ simplificado
st.markdown("---")
st.markdown("## ❓ Perguntas Frequentes")

with st.expander("📋 Como funciona a cotação?"):
    st.write("""
    Nossa cotação é totalmente transparente e baseada em custos reais:
    - Combustível (baseado no consumo da aeronave)
    - Custos operacionais (piloto, manutenção)
    - Sem taxas ocultas ou surpresas
    """)

with st.expander("🛡️ Quais são as garantias de segurança?"):
    st.write("""
    Mantemos os mais altos padrões de segurança:
    - Pilotos com certificação internacional
    - Manutenção rigorosa seguindo protocolos da ANAC
    - Seguro completo para passageiros e aeronave
    - Aeronaves com certificados de aeronavegabilidade em dia
    """)

with st.expander("⏰ Como é a disponibilidade?"):
    st.write("""
    Oferecemos máxima flexibilidade:
    - Atendimento 24 horas por dia, 7 dias por semana
    - Agendamento com antecedência mínima de 2 horas
    - Possibilidade de alterações até 1 hora antes do voo
    - Rotas personalizadas conforme sua necessidade
    """)

with st.expander("💳 Quais são as formas de pagamento?"):
    st.write("""
    Aceitamos diversas formas de pagamento:
    - Transferência bancária
    - Cartão de crédito corporativo
    - Boleto bancário
    - Contratos mensais para clientes frequentes
    """)

# Footer do modo cliente
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); border-radius: 15px; margin-top: 3rem;">
    <h3 style="color: #8c1d40; margin: 0;">✈️ Amaro Aviation</h3>
    <p style="color: #666; margin: 0.5rem 0;">Excelência em Aviação Executiva</p>
    <p style="color: #999; margin: 0; font-size: 0.9rem;">
        Sua economia começa aqui. Sua satisfação é nossa prioridade.
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar com informações de contato
with st.sidebar:
    st.markdown("""
    ### 📞 Contato Direto
    
    **📱 WhatsApp Business**  
    (11) 99999-9999
    
    **📧 E-mail Comercial**  
    vendas@amaroaviation.com
    
    **🏢 Escritório**  
    São Paulo - SP  
    Horário: 24h
    
    **🌐 Website**  
    www.amaroaviation.com
    """)
    
    st.markdown("""
    ### 📋 Solicitar Cotação
    
    Para uma cotação personalizada, envie:
    - Rota desejada
    - Data e horário
    - Número de passageiros
    - Preferência de aeronave
    
    **⚡ Resposta em até 30 minutos**
    """)
    
    st.markdown("""
    ### 🎁 Oferta Especial
    
    **Primeira viagem com 15% de desconto**
    
    Válido para novos clientes até o final do mês.
    """)
    
    st.success("💚 **Satisfação Garantida**\n\nSe não ficar satisfeito, devolvemos seu dinheiro!")

# JavaScript para melhorar a experiência (se necessário)
st.markdown("""
<script>
// Smooth scrolling para melhor experiência
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
</script>
""", unsafe_allow_html=True)