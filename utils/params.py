"""params.py - Sistema de parâmetros premium com fallbacks e validação"""

import json
import pandas as pd
from pathlib import Path
import streamlit as st

PARAMS_FILE = "config/parametros.json"
MODELOS_FILE = "data/modelos.csv"

def get_default_params():
    """Parâmetros padrão caso o arquivo não exista ou seja inválido"""
    return {
        "preco_combustivel": 8.66,
        "custo_piloto_hora": 1200,
        "depreciacao_anual_pct": 8,
        "custo_manutencao_hora": {
            "turboprop": 1500,
            "jato": 3000
        },
        "percentual_proprietario": 0.9,
        "preco_mercado": {
            "turboprop": 8000,
            "jato": 15000
        }
    }

def get_default_modelos():
    """Modelos padrão caso o CSV não exista"""
    return pd.DataFrame([
        {"modelo": "Pilatus PC-12", "consumo_l_por_h": 260, "manut_tipo": "turboprop", "tipo": "turboprop"},
        {"modelo": "Cessna Citation XLS", "consumo_l_por_h": 600, "manut_tipo": "jato", "tipo": "jato"},
        {"modelo": "Embraer Phenom 300E", "consumo_l_por_h": 650, "manut_tipo": "jato", "tipo": "jato"}
    ])

@st.cache_data
def load_params():
    """
    Carrega parâmetros do JSON e dados dos modelos, com fallbacks robustos
    """
    # Carregamento dos parâmetros básicos com fallback
    try:
        if Path(PARAMS_FILE).exists():
            with open(PARAMS_FILE, "r", encoding="utf-8") as f:
                params = json.load(f)
        else:
            params = get_default_params()
            save_params(params)  # Cria arquivo padrão
    except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
        st.warning(f"Erro ao carregar parâmetros: {e}. Usando valores padrão.")
        params = get_default_params()
    
    # Carregamento dos modelos com fallback
    try:
        if Path(MODELOS_FILE).exists():
            df_modelos = pd.read_csv(MODELOS_FILE)
        else:
            df_modelos = get_default_modelos()
            df_modelos.to_csv(MODELOS_FILE, index=False)
    except (pd.errors.EmptyDataError, FileNotFoundError, KeyError) as e:
        st.warning(f"Erro ao carregar modelos: {e}. Usando modelos padrão.")
        df_modelos = get_default_modelos()
    
    # Construção dos dicionários dinâmicos baseados nos modelos
    consumo_modelos = {}
    custo_manutencao = {}
    custo_piloto_hora = {}
    depreciacao_hora = {}
    preco_mercado_hora = {}
    
    for _, row in df_modelos.iterrows():
        modelo = row['modelo']
        tipo = row['tipo']
        
        # Consumo por modelo
        consumo_modelos[modelo] = float(row['consumo_l_por_h'])
        
        # Custo de manutenção baseado no tipo
        custo_manutencao[modelo] = float(params['custo_manutencao_hora'][tipo])
        
        # Custo do piloto (igual para todos)
        custo_piloto_hora[modelo] = float(params['custo_piloto_hora'])
        
        # Depreciação por hora (baseada em valor estimado da aeronave)
        valor_base = 50000000 if tipo == 'jato' else 20000000
        horas_ano = 400
        depreciacao_hora[modelo] = (valor_base * params['depreciacao_anual_pct'] / 100) / horas_ano
        
        # Preço de mercado baseado no tipo
        preco_mercado_hora[modelo] = float(params['preco_mercado'][tipo])
    
    # Adicionar dicionários calculados aos parâmetros
    params.update({
        'consumo_modelos': consumo_modelos,
        'custo_manutencao': custo_manutencao,
        'custo_piloto_hora_modelo': custo_piloto_hora,
        'depreciacao_hora': depreciacao_hora,
        'preco_mercado_hora': preco_mercado_hora,
        'modelos_disponiveis': list(consumo_modelos.keys())
    })
    
    return params

def save_params(params_data):
    """
    Salva apenas os parâmetros básicos (não os calculados)
    """
    try:
        # Criar diretório se não existir
        Path(PARAMS_FILE).parent.mkdir(parents=True, exist_ok=True)
        
        # Extrair apenas parâmetros básicos para salvar
        basic_params = {
            'preco_combustivel': float(params_data['preco_combustivel']),
            'custo_piloto_hora': float(params_data['custo_piloto_hora']),
            'depreciacao_anual_pct': float(params_data['depreciacao_anual_pct']),
            'custo_manutencao_hora': params_data['custo_manutencao_hora'],
            'percentual_proprietario': float(params_data.get('percentual_proprietario', 0.9)),
            'preco_mercado': params_data['preco_mercado']
        }
        
        with open(PARAMS_FILE, "w", encoding="utf-8") as f:
            json.dump(basic_params, f, indent=2, ensure_ascii=False)
            
        # Limpar cache para recarregar parâmetros
        load_params.clear()
        
        return True
        
    except Exception as e:
        st.error(f"Erro ao salvar parâmetros: {e}")
        return False

def validate_params(params):
    """
    Valida se os parâmetros estão em formato correto
    """
    required_keys = [
        'preco_combustivel', 'custo_piloto_hora', 'depreciacao_anual_pct',
        'custo_manutencao_hora', 'preco_mercado', 'consumo_modelos'
    ]
    
    for key in required_keys:
        if key not in params:
            return False, f"Parâmetro '{key}' ausente"
    
    if not isinstance(params['custo_manutencao_hora'], dict):
        return False, "custo_manutencao_hora deve ser um dicionário"
    
    if not isinstance(params['preco_mercado'], dict):
        return False, "preco_mercado deve ser um dicionário"
        
    return True, "Parâmetros válidos"
# Adicionar ao final do arquivo utils/params.py
def format_currency(value, lang='pt'):
    """Formata valores monetários"""
    try:
        if lang == 'pt':
            return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            return f"R$ {value:,.2f}"
    except:
        return str(value)

def format_percentage(value, lang='pt'):
    """Formata percentuais"""
    try:
        if lang == 'pt':
            return f"{value:.1f}%".replace(".", ",")
        else:
            return f"{value:.1f}%"
    except:
        return str(value)