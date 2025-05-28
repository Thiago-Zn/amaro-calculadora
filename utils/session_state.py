"""
Utilitário para persistência de selectbox entre navegações
"""

import streamlit as st

def get_selectbox_index(options, saved_value, default_index=0):
    """
    Retorna o índice correto para o selectbox baseado no valor salvo
    
    Args:
        options: Lista de opções do selectbox
        saved_value: Valor salvo no session_state
        default_index: Índice padrão se não encontrar
    
    Returns:
        int: Índice da opção selecionada
    """
    if saved_value and saved_value in options:
        return options.index(saved_value)
    return default_index

def persistent_selectbox(label, options, key, default_index=0, **kwargs):
    """
    Selectbox que mantém o valor selecionado entre navegações
    
    Args:
        label: Label do selectbox
        options: Lista de opções
        key: Chave única para o session_state
        default_index: Índice padrão
        **kwargs: Outros parâmetros do st.selectbox
    
    Returns:
        Valor selecionado
    """
    # Recuperar valor salvo
    saved_value = st.session_state.get(key)
    
    # Determinar índice inicial
    initial_index = get_selectbox_index(options, saved_value, default_index)
    
    # Criar selectbox com valor persistido
    selected = st.selectbox(
        label,
        options,
        index=initial_index,
        key=key,
        **kwargs
    )
    
    return selected

def persistent_number_input(label, key, default_value=0, **kwargs):
    """
    Number input que mantém o valor entre navegações
    """
    saved_value = st.session_state.get(key, default_value)
    
    return st.number_input(
        label,
        value=saved_value,
        key=key,
        **kwargs
    )

def persistent_slider(label, key, min_value=0, max_value=100, default_value=50, **kwargs):
    """
    Slider que mantém o valor entre navegações
    """
    saved_value = st.session_state.get(key, default_value)
    
    return st.slider(
        label,
        min_value=min_value,
        max_value=max_value,
        value=saved_value,
        key=key,
        **kwargs
    )