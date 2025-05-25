import streamlit as st
from utils.calculations import calcula_custo_trecho
from utils.params import load_params
from utils.charts import grafico_composicao, grafico_comparativo

st.title('Cálculo de Custo por Trecho')

params = load_params()
modelos = list(params['consumo_modelos'].keys())
origens = ['GRU', 'CGH', 'BSB', 'SDU']
destinos = origens.copy()

modelo = st.selectbox('Modelo', modelos)
origem = st.selectbox('Origem', origens)
destino = st.selectbox('Destino', [d for d in destinos if d != origem])
duracao = st.number_input('Duração (h)', min_value=0.0, step=0.1, value=1.0)

if st.button('Calcular'):
    result = calcula_custo_trecho(modelo, duracao, params)
    st.metric('Custo Total (R$)', f"{result['total']:,.2f}")
    st.metric('Economia vs Mercado (R$)', f"{params['preco_mercado_hora'][modelo]*duracao - result['total']:,.2f}")
    # Gráficos
    fig1 = grafico_composicao({
        'Combustível': result['preco_comb'],
        'Manutenção': result['manut'],
        'Piloto': result['piloto'],
        'Depreciação': result['depr']
    })
    st.plotly_chart(fig1, use_container_width=True)
    fig2 = grafico_comparativo(result['total'], params['preco_mercado_hora'][modelo]*duracao)
    st.plotly_chart(fig2, use_container_width=True)