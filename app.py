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

pil_längd_extra = 3  # För horisontell pil FH
pil_längd_extra_vert = 1.5  # För vertikal pil FV (kan justeras)

col_in, col_out, col_res = st.columns([1, 1, 1])

with col_in:
    st.header("Indata")
    st.subheader("Geometri")

    st.markdown("**Bottenplatta**")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        D_b_str = st.text_input(r"Diameter $D_{b}$ (m)", value="5.0")
    with col_b2:
        H_b_str = st.text_input(r"Höjd $H_{b}$ (m)", value="1.0")

    st.markdown("**Skaft**")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        D_s_str = st.text_input(r"Diameter $D_{s}$ (m)", value="1.0")
    with col_s2:
        H_s_str = st.text_input(r"Höjd $H_{s}$ (m)", value="5.0")

    col_chk, col_zv = st.columns(2)
    with col_chk:
        fundament_i_vatten = st.checkbox("Fundament delvis i vatten", value=False)
    with col_zv:
        if fundament_i_vatten:
            z_niva_str = st.text_input(r"$z_{v}$ (m) från underkant fundament", value="0.0", key="z_niva")
        else:
            z_niva_str = None

    st.subheader("Laster")
    col_fh, col_zf = st.columns(2)
    with col_fh:
        F_H_str = st.text_input(r"Horisontell punktlast $F_{H}$ (kN)", value="0.0")
    with col_zf:
        z_F_str = st.text_input(r"Angreppsplan $z_{F}$ (m)", value="0.0")

    # Vertikal last FV
    F_V_str = st.text_input(r"Vertikal, permanent, punktlast $F_{V}$ (kN)", value="0.0")

    try:
        D_b = round(float(D_b_str), 1)
        H_b = round(float(H_b_str), 1)
        D_s = round(float(D_s_str), 1)
        H_s = round(float(H_s_str), 1)
        F_H = float(F_H_str)
        z_F = round(float(z_F_str), 1)
        F_V = float(F_V_str)
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

    if fundament_i_vatten and z_v is not None and z_v > 0:
        ax.fill_between(
            x=[-max_diameter - 1, max_diameter + 1],
            y1=0, y2=z_v, color='lightblue', alpha=0.5)
        ax.hlines(y=z_v, xmin=-max_diameter - 1, xmax=max_diameter + 1,
                  colors='blue', linestyles='--', linewidth=2)

        ax.annotate("", xy=(max_diameter + 0.5, 0), xytext=(max_diameter + 0.5, z_v),
                    arrowprops=dict(arrowstyle="<->", color='blue'))
        ax.text(max_diameter + 0.7, z_v / 2, r"$z_{v}$", va='center', fontsize=12, color='blue')

    # Bottenplatta
    ax.plot([-D_b / 2, D_b / 2], [0, 0], 'k-')
    ax.plot([-D_b / 2, -D_b / 2], [0, H_b], 'k-')
    ax.plot([D_b / 2, D_b / 2], [0, H_b], 'k-')
    ax.plot([-D_b / 2, D_b / 2], [H_b, H_b], 'k-')

    # Skaft
    ax.plot([-D_s / 2, D_s / 2], [H_b, H_b], 'k-')
    ax.plot([-D_s / 2, -D_s / 2], [H_b, H_b + H_s], 'k-')
    ax.plot([D_s / 2, D_s / 2], [H_b, H_b + H_s], 'k-')
    ax.plot([-D_s / 2, D_s / 2], [H_b + H_s, H_b + H_s], 'k-')

    # Måttpilar och etiketter - diametrar
    ax.annotate("", xy=(D_b / 2, -0.5), xytext=(-D_b / 2, -0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, -0.7, r"$D_b$", ha='center', va='top', fontsize=12)

    ax.annotate("", xy=(D_s / 2, H_b + H_s + 0.5), xytext=(-D_s / 2, H_b + H_s + 0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, H_b + H_s + 0.7, r"$D_s$", ha='center', va='bottom', fontsize=12)

    # Måttpilar och etiketter - höjder
    ax.annotate("", xy=(D_b / 2 + 0.5, 0), xytext=(D_b / 2 + 0.5, H_b),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_b / 2 + 0.6, H_b / 2, r"$H_b$", va='center', fontsize=12)

    ax.annotate("", xy=(D_s / 2 + 0.5, H_b), xytext=(D_s / 2 + 0.5, H_b + H_s),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_s / 2 + 0.6, H_b + H_s / 2, r"$H_s$", va='center', fontsize=12)

    # --- Horisontell punktlast F_H ---
    if F_H > 0:
        ax.annotate(
            "",
            xy=(-D_s / 2, z_F),
            xytext=(-D_s / 2 - pil_längd_extra, z_F),
            arrowprops=dict(arrowstyle='->', color='red', linewidth=3)
        )
        ax.text(-D_s / 2 - pil_längd_extra / 2, z_F + 0.3, r"$F_{H}$", fontsize=14, color='red', ha='center')

        # Måttlinje och text för z_F
        ax.annotate(
            "",
            xy=(-D_s / 2 - pil_längd_extra - 0.3, 0),
            xytext=(-D_s / 2 - pil_längd_extra - 0.3, z_F),
            arrowprops=dict(arrowstyle="<->", color='red')
        )
        ax.text(-D_s / 2 - pil_längd_extra - 0.1, z_F / 2, r"$z_{F}$", va='center', fontsize=12, color='red')

    # --- Vertikal punktlast F_V ---
    if F_V > 0:
        ax.annotate(
            "",
            xy=(0, 0),                   # Pilspets vid underkant fundament (y=0)
            xytext=(0, pil_längd_extra_vert),  # Pilens startpunkt ovanför
            arrowprops=dict(arrowstyle='->', color='red', linewidth=3)
        )
        ax.text(0, pil_längd_extra_vert + 0.3, r"$F_{V}$", fontsize=14, color='red', ha='center')

    ax.set_xlim(-max_diameter - pil_längd_extra - 1, max_diameter + 1.5)
    ax.set_ylim(-pil_längd_extra_vert - 1, max(H_b + H_s, z_v if z_v else 0, z_F) + 1)
    ax.set_aspect('equal')
    ax.axis('off')

    st.pyplot(fig)

with col_res:
    st.header("Resultat")

    pi = np.pi

    # Volymer
    vol_bottenplatta = pi * (D_b / 2) ** 2 * H_b
    vol_skaft = pi * (D_s / 2) ** 2 * H_s

    # Volymer under vatten och ovan vatten
    if fundament_i_vatten and z_v is not None and z_v > 0:
        under_vatten_botten = max(0, min(z_v, H_b)) * pi * (D_b / 2) ** 2
        ovan_vatten_botten = vol_bottenplatta - under_vatten_botten

        under_vatten_skaft = max(0, min(z_v - H_b, H_s)) * pi * (D_s / 2) ** 2
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

    # Underrubrik Volym
    st.markdown("### Volym")

    # Tabell med volymer (avrundat till 1 decimal och formaterat)
    df_volymer = pd.DataFrame({
        "Över vatten (m³)": [ovan_vatten_botten, ovan_vatten_skaft],
        "Under vatten (m³)": [under_vatten_botten, under_vatten_skaft]
    }, index=["Bottenplatta", "Skaft"])
    st.table(df_volymer.style.format("{:.1f}"))

    # Underrubrik Egenvikt
    st.markdown("### Egenvikt")

    # Tabell med vikter (avrundat till 1 decimal och formaterat)
    df_vikter = pd.DataFrame({
        "Vikt (kN)": [vikt_ovan, vikt_under, vikt_tot]
    }, index=["Över vatten", "Under vatten", "Total egenvikt (Gk, fund)"])
    st.table(df_vikter.style.format("{:.1f}"))
