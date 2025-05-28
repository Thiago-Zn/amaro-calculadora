"""
Sistema de persistência DEFINITIVO para Streamlit
Mantém seleções entre páginas de forma robusta
"""

import streamlit as st

def init_session_defaults():
    """Inicializa valores padrão no session_state se não existirem"""
    defaults = {
        'modelo_persist': None,
        'horas_persist': 80,
        'taxa_ocupacao_persist': 75,
        'preco_charter_persist': 8000.0,
        'origem_rota_persist': None,
        'destino_rota_persist': None,
        'modelo_rota_persist': None,
        'modelo_breakdown': None,
        'modelo_proj': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get_persistent_value(key, default=None):
    """Obtém valor persistente do session_state"""
    init_session_defaults()
    return st.session_state.get(key, default)

def set_persistent_value(key, value):
    """Define valor persistente no session_state"""
    st.session_state[key] = value

def persistent_selectbox(label, options, key, help=None, **kwargs):
    """
    Selectbox que mantém seleção entre páginas
    """
    if not options:
        st.warning(f"⚠️ Nenhuma opção disponível para {label}")
        return None
    
    # Obter valor atual do session_state
    current_value = get_persistent_value(key)
    
    # Determinar índice inicial
    if current_value and current_value in options:
        initial_index = options.index(current_value)
    else:
        initial_index = 0
        # Definir valor padrão no session_state
        set_persistent_value(key, options[0])
    
    # Criar selectbox
    selected = st.selectbox(
        label,
        options,
        index=initial_index,
        key=f"{key}_widget",
        help=help,
        **kwargs
    )
    
    # Atualizar session_state se mudou
    if selected != current_value:
        set_persistent_value(key, selected)
    
    return selected

def persistent_number_input(label, key, default_value=0, help=None, **kwargs):
    """
    Number input que mantém valor entre páginas
    """
    # Obter valor atual do session_state
    current_value = get_persistent_value(key, default_value)
    
    # Garantir que todos os valores numéricos sejam do mesmo tipo
    # Converter todos para float para consistência
    if 'min_value' in kwargs and kwargs['min_value'] is not None:
        kwargs['min_value'] = float(kwargs['min_value'])
    if 'max_value' in kwargs and kwargs['max_value'] is not None:
        kwargs['max_value'] = float(kwargs['max_value'])
    if 'step' in kwargs and kwargs['step'] is not None:
        kwargs['step'] = float(kwargs['step'])
    
    # Criar number input
    value = st.number_input(
        label,
        value=float(current_value),
        key=f"{key}_widget",
        help=help,
        **kwargs
    )
    
    # Atualizar session_state se mudou
    if value != current_value:
        set_persistent_value(key, value)
    
    return value

def persistent_slider(label, key, min_value=0, max_value=100, default_value=50, help=None, **kwargs):
    """
    Slider que mantém valor entre páginas
    """
    # Obter valor atual do session_state
    current_value = get_persistent_value(key, default_value)
    
    # Garantir que o valor está dentro dos limites
    if current_value < min_value:
        current_value = min_value
    elif current_value > max_value:
        current_value = max_value
    
    # Garantir que todos os valores sejam int para sliders
    min_value = int(min_value)
    max_value = int(max_value)
    current_value = int(current_value)
    
    # Criar slider
    value = st.slider(
        label,
        min_value=min_value,
        max_value=max_value,
        value=current_value,
        key=f"{key}_widget",
        help=help,
        **kwargs
    )
    
    # Atualizar session_state se mudou
    if value != current_value:
        set_persistent_value(key, value)
    
    return value

def reset_all_persistent_values():
    """Reset todos os valores persistentes (para debug)"""
    keys_to_reset = [
        'modelo_persist', 'horas_persist', 'taxa_ocupacao_persist', 'preco_charter_persist',
        'origem_rota_persist', 'destino_rota_persist', 'modelo_rota_persist',
        'modelo_breakdown', 'modelo_proj'
    ]
    
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
    
    init_session_defaults()

def debug_session_state():
    """Mostra estado atual do session_state (para debug)"""
    st.write("### Debug Session State")
    persistent_keys = [k for k in st.session_state.keys() if 'persist' in k or 'breakdown' in k or 'proj' in k]
    for key in sorted(persistent_keys):
        st.write(f"**{key}**: {st.session_state[key]}")

# Inicializar automaticamente quando importado
init_session_defaults()