"""
Sistema de cálculos refatorado para estrutura multipage
Função principal calcula_custo_trecho() atualizada conforme especificação
"""

def calcula_custo_trecho(modelo, horas, params):
    """
    Calcula todos os custos para um trecho/período específico
    
    Args:
        modelo: Nome do modelo da aeronave
        horas: Número de horas de voo
        params: Dicionário com parâmetros carregados
    
    Returns:
        Dict com breakdown detalhado conforme especificação:
        {
            "combustivel": ...,
            "manutencao": ...,
            "tripulacao": ...,
            "seguro": ...,
            "hangar": ...,
            "ferry": ...,
            "planejamento": ...,
            "depreciacao": ...,
            "total": soma
        }
    """
    if modelo not in params.get('consumo_modelos', {}):
        raise ValueError(f"Modelo '{modelo}' não encontrado")
    
    if horas <= 0:
        raise ValueError("Número de horas deve ser maior que zero")
    
    # Cálculo do combustível
    consumo_lh = params['consumo_modelos'][modelo]
    preco_combustivel = params['preco_combustivel']
    custo_combustivel = horas * consumo_lh * preco_combustivel
    
    # Cálculo da manutenção
    custo_manutencao_hora = params['custo_manutencao'][modelo]
    custo_manutencao = horas * custo_manutencao_hora
    
    # Cálculo da tripulação (piloto)
    custo_piloto_hora = params['custo_piloto_hora_modelo'][modelo]
    custo_tripulacao = horas * custo_piloto_hora
    
    # Cálculo da depreciação
    depreciacao_hora = params['depreciacao_hora'][modelo]
    custo_depreciacao = horas * depreciacao_hora
    
    # Custos fixos proporcionais (estimativa para o período)
    # Baseado em horas anuais típicas de 400h
    horas_anuais_ref = 400
    fator_proporcional = horas / horas_anuais_ref
    
    # Estimativas de custos fixos anuais
    custo_seguro = 200000 * fator_proporcional  # Seguro anual proporcional
    custo_hangar = 120000 * fator_proporcional  # Hangar anual proporcional
    custo_ferry = horas * 200  # Ferry/posicionamento estimado por hora
    custo_planejamento = horas * 150  # Planejamento/administração por hora
    
    # Total
    total = (custo_combustivel + custo_manutencao + custo_tripulacao + 
             custo_seguro + custo_hangar + custo_ferry + 
             custo_planejamento + custo_depreciacao)
    
    return {
        "combustivel": custo_combustivel,
        "manutencao": custo_manutencao,
        "tripulacao": custo_tripulacao,
        "seguro": custo_seguro,
        "hangar": custo_hangar,
        "ferry": custo_ferry,
        "planejamento": custo_planejamento,
        "depreciacao": custo_depreciacao,
        "total": total,
        
        # Manter compatibilidade com código existente
        "preco_comb": custo_combustivel,
        "manut": custo_manutencao,
        "piloto": custo_tripulacao,
        "depr": custo_depreciacao
    }

