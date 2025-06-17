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
    div[data-testid="stTextInput"][data-key="z_Q2"] > div > input {
        max-width: 150px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

pil_längd_extra = 2
pil_längd_extra_vert = 1.5
zQ1_x_offset = 1.2  # flytt ut åt vänster för zQ1
zQ2_x_offset = 0.9  # flytt ut åt vänster för zQ2

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
    
    # Säkerhetsklass rullgardin med kopplade γd-värden
    säkerhetsklasser = {
        "Säkerhetsklass 1 (γd=0.83)": 0.83,
        "Säkerhetsklass 2 (γd=0.91)": 0.91,
        "Säkerhetsklass 3 (γd=1.00)": 1.00
    }
    vald_säkerhetsklass = st.selectbox("Välj säkerhetsklass", list(säkerhetsklasser.keys()))
    gamma_d = säkerhetsklasser[vald_säkerhetsklass]

    col_q1, col_zq1 = st.columns(2)
    with col_q1:
        Qk_H1_str = st.text_input(r"Huvudlast horisontell $Q_{k,H1}$ (kN)", value="5.0")
    with col_zq1:
        z_Q1_str = st.text_input(r"Angreppsplan $z_{Q1}$ (m)", value="0.0")

    col_q2, col_zq2 = st.columns(2)
    with col_q2:
        Qk_H2_str = st.text_input(r"Övrig last horisontell $Q_{k,H2}$ (kN)", value="0.0")
    with col_zq2:
        z_Q2_str = st.text_input(r"Angreppsplan $z_{Q2}$ (m)", value="0.0", key="z_Q2")

    Gk_ovr_str = st.text_input(r"Vertikal last $G_{k,\mathrm{övrigt}}$ (kN)", value="5.0")

    try:
        D_b = round(float(D_b_str), 1)
        H_b = round(float(H_b_str), 1)
        D_s = round(float(D_s_str), 1)
        H_s = round(float(H_s_str), 1)

        Qk_H1 = float(Qk_H1_str)
        z_Q1 = round(float(z_Q1_str), 1)
        Qk_H2 = float(Qk_H2_str)
        z_Q2 = round(float(z_Q2_str), 1)
        Gk_ovr = float(Gk_ovr_str)

        if fundament_i_vatten:
            z_v = float(z_niva_str)
        else:
            z_v = None
    except ValueError:
        st.error("❌ Ange giltiga numeriska värden för geometri, vattennivå och laster.")
        st.stop()

with col_out:
    st.header("Figur")
    # ... Figurkod som tidigare ...

    # Placera din befintliga figurkod här utan ändring ...

with col_res:
    st.header("Resultat")

    pi = np.pi

    vol_bottenplatta = pi * (D_b / 2) ** 2 * H_b
    vol_skaft = pi * (D_s / 2) ** 2 * H_s

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

    vikt_ovan = (ovan_vatten_botten + ovan_vatten_skaft) * 25
    vikt_under = (under_vatten_botten + under_vatten_skaft) * 15
    vikt_tot = vikt_ovan + vikt_under

    # Vertikala laster från fundamentets delar
    Gk_b = (ovan_vatten_botten * 25) + (under_vatten_botten * 15)
    Gk_s = (ovan_vatten_skaft * 25) + (under_vatten_skaft * 15)
    Gk_ovr = float(Gk_ovr_str)
    Gk_tot = Gk_b + Gk_s + Gk_ovr

    # Moment från horisontella laster (kraft * momentarm)
    M_Q1 = Qk_H1 * z_Q1
    M_Q2 = Qk_H2 * z_Q2
    M_tot = M_Q1 + M_Q2

    # Lastkombinationer med vald säkerhetsklass γd
    VEd_ULS_STR = gamma_d * Gk_tot + 1.5 * M_tot
    VEd_ULS_EQU = 0.9 * gamma_d * Gk_tot + 1.5 * M_tot
    VEd_SLS = Gk_tot + M_tot

    st.markdown("### Vertikala laster")

    df_vertikala = pd.DataFrame({
        "Värde (kN)": [Gk_b, Gk_s, Gk_ovr, Gk_tot]
    }, index=[r"$G_{k,b}$ (Bottenplatta)", r"$G_{k,s}$ (Skaft)", r"$G_{k,\mathrm{övrigt}}$", r"$G_{k,\mathrm{tot}}$"])
    st.table(df_vertikala.style.format("{:.1f}"))

    st.markdown("### Moment vid fundamentets underkant")

    df_moment = pd.DataFrame({
        "Moment (kNm)": [M_Q1, M_Q2, M_tot]
    }, index=[r"$M_{Q1} = Q_{k,H1} \cdot z_{Q1}$", r"$M_{Q2} = Q_{k,H2} \cdot z_{Q2}$", r"$M_{\mathrm{tot}}$"])
    st.table(df_moment.style.format("{:.1f}"))

    st.markdown("### Lastkombinationer enligt SS-EN 1990")

    df_lastkomb = pd.DataFrame({
        "ULS STR 6.10": [f"$V_{{Ed}} = {gamma_d:.2f} \cdot G_{{tot}} + 1.5 \cdot M_{{tot}}$", f"{VEd_ULS_STR:.1f}"],
        "ULS EQU 6.10": [f"$V_{{Ed}} = 0.9 \cdot {gamma_d:.2f} \cdot G_{{tot}} + 1.5 \cdot M_{{tot}}$", f"{VEd_ULS_EQU:.1f}"],
        "SLS 6.14b": [r"$V_{Ed} = G_{tot} + M_{tot}$", f"{VEd_SLS:.1f}"]
    }, index=[r"$V_{Ed}$", "Värde (kN)"])
    st.table(df_lastkomb)
