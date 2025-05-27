"""
Amaro Aviation Calculator v3.0 - Entry Point
Aplicação multipage refatorada com estrutura modular
"""

import streamlit as st
from pathlib import Path

# Imports dos componentes
from config.theme import load_theme
from config.idiomas import get_text, detect_language_from_selection
from components.header import render_header
from components.sidebar import render_sidebar
from components.status import render_system_status
from utils.params import load_params

# ========================================================================
# CONFIGURAÇÃO DA PÁGINA PRINCIPAL
# ========================================================================
st.set_page_config(
    page_title="Amaro Aviation – Simulador Estratégico",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
    # -------------  SEU STREAMLIT NÃO SUPORTA "theme=" -------------
    # As cores serão aplicadas somente pelo CSS do load_theme()
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": (
            "Amaro Aviation Calculator v3.0 – "
            "Sistema profissional de análise de custos operacionais"
        ),
    },
)



# ========================================================================
# CARREGAMENTO DO TEMA E CONFIGURAÇÕES
# ========================================================================
load_theme()

# ========================================================================
# SIDEBAR E SELEÇÃO DE IDIOMA
# ========================================================================
lang = render_sidebar()

# ========================================================================
# HEADER PRINCIPAL
# ========================================================================
render_header(lang)

# ========================================================================
# VERIFICAÇÃO DO SISTEMA
# ========================================================================
try:
    # Carrega todos os parâmetros gravados em disco
    params = load_params()

    # Mostra a caixa verde "Sistema Operacional"
    # (a função já formata o HTML internamente; não enviamos tags aqui)
    system_ok = render_system_status(params, lang)

    # Se ainda não existem modelos ou parâmetros, interrompe o fluxo
    if not system_ok:
        st.markdown("### ⚠️ Sistema Requer Configuração")

        st.markdown(
            """
Para começar a usar o simulador:

1. **Execute o setup inicial**
   ```bash
   python setup_initial.py
           ```
        
        2. **Ou configure manualmente:**
           - Acesse a página de **Configurações**
           - Configure pelo menos um modelo de aeronave
           - Ajuste os parâmetros financeiros
        
        3. **Reinicie a aplicação**
        """)
        st.stop()
        
except Exception as e:
    st.error(f"❌ Erro crítico no sistema: {e}")
    st.markdown("""
    ### 🔧 Soluções Sugeridas:
    
    1. **Executar setup inicial:**
       ```bash
       python setup_initial.py
       ```
    
    2. **Reinstalar dependências:**
       ```bash
       pip install -r requirements.txt
       ```
    
    3. **Verificar estrutura de arquivos:**
       - `config/parametros.json`
       - `data/modelos.csv`
       - `data/rotas.csv`
    """)
    st.stop()

# ========================================================================
# CONTEÚDO PRINCIPAL - PÁGINA DE BOAS-VINDAS
# ========================================================================

# Mensagem de boas-vindas
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    padding: 3rem 2rem;
    border-radius: 12px;
    text-align: center;
    margin: 2rem 0;
    border-left: 4px solid #8C1D40;
">
    <h2 style="color: #8C1D40; margin-bottom: 1rem;">
        {get_text('welcome_message' if lang == 'pt' else 'welcome_message', lang)}
    </h2>
    <p style="color: #6B7280; font-size: 1.1rem; max-width: 600px; margin: 0 auto;">
        {'Utilize o menu lateral para navegar entre as diferentes funcionalidades do sistema' if lang == 'pt' 
         else 'Use the sidebar menu to navigate between different system functionalities'}
    </p>
