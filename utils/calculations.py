"""calculations.py - Sistema de cálculos premium com validação e flexibilidade"""

def calcular_combustivel(duracao, consumo_lh, preco_litro):
    """Calcula o custo de combustível para um voo"""
    if duracao <= 0 or consumo_lh <= 0 or preco_litro <= 0:
        return 0.0
    return float(duracao * consumo_lh * preco_litro)

def calcular_piloto(duracao, custo_piloto_hora):
    """Calcula o custo do piloto para um voo"""
    if duracao <= 0 or custo_piloto_hora <= 0:
        return 0.0
    return float(duracao * custo_piloto_hora)

def calcular_manutencao(duracao, custo_manutencao_hora):
    """Calcula o custo de manutenção para um voo"""
    if duracao <= 0 or custo_manutencao_hora <= 0:
        return 0.0
    return float(duracao * custo_manutencao_hora)

def calcular_depreciacao(duracao, depreciacao_por_hora):
    """Calcula a depreciação para um voo baseada no valor por hora"""
    if duracao <= 0 or depreciacao_por_hora <= 0:
        return 0.0
    return float(duracao * depreciacao_por_hora)

def calcular_depreciacao_detalhada(duracao, depreciacao_anual_pct, valor_aeronave, horas_anuais=400):
    """
    Calcula depreciação detalhada baseada no valor da aeronave
    """
    if any(val <= 0 for val in [duracao, depreciacao_anual_pct, valor_aeronave, horas_anuais]):
        return 0.0
    
    depreciacao_anual = valor_aeronave * (depreciacao_anual_pct / 100)
    depreciacao_por_hora = depreciacao_anual / horas_anuais
    return float(duracao * depreciacao_por_hora)

def calcular_total(custos_dict):
    """Soma todos os custos de um dicionário"""
    if not isinstance(custos_dict, dict):
        return 0.0
    return float(sum(valor for valor in custos_dict.values() if isinstance(valor, (int, float))))

def calcular_economia(custo_total, preco_mercado):
    """Calcula a economia em relação ao preço de mercado"""
    if preco_mercado <= 0:
        return 0.0
    return float(preco_mercado - custo_total)

def calcular_percentual_economia(custo_total, preco_mercado):
    """Calcula o percentual de economia"""
    if preco_mercado <= 0:
        return 0.0
    economia = calcular_economia(custo_total, preco_mercado)
    return float((economia / preco_mercado) * 100)

def calcular_lucro_operacao(receita, custos_dict, percentual_margem=0.0):
    """
    Calcula o lucro da operação considerando margem de lucro
    """
    custo_total = calcular_total(custos_dict)
    lucro_bruto = receita - custo_total
    margem_adicional = receita * (percentual_margem / 100)
    return float(lucro_bruto - margem_adicional)

def calcula_custo_trecho(modelo, duracao, params):
    """
    Calcula todos os custos para um trecho específico
    
    Args:
        modelo: Nome do modelo da aeronave
        duracao: Duração do voo em horas
        params: Dicionário com todos os parâmetros carregados
    
    Returns:
        Dict com breakdown detalhado dos custos
    """
    if modelo not in params.get('consumo_modelos', {}):
        raise ValueError(f"Modelo '{modelo}' não encontrado nos parâmetros")
    
    if duracao <= 0:
        raise ValueError("Duração deve ser maior que zero")
    
    # Cálculo de cada componente
    custo_combustivel = calcular_combustivel(
        duracao, 
        params['consumo_modelos'][modelo], 
        params['preco_combustivel']
    )
    
    custo_piloto = calcular_piloto(
        duracao, 
        params['custo_piloto_hora_modelo'][modelo]
    )
    
    custo_manutencao = calcular_manutencao(
        duracao, 
        params['custo_manutencao'][modelo]
    )
    
    custo_depreciacao = calcular_depreciacao(
        duracao, 
        params['depreciacao_hora'][modelo]
    )
    
    # Total
    custos = {
        'combustivel': custo_combustivel,
        'piloto': custo_piloto,
        'manutencao': custo_manutencao,
        'depreciacao': custo_depreciacao
    }
    
    total = calcular_total(custos)
    preco_mercado_total = params['preco_mercado_hora'][modelo] * duracao
    economia = calcular_economia(total, preco_mercado_total)
    percentual_economia = calcular_percentual_economia(total, preco_mercado_total)
    
    return {
        'preco_comb': custo_combustivel,
        'piloto': custo_piloto,
        'manut': custo_manutencao,
        'depr': custo_depreciacao,
        'total': total,
        'preco_mercado': preco_mercado_total,
        'economia': economia,
        'percentual_economia': percentual_economia,
        'detalhes': {
            'modelo': modelo,
            'duracao': duracao,
            'consumo_lh': params['consumo_modelos'][modelo],
            'preco_combustivel': params['preco_combustivel'],
            'custo_piloto_hora': params['custo_piloto_hora_modelo'][modelo],
            'custo_manutencao_hora': params['custo_manutencao'][modelo],
            'depreciacao_hora': params['depreciacao_hora'][modelo],
            'preco_mercado_hora': params['preco_mercado_hora'][modelo]
        }
    }

def calcular_projecao_mensal(modelo, dias_mes, horas_dia, params):
    """
    Calcula projeção de custos e lucros mensais
    """
    horas_total = dias_mes * horas_dia
    
    if horas_total <= 0:
        return {
            'horas_total': 0,
            'custo_total': 0,
            'receita_mercado': 0,
            'lucro': 0,
            'margem_percentual': 0
        }
    
    resultado_hora = calcula_custo_trecho(modelo, 1.0, params)
    
    custo_total = resultado_hora['total'] * horas_total
    receita_mercado = params['preco_mercado_hora'][modelo] * horas_total
    lucro = receita_mercado - custo_total
    margem_percentual = (lucro / receita_mercado * 100) if receita_mercado > 0 else 0
    
    return {
        'horas_total': horas_total,
        'custo_total': custo_total,
        'receita_mercado': receita_mercado,
        'lucro': lucro,
        'margem_percentual': margem_percentual,
        'breakdown': {
            'combustivel_mensal': resultado_hora['preco_comb'] * horas_total,
            'piloto_mensal': resultado_hora['piloto'] * horas_total,
            'manutencao_mensal': resultado_hora['manut'] * horas_total,
            'depreciacao_mensal': resultado_hora['depr'] * horas_total
        }
    }

def calcular_horas_para_meta(meta_receita, modelo, params):
    """
    Calcula quantas horas são necessárias para atingir uma meta de receita
    """
    if meta_receita <= 0:
        return 0
    
    preco_hora = params['preco_mercado_hora'][modelo]
    if preco_hora <= 0:
        return 0
        
    return float(meta_receita / preco_hora)