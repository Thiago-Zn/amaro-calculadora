"""
Página 5: Configurações e Parâmetros
Edição de parâmetros + CRUD para modelos.csv e rotas.csv
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from config.theme import load_theme
from config.idiomas import get_text, detect_language_from_selection
from components.header import render_page_header
from components.sidebar import render_sidebar
from components.status import render_status_box
from utils.params import load_params, save_params

# Configuração da página
st.set_page_config(
    page_title="Configurações | Amaro Aviation",
    page_icon="⚙️",
    layout="wide"
)

# Carregar tema
load_theme()

# Sidebar e idioma
lang = render_sidebar()

# Header da página
render_page_header(
    'page_settings',
    'Configuração de parâmetros operacionais e gestão de dados do sistema' if lang == 'pt' 
    else 'Operational parameter configuration and system data management',
    lang
)

# Carregar parâmetros atuais
try:
    params = load_params()
except Exception as e:
    st.error(f"❌ Erro ao carregar parâmetros: {e}")
    params = {}

# Interface principal
st.markdown(f"### ⚙️ {get_text('page_settings', lang)}")

st.info(f"""
💡 **Dica**: Ajuste os parâmetros abaixo para personalizar as simulações de acordo com a realidade 
do seu mercado e operação. As alterações serão aplicadas em todos os cálculos.
""" if lang == 'pt' else """
💡 **Tip**: Adjust the parameters below to customize simulations according to your market 
and operation reality. Changes will be applied to all calculations.
""")

# Organizar em abas
config_tab1, config_tab2, config_tab3 = st.tabs([
    f"💰 {get_text('financial_parameters', lang)}",
    f"✈️ {get_text('aircraft_models', lang)}",
    f"🗺️ {get_text('available_routes', lang)}"
])

# ==========================================
# TAB 1: PARÂMETROS FINANCEIROS
# ==========================================
with config_tab1:
    st.markdown(f"#### 💰 {get_text('financial_parameters', lang)}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"##### {get_text('operational_costs', lang)}")
        
        preco_combustivel = st.number_input(
            get_text('fuel_price', lang),
            value=float(params.get('preco_combustivel', 8.66)),
            min_value=1.0,
            max_value=20.0,
            step=0.1,
            format="%.2f",
            help="Preço médio do QAV-1 (querosene de aviação)" if lang == 'pt'
                 else "Average price of QAV-1 (aviation kerosene)"
        )
        
        custo_piloto = st.number_input(
            get_text('pilot_cost', lang),
            value=float(params.get('custo_piloto_hora', 1200)),
            min_value=500.0,
            max_value=5000.0,
            step=100.0,
            help="Custo médio por hora de voo do piloto" if lang == 'pt'
                 else "Average cost per pilot flight hour"
        )
        
        depreciacao = st.number_input(
            get_text('annual_depreciation', lang),
            value=float(params.get('depreciacao_anual_pct', 8)),
            min_value=1.0,
            max_value=20.0,
            step=0.5,
            help="Taxa de depreciação anual da aeronave" if lang == 'pt'
                 else "Annual aircraft depreciation rate"
        )
    
    with col2:
        st.markdown(f"##### {get_text('maintenance_by_type', lang)}")
        
        custo_manut = params.get('custo_manutencao_hora', {'turboprop': 1500, 'jato': 3000})
        
        manut_turboprop = st.number_input(
            get_text('turboprop_maintenance', lang),
            value=float(custo_manut.get('turboprop', 1500)),
            min_value=500.0,
            max_value=5000.0,
            step=100.0,
            help="Custo médio de manutenção para turboprops" if lang == 'pt'
                 else "Average maintenance cost for turboprops"
        )
        
        manut_jato = st.number_input(
            get_text('jet_maintenance', lang),
            value=float(custo_manut.get('jato', 3000)),
            min_value=1000.0,
            max_value=10000.0,
            step=200.0,
            help="Custo médio de manutenção para jatos" if lang == 'pt'
                 else "Average maintenance cost for jets"
        )
    
    st.markdown(f"##### {get_text('market_prices', lang)}")
    
    col1, col2 = st.columns(2)
    
    preco_mercado = params.get('preco_mercado', {'turboprop': 8000, 'jato': 15000})
    
    with col1:
        mercado_turboprop = st.number_input(
            get_text('turboprop_charter', lang),
            value=float(preco_mercado.get('turboprop', 8000)),
            min_value=3000.0,
            max_value=15000.0,
            step=500.0,
            help="Preço médio de mercado para charter de turboprops" if lang == 'pt'
                 else "Average market price for turboprop charter"
        )
    
    with col2:
        mercado_jato = st.number_input(
            get_text('jet_charter', lang),
            value=float(preco_mercado.get('jato', 15000)),
            min_value=8000.0,
            max_value=30000.0,
            step=1000.0,
            help="Preço médio de mercado para charter de jatos" if lang == 'pt'
                 else "Average market price for jet charter"
        )
    
    # Botão de salvamento
    if st.button(f"💾 {get_text('save_financial_config', lang)}", type="primary"):
        novos_params = {
            'preco_combustivel': preco_combustivel,
            'custo_piloto_hora': custo_piloto,
            'depreciacao_anual_pct': depreciacao,
            'custo_manutencao_hora': {
                'turboprop': manut_turboprop,
                'jato': manut_jato
            },
            'percentual_proprietario': params.get('percentual_proprietario', 0.9),
            'preco_mercado': {
                'turboprop': mercado_turboprop,
                'jato': mercado_jato
            }
        }
        
        if save_params(novos_params):
            render_status_box(
                'success',
                get_text('config_saved', lang),
                "Parâmetros financeiros atualizados com sucesso!" if lang == 'pt'
                else "Financial parameters updated successfully!"
            )
            st.rerun()
        else:
            render_status_box(
                'error',
                get_text('save_error', lang),
                "Não foi possível salvar as configurações." if lang == 'pt'
                else "Could not save settings."
            )

# ==========================================
# TAB 2: MODELOS DE AERONAVES
# ==========================================
with config_tab2:
    st.markdown(f"#### ✈️ {get_text('aircraft_management', lang)}")
    
    # Carregar modelos atuais
    try:
        df_modelos = pd.read_csv('data/modelos.csv')
    except:
        st.warning("⚠️ Arquivo de modelos não encontrado. Criando arquivo padrão.")
        df_modelos = pd.DataFrame({
            'modelo': ['Pilatus PC-12'],
            'consumo_l_por_h': [260],
            'manut_tipo': ['turboprop'],
            'tipo': ['turboprop']
        })
        df_modelos.to_csv('data/modelos.csv', index=False)
    
    # Editor de dados
    st.markdown(f"##### {get_text('edit_existing_models', lang)}")
    
    # Explicação das colunas
    with st.expander("ℹ️ Explicação das Colunas" if lang == 'pt' else "ℹ️ Column Explanation"):
        if lang == 'pt':
            st.markdown("""
            - **Modelo**: Nome do modelo da aeronave
            - **Consumo (L/h)**: Consumo de combustível em litros por hora
            - **Tipo Manutenção**: Categoria para cálculo de manutenção (turboprop ou jato)
            - **Tipo Aeronave**: Classificação geral da aeronave (turboprop ou jato)
            """)
        else:
            st.markdown("""
            - **Model**: Aircraft model name
            - **Consumption (L/h)**: Fuel consumption in liters per hour
            - **Maintenance Type**: Category for maintenance calculation (turboprop or jet)
            - **Aircraft Type**: General aircraft classification (turboprop or jet)
            """)
    
    # Editor interativo
    df_editado = st.data_editor(
        df_modelos,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "modelo": st.column_config.TextColumn(
                get_text('model', lang),
                help="Nome do modelo da aeronave" if lang == 'pt' else "Aircraft model name"
            ),
            "consumo_l_por_h": st.column_config.NumberColumn(
                get_text('consumption', lang),
                help="Consumo de combustível em litros por hora" if lang == 'pt' else "Fuel consumption in liters per hour",
                min_value=100,
                max_value=1000,
                step=10
            ),
            "manut_tipo": st.column_config.SelectboxColumn(
                get_text('maintenance_type', lang),
                options=["turboprop", "jato"],
                help="Tipo para cálculo de manutenção" if lang == 'pt' else "Type for maintenance calculation"
            ),
            "tipo": st.column_config.SelectboxColumn(
                get_text('aircraft_type', lang),
                options=["turboprop", "jato"],
                help="Classificação geral da aeronave" if lang == 'pt' else "General aircraft classification"
            )
        }
    )
    
    # Botões de ação
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"💾 {get_text('save_model_changes', lang)}", type="primary"):
            try:
                # Validar dados
                if df_editado.empty:
                    st.error("❌ Deve haver pelo menos um modelo configurado.")
                elif df_editado['modelo'].duplicated().any():
                    st.error("❌ Nomes de modelo devem ser únicos.")
                else:
                    df_editado.to_csv('data/modelos.csv', index=False)
                    render_status_box(
                        'success',
                        get_text('models_updated', lang),
                        f"Salvos {len(df_editado)} modelos com sucesso!" if lang == 'pt'
                        else f"Successfully saved {len(df_editado)} models!"
                    )
                    st.rerun()
            except Exception as e:
                render_status_box(
                    'error',
                    get_text('save_error', lang),
                    f"Erro ao salvar modelos: {e}"
                )
    
    with col2:
        # Download do template
        csv_template = df_modelos.to_csv(index=False)
        st.download_button(
            f"📥 {get_text('download_template', lang)}",
            csv_template,
            "modelos_template.csv",
            "text/csv",
            help="Baixe o template para editar externamente" if lang == 'pt'
                 else "Download template for external editing"
        )

# ==========================================
# TAB 3: ROTAS DISPONÍVEIS
# ==========================================
with config_tab3:
    st.markdown(f"#### 🗺️ {get_text('route_management', lang)}")
    
    # Carregar rotas atuais
    try:
        df_rotas = pd.read_csv('data/rotas.csv')
    except:
        st.warning("⚠️ Arquivo de rotas não encontrado. Criando arquivo padrão.")
        df_rotas = pd.DataFrame({
            'origem': ['GRU'],
            'destino': ['SDU'],
            'duracao_h': [1.0]
        })
        df_rotas.to_csv('data/rotas.csv', index=False)
    
    # Editor de dados
    st.markdown(f"##### {get_text('edit_available_routes', lang)}")
    
    # Explicação das colunas
    with st.expander("ℹ️ Explicação das Colunas" if lang == 'pt' else "ℹ️ Column Explanation"):
        if lang == 'pt':
            st.markdown("""
            - **Origem**: Código IATA do aeroporto de origem (ex: GRU, CGH)
            - **Destino**: Código IATA do aeroporto de destino (ex: SDU, BSB)
            - **Duração (h)**: Duração do voo em horas (tempo de voo real)
            
            **Códigos IATA Comuns:**
            - GRU: Guarulhos (São Paulo)
            - CGH: Congonhas (São Paulo)
            - SDU: Santos Dumont (Rio de Janeiro)
            - BSB: Brasília
            - CNF: Confins (Belo Horizonte)
            - CWB: Afonso Pena (Curitiba)
            """)
        else:
            st.markdown("""
            - **Origin**: IATA code of origin airport (e.g., GRU, CGH)
            - **Destination**: IATA code of destination airport (e.g., SDU, BSB)
            - **Duration (h)**: Flight duration in hours (actual flight time)
            
            **Common IATA Codes:**
            - GRU: Guarulhos (São Paulo)
            - CGH: Congonhas (São Paulo)
            - SDU: Santos Dumont (Rio de Janeiro)
            - BSB: Brasília
            - CNF: Confins (Belo Horizonte)
            - CWB: Afonso Pena (Curitiba)
            """)
    
    # Editor interativo
    df_rotas_editado = st.data_editor(
        df_rotas,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "origem": st.column_config.TextColumn(
                get_text('origin', lang),
                help="Código IATA do aeroporto de origem" if lang == 'pt' else "Origin airport IATA code",
                max_chars=3
            ),
            "destino": st.column_config.TextColumn(
                get_text('destination', lang),
                help="Código IATA do aeroporto de destino" if lang == 'pt' else "Destination airport IATA code",
                max_chars=3
            ),
            "duracao_h": st.column_config.NumberColumn(
                get_text('duration', lang),
                help="Duração do voo em horas" if lang == 'pt' else "Flight duration in hours",
                min_value=0.1,
                max_value=10.0,
                step=0.1,
                format="%.1f"
            )
        }
    )
    
    # Botões de ação
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"💾 {get_text('save_route_changes', lang)}", type="primary"):
            try:
                # Validar dados
                if df_rotas_editado.empty:
                    st.error("❌ Deve haver pelo menos uma rota configurada.")
                else:
                    # Converter códigos para maiúsculo
                    df_rotas_editado['origem'] = df_rotas_editado['origem'].str.upper()
                    df_rotas_editado['destino'] = df_rotas_editado['destino'].str.upper()
                    
                    # Verificar duplicatas
                    df_rotas_editado['rota_key'] = df_rotas_editado['origem'] + '_' + df_rotas_editado['destino']
                    if df_rotas_editado['rota_key'].duplicated().any():
                        st.error("❌ Não podem existir rotas duplicadas (mesma origem e destino).")
                    else:
                        df_rotas_editado = df_rotas_editado.drop('rota_key', axis=1)
                        df_rotas_editado.to_csv('data/rotas.csv', index=False)
                        render_status_box(
                            'success',
                            get_text('routes_updated', lang),
                            f"Salvas {len(df_rotas_editado)} rotas com sucesso!" if lang == 'pt'
                            else f"Successfully saved {len(df_rotas_editado)} routes!"
                        )
                        st.rerun()
            except Exception as e:
                render_status_box(
                    'error',
                    get_text('save_error', lang),
                    f"Erro ao salvar rotas: {e}"
                )
    
    with col2:
        # Download do template
        csv_rotas = df_rotas.to_csv(index=False)
        st.download_button(
            f"📥 {get_text('download_template', lang)}",
            csv_rotas,
            "rotas_template.csv",
            "text/csv",
            help="Baixe o template para editar externamente" if lang == 'pt'
                 else "Download template for external editing"
        )
    
    # Visualização das rotas em mapa conceitual
    with st.expander("🗺️ Visualização das Rotas" if lang == 'pt' else "🗺️ Route Visualization"):
        if not df_rotas_editado.empty:
            # Criar grafo simples das conexões
            origens = df_rotas_editado['origem'].unique()
            destinos = df_rotas_editado['destino'].unique()
            todos_aeroportos = sorted(set(list(origens) + list(destinos)))
            
            st.markdown("**Aeroportos na Rede:**" if lang == 'pt' else "**Airports in Network:**")
            st.write(", ".join(todos_aeroportos))
            
            st.markdown("**Conexões Diretas:**" if lang == 'pt' else "**Direct Connections:**")
            for _, rota in df_rotas_editado.iterrows():
                st.write(f"• {rota['origem']} → {rota['destino']} ({rota['duracao_h']:.1f}h)")

# Informações do sistema
st.markdown("---")
with st.expander("ℹ️ Informações do Sistema" if lang == 'pt' else "ℹ️ System Information"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Arquivos de Configuração:**" if lang == 'pt' else "**Configuration Files:**")
        st.code("""
        config/parametros.json     # Parâmetros financeiros
        data/modelos.csv          # Modelos de aeronaves  
        data/rotas.csv            # Rotas disponíveis
        """)
    
    with col2:
        st.markdown("**Backup Recomendado:**" if lang == 'pt' else "**Recommended Backup:**")
        st.markdown("""
        - Faça backup dos arquivos antes de grandes alterações
        - Teste as configurações após modificações
        - Mantenha versões de desenvolvimento e produção
        """ if lang == 'pt' else """
        - Backup files before major changes
        - Test configurations after modifications
        - Maintain development and production versions
        """)

# Footer da página
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6B7280; padding: 1rem;">
    <p>⚙️ <strong>{get_text('page_settings', lang)}</strong> - Configuração completa do sistema</p>
</div>
""", unsafe_allow_html=True)