</div>
""", unsafe_allow_html=True)

# ========================================================================
# OVERVIEW DAS FUNCIONALIDADES
# ========================================================================

st.markdown(f"### 🎯 {'Funcionalidades Principais' if lang == 'pt' else 'Main Features'}")

# Cards das funcionalidades
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style="
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 2rem;
        height: 200px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 2rem; margin-right: 1rem;">📈</span>
            <h4 style="color: #8C1D40; margin: 0;">{get_text('page_profit', lang)}</h4>
        </div>
        <p style="color: #6B7280; font-size: 0.9rem; line-height: 1.5;">
            {'Análise completa de rentabilidade mensal considerando operação charter, custos operacionais e ROI.' if lang == 'pt'
             else 'Complete monthly profitability analysis considering charter operation, operational costs and ROI.'}
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 2rem;
        height: 200px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 2rem; margin-right: 1rem;">📊</span>
            <h4 style="color: #8C1D40; margin: 0;">{get_text('page_breakdown', lang)}</h4>
        </div>
        <p style="color: #6B7280; font-size: 0.9rem; line-height: 1.5;">
            {'Comparação detalhada item por item entre gestão própria e gestão Amaro Aviation.' if lang == 'pt'
             else 'Detailed item-by-item comparison between own management and Amaro Aviation management.'}
        </p>
    </div>
    """, unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown(f"""
    <div style="
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 2rem;
        height: 200px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 2rem; margin-right: 1rem;">✈️</span>
            <h4 style="color: #8C1D40; margin: 0;">{get_text('page_simulator', lang)}</h4>
        </div>
        <p style="color: #6B7280; font-size: 0.9rem; line-height: 1.5;">
            {'Simulação de custos específicos por rota origem-destino com análise de viabilidade.' if lang == 'pt'
             else 'Specific cost simulation per origin-destination route with viability analysis.'}
        </p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 2rem;
        height: 200px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 2rem; margin-right: 1rem;">📈</span>
            <h4 style="color: #8C1D40; margin: 0;">{get_text('page_projection', lang)}</h4>
        </div>
        <p style="color: #6B7280; font-size: 0.9rem; line-height: 1.5;">
            {'Projeção financeira de longo prazo (12-60 meses) com análise de breakeven.' if lang == 'pt'
             else 'Long-term financial projection (12-60 months) with breakeven analysis.'}
        </p>
    </div>
    """, unsafe_allow_html=True)

# ========================================================================
# INFORMAÇÕES TÉCNICAS
# ========================================================================

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### 📊 {'Status do Sistema' if lang == 'pt' else 'System Status'}")
    
    modelos_count = len(params.get('modelos_disponiveis', []))
    
    st.metric(
        "Modelos Configurados" if lang == 'pt' else "Configured Models",
        modelos_count
    )
    
    try:
        import pandas as pd
        df_rotas = pd.read_csv('data/rotas.csv')
        rotas_count = len(df_rotas)
    except:
        rotas_count = 0
    
    st.metric(
        "Rotas Disponíveis" if lang == 'pt' else "Available Routes",
        rotas_count
    )

with col2:
    st.markdown(f"### ⚙️ {'Configuração Rápida' if lang == 'pt' else 'Quick Setup'}")
    
    if lang == 'pt':
        st.markdown("""
        **Para começar rapidamente:**
        
        1. 📈 Vá para **Estimativa de Lucro**
        2. ✈️ Selecione um modelo de aeronave
        3. 📊 Configure horas mensais e ocupação
        4. 🚀 Clique em **Calcular**
        
        **Para personalizar:**
        
        - ⚙️ Acesse **Configurações**
        - 💰 Ajuste parâmetros financeiros
        - ✈️ Adicione novos modelos
        - 🗺️ Configure rotas específicas
        """)
    else:
        st.markdown("""
        **To get started quickly:**
        
        1. 📈 Go to **Profit Estimation**
        2. ✈️ Select an aircraft model
        3. 📊 Configure monthly hours and occupancy
        4. 🚀 Click **Calculate**
        
        **To customize:**
        
        - ⚙️ Access **Settings**
        - 💰 Adjust financial parameters
        - ✈️ Add new models
        - 🗺️ Configure specific routes
        """)

# ========================================================================
# INSTRUÇÕES DE NAVEGAÇÃO
# ========================================================================

st.markdown("---")

if lang == 'pt':
    st.info("""
    💡 **Navegação:** Use o menu lateral esquerdo para acessar as diferentes páginas do sistema. 
    Cada página oferece funcionalidades específicas para análise de custos operacionais.
    """)
else:
    st.info("""
    💡 **Navigation:** Use the left sidebar menu to access different system pages. 
    Each page offers specific functionalities for operational cost analysis.
    """)

# ========================================================================
# FOOTER
# ========================================================================

st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #6B7280; padding: 2rem;">
    <p>✈️ <strong>Amaro Aviation Calculator v3.0</strong></p>
    <p style="font-size: 0.875rem;">
        {'Sistema profissional de análise de custos operacionais em aviação executiva' if lang == 'pt'
         else 'Professional operational cost analysis system for executive aviation'}
    </p>
    <p style="font-size: 0.75rem; margin-top: 1rem;">
        {'Desenvolvido com' if lang == 'pt' else 'Developed with'} ❤️ 
        {'pela equipe técnica Amaro Aviation' if lang == 'pt' else 'by Amaro Aviation technical team'}
    </p>
</div>
""", unsafe_allow_html=True)