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
    div[data-testid="stTextInput"][data-key="z_niva"] > div > input,
    div[data-testid="stTextInput"][data-key="z_F"] > div > input {
        max-width: 150px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Alla kolumner lika breda
col_in, col_out, col_res = st.columns([1, 1, 1])

with col_in:
    st.header("Indata")
    st.subheader("Geometri")

    st.markdown("**Bottenplatta**")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        D_b_str = st.text_input("Diameter $D_b$ (m)", value="5.0")
    with col_b2:
        h_b_str = st.text_input("Höjd $H_b$ (m)", value="1.0")

    st.markdown("**Skaft**")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        D_s_str = st.text_input("Diameter $D_s$ (m)", value="1.0")
    with col_s2:
        h_s_str = st.text_input("Höjd $h_s$ (m)", value="2.0")

    fundament_i_vatten = st.checkbox("Fundament delvis i vatten", value=False)

    if fundament_i_vatten:
        z_niva_str = st.text_input(" $z_v$ (m) från underkant fundament", value="0.0", key="z_niva")
    else:
        z_niva_str = None

    st.subheader("Laster")
    F_str = st.text_input("Horisontell punktlast $F$ (kN)", value="0.0")
    z_F_str = st.text_input("Lastens angreppspunkt $z_F$ (m)", value="0.0", key="z_F")

    # Konvertera till float med avrundning till 1 decimal
    try:
        D_b = round(float(D_b_str), 1)
        H_b = round(float(h_b_str), 1)
        D_s = round(float(D_s_str), 1)
        h_s = round(float(h_s_str), 1)
        F = round(float(F_str), 1)
        z_F = round(float(z_F_str), 1)
        if fundament_i_vatten:
            z_v = float(z_niva_str)
        else:
            z_v = None
    except ValueError:
        st.error("❌ Ange giltiga numeriska värden för geometri, vattennivå och laster.")
        st.stop()

with col_out:
    st.header("Figur")

    fig, ax = plt.subplots(figsize=(6, 6))

    max_diameter = max(D_b, D_s)

    # Vattenområde och vattenlinje
    if fundament_i_vatten and z_v is not None and z_v > 0:
        ax.fill_between(
            x=[-max_diameter - 1, max_diameter + 1],
            y1=0, y2=z_v, color='lightblue', alpha=0.5)
        ax.hlines(y=z_v, xmin=-max_diameter - 1, xmax=max_diameter + 1,
                  colors='blue', linestyles='--', linewidth=2, label='Vattenlinje')
        # z_v måttsättning
        ax.text(max_diameter + 0.8, z_v/2, r"$z_v$", va='center', fontsize=12)

    # Bottenplatta
    ax.plot([-D_b/2, D_b/2], [0, 0], 'k-')
    ax.plot([-D_b/2, -D_b/2], [0, H_b], 'k-')
    ax.plot([D_b/2, D_b/2], [0, H_b], 'k-')
    ax.plot([-D_b/2, D_b/2], [H_b, H_b], 'k-')

    # Skaft
    ax.plot([-D_s/2, D_s/2], [H_b, H_b], 'k-')
    ax.plot([-D_s/2, -D_s/2], [H_b, H_b + h_s], 'k-')
    ax.plot([D_s/2, D_s/2], [H_b, H_b + h_s], 'k-')
    ax.plot([-D_s/2, D_s/2], [H_b + h_s, H_b + h_s], 'k-')

    # Centrumlinje (streckad) från bottenplatta till toppen av skaft
    ax.vlines(x=0, ymin=0, ymax=H_b + h_s, colors='red', linestyles='dotted', linewidth=1)

    # Måttpilar och etiketter - diametrar
    ax.annotate("", xy=(D_b/2, -0.5), xytext=(-D_b/2, -0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, -0.7, r"$D_b$", ha='center', va='top', fontsize=12)

    ax.annotate("", xy=(D_s/2, H_b + h_s + 0.5), xytext=(-D_s/2, H_b + h_s + 0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, H_b + h_s + 0.7, r"$D_s$", ha='center', va='bottom', fontsize=12)

    # Måttpilar och etiketter - höjder
    ax.annotate("", xy=(D_b/2 + 0.5, 0), xytext=(D_b/2 + 0.5, H_b),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_b/2 + 0.6, H_b/2, r"$H_b$", va='center', fontsize=12)

    ax.annotate("", xy=(D_s/2 + 0.5, H_b), xytext=(D_s/2 + 0.5, H_b + h_s),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_s/2 + 0.6, H_b + h_s/2, r"$h_s$", va='center', fontsize=12)

    # Punktlast F och måttsättning z_F från bottenplatta (y=0)
    if F > 0:
        ax.annotate("", xy=(0, z_F), xytext=(-max_diameter/2 - 1, z_F),
                    arrowprops=dict(arrowstyle="->", color='black', lw=2))
        ax.text(-max_diameter/2 - 1.1, z_F + 0.1, r"$z_{F}$", color='black', va='bottom', ha='right', fontsize=12)
        ax.text(-max_diameter/2 - 0.4, z_F + 0.2, r"$F$", color='black', va='bottom', ha='left', fontsize=14)

    ax.set_xlim(-max_diameter - 2, max_diameter + 2)
    ax.set_ylim(-1, max(H_b + h_s, z_v if z_v else 0, z_F) + 1)
    ax.set_aspect('equal')
    ax.axis('off')

    st.pyplot(fig)

with col_res:
    st.header("Resultat")

    pi = np.pi

    # Volymer
    vol_bottenplatta = pi * (D_b / 2) ** 2 * H_b
    vol_skaft = pi * (D_s / 2) ** 2 * h_s

    # Volymer under vatten och ovan vatten
    if fundament_i_vatten and z_v is not None and z_v > 0:
        under_vatten_botten = max(0, min(z_v, H_b)) * pi * (D_b / 2) ** 2
        ovan_vatten_botten = vol_bottenplatta - under_vatten_botten

        under_vatten_skaft = max(0, min(z_v - H_b, h_s)) * pi * (D_s / 2) ** 2
        ovan_vatten_skaft = vol_skaft - under_vatten_skaft
    else:
        under_vatten_botten = 0
        ovan_vatten_botten = vol_bottenplatta
        under_vatten_skaft = 0
        ovan_vatten_skaft = vol_skaft

    # Vikter (kN)
    vikt_ovan = (ovan_vatten_botten + ovan_vatten_skaft) * 25
    vikt_under = (under_vatten_botten + under_vatten_skaft) * 15
    vikt_tot = vikt_ovan + vikt_under

    # Tabell med volymer
    st.subheader("Volym")
    df_volymer = pd.DataFrame({
        "Över vatten (m³)": [round(ovan_vatten_botten, 1), round(ovan_vatten_skaft, 1)],
        "Under vatten (m³)": [round(under_vatten_botten, 1), round(under_vatten_skaft, 
