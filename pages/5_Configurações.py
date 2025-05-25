import streamlit as st
from utils.params import load_params, save_params

st.title('Configurações (Uso Interno)')
params = load_params()

preco_comb = st.number_input('Preço do combustível (R$/L)', value=params['preco_combustivel'])
if st.button('Salvar Configurações'):
    params['preco_combustivel'] = preco_comb
    save_params(params)
    st.success('Configurações salvas com sucesso!')