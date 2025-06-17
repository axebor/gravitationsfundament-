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

# parametrar för pilar och offset
pil_längd_extra = 3
pil_längd_extra_vert = 1.5
zQ1_x_offset = 1.2
zQ2_x_offset = 0.9

# Huvudkolumner: indata, figur, resultat
col_in, col_out, col_res = st.columns([1, 1, 1])

# ───────────────
# INDATA
# ───────────────
with col_in:
    st.header("Indata")
    st.subheader("Geometri")

    st.markdown("**Bottenplatta**")
    c1, c2 = st.columns(2)
    with c1:
        D_b_str = st.text_input(r"Diameter $D_{b}$ (m)", "5.0")
    with c2:
        H_b_str = st.text_input(r"Höjd $H_{b}$ (m)", "1.0")

    st.markdown("**Skaft**")
    c3, c4 = st.columns(2)
    with c3:
        D_s_str = st.text_input(r"Diameter $D_{s}$ (m)", "1.0")
    with c4:
        H_s_str = st.text_input(r"Höjd $H_{s}$ (m)", "5.0")

    chk, zvcol = st.columns(2)
    with chk:
        fundament_i_vatten = st.checkbox("Fundament delvis i vatten", False)
    with zvcol:
        if fundament_i_vatten:
            z_niva_str = st.text_input(r"$z_{v}$ (m) från underkant fundament", "0.0", key="z_niva")
        else:
            z_niva_str = None

    st.subheader("Laster")
    c5, c6 = st.columns(2)
    with c5:
        Qk_H1_str = st.text_input(r"Horisontell last $Q_{k,H1}$ (kN)", "5.0")
    with c6:
        z_Q1_str = st.text_input(r"Angreppsplan $z_{Q1}$ (m)", "0.0")

    c7, c8 = st.columns(2)
    with c7:
        Qk_H2_str = st.text_input(r"Horisontell last $Q_{k,H2}$ (kN)", "0.0")
    with c8:
        z_Q2_str = st.text_input(r"Angreppsplan $z_{Q2}$ (m)", "0.0", key="z_Q2")

    Gk_ovr_str = st.text_input(r"Vertikal last $G_{k,\mathrm{övrigt}}$ (kN)", "5.0")

    # Konvertera indata
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

        z_v = float(z_niva_str) if fundament_i_vatten else None
    except ValueError:
        st.error("❌ Ogiltiga värden i indata.")
        st.stop()

