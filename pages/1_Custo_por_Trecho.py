import streamlit as st
import pandas as pd
from utils.params import load_params
from utils.calculations import (
    calcular_combustivel,
    calcular_piloto,
    calcular_manutencao,
    calcular_depreciacao,
    calcular_total,
    calcular_economia,
)
from utils.charts import grafico_composicao, grafico_comparativo
from utils.exportador_excel import gerar_excel
from utils.exportador_pdf import gerar_pdf
from io import BytesIO

st.set_page_config(page_title="Custo por Trecho", layout="wide")
st.title("✈️ Custo por Trecho")

# Dados
modelos_df = pd.read_csv("data/modelos.csv")
rotas_df = pd.read_csv("data/rotas.csv")
params = load_params()

# Seletor de modelo
modelo = st.selectbox("Modelo da Aeronave", modelos_df["modelo"].unique())
modelo_info = modelos_df[modelos_df["modelo"] == modelo].iloc[0]
tipo = modelo_info["tipo"]
consumo_lh = modelo_info["consumo_l_por_h"]
custo_manutencao = params["custo_manutencao_hora"][tipo]
preco_mercado = params["preco_mercado"][tipo]

# Filtra as rotas disponíveis para esse modelo
origens = rotas_df["origem"].unique()
origem = st.selectbox("Origem", origens)
destinos_disponiveis = rotas_df[rotas_df["origem"] == origem]["destino"].unique()
destino = st.selectbox("Destino", destinos_disponiveis)

# Busca a duração da rota
duracao = rotas_df[
    (rotas_df["origem"] == origem) & (rotas_df["destino"] == destino)
]["duracao_h"].values
if len(duracao) == 0:
    st.error("Essa rota não existe.")
    st.stop()
duracao = duracao[0]

# Cálculos
custo_comb = calcular_combustivel(duracao, consumo_lh, params["preco_combustivel"])
custo_piloto = calcular_piloto(duracao, params["custo_piloto_hora"])
custo_manut = calcular_manutencao(duracao, custo_manutencao)
custo_deprec = calcular_depreciacao(duracao, params["depreciacao_anual_pct"])
custo_total = calcular_total({
    "Combustível": custo_comb,
    "Piloto": custo_piloto,
    "Manutenção": custo_manut,
    "Depreciação": custo_deprec
})
economia = calcular_economia(custo_total, preco_mercado * duracao)
lucro_estimado = preco_mercado * duracao * params["percentual_proprietario"] - custo_total

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("💰 Custo Total", f"R$ {custo_total:,.2f}".replace(".", ",").replace(",", ".", 1))
col2.metric("📉 Economia Amaro", f"R$ {economia:,.2f}".replace(".", ",").replace(",", ".", 1))
col3.metric("📈 Lucro Estimado", f"R$ {lucro_estimado:,.2f}".replace(".", ",").replace(",", ".", 1))

# Gráficos
st.plotly_chart(grafico_composicao({
    "Combustível": custo_comb,
    "Piloto": custo_piloto,
    "Manutenção": custo_manut,
    "Depreciação": custo_deprec
}), use_container_width=True)

st.plotly_chart(grafico_comparativo(custo_total, preco_mercado * duracao), use_container_width=True)

# Dados para exportação
dados_resultado = {
    "Modelo": modelo,
    "Origem": origem,
    "Destino": destino,
    "Duração (h)": duracao,
    "Combustível": custo_comb,
    "Piloto": custo_piloto,
    "Manutenção": custo_manut,
    "Depreciação": custo_deprec,
    "Custo Total": custo_total,
    "Preço de Mercado": preco_mercado * duracao,
    "Economia": economia,
    "Lucro Estimado": lucro_estimado,
}

# Exportar Excel
excel_buffer = BytesIO()
gerar_excel(excel_buffer, dados_resultado)
st.download_button("⬇️ Baixar Excel", excel_buffer.getvalue(), file_name="relatorio_amaro.xlsx")

# Exportar PDF
pdf_buffer = BytesIO()
gerar_pdf(pdf_buffer, dados_resultado)
st.download_button("⬇️ Baixar PDF", pdf_buffer.getvalue(), file_name="relatorio_amaro.pdf")
