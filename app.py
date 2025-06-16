import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# CSS för lika breda inputfält
st.markdown(
    """
    <style>
    div[data-testid="stTextInput"] > div > input {
        max-width: 120px;
        width: 100%;
        box-sizing: border-box;
    }
    div[data-testid="stTextInput"][data-key="z_niva"] > div > input {
        max-width: 150px;
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
        zv_str = st.text_input("zv (v nedsänkt) (m) från underkant fundament", value="0.0", key="z_niva")
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

with col_out:
    st.header("Figur")

    fig, ax = plt.subplots(figsize=(6, 6))

if fundament_i_vatten:
    zv_str = st.text_input("z_v (m) från underkant fundament", value="0.0", key="z_niva")
        ax.fill_between(
            x=[-max(D_b, D_s) - 1, max(D_b, D_s) + 1],
            y1=0, y2=zv, color='lightblue', alpha=0.5)
        ax.hlines(y=zv, xmin=-max(D_b, D_s) - 1, xmax=max(D_b, D_s) + 1,
                  colors='blue', linestyles='--', linewidth=2, label='Vattenlinje')

        # Måttpil för vattennivå zv
        ax.annotate("", xy=(max(D_b, D_s) + 0.5, 0), xytext=(max(D_b, D_s) + 0.5, zv),
                    arrowprops=dict(arrowstyle="<->"))
        ax.text(max(D_b, D_s) + 0.7, zv / 2, r"$z_v$", va='center', fontsize=12, color='blue')

    # Bottenplatta
    ax.plot([-D_b/2, D_b/2], [0, 0], 'k-')
    ax.plot([-D_b/2, -D_b/2], [0, h_b], 'k-')
    ax.plot([D_b/2, D_b/2], [0, h_b], 'k-')
    ax.plot([-D_b/2, D_b/2], [h_b, h_b], 'k-')

    # Skaft
    ax.plot([-D_s/2, D_s/2], [h_b, h_b], 'k-')
    ax.plot([-D_s/2, -D_s/2], [h_b, h_b + h_s], 'k-')
    ax.plot([D_s/2, D_s/2], [h_b, h_b + h_s], 'k-')
    ax.plot([-D_s/2, D_s/2], [h_b + h_s, h_b + h_s], 'k-')

    # Måttpilar och etiketter - diametrar
    ax.annotate("", xy=(D_b/2, -0.5), xytext=(-D_b/2, -0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, -0.7, r"$D_b$", ha='center', va='top', fontsize=12)

    ax.annotate("", xy=(D_s/2, h_b + h_s + 0.5), xytext=(-D_s/2, h_b + h_s + 0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, h_b + h_s + 0.7, r"$D_s$", ha='center', va='bottom', fontsize=12)

    # Måttpilar och etiketter - höjder
    ax.annotate("", xy=(D_b/2 + 0.5, 0), xytext=(D_b/2 + 0.5, h_b),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_b/2 + 0.6, h_b/2, r"$h_b$", va='center', fontsize=12)

    ax.annotate("", xy=(D_s/2 + 0.5, h_b), xytext=(D_s/2 + 0.5, h_b + h_s),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_s/2 + 0.6, h_b + h_s/2, r"$h_s$", va='center', fontsize=12)

    ax.set_xlim(-max(D_b, D_s) - 1, max(D_b, D_s) + 1.5)
    ax.set_ylim(-1, max(h_b + h_s, zv if zv else 0) + 1)
    ax.set_aspect('equal')
    ax.axis('off')

    st.pyplot(fig)

with col_res:
    st.header("Resultat")

    pi = np.pi

    vol_bottenplatta = pi * (D_b / 2) ** 2 * h_b
    vol_skaft = pi * (D_s / 2) ** 2 * h_s

    if fundament_i_vatten and zv is not None and zv > 0:
        under_vatten_botten = max(0, min(zv, h_b)) * pi * (D_b / 2) ** 2
        ovan_vatten_botten = vol_bottenplatta - under_vatten_botten

        under_vatten_skaft = max(0, min(zv - h_b, h_s)) * pi * (D_s / 2) ** 2
        ovan_vatten_skaft = vol_skaft - under_vatten_skaft
    else:
        under_vatten_botten = 0
        ovan_vatten_botten = vol_bottenplatta
        under_vatten_skaft = 0
        ovan_vatten_skaft = vol_skaft

    vikt_ovan = (ovan_vatten_botten + ovan_vatten_skaft) * 25
    vikt_under = (under_vatten_botten + under_vatten_skaft) * 15
    vikt_tot = vikt_ovan + vikt_under

    st.subheader("Volym")
    df_volymer = pd.DataFrame({
        "Över vatten (m³)": [ovan_vatten_botten, ovan_vatten_skaft],
        "Under vatten (m³)": [under_vatten_botten, under_vatten_skaft]
    }, index=["Bottenplatta", "Skaft"])
    st.table(df_volymer.style.format("{:.1f}"))

    st.subheader("Gk, fund")
    df_vikter = pd.DataFrame({
        "Vikt (kN)": [vikt_ovan, vikt_under, vikt_tot]
    }, index=["Över vatten", "Under vatten", "Total egenvikt (Gk)"])
    st.table(df_vikter.style.format("{:.1f}"))

