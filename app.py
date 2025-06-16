import streamlit as st

st.set_page_config(page_title="Gravitationsfundament", layout="wide")
col_in, col_out = st.columns(2)

with col_in:
    st.header("Indata")

    def rad(beskrivning, beteckning, enhet, key, default):
        col1, col2, col3, col4 = st.columns([2.8, 0.8, 1.2, 0.5])
        col1.write(beskrivning)
        col2.write(f"({beteckning})")
        val = col3.text_input(label="", value=default, key=key)
        col4.write(enhet)
        return float(val)

    D_b = rad("Diameter bottenplatta", "D_b", "m", "D_b", "5.0")
    h_b = rad("Höjd bottenplatta", "h_b", "m", "h_b", "1.0")
    D_s = rad("Diameter skaft", "D_s", "m", "D_s", "1.0")
    h_s = rad("Höjd skaft", "h_s", "m", "h_s", "2.0")
