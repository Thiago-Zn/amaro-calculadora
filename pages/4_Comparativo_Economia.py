import streamlit as st
from utils.params import load_params
from utils.charts import grafico_comparativo

st.title('Comparativo de Economia Anual')

params = load_params()
modelos = list(params['consumo_modelos'].keys())

modelo = st.selectbox('Modelo', modelos)
horas_ano = st.number_input('Horas por ano', min_value=0, value=200)

if st.button('Comparar'):
    custo_amaro = params['custo_manutencao'][modelo]*horas_ano                   + params['custo_piloto_hora'][modelo]*horas_ano                   + params['depreciacao_hora'][modelo]*horas_ano                   + params['preco_combustivel']*params['consumo_modelos'][modelo]*horas_ano
    custo_mercado = params['preco_mercado_hora'][modelo]*horas_ano
    st.metric('Economia Anual (R$)', f"{custo_mercado - custo_amaro:,.2f}")
    fig = grafico_comparativo(custo_amaro, custo_mercado)
    st.plotly_chart(fig, use_container_width=True)