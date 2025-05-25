"""exportador_excel.py - Exporta os dados do voo para Excel"""

import pandas as pd

def gerar_excel(caminho_arquivo, dados: dict):
    df = pd.DataFrame(list(dados.items()), columns=["Categoria", "Valor (R$)"])
    df.to_excel(caminho_arquivo, index=False)
