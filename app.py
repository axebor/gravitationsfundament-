import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# ─────────────────────────────────────────────────────────────────────────────
# CSS för lika breda inputfält
# ─────────────────────────────────────────────────────────────────────────────
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

pil_längd_extra     = 2
pil_längd_extra_vert= 1.5
zQ1_x_offset        = 1.2
zQ2_x_offset        = 0.9

# ─────────────────────────────────────────────────────────────────────────────
# Tre lika kolumner
# ─────────────────────────────────────────────────────────────────────────────
col_in, col_out, col_res = st.columns([1,1,1])

# ───────────────
# INDATA
# ───────────────
with col_in:
    st.header("Indata")
    st.subheader("Geometri")

    st.markdown("**Bottenplatta**")
    b1, b2 = st.columns(2)
    with b1:
        D_b_str = st.text_input(r"Diameter $D_{b}$ (m)", "5.0")
    with b2:
        H_b_str = st.text_input(r"Höjd $H_{b}$ (m)", "1.0")

    st.markdown("**Skaft**")
    s1, s2 = st.columns(2)
    with s1:
        D_s_str = st.text_input(r"Diameter $D_{s}$ (m)", "1.0")
    with s2:
        H_s_str = st.text_input(r"Höjd $H_{s}$ (m)", "5.0")

    chk, zvc = st.columns(2)
    with chk:
        fundament_i_vatten = st.checkbox("Fundament delvis i vatten", False)
    with zvc:
        z_niv_str = (
            st.text_input(r"$z_{v}$ (m) från underkant fundament", "0.0", key="z_niva")
            if fundament_i_vatten else None
        )

    st.subheader("Laster")
    q1, zq1c = st.columns(2)
    with q1:
        Q1_str = st.text_input(r"Horisontell last $Q_{k,H1}$ (kN)", "5.0")
    with zq1c:
        zQ1_str = st.text_input(r"Angreppsplan $z_{Q1}$ (m)", "0.0")

    q2, zq2c = st.columns(2)
    with q2:
        Q2_str = st.text_input(r"Horisontell last $Q_{k,H2}$ (kN)", "0.0")
    with zq2c:
        zQ2_str = st.text_input(r"Angreppsplan $z_{Q2}$ (m)", "0.0", key="z_Q2")

    Govr_str = st.text_input(r"Vertikal last $G_{k,\mathrm{övrigt}}$ (kN)", "5.0")

    # Konvertering
    try:
        D_b   = round(float(D_b_str),1)
        H_b   = round(float(H_b_str),1)
        D_s   = round(float(D_s_str),1)
        H_s   = round(float(H_s_str),1)
        Q1    = float(Q1_str)
        zQ1   = round(float(zQ1_str),1)
        Q2    = float(Q2_str)
        zQ2   = round(float(zQ2_str),1)
        Govr  = float(Govr_str)
        z_v   = float(z_niv_str) if fundament_i_vatten else None
    except:
        st.error("❌ Ange giltiga numeriska värden.")
        st.stop()

