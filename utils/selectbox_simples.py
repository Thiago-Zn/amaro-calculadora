"""
SELECTBOX SIMPLES QUE MANTÉM SELEÇÃO VISÍVEL
Sistema direto sem complicação
"""

import streamlit as st

def selectbox_que_funciona(label, opcoes, chave_unica, valor_padrao=None):
    """
    Selectbox que SEMPRE mostra o valor selecionado
    
    Args:
        label: Texto do label
        opcoes: Lista de opções
        chave_unica: Chave única para este selectbox
        valor_padrao: Valor padrão se nada selecionado
    
    Returns:
        Valor selecionado
    """
    
    if not opcoes:
        st.warning(f"⚠️ Nenhuma opção disponível para {label}")
        return None
    
    # Chave para armazenar no session_state
    chave = f"select_{chave_unica}"
    
    # Valor atual armazenado
    if chave not in st.session_state:
        if valor_padrao and valor_padrao in opcoes:
            st.session_state[chave] = valor_padrao
        else:
            st.session_state[chave] = opcoes[0]
    
    # Garantir que o valor ainda existe nas opções
    if st.session_state[chave] not in opcoes:
        st.session_state[chave] = opcoes[0]
    
    # Encontrar índice do valor atual
    try:
        indice_atual = opcoes.index(st.session_state[chave])
    except ValueError:
        indice_atual = 0
        st.session_state[chave] = opcoes[0]
    
    # Criar selectbox
    valor_selecionado = st.selectbox(
        label,
        opcoes,
        index=indice_atual,
        key=f"widget_{chave_unica}"
    )
    
    # Atualizar session_state
    st.session_state[chave] = valor_selecionado
    
    return valor_selecionado

def number_input_que_funciona(label, chave_unica, padrao=0, minimo=0, maximo=1000):
    """
    Number input simples que mantém valor
    """
    
    chave = f"number_{chave_unica}"
    
    # Valor atual
    if chave not in st.session_state:
        st.session_state[chave] = float(padrao)
    
    # Criar input
    valor = st.number_input(
        label,
        min_value=float(minimo),
        max_value=float(maximo),
        value=float(st.session_state[chave]),
        key=f"widget_number_{chave_unica}"
    )
    
    # Atualizar session_state
    st.session_state[chave] = valor
    
    return valor

def slider_que_funciona(label, chave_unica, padrao=50, minimo=0, maximo=100):
    """
    Slider simples que mantém valor
    """
    
    chave = f"slider_{chave_unica}"
    
    # Valor atual
    if chave not in st.session_state:
        st.session_state[chave] = int(padrao)
    
    # Criar slider
    valor = st.slider(
        label,
        min_value=int(minimo),
        max_value=int(maximo),
        value=int(st.session_state[chave]),
        key=f"widget_slider_{chave_unica}"
    )
    
    # Atualizar session_state
    st.session_state[chave] = valor
    
    return valor

def mostrar_debug_session():
    """
    Mostra o que está armazenado (para debug)
    """
    st.write("🔍 DEBUG - Valores armazenados:")
    for chave, valor in st.session_state.items():
        if chave.startswith(('select_', 'number_', 'slider_')):
            st.write(f"**{chave}**: {valor}")

def limpar_todos_valores():
    """
    Limpa todos os valores armazenados (reset)
    """
    chaves_para_remover = []
    for chave in st.session_state.keys():
        if chave.startswith(('select_', 'number_', 'slider_', 'widget_')):
            chaves_para_remover.append(chave)
    
    for chave in chaves_para_remover:
        del st.session_state[chave]
    
    st.success("✅ Todos os valores foram resetados!")
    st.rerun()

# Teste se executado diretamente
if __name__ == "__main__":
    st.write("🧪 Teste dos Selectbox")
    
    # Teste selectbox
    opcoes_teste = ["Opção 1", "Opção 2", "Opção 3"]
    selecionado = selectbox_que_funciona("Teste Selectbox", opcoes_teste, "teste1")
    st.write(f"Selecionado: {selecionado}")
    
    # Teste number input
    numero = number_input_que_funciona("Teste Number", "teste2", 50, 0, 100)
    st.write(f"Número: {numero}")
    
    # Teste slider
    slide = slider_que_funciona("Teste Slider", "teste3", 75, 0, 100)
    st.write(f"Slider: {slide}")
    
    # Debug
    mostrar_debug_session()
    
    # Botão reset
    if st.button("🔄 Reset Tudo"):
        limpar_todos_valores()