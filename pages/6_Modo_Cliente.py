import streamlit as st
from utils.params import load_params
from utils.calculations import calcula_custo_trecho

st.title('Modo Cliente')

params = load_params()
modelos = list(params['consumo_modelos'].keys())
origens = ['GRU', 'CGH', 'BSB', 'SDU']

modelo = st.selectbox('Modelo', modelos)
origem = st.selectbox('Origem', origens)
destino = st.selectbox('Destino', [d for d in origens if d != origem])
voos = st.number_input('Quantidade de voos por mês', min_value=1, value=5)

if st.button('Simular Mês'):
    # Simples: assume duração média de rota fixa (1h)
    dur = 1.0
    res = calcula_custo_trecho(modelo, dur, params)
    total = res['total']*voos
    market = params['preco_mercado_hora'][modelo]*dur*voos
    st.write(f'Economia estimada: R$ {market - total:,.2f}')