# ───────────────
# FIGUR
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
        ax.annotate("", (max_d+0.5,0),(max_d+0.5,z_v),
                    arrowprops=dict(arrowstyle="<->", color='blue'))
        ax.text(max_d+0.7,z_v/2, r"$z_{v}$", color='blue', va='center')

    # geometri-ram
    # bottenplatta
    ax.plot([-D_b/2,D_b/2],[0,0],'k-')
    ax.plot([-D_b/2,-D_b/2],[0,H_b],'k-')
    ax.plot([D_b/2,D_b/2],[0,H_b],'k-')
    ax.plot([-D_b/2,D_b/2],[H_b,H_b],'k-')
    # skaft
    ax.plot([-D_s/2,D_s/2],[H_b,H_b],'k-')
    ax.plot([-D_s/2,-D_s/2],[H_b,H_b+H_s],'k-')
    ax.plot([D_s/2,D_s/2],[H_b,H_b+H_s],'k-')
    ax.plot([-D_s/2,D_s/2],[H_b+H_s,H_b+H_s],'k-')

    # D_b
    ax.annotate("", (D_b/2,-0.5),(-D_b/2,-0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0,-0.7,r"$D_b$",ha='center',va='top')
    # D_s
    ax.annotate("", (D_s/2,H_b+H_s+0.5),(-D_s/2,H_b+H_s+0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0,H_b+H_s+0.7, r"$D_s$",ha='center',va='bottom')
    # H_b
    ax.annotate("", (D_b/2+0.5,0),(D_b/2+0.5,H_b),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_b/2+0.6,H_b/2,r"$H_b$",va='center')
    # H_s
    ax.annotate("", (D_s/2+0.5,H_b),(D_s/2+0.5,H_b+H_s),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_s/2+0.6,H_b+H_s/2,r"$H_s$",va='center')

    # Q1
    if Q1>0:
        ax.annotate("",(-D_s/2,zQ1),(-D_s/2-pil_längd_extra,zQ1),
                    arrowprops=dict(arrowstyle="->",color='red',linewidth=3))
        ax.text(-D_s/2-pil_längd_extra/2 - zQ1_x_offset,
                zQ1+0.2,r"$Q_{k,H1}$",color='red',ha='center')
        ax.annotate("",(-D_s/2-pil_längd_extra-0.3-zQ1_x_offset,0),
                    (-D_s/2-pil_längd_extra-0.3-zQ1_x_offset,zQ1),
                    arrowprops=dict(arrowstyle="<->",color='red'))
        ax.text(-D_s/2-pil_längd_extra-0.1-zQ1_x_offset,
                zQ1/2,r"$z_{Q1}$",color='red',va='center')

    # Q2
    if Q2>0:
        ax.annotate("",(-D_s/2,zQ2),(-D_s/2-pil_längd_extra,zQ2),
                    arrowprops=dict(arrowstyle="->",color='red',linewidth=3))
        ax.text(-D_s/2-pil_längd_extra/2 - zQ2_x_offset,
                zQ2+0.2,r"$Q_{k,H2}$",color='red',ha='center')
        ax.annotate("",(-D_s/2-pil_längd_extra-0.3-zQ2_x_offset,0),
                    (-D_s/2-pil_längd_extra-0.3-zQ2_x_offset,zQ2),
                    arrowprops=dict(arrowstyle="<->",color='red'))
        ax.text(-D_s/2-pil_längd_extra-0.1-zQ2_x_offset,
                zQ2/2,r"$z_{Q2}$",color='red',va='center')

    # Gk,övrigt
    if Govr>0:
        ax.annotate("", (0,0),(0,pil_längd_extra_vert),
                    arrowprops=dict(arrowstyle="->",color='red',linewidth=3))
        ax.text(0,pil_längd_extra_vert+0.2,
                r"$G_{k,\mathrm{övrigt}}$",color='red',ha='center')

    ax.set_xlim(-max_d-pil_längd_extra-1 - max(zQ1_x_offset,zQ2_x_offset),
                 max_d+1.5)
    ax.set_ylim(-pil_längd_extra_vert-1,
                max(H_b+H_s, z_v or 0, zQ1, zQ2)+1)
    ax.set_aspect('equal')
    ax.axis('off')

    # ─────────────────────────────────────────────────────────────────────────
    # RENDERA SOM BILD – blir automatiskt centrerad och fylld i kolumnen
    # ─────────────────────────────────────────────────────────────────────────
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    st.image(buf, use_column_width=True)

# ───────────────
# RESULTAT
# ───────────────
with col_res:
    st.header("Resultat")
    pi = np.pi

    # volymer + vikter
    vol_b = pi*(D_b/2)**2 * H_b
    vol_s = pi*(D_s/2)**2 * H_s
    under_b = max(0,min(z_v or 0,H_b)) * pi*(D_b/2)**2
    over_b  = vol_b - under_b
    under_s = max(0,min((z_v or 0)-H_b,H_s)) * pi*(D_s/2)**2
    over_s  = vol_s - under_s

    Gk_b   = over_b*25 + under_b*15
    Gk_s   = over_s*25 + under_s*15
    Gk_tot = Gk_b + Gk_s + Govr

    M1 = Q1*zQ1
    M2 = Q2*zQ2

    st.markdown("### Vertikala laster")
    dfV = pd.DataFrame({
        "Värde (kN)": [Gk_b, Gk_s, Govr, Gk_tot]
    }, index=[r"$G_{k,b}$","$G_{k,s}$","$G_{k,\mathrm{övrigt}}$","$G_{k,\mathrm{tot}}$"])
    st.table(dfV.style.format("{:.1f}"))

    st.markdown("### Horisontella moment")
    dfM = pd.DataFrame({
        "Moment (kNm)": [M1, M2, M1+M2]
    }, index=[r"$M_{Q1}$",r"$M_{Q2}$",r"$M_{\mathrm{tot}}$"])
    st.table(dfM.style.format("{:.1f}"))
