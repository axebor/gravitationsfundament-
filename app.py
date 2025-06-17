import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# ───────────────────────────────────────────────────────────
# CSS för att begränsa bredden på dina text-inputs
# ───────────────────────────────────────────────────────────
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

# ───────────────────────────────────────────────────────────
# Definiera lite parametrar för pilstorlekar och offset
# ───────────────────────────────────────────────────────────
pil_längd_extra = 2
pil_längd_extra_vert = 1.5
zQ1_x_offset = 1.2
zQ2_x_offset = 0.9

# ───────────────────────────────────────────────────────────
# Skapa tre lika kolumner för Indata / Figur / Resultat
# ───────────────────────────────────────────────────────────
col_in, col_out, col_res = st.columns([1, 1, 1])

# ───────────────
# INDATA – vänster
# ───────────────
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

    # vattennivå
    col_chk, col_zv = st.columns(2)
    with col_chk:
        fundament_i_vatten = st.checkbox("Fundament delvis i vatten", value=False)
    with col_zv:
        if fundament_i_vatten:
            z_niva_str = st.text_input(r"$z_{v}$ (m) från underkant fundament", value="0.0", key="z_niva")
        else:
            z_niva_str = None

    st.subheader("Laster")
    col_q1, col_zq1 = st.columns(2)
    with col_q1:
        Qk_H1_str = st.text_input(r"Horisontell last $Q_{k,H1}$ (kN)", value="5.0")
    with col_zq1:
        z_Q1_str = st.text_input(r"Angreppsplan $z_{Q1}$ (m)", value="0.0")

    col_q2, col_zq2 = st.columns(2)
    with col_q2:
        Qk_H2_str = st.text_input(r"Horisontell last $Q_{k,H2}$ (kN)", value="0.0")
    with col_zq2:
        z_Q2_str = st.text_input(r"Angreppsplan $z_{Q2}$ (m)", value="0.0", key="z_Q2")

    Gk_ovr_str = st.text_input(r"Vertikal last $G_{k,\mathrm{övrigt}}$ (kN)", value="5.0")

    # konvertera
    try:
        D_b   = round(float(D_b_str), 1)
        H_b   = round(float(H_b_str), 1)
        D_s   = round(float(D_s_str), 1)
        H_s   = round(float(H_s_str), 1)
        Qk_H1 = float(Qk_H1_str)
        z_Q1  = round(float(z_Q1_str), 1)
        Qk_H2 = float(Qk_H2_str)
        z_Q2  = round(float(z_Q2_str), 1)
        Gk_ovr= float(Gk_ovr_str)
        z_v   = float(z_niva_str) if fundament_i_vatten else None
    except:
        st.error("❌ Fel: ange numeriska värden!")
        st.stop()

