import streamlit as st

st.set_page_config(page_title="Gravitationsfundament", layout="wide")
col_in, col_out = st.columns(2)

with col_in:
    st.header("Indata")
    
    def indata_rad(label, symbol, enhet, key, default):
        col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
        col1.write(label)
        col2.write(symbol)
        val = col3.text_input(label="", value=default, key=key)
        col4.write(enhet)
        return float(val)

    D_b = indata_rad("Diameter bottenplatta", "D_b", "m", "D_b", "5.0")
    h_b = indata_rad("Höjd bottenplatta", "h_b", "m", "h_b", "1.0")
    D_s = indata_rad("Diameter skaft", "D_s", "m", "D_s", "1.0")
    h_s = indata_rad("Höjd skaft", "h_s", "m", "h_s", "2.0")

