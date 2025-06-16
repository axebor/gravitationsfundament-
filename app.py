import streamlit as st

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# CSS för lika breda inputfält
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
    span.unit {
        display: inline-block;
        margin-left: 6px;
        vertical-align: middle;
        color: #444;
        font-size: 16px;
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
        st.markdown("Diameter Dₐ (m)")
        D_b_str = st.text_input("", value="5.0", key="D_b", max_chars=6)
    with col_b2:
        st.markdown("Höjd hₐ (m)")
        h_b_str = st.text_input("", value="1.0", key="h_b", max_chars=6)

    st.markdown("**Skaft (centrerat ovanpå)**")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("Diameter Dₛ (m)")
        D_s_str = st.text_input("", value="1.0", key="D_s", max_chars=6)
    with col_s2:
        st.markdown("Höjd hₛ (m)")
        h_s_str = st.text_input("", value="2.0", key="h_s", max_chars=6)

    fundament_i_vatten = st.checkbox("Fundament delvis i vatten", value=False)

    if fundament_i_vatten:
        st.markdown("Mått från underkant fundament,  $z_{v}$ (m)")
        zv_str = st.text_input("", value="0.0", key="zv", max_chars=6)
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