# ───────────────
# FIGUR – mitten
# ───────────────
with col_out:
    st.header("Figur")

    fig, ax = plt.subplots(figsize=(6,6))
    max_d = max(D_b, D_s)

    # vatten
    if fundament_i_vatten and z_v>0:
        ax.fill_between([-max_d-1, max_d+1],[0,0],[z_v,z_v],
                        color='lightblue', alpha=0.5)
        ax.hlines(z_v, -max_d-1, max_d+1, linestyles='--', color='blue')
        ax.annotate("", xy=(max_d+0.5,0), xytext=(max_d+0.5,z_v),
                    arrowprops=dict(arrowstyle="<->", color='blue'))
        ax.text(max_d+0.7, z_v/2, r"$z_{v}$", va='center', color='blue')

    # geometri
    ax.plot([-D_b/2,D_b/2],[0,0],'k-')
    ax.plot([-D_b/2,-D_b/2],[0,H_b],'k-')
    ax.plot([D_b/2,D_b/2],[0,H_b],'k-')
    ax.plot([-D_b/2,D_b/2],[H_b,H_b],'k-')
    ax.plot([-D_s/2,D_s/2],[H_b,H_b],'k-')
    ax.plot([-D_s/2,-D_s/2],[H_b,H_b+H_s],'k-')
    ax.plot([D_s/2,D_s/2],[H_b,H_b+H_s],'k-')
    ax.plot([-D_s/2,D_s/2],[H_b+H_s,H_b+H_s],'k-')

    # D_b
    ax.annotate("", xy=(D_b/2,-0.5), xytext=(-D_b/2,-0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0,-0.7, r"$D_b$", ha='center', va='top')
    # D_s
    ax.annotate("", xy=(D_s/2,H_b+H_s+0.5), xytext=(-D_s/2,H_b+H_s+0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, H_b+H_s+0.7, r"$D_s$", ha='center', va='bottom')
    # H_b
    ax.annotate("", xy=(D_b/2+0.5,0), xytext=(D_b/2+0.5,H_b),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_b/2+0.6, H_b/2, r"$H_b$", va='center')
    # H_s
    ax.annotate("", xy=(D_s/2+0.5,H_b), xytext=(D_s/2+0.5,H_b+H_s),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_s/2+0.6, H_b+H_s/2, r"$H_s$", va='center')

    # Q1
    if Qk_H1>0:
        ax.annotate("", xy=(-D_s/2,z_Q1),
                    xytext=(-D_s/2-pil_längd_extra,z_Q1),
                    arrowprops=dict(arrowstyle="->", color='red', linewidth=3))
        ax.text(-D_s/2-pil_längd_extra/2 - zQ1_x_offset,
                z_Q1+0.2, r"$Q_{k,H1}$", color='red', ha='center')
        ax.annotate("", xy=(-D_s/2-pil_längd_extra-0.3-zQ1_x_offset,0),
                    xytext=(-D_s/2-pil_längd_extra-0.3-zQ1_x_offset,z_Q1),
                    arrowprops=dict(arrowstyle="<->", color='red'))
        ax.text(-D_s/2-pil_längd_extra-0.1-zQ1_x_offset,
                z_Q1/2, r"$z_{Q1}$", color='red', va='center')

    # Q2
    if Qk_H2>0:
        ax.annotate("", xy=(-D_s/2,z_Q2),
                    xytext=(-D_s/2-pil_längd_extra,z_Q2),
                    arrowprops=dict(arrowstyle="->", color='red', linewidth=3))
        ax.text(-D_s/2-pil_längd_extra/2 - zQ2_x_offset,
                z_Q2+0.2, r"$Q_{k,H2}$", color='red', ha='center')
        ax.annotate("", xy=(-D_s/2-pil_längd_extra-0.3-zQ2_x_offset,0),
                    xytext=(-D_s/2-pil_längd_extra-0.3-zQ2_x_offset,z_Q2),
                    arrowprops=dict(arrowstyle="<->", color='red'))
        ax.text(-D_s/2-pil_längd_extra-0.1-zQ2_x_offset,
                z_Q2/2, r"$z_{Q2}$", color='red', va='center')

    # Gk,övrigt
    if Gk_ovr>0:
        ax.annotate("", xy=(0,0), xytext=(0,pil_längd_extra_vert),
                    arrowprops=dict(arrowstyle="->", color='red', linewidth=3))
        ax.text(0, pil_längd_extra_vert+0.2,
                r"$G_{k,\mathrm{övrigt}}$", color='red', ha='center')

    ax.set_xlim(-max_d-pil_längd_extra-1 - max(zQ1_x_offset,zQ2_x_offset),
                 max_d+1.5)
    ax.set_ylim(-pil_längd_extra_vert-1,
                max(H_b+H_s, z_v or 0, z_Q1, z_Q2)+1)
    ax.set_aspect('equal')
    ax.axis('off')

    # ───────────────────────────────────────────────────────────
    # Här kommer knepet: tre kolumner, figuren i MITTKOL.
    # ───────────────────────────────────────────────────────────
    left, center, right = st.columns([1,2,1])
    with center:
        # minska marginaler i figuren så all annotation ryms
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
        # klipp allt som sticker ut
        for art in ax.texts + ax.patches:
            art.set_clip_on(True)
        st.pyplot(fig, use_container_width=True)

# ───────────────
# RESULTAT – höger
# ───────────────
with col_res:
    st.header("Resultat")
    pi = np.pi

    # volymer
    vol_b = pi*(D_b/2)**2*H_b
    vol_s = pi*(D_s/2)**2*H_s
    under_b = max(0,min(z_v or 0,H_b))*pi*(D_b/2)**2
    over_b  = vol_b - under_b
    under_s = max(0,min((z_v or 0)-H_b,H_s))*pi*(D_s/2)**2
    over_s  = vol_s - under_s

    Gk_b = over_b*25 + under_b*15
    Gk_s = over_s*25 + under_s*15
    Gk_tot = Gk_b + Gk_s + Gk_ovr

    M1 = Qk_H1 * z_Q1
    M2 = Qk_H2 * z_Q2

    st.markdown("### Vertikala laster")
    dfV = pd.DataFrame({
        "Värde (kN)": [Gk_b, Gk_s, Gk_ovr, Gk_tot]
    }, index=[r"$G_{k,b}$","$G_{k,s}$","$G_{k,\mathrm{övrigt}}$","$G_{k,\mathrm{tot}}$"])
    st.table(dfV.style.format("{:.1f}"))

    st.markdown("### Horisontella moment")
    dfM = pd.DataFrame({
        "Moment (kNm)": [M1, M2, M1+M2]
    }, index=[r"$M_{Q1}$",r"$M_{Q2}$",r"$M_{\mathrm{tot}}$"])
    st.table(dfM.style.format("{:.1f}"))