def calcular_projecao_mensal(modelo, horas_mes, num_meses, params, 
                           taxa_crescimento=0, inflacao_custos=0, 
                           reajuste_preco=0, investimento_inicial=0):
    """
    Calcula projeção de custos e receitas mensais
    
    Args:
        modelo: Modelo da aeronave
        horas_mes: Horas mensais iniciais
        num_meses: Número de meses para projetar
        params: Parâmetros do sistema
        taxa_crescimento: Taxa de crescimento anual (%)
        inflacao_custos: Taxa de inflação de custos anual (%)
        reajuste_preco: Taxa de reajuste de preços anual (%)
        investimento_inicial: Investimento inicial
    
    Returns:
        Dict com projeção detalhada
    """
    
    projecao = {
        'meses': [],
        'receitas': [],
        'custos': [],
        'lucros': [],
        'fluxo_caixa': [],
        'horas_mensais': [],
        'breakeven_mes': None
    }
    
    # Valores iniciais
    horas_atual = horas_mes
    preco_hora_atual = params['preco_mercado_hora'][modelo]
    saldo_acumulado = -investimento_inicial
    
    # Fatores de crescimento mensais
    fator_crescimento_mensal = (1 + taxa_crescimento/100) ** (1/12)
    fator_inflacao_mensal = (1 + inflacao_custos/100) ** (1/12)
    fator_reajuste_mensal = (1 + reajuste_preco/100) ** (1/12)
    
    for mes in range(1, num_meses + 1):
        # Aplicar crescimento
        if mes > 1:
            if mes % 12 == 1:  # A cada ano
                horas_atual *= fator_crescimento_mensal ** 12
                preco_hora_atual *= fator_reajuste_mensal ** 12
        
        # Calcular custos do mês
        resultado_mes = calcula_custo_trecho(modelo, horas_atual, params)
        custo_mensal = resultado_mes['total']
        
        # Aplicar inflação nos custos
        if mes > 1 and mes % 12 == 1:  # A cada ano
            custo_mensal *= fator_inflacao_mensal ** 12
        
        # Calcular receita (assumindo 50% das horas para charter com 75% ocupação)
        horas_charter = horas_atual * 0.5 * 0.75
        receita_bruta = horas_charter * preco_hora_atual
        receita_proprietario = receita_bruta * 0.9  # 90% para proprietário
        
        # Lucro mensal
        lucro_mensal = receita_proprietario - custo_mensal
        saldo_acumulado += lucro_mensal
        
        # Verificar breakeven
        if saldo_acumulado > 0 and projecao['breakeven_mes'] is None:
            projecao['breakeven_mes'] = mes
        
        # Armazenar dados
        projecao['meses'].append(mes)
        projecao['receitas'].append(receita_proprietario)
        projecao['custos'].append(custo_mensal)
        projecao['lucros'].append(lucro_mensal)
        projecao['fluxo_caixa'].append(saldo_acumulado)
        projecao['horas_mensais'].append(horas_atual)
    
    return projecao

def calcular_comparativo_gestao(modelo, horas_anuais, params, custos_fixos_externos):
    """
    Calcula comparativo entre gestão própria e gestão Amaro
    
    Args:
        modelo: Modelo da aeronave
        horas_anuais: Horas voadas por ano
        params: Parâmetros do sistema
        custos_fixos_externos: Dict com custos fixos da gestão própria
            {
                'hangar': valor,
                'seguro': valor,
                'tripulacao': valor,
                'administracao': valor
            }
    
    Returns:
        Dict com comparativo detalhado
    """
    
    # Custos variáveis (iguais para ambos)
    resultado_anual = calcula_custo_trecho(modelo, horas_anuais, params)
    custos_variaveis = {
        'combustivel': resultado_anual['combustivel'],
        'manutencao': resultado_anual['manutencao'],
        'depreciacao': resultado_anual['depreciacao'],
        'tripulacao_variavel': resultado_anual['tripulacao']
    }
    
    # GESTÃO PRÓPRIA
    custos_fixos_proprio = sum(custos_fixos_externos.values())
    custos_variaveis_proprio = sum(custos_variaveis.values())
    total_proprio = custos_fixos_proprio + custos_variaveis_proprio
    
    # GESTÃO AMARO (sem custos fixos)
    total_amaro = custos_variaveis_proprio  # Amaro absorve custos fixos
    
    # Economia
    economia_anual = total_proprio - total_amaro
    economia_percentual = (economia_anual / total_proprio * 100) if total_proprio > 0 else 0
    
    return {
        'gestao_propria': {
            'custos_fixos': custos_fixos_proprio,
            'custos_variaveis': custos_variaveis_proprio,
            'total': total_proprio,
            'breakdown_fixos': custos_fixos_externos,
            'breakdown_variaveis': custos_variaveis
        },
        'gestao_amaro': {
            'custos_fixos': 0,
            'custos_variaveis': custos_variaveis_proprio,
            'total': total_amaro,
            'breakdown_variaveis': custos_variaveis
        },
        'economia': {
            'valor_anual': economia_anual,
            'percentual': economia_percentual,
            'economia_5_anos': economia_anual * 5
        }
    }

