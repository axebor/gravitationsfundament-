import streamlit as st

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# Två kolumner
col_in, col_out = st.columns(2)

# Vänsterkolumn – Indata
with col_in:
    st.header("Indata")
    st.subheader("Geometri")

    # Rubrikrad
    col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
    col1.markdown("**Parameter**")
    col2.markdown("**Beteckning**")
    col3.markdown("**Värde**")
    col4.markdown("**Enhet**")

    # --- Diameter bottenplatta ---
    with st.container():
        col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
        col1.write("Diameter bottenplatta")
        col2.markdown("$D_b$")
        D_b = col3.number_input(label="", value=5.0, step=0.1, format="%.1f", key="D_b")
        col4.write("m")

    # --- Höjd bottenplatta ---
    with st.container():
        col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
        col1.write("Höjd bottenplatta")
        col2.markdown("$h_b$")
        h_b_str = col3.text_input(label="", value="1.0", key="h_b")
        col4.write("m")

    # --- Diameter skaft ---
    with st.container():
        col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
        col1.write("Diameter skaft")
        col2.markdown("$D_s$")
        D_s_str = col3.text_input(label="", value="1.0", key="D_s")
        col4.write("m")

    # --- Höjd skaft ---
    with st.container():
        col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
        col1.write("Höjd skaft")
        col2.markdown("$h_s$")
        h_s_str = col3.text_input(label="", value="2.0", key="h_s")
        col4.write("m")

    # --- Konvertera till tal ---

# Högerkolumn – Resultat (tom för nu)
with col_out:
    st.header("Resultat")
    st.info("Resultat kommer att visas här.")
