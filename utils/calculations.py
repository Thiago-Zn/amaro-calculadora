"""calculations.py - funções de cálculo de custos e economia"""

def calcular_combustivel(duracao, consumo_lh, preco_litro):
    return duracao * consumo_lh * preco_litro

def calcular_piloto(duracao, custo_piloto_hora):
    return duracao * custo_piloto_hora

def calcular_manutencao(duracao, custo_manutencao_hora):
    return duracao * custo_manutencao_hora

def calcular_depreciacao(duracao, depreciacao_anual_pct, valor_base=50000000, horas_ano=400):
    custo_por_hora = (valor_base * depreciacao_anual_pct / 100) / horas_ano
    return duracao * custo_por_hora

def calcular_total(itens: dict):
    return sum(itens.values())

def calcular_economia(custo_total, preco_mercado):
    return preco_mercado - custo_total
