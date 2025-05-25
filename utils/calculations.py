"""calculations.py - funções de cálculo de custos e economia""\"

def calcula_custo_trecho(modelo, duracao_h, params):
    consumo = params['consumo_modelos'].get(modelo, 0) * duracao_h
    preco_comb = consumo * params['preco_combustivel']
    manut = params['custo_manutencao'].get(modelo, 0) * duracao_h
    piloto = params['custo_piloto_hora'].get(modelo, 0) * duracao_h
    depr = params['depreciacao_hora'].get(modelo, 0) * duracao_h
    total = preco_comb + manut + piloto + depr
    return {
        'consumo': consumo,
        'preco_comb': preco_comb,
        'manut': manut,
        'piloto': piloto,
        'depr': depr,
        'total': total
    }