import streamlit as st

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# ─────────────────────────────────────
# Layout: två kolumner – vänster & höger
# ─────────────────────────────────────
col_in, col_out = st.columns(2)

# ───────────────
# INDATA – Vänster kolumn
# ───────────────
with col_in:
    st.header("Indata")
    st.subheader("Geometri")

    # --- Bottenplatta ---
    st.markdown("**Bottenplatta**")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        D_b_str = st.text_input("Diameter Dₐ (m)", value="5.0")
    with col_b2:
        h_b_str = st.text_input("Höjd hₐ (m)", value="1.0")

    # --- Skaft ---
    st.markdown("**Skaft (centrerat ovanpå)**")
    col_s1,_