# ───────────────
# FIGUR
# ───────────────
with col_out:
    st.header("Figur")

    # Rita figuren
    fig, ax = plt.subplots(figsize=(10, 10))
    max_d = max(D_b, D_s)

    # Vattennivå
    if fundament_i_vatten and z_v and z_v > 0:
        ax.fill_between([-max_d - 1, max_d + 1], 0, z_v, color="lightblue", alpha=0.5)
        ax.hlines(z_v, -max_d - 1, max_d + 1, colors="blue", linestyles="--", linewidth=2)
        ax.annotate("", xy=(max_d + 0.5, 0), xytext=(max_d + 0.5, z_v),
                    arrowprops=dict(arrowstyle="<->", color="blue"))
        ax.text(max_d + 0.7, z_v / 2, r"$z_{v}$", va="center", color="blue")

    # Bottenplatta
    ax.plot([-D_b/2, D_b/2], [0, 0], "k-")
    ax.plot([-D_b/2, -D_b/2], [0, H_b], "k-")
    ax.plot([ D_b/2,  D_b/2], [0, H_b], "k-")
    ax.plot([-D_b/2,  D_b/2], [H_b, H_b], "k-")

    # Skaft
    ax.plot([-D_s/2, D_s/2], [H_b, H_b], "k-")
    ax.plot([-D_s/2, -D_s/2], [H_b, H_b + H_s], "k-")
    ax.plot([ D_s/2,  D_s/2], [H_b, H_b + H_s], "k-")
    ax.plot([-D_s/2, D_s/2], [H_b + H_s, H_b + H_s], "k-")

    # Diametrar
    ax.annotate("", xy=(D_b/2, -0.5), xytext=(-D_b/2, -0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, -0.7, r"$D_b$", ha="center", va="top", fontsize=12)

    ax.annotate("", xy=(D_s/2, H_b + H_s + 0.5), xytext=(-D_s/2, H_b + H_s + 0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, H_b + H_s + 0.7, r"$D_s$", ha="center", va="bottom", fontsize=12)

    # Höjder
    ax.annotate("", xy=(D_b/2 + 0.5, 0), xytext=(D_b/2 + 0.5, H_b),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_b/2 + 0.6, H_b/2, r"$H_b$", va="center", fontsize=12)

    ax.annotate("", xy=(D_s/2 + 0.5, H_b), xytext=(D_s/2 + 0.5, H_b + H_s),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_s/2 + 0.6, H_b + H_s/2, r"$H_s$", va="center", fontsize=12)

    # Horisontella laster Qk,H1 och Qk,H2
    if Qk_H1 > 0:
        ax.annotate("", xy=(-D_s/2, z_Q1), xytext=(-D_s/2 - pil_längd_extra, z_Q1),
                    arrowprops=dict(arrowstyle="->", color="red", linewidth=3))
        ax.text(-D_s/2 - pil_längd_extra/2 - zQ1_x_offset, z_Q1 + 0.3,
                r"$Q_{k,H1}$", color="red", ha="center")
        ax.annotate("", xy=(-D_s/2 - pil_längd_extra - 0.3 - zQ1_x_offset, 0),
                    xytext=(-D_s/2 - pil_längd_extra - 0.3 - zQ1_x_offset, z_Q1),
                    arrowprops=dict(arrowstyle="<->", color="red"))
        ax.text(-D_s/2 - pil_längd_extra - 0.1 - zQ1_x_offset, z_Q1/2,
                r"$z_{Q1}$", va="center", color="red")

    if Qk_H2 > 0:
        ax.annotate("", xy=(-D_s/2, z_Q2), xytext=(-D_s/2 - pil_längd_extra, z_Q2),
                    arrowprops=dict(arrowstyle="->", color="red", linewidth=3))
        ax.text(-D_s/2 - pil_längd_extra/2 - zQ2_x_offset, z_Q2 + 0.3,
                r"$Q_{k,H2}$", color="red", ha="center")
        ax.annotate("", xy=(-D_s/2 - pil_längd_extra - 0.3 - zQ2_x_offset, 0),
                    xytext=(-D_s/2 - pil_längd_extra - 0.3 - zQ2_x_offset, z_Q2),
                    arrowprops=dict(arrowstyle="<->", color="red"))
        ax.text(-D_s/2 - pil_längd_extra - 0.1 - zQ2_x_offset, z_Q2/2,
                r"$z_{Q2}$", va="center", color="red")

    # Vertikal last Gk,övrigt
    if Gk_ovr > 0:
        ax.annotate("", xy=(0, 0), xytext=(0, pil_längd_extra_vert),
                    arrowprops=dict(arrowstyle="->", color="red", linewidth=3))
        ax.text(0, pil_längd_extra_vert + 0.3,
                r"$G_{k,\mathrm{övrigt}}$", color="red", ha="center")

    ax.set_xlim(-max_d - pil_längd_extra - 1 - max(zQ1_x_offset, zQ2_x_offset), max_d + 1.5)
    ax.set_ylim(-pil_längd_extra_vert - 1, max(H_b + H_s, z_v or 0, z_Q1, z_Q2) + 1)
    ax.set_aspect("equal")
    ax.axis("off")

# ───────────────
# RESULTAT
# ───────────────
with col_res:
    st.header("Resultat")

    pi = np.pi
    vikt_ovan = lambda vol: vol * 25
    vikt_under = lambda vol: vol * 15

    # Volymer
    vol_b = pi * (D_b / 2) ** 2 * H_b
    vol_s = pi * (D_s / 2) ** 2 * H_s

    # Volymer över/under vatten
    if fundament_i_vatten and z_v and z_v > 0:
        vol_b_u = max(0, min(z_v, H_b)) * np.pi * (D_b / 2) ** 2
        vol_b_o = vol_b - vol_b_u
        vol_s_u = max(0, min(z_v - H_b, H_s)) * np.pi * (D_s / 2) ** 2
        vol_s_o = vol_s - vol_s_u
    else:
        vol_b_o, vol_b_u = vol_b, 0
        vol_s_o, vol_s_u = vol_s, 0

    # Egenvikter
    Gk_b = vikt_ovan(vol_b_o) + vikt_under(vol_b_u)
    Gk_s = vikt_ovan(vol_s_o) + vikt_under(vol_s_u)
    Gk_tot = Gk_b + Gk_s + Gk_ovr

    # Moment
    M_Q1 = Qk_H1 * z_Q1
    M_Q2 = Qk_H2 * z_Q2

    # Visa resultat
    st.markdown("### Vertikala laster")
    df_vert = pd.DataFrame({
        "Värde (kN)": [Gk_b, Gk_s, Gk_ovr, Gk_tot]
    }, index=[r"$G_{k,b}$", r"$G_{k,s}$", r"$G_{k,\mathrm{övrigt}}$", r"$G_{k,\mathrm{tot}}$"])
    st.table(df_vert.style.format("{:.1f}"))

    st.markdown("### Horisontella moment i bottenplattan")
    df_mom = pd.DataFrame({
        "Moment (kNm)": [M_Q1, M_Q2]
    }, index=[r"$M_{Q1}$", r"$M_{Q2}$"])
    st.table(df_mom.style.format("{:.1f}"))
