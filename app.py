import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# CSS för att styra bredd på inputfält och justera enhets-text inline
st.markdown(
    """
    <style>
    div[data-testid="stTextInput"] > div > input {
        max-width: 120px;
        width: 100%;
        box-sizing: border-box;
        display: inline-block;
        vertical-align: middle;
    }
    .inline-unit {
        display: inline-block;
        margin-left: 6px;
        vertical-align: middle;
        font-size: 16px;
        color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

col_in, col_out, col_res = st.columns([1, 1, 1])

with col_in:
    st.header("Indata")
    st.subheader("Geometri")

    st.markdown("**Bottenplatta**")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        D_b_str = st.text_input("Diameter Dₐ (m)", value="5.0")
    with col_b2:
        h_b_str = st.text_input("Höjd hₐ (m)", value="1.0")

    st.markdown("**Skaft (centrerat ovanpå)**")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        D_s_str = st.text_input("Diameter Dₛ (m)", value="1.0")
    with col_s2:
        h_s_str = st.text_input("Höjd hₛ (m)", value="2.0")

    fundament_i_vatten = st.checkbox("Fundament delvis i vatten", value=False)

    if fundament_i_vatten:
        st.markdown("Mått från underkant fundament,  $z_{v}$")
        # Här kommer inputfält och enhet på samma rad i inline-block
        zv_input = st.text_input("", value="0.0", key="z_niva")
        st.markdown(f'<span class="inline-unit">m</span>', unsafe_allow_html=True)
        zv_str = zv_input
    else:
        zv_str = None

    try:
        D_b = round(float(D_b_str), 1)
        h_b = round(float(h_b_str), 1)
        D_s = round(float(D_s_str), 1)
        h_s = round(float(h_s_str), 1)
        if fundament_i_vatten:
            zv = float(zv_str)
        else:
            zv = None
    except ValueError:
        st.error("❌ Ange giltiga numeriska värden för geometri och vattennivå.")
        st.stop()

# Resten av din kod för figur och resultat...


