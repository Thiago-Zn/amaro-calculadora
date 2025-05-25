import streamlit as st
from utils.params import load_params, save_params

st.set_page_config(page_title="Configurações", layout="wide")
st.title("Configurações (Uso Interno)")
st.markdown("⚙️ Ajuste os parâmetros que afetam os cálculos.")

params = load_params()

with st.form("form_config"):
    preco_comb = st.number_input("Preço do combustível (R$/L)", value=params["preco_combustivel"])
    custo_piloto = st.number_input("Custo piloto/hora", value=params["custo_piloto_hora"])
    depreciacao = st.number_input("Depreciação anual (%)", value=params["depreciacao_anual_pct"])

    st.markdown("### Custo de manutenção por tipo de aeronave:")
    manut_turbo = st.number_input("Turboprop (R$/h)", value=params["custo_manutencao_hora"]["turboprop"])
    manut_jato = st.number_input("Jato (R$/h)", value=params["custo_manutencao_hora"]["jato"])

    st.markdown("### Preço médio de mercado por tipo:")
    mercado_turbo = st.number_input("Turboprop", value=params["preco_mercado"]["turboprop"])
    mercado_jato = st.number_input("Jato", value=params["preco_mercado"]["jato"])

    if st.form_submit_button("Salvar configurações"):
        params["preco_combustivel"] = preco_comb
        params["custo_piloto_hora"] = custo_piloto
        params["depreciacao_anual_pct"] = depreciacao
        params["custo_manutencao_hora"]["turboprop"] = manut_turbo
        params["custo_manutencao_hora"]["jato"] = manut_jato
        params["preco_mercado"]["turboprop"] = mercado_turbo
        params["preco_mercado"]["jato"] = mercado_jato
        save_params(params)
        st.success("Parâmetros atualizados com sucesso.")