def calcular_custo_rota(origem, destino, modelo, params, rotas_disponiveis):
    """
    Calcula custo específico para uma rota
    
    Args:
        origem: Código do aeroporto de origem
        destino: Código do aeroporto de destino
        modelo: Modelo da aeronave
        params: Parâmetros do sistema
        rotas_disponiveis: Lista de rotas disponíveis
    
    Returns:
        Dict com análise da rota
    """
    
    # Buscar duração da rota
    rota_info = None
    for rota in rotas_disponiveis:
        if rota['origem'] == origem and rota['destino'] == destino:
            rota_info = rota
            break
    
    if not rota_info:
        raise ValueError(f"Rota {origem} → {destino} não encontrada")
    
    duracao = rota_info['duracao_h']
    
    # Calcular custos
    resultado_rota = calcula_custo_trecho(modelo, duracao, params)
    
    # Preço de mercado para esta rota
    preco_mercado_hora = params['preco_mercado_hora'][modelo]
    preco_mercado_total = preco_mercado_hora * duracao
    
    # Economia
    economia = preco_mercado_total - resultado_rota['total']
    economia_percentual = (economia / preco_mercado_total * 100) if preco_mercado_total > 0 else 0
    
    return {
        'rota': f"{origem} → {destino}",
        'duracao_horas': duracao,
        'custo_amaro': resultado_rota['total'],
        'preco_mercado': preco_mercado_total,
        'economia': economia,
        'economia_percentual': economia_percentual,
        'breakdown_custos': {
            'combustivel': resultado_rota['combustivel'],
            'manutencao': resultado_rota['manutencao'],
            'tripulacao': resultado_rota['tripulacao'],
            'depreciacao': resultado_rota['depreciacao']
        },
        'viavel': economia > 0
    }

def calcular_lucro_mensal_charter(modelo, horas_charter, taxa_ocupacao, preco_hora, params):
    """
    Calcula análise de lucro mensal com operação charter
    
    Args:
        modelo: Modelo da aeronave
        horas_charter: Horas disponíveis para charter por mês
        taxa_ocupacao: Taxa de ocupação (0-100)
        preco_hora: Preço por hora de charter
        params: Parâmetros do sistema
    
    Returns:
        Dict com análise completa de lucro
    """
    
    # Horas efetivas
    horas_efetivas = horas_charter * (taxa_ocupacao / 100)
    
    # Receitas
    receita_bruta = preco_hora * horas_efetivas
    receita_proprietario = receita_bruta * params.get('percentual_proprietario', 0.9)
    taxa_amaro = receita_bruta - receita_proprietario
    
    # Custos operacionais
    resultado_custos = calcula_custo_trecho(modelo, horas_efetivas, params)
    
    # Lucro
    lucro_liquido = receita_proprietario - resultado_custos['total']
    roi_mensal = (lucro_liquido / resultado_custos['total'] * 100) if resultado_custos['total'] > 0 else 0
    
    return {
        'horas_disponiveis': horas_charter,
        'horas_efetivas': horas_efetivas,
        'taxa_ocupacao': taxa_ocupacao,
        'receita_bruta': receita_bruta,
        'receita_proprietario': receita_proprietario,
        'taxa_amaro': taxa_amaro,
        'custos_operacionais': resultado_custos['total'],
        'lucro_liquido': lucro_liquido,
        'roi_mensal': roi_mensal,
        'breakdown_custos': {
            'combustivel': resultado_custos['combustivel'],
            'manutencao': resultado_custos['manutencao'],
            'tripulacao': resultado_custos['tripulacao'],
            'depreciacao': resultado_custos['depreciacao']
        },
        'lucrativo': lucro_liquido > 0
    }