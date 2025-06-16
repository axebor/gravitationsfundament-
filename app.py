import streamlit as st

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

st.markdown(
    """
    <style>
    div[data-testid="stTextInput"] > div > input {
        max-width: 120px;
        width: 100%;
        box-sizing: border-box;
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
        st.markdown("Diameter D_b (m)")
        D_b_str = st.text_input("", value="5.0", key="D_b")
    with col_b2:
        st.markdown("Höjd h_b (m)")
        h_b_str = st.text_input("", value="1.0", key="h_b")

    st.markdown("**Skaft (centrerat ovanpå)**")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("Diameter D_s (m)")
        D_s_str = st.text_input("", value="1.0", key="D_s")
    with col_s2:
        st.markdown("Höjd h_s (m)")
        h_s_str = st.text_input("", value="2.0", key="h_s")

    fundament_i_vatten = st.checkbox("Fundament delvis i vatten", value=False)

    if fundament_i_vatten:
        st.markdown("Mått från underkant fundament,  $z_{v}$ (m)")
        zv_str = st.text_input("", value="0.0", key="zv")
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


