import streamlit as st
from utils.params import load_params
from utils.charts import grafico_comparativo

st.title('Projeção de Lucros Mensais')

params = load_params()
modelos = list(params['consumo_modelos'].keys())

dias = st.slider('Dias por mês', 0, 31, 17)
horas_por_dia = st.number_input('Horas por dia', min_value=0, value=2)
modelo = st.selectbox('Modelo', modelos)

if st.button('Calcular Mensal'):
    horas_total = dias * horas_por_dia
    custo_total = params['custo_manutencao'][modelo] * horas_total                  + params['custo_piloto_hora'][modelo] * horas_total                  + params['depreciacao_hora'][modelo] * horas_total                  + params['preco_combustivel'] * params['consumo_modelos'][modelo] * horas_total
    receita = params['preco_mercado_hora'][modelo] * horas_total
    lucro = receita - custo_total
    st.metric('Lucro Mensal (R$)', f"{lucro:,.2f}")
    fig = grafico_comparativo(custo_total, receita)
    st.plotly_chart(fig, use_container_width=True)