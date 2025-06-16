import streamlit as st

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# CSS: Alla textinput-fält får samma maxbredd och bredd
st.markdown("""
    <style>
    div[data-testid="stTextInput"] > div > input {
        width: 120px !important;
        max-width: 120px !important;
        box-sizing: border-box;
    }
    </style>
""", unsafe_allow_html=True)

col_in, col_out = st.columns(2)

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

    try:
        D_b = round(float(D_b_str), 1)
        h_b = round(float(h_b_str), 1)
        D_s = round(float(D_s_str), 1)
        h_s = round(float(h_s_str), 1)
    except ValueError:
        st.error("❌ Ange giltiga numeriska värden för geometri.")
        st.stop()


