import streamlit as st
from utils.params import load_params

st.title('Meta de Receita Mensal')

params = load_params()
modelos = list(params['consumo_modelos'].keys())

meta = st.number_input('Meta de receita (R$)', min_value=0.0, value=100000.0)
modelo = st.selectbox('Modelo', modelos)

if st.button('Calcular Estratégia'):
    preco_hora = params['preco_mercado_hora'][modelo]
    horas_necessarias = meta / preco_hora
    st.metric('Horas Necessárias', f"{horas_necessarias:,.1f}")
    # Exemplo de roteiros simplificado
    st.write('Sugestão de voos:')
    st.write(f"- {int(horas_necessarias)} horas de voo no modelo {modelo}")