import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
from pathlib import Path
from utils.params import load_params, save_params, validate_params

# Configuração da página
st.set_page_config(
    page_title="Configurações - Amaro Aviation", 
    layout="wide",
    page_icon="⚙️"
)

# CSS Premium para configurações
st.markdown("""
<style>
.config-header {
    background: linear-gradient(135deg, #8c1d40 0%, #a02050 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
}

.config-section {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    border: 1px solid #e9ecef;
    margin: 1rem 0;
}

.warning-box {
    background: linear-gradient(135deg, #FFF3CD 0%, #FCF8E3 100%);
    border: 1px solid #FFEAA7;
    border-radius: 10px;
    padding: 1rem;
    margin: 1rem 0;
}

.success-box {
    background: linear-gradient(135deg, #D4EDDA 0%, #C3E6CB 100%);
    border: 1px solid #A3CFB4;
    border-radius: 10px;
    padding: 1rem;
    margin: 1rem 0;
}

.parameter-preview {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
    border-left: 4px solid #8c1d40;
}
</style>
""", unsafe_allow_html=True)

# Header da página
st.markdown("""
<div class="config-header">
    <h1 style="margin: 0;">⚙️ Configurações do Sistema</h1>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Ajuste dos parâmetros operacionais - Uso interno Amaro Aviation</p>
</div>
""", unsafe_allow_html=True)

# Aviso de uso interno
st.markdown("""
<div class="warning-box">
    <h4>⚠️ ATENÇÃO - USO INTERNO</h4>
    <p>Esta página é destinada exclusivamente à equipe técnica da Amaro Aviation. 
    As alterações aqui realizadas afetarão todos os cálculos do sistema em tempo real.</p>
</div>
""", unsafe_allow_html=True)

# Carregamento de parâmetros
try:
    params = load_params()
    
    # Validar parâmetros
    is_valid, validation_message = validate_params(params)
    if not is_valid:
        st.error(f"❌ Erro na validação dos parâmetros: {validation_message}")
        
except Exception as e:
    st.error(f"❌ Erro crítico ao carregar parâmetros: {e}")
    st.stop()

# Tabs para organizar configurações
tab1, tab2, tab3, tab4 = st.tabs(["💰 Custos Operacionais", "🛩️ Modelos de Aeronaves", "📊 Preços de Mercado", "💾 Backup & Restore"])

with tab1:
    st.markdown("## 💰 Parâmetros de Custos Operacionais")
    
    with st.form("form_custos_operacionais"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="config-section">
                <h4>⛽ Combustível</h4>
            """, unsafe_allow_html=True)
            
            preco_comb = st.number_input(
                "Preço do combustível (R$/L)",
                value=float(params["preco_combustivel"]),
                min_value=0.01,
                max_value=50.0,
                step=0.01,
                help="Preço atual do combustível por litro"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class="config-section">
                <h4>👨‍✈️ Recursos Humanos</h4>
            """, unsafe_allow_html=True)
            
            custo_piloto = st.number_input(
                "Custo piloto/hora (R$)",
                value=float(params["custo_piloto_hora"]),
                min_value=0.0,
                max_value=10000.0,
                step=50.0,
                help="Custo hora do piloto (salário + encargos)"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="config-section">
                <h4>📉 Depreciação</h4>
            """, unsafe_allow_html=True)
            
            depreciacao = st.number_input(
                "Depreciação anual (%)",
                value=float(params["depreciacao_anual_pct"]),
                min_value=0.0,
                max_value=50.0,
                step=0.1,
                help="Percentual de depreciação anual das aeronaves"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class="config-section">
                <h4>🔧 Manutenção por Tipo</h4>
            """, unsafe_allow_html=True)
            
            manut_turbo = st.number_input(
                "Turboprop (R$/h)",
                value=float(params["custo_manutencao_hora"]["turboprop"]),
                min_value=0.0,
                max_value=5000.0,
                step=100.0,
                help="Custo de manutenção para aeronaves turboprop"
            )
            
            manut_jato = st.number_input(
                "Jato (R$/h)",
                value=float(params["custo_manutencao_hora"]["jato"]),
                min_value=0.0,
                max_value=10000.0,
                step=100.0,
                help="Custo de manutenção para jatos"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Botão de salvar
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.form_submit_button("💾 Salvar Custos Operacionais", type="primary", use_container_width=True):
                try:
                    # Atualizar parâmetros
                    params["preco_combustivel"] = preco_comb
                    params["custo_piloto_hora"] = custo_piloto
                    params["depreciacao_anual_pct"] = depreciacao
                    params["custo_manutencao_hora"]["turboprop"] = manut_turbo
                    params["custo_manutencao_hora"]["jato"] = manut_jato
                    
                    # Salvar
                    if save_params(params):
                        st.success("✅ Custos operacionais atualizados com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao salvar parâmetros")
                        
                except Exception as e:
                    st.error(f"❌ Erro ao processar dados: {e}")

with tab2:
    st.markdown("## 🛩️ Modelos de Aeronaves")
    
    # Exibir modelos atuais
    if 'modelos_disponiveis' in params:
        st.markdown("### Modelos Configurados")
        
        for modelo in params['modelos_disponiveis']:
            with st.expander(f"✈️ {modelo}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Consumo",
                        f"{params['consumo_modelos'][modelo]} L/h"
                    )
                
                with col2:
                    st.metric(
                        "Manutenção",
                        f"R$ {params['custo_manutencao'][modelo]:,.0f}/h"
                    )
                
                with col3:
                    st.metric(
                        "Preço Mercado",
                        f"R$ {params['preco_mercado_hora'][modelo]:,.0f}/h"
                    )
    
    st.markdown("### 📁 Gerenciamento de Modelos")
    st.info("""
    **💡 Como adicionar novos modelos:**
    1. Edite o arquivo `data/modelos.csv`
    2. Adicione uma linha com: modelo, consumo_l_por_h, manut_tipo, tipo
    3. Reinicie a aplicação para carregar os novos dados
    
    **Tipos disponíveis:** turboprop, jato
    """)

with tab3:
    st.markdown("## 📊 Preços de Mercado")
    
    with st.form("form_precos_mercado"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🛩️ Turboprop")
            mercado_turbo = st.number_input(
                "Preço médio turboprop (R$/h)",
                value=float(params["preco_mercado"]["turboprop"]),
                min_value=1000.0,
                max_value=20000.0,
                step=500.0,
                help="Preço médio de mercado para aeronaves turboprop"
            )
        
        with col2:
            st.markdown("### ✈️ Jato")
            mercado_jato = st.number_input(
                "Preço médio jato (R$/h)",
                value=float(params["preco_mercado"]["jato"]),
                min_value=5000.0,
                max_value=50000.0,
                step=1000.0,
                help="Preço médio de mercado para jatos"
            )
        
        # Preview do impacto
        st.markdown("### 📈 Preview do Impacto")
        
        if params.get('modelos_disponiveis'):
            preview_data = []
            for modelo in params['modelos_disponiveis']:
                custo_atual = (
                    params['consumo_modelos'][modelo] * params['preco_combustivel'] +
                    params['custo_manutencao'][modelo] +
                    params['custo_piloto_hora_modelo'][modelo] +
                    params['depreciacao_hora'][modelo]
                )
                
                tipo_modelo = "turboprop" if params['preco_mercado_hora'][modelo] < 10000 else "jato"
                novo_preco = mercado_turbo if tipo_modelo == "turboprop" else mercado_jato
                nova_economia = novo_preco - custo_atual
                
                preview_data.append({
                    "Modelo": modelo,
                    "Custo Operacional": f"R$ {custo_atual:,.0f}",
                    "Novo Preço Mercado": f"R$ {novo_preco:,.0f}",
                    "Nova Economia": f"R$ {nova_economia:,.0f}",
                    "Margem": f"{(nova_economia/novo_preco*100):.1f}%"
                })
            
            df_preview = pd.DataFrame(preview_data)
            st.dataframe(df_preview, use_container_width=True, hide_index=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.form_submit_button("💾 Salvar Preços de Mercado", type="primary", use_container_width=True):
                try:
                    # Atualizar preços de mercado
                    params["preco_mercado"]["turboprop"] = mercado_turbo
                    params["preco_mercado"]["jato"] = mercado_jato
                    
                    # Salvar
                    if save_params(params):
                        st.success("✅ Preços de mercado atualizados com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao salvar parâmetros")
                        
                except Exception as e:
                    st.error(f"❌ Erro ao processar dados: {e}")

with tab4:
    st.markdown("## 💾 Backup & Restore")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="config-section">
            <h4>📥 Backup dos Parâmetros</h4>
            <p>Faça download dos parâmetros atuais para backup de segurança.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Preparar dados para backup
        backup_data = {
            "preco_combustivel": params["preco_combustivel"],
            "custo_piloto_hora": params["custo_piloto_hora"],
            "depreciacao_anual_pct": params["depreciacao_anual_pct"],
            "custo_manutencao_hora": params["custo_manutencao_hora"],
            "percentual_proprietario": params.get("percentual_proprietario", 0.9),
            "preco_mercado": params["preco_mercado"],
            "backup_timestamp": str(pd.Timestamp.now()),
            "backup_version": "1.0"
        }
        
        backup_json = json.dumps(backup_data, indent=2, ensure_ascii=False)
        
        st.download_button(
            "📥 Download Backup",
            data=backup_json,
            file_name=f"amaro_backup_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        st.markdown("""
        <div class="config-section">
            <h4>📤 Restaurar Parâmetros</h4>
            <p>Carregue um arquivo de backup para restaurar configurações anteriores.</p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Selecione arquivo de backup",
            type=['json'],
            help="Arquivo JSON gerado pelo sistema de backup"
        )
        
        if uploaded_file is not None:
            try:
                backup_content = json.loads(uploaded_file.getvalue().decode('utf-8'))
                
                st.markdown("**📋 Preview do Backup:**")
                
                preview_info = f"""
                - **Data do Backup:** {backup_content.get('backup_timestamp', 'Não informado')}
                - **Versão:** {backup_content.get('backup_version', 'Não informado')}
                - **Combustível:** R$ {backup_content.get('preco_combustivel', 0):.2f}/L
                - **Piloto:** R$ {backup_content.get('custo_piloto_hora', 0):,.0f}/h
                - **Depreciação:** {backup_content.get('depreciacao_anual_pct', 0):.1f}%
                """
                
                st.info(preview_info)
                
                if st.button("🔄 Restaurar Configurações", type="secondary", use_container_width=True):
                    try:
                        # Validar estrutura do backup
                        required_keys = ["preco_combustivel", "custo_piloto_hora", "depreciacao_anual_pct", 
                                       "custo_manutencao_hora", "preco_mercado"]
                        
                        missing_keys = [key for key in required_keys if key not in backup_content]
                        
                        if missing_keys:
                            st.error(f"❌ Backup incompleto. Chaves ausentes: {missing_keys}")
                        else:
                            # Restaurar parâmetros
                            restored_params = {
                                "preco_combustivel": backup_content["preco_combustivel"],
                                "custo_piloto_hora": backup_content["custo_piloto_hora"],
                                "depreciacao_anual_pct": backup_content["depreciacao_anual_pct"],
                                "custo_manutencao_hora": backup_content["custo_manutencao_hora"],
                                "percentual_proprietario": backup_content.get("percentual_proprietario", 0.9),
                                "preco_mercado": backup_content["preco_mercado"]
                            }
                            
                            if save_params(restored_params):
                                st.success("✅ Configurações restauradas com sucesso!")
                                st.rerun()
                            else:
                                st.error("❌ Erro ao restaurar configurações")
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao restaurar backup: {e}")
                        
            except json.JSONDecodeError:
                st.error("❌ Arquivo de backup inválido. Verifique o formato JSON.")
            except Exception as e:
                st.error(f"❌ Erro ao processar arquivo: {e}")

# Seção de resumo atual
st.markdown("---")
st.markdown("## 📊 Resumo dos Parâmetros Atuais")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="parameter-preview">
        <h4>💰 Custos Operacionais</h4>
    """, unsafe_allow_html=True)
    
    st.write(f"**⛽ Combustível:** R$ {params['preco_combustivel']:.2f}/L")
    st.write(f"**👨‍✈️ Piloto:** R$ {params['custo_piloto_hora']:,.0f}/h")
    st.write(f"**📉 Depreciação:** {params['depreciacao_anual_pct']:.1f}% ao ano")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="parameter-preview">
        <h4>🔧 Manutenção</h4>
    """, unsafe_allow_html=True)
    
    st.write(f"**🛩️ Turboprop:** R$ {params['custo_manutencao_hora']['turboprop']:,.0f}/h")
    st.write(f"**✈️ Jato:** R$ {params['custo_manutencao_hora']['jato']:,.0f}/h")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="parameter-preview">
        <h4>📈 Preços de Mercado</h4>
    """, unsafe_allow_html=True)
    
    st.write(f"**🛩️ Turboprop:** R$ {params['preco_mercado']['turboprop']:,.0f}/h")
    st.write(f"**✈️ Jato:** R$ {params['preco_mercado']['jato']:,.0f}/h")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Gráfico de impacto dos parâmetros
if params.get('modelos_disponiveis'):
    st.markdown("### 📊 Impacto dos Parâmetros por Modelo")
    
    # Calcular impacto para cada modelo
    impact_data = {
        'Modelo': [],
        'Combustível': [],
        'Piloto': [],
        'Manutenção': [],
        'Depreciação': [],
        'Total': []
    }
    
    for modelo in params['modelos_disponiveis']:
        consumo = params['consumo_modelos'][modelo]
        custo_comb = consumo * params['preco_combustivel']
        custo_piloto = params['custo_piloto_hora_modelo'][modelo]
        custo_manut = params['custo_manutencao'][modelo]
        custo_depr = params['depreciacao_hora'][modelo]
        total = custo_comb + custo_piloto + custo_manut + custo_depr
        
        impact_data['Modelo'].append(modelo)
        impact_data['Combustível'].append(custo_comb)
        impact_data['Piloto'].append(custo_piloto)
        impact_data['Manutenção'].append(custo_manut)
        impact_data['Depreciação'].append(custo_depr)
        impact_data['Total'].append(total)
    
    # Criar gráfico de barras empilhadas
    fig = go.Figure()
    
    cores = ['#8c1d40', '#a02050', '#3498DB', '#F39C12']
    componentes = ['Combustível', 'Piloto', 'Manutenção', 'Depreciação']
    
    for i, componente in enumerate(componentes):
        fig.add_trace(go.Bar(
            name=componente,
            x=impact_data['Modelo'],
            y=impact_data[componente],
            marker_color=cores[i]
        ))
    
    fig.update_layout(
        title='Composição de Custos por Modelo (R$/h)',
        barmode='stack',
        xaxis_title='Modelo',
        yaxis_title='Custo (R$/h)',
        yaxis_tickformat=',.0f',
        template='plotly_white',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Avisos finais
st.markdown("---")
st.markdown("""
<div class="warning-box">
    <h4>🔒 Segurança e Backup</h4>
    <ul>
        <li>Sempre faça backup antes de alterações importantes</li>
        <li>Teste as configurações em ambiente controlado</li>
        <li>Mantenha histórico de alterações para auditoria</li>
        <li>Em caso de problemas, restaure o último backup funcional</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Sidebar com informações técnicas
with st.sidebar:
    st.markdown("### ⚙️ Informações Técnicas")
    
    st.info(f"""
    **📁 Arquivos de Configuração:**
    - Parâmetros: `config/parametros.json`
    - Modelos: `data/modelos.csv`
    - Rotas: `data/rotas.csv`
    
    **🔧 Status:**
    - Parâmetros: ✅ Carregados
    - Modelos: {len(params.get('modelos_disponiveis', []))} configurados
    - Validação: {"✅ OK" if is_valid else "❌ Erro"}
    """)
    
    st.markdown("### 📚 Documentação")
    st.markdown("""
    **Tipos de Aeronave:**
    - `turboprop`: Aeronaves turboélice
    - `jato`: Aeronaves a jato
    
    **Parâmetros Principais:**
    - Combustível: Preço por litro
    - Piloto: Custo total por hora
    - Manutenção: Por tipo de aeronave
    - Depreciação: Percentual anual
    """)