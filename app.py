import streamlit as st

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# Två kolumner – vänster för indata, höger för resultat
col_in, col_out = st.columns(2)

# ───────────────────────────────
# Vänster kolumn – INDATA
# ───────────────────────────────
with col_in:
    st.header("Indata")
    st.subheader("Geometri")

    # Rubrikrad
    col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
    col1.markdown("**Parameter**")
    col2.markdown("**Beteckning**")
    col3.markdown("**Värde**")
    col4.markdown("**Enhet**")

    # Diameter bottenplatta
    col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
    col1.write("Diameter bottenplatta")
    col2.latex("D_b")
    D_b_str = col3.text_input(label="", value="5.0", key="D_b")
    col4.write("m")

    # Höjd bottenplatta
    col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
    col1.write("Höjd bottenplatta")
    col2.latex("h_b")
    h_b_str = col3.text_input(label="", value="1.0", key="h_b")
    col4.write("m")

    # Diameter skaft
    col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
    col1.write("Diameter skaft")
    col2.latex("D_s")
    D_s_str = col3.text_input(label="", value="1.0", key="D_s")
    col4.write("m")

    # Höjd skaft
    col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
    col1.write("Höjd skaft")
    col2.latex("h_s")
    h_s_str = col3.text_input(label="", value="2.0", key="h_s")
    col4.write("m")

    # Konvertera till float
    try:
        D_b = round(float(D_b_str), 1)
        h_b = round(float(h_b_str), 1)
        D_s = round(float(D_s_str), 1)
        h_s = round(float(h_s_str), 1)
    except ValueError:
        st.error("❌ Ange numeriska värden i fälten ovan.")
        st.stop()

# ───────────────────────────────
# Höger kolumn – RESULTAT (än så länge tom)
# ───────────────────────────────
with col_out:
    st.header("Resultat")
    st.info("Resultat kommer att visas här.")
