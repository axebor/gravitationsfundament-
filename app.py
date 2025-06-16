import streamlit as st

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# Kompakt stilfix för latex-rader
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
        }
        .element-container:has(.stMarkdown) {
            line-height: 1.1rem;
        }
        .stMarkdown {
            vertical-align: top;
        }
        input[type="text"] {
            margin-top: 0.2rem;
        }
    </style>
""", unsafe_allow_html=True)


# Två kolumner: vänster = indata, höger = resultat
col_in, col_out = st.columns(2)

# ───────────────────────────────
# Vänsterkolumn: INDATA
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

    # --- Diameter bottenplatta ---
    with st.container():
        col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
        col1.write("Diameter bottenplatta")
        col2.markdown("$D_b$")
        with col3:
            D_b = float(st.text_input(label="", value="5.0", key="D_b"))
        col4.write("m")

    # --- Höjd bottenplatta ---
    with st.container():
        col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
        col1.write("Höjd bottenplatta")
        col2.markdown("$h_b$")
        with col3:
            h_b = float(st.text_input(label="", value="1.0", key="h_b"))
        col4.write("m")

    # --- Diameter skaft ---
    with st.container():
        col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
        col1.write("Diameter skaft")
        col2.markdown("$D_s$")
        with col3:
            D_s = float(st.text_input(label="", value="1.0", key="D_s"))
        col4.write("m")

    # --- Höjd skaft ---
    with st.container():
        col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
        col1.write("Höjd skaft")
        col2.markdown("$h_s$")
        with col3:
            h_s = float(st.text_input(label="", value="2.0", key="h_s"))
        col4.write("m")

# ───────────────────────────────
# Högerkolumn: RESULTAT (tom än så länge)
# ───────────────────────────────
with col_out:
    st.header("Resultat")
    st.info("Resultat kommer att visas här.")
