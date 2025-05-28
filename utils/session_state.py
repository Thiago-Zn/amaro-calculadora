import streamlit as st

def persistent_selectbox(label, options, key, default_index=0, **kwargs):
    saved_value = st.session_state.get(key)
    initial_index = options.index(saved_value) if saved_value and saved_value in options else default_index
    return st.selectbox(label, options, index=initial_index, key=key, **kwargs)

def persistent_number_input(label, key, default_value=0, **kwargs):
    saved_value = st.session_state.get(key, default_value)
    return st.number_input(label, value=saved_value, key=key, **kwargs)

def persistent_slider(label, key, min_value=0, max_value=100, default_value=50, **kwargs):
    saved_value = st.session_state.get(key, default_value)
    return st.slider(label, min_value=min_value, max_value=max_value, value=saved_value, key=key, **kwargs)