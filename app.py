import streamlit as st

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# Två kolumner
col_in, col_out = st.columns(2)

# VÄNSTERKOLUMN – INDATA
with col_in:
    st.header("Indata")
    st.subheader("Geometri")

    st.latex(r"D_b = \text{Diameter bottenplatta (m)}")
    D_b = st.number_input(label="", value=5.0, step=0.1, format="%.1f", key="D_b")

    st.latex(r"h_b = \text{Höjd bottenplatta (m)}")
    h_b = st.number_input(label="", value=1.0, step=0.1, format="%.1f", key="h_b")

    st.latex(r"D_s = \text{Diameter skaft (m)}")
    D_s = st.number_input(label="", value=1.0, step=0.1, format="%.1f", key="D_s")

    st.latex(r"h_s = \text{Höjd skaft (m)}")
    h_s = st.number_input(label="", value=2.0, step=0.1, format="%.1f", key="h_s")

# HÖGERKOLUMN – RESULTAT
with col_out:
    st.header("Resultat")
    st.info("Resultat kommer att visas här.")
