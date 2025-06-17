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

    fig, ax = plt.subplots(figsize=(8, 8))
    max_diameter = max(D_b, D_s)

    # Vattennivå
    if fundament_i_vatten and z_v is not None and z_v > 0:
        ax.fill_between(
            x=[-max_diameter - 1, max_diameter + 1],
            y1=0, y2=z_v, color='lightblue', alpha=0.5)
        ax.hlines(y=z_v, xmin=-max_diameter - 1, xmax=max_diameter + 1,
                  colors='blue', linestyles='--', linewidth=2)

        ax.annotate("", xy=(max_diameter + 0.5, 0), xytext=(max_diameter + 0.5, z_v),
                    arrowprops=dict(arrowstyle="<->", color='blue'))
        ax.text(max_diameter + 0.7, z_v / 2, r"$z_{v}$", va='center', fontsize=12, color='blue')

    # Fundamentets geometri
    ax.plot([-D_b / 2, D_b / 2], [0, 0], 'k-')
    ax.plot([-D_b / 2, -D_b / 2], [0, H_b], 'k-')
    ax.plot([D_b / 2, D_b / 2], [0, H_b], 'k-')
    ax.plot([-D_b / 2, D_b / 2], [H_b, H_b], 'k-')

    ax.plot([-D_s / 2, D_s / 2], [H_b, H_b], 'k-')
    ax.plot([-D_s / 2, -D_s / 2], [H_b, H_b + H_s], 'k-')
    ax.plot([D_s / 2, D_s / 2], [H_b, H_b + H_s], 'k-')
    ax.plot([-D_s / 2, D_s / 2], [H_b + H_s, H_b + H_s], 'k-')

    # Måttlinjer - diametrar
    ax.annotate("", xy=(D_b / 2, -0.5), xytext=(-D_b / 2, -0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, -0.7, r"$D_b$", ha='center', va='top', fontsize=12)

    ax.annotate("", xy=(D_s / 2, H_b + H_s + 0.5), xytext=(-D_s / 2, H_b + H_s + 0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, H_b + H_s + 0.7, r"$D_s$", ha='center', va='bottom', fontsize=12)

    # Måttlinjer - höjder
    ax.annotate("", xy=(D_b / 2 + 0.5, 0), xytext=(D_b / 2 + 0.5, H_b),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_b / 2 + 0.6, H_b / 2, r"$H_b$", va='center', fontsize=12)

    ax.annotate("", xy=(D_s / 2 + 0.5, H_b), xytext=(D_s / 2 + 0.5, H_b + H_s),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_s / 2 + 0.6, H_b + H_s / 2, r"$H_s$", va='center', fontsize=12)

    # Horisontella laster Qk,H1 och Qk,H2 i rött, med större x-offset på zQ1 och zQ2
    if Qk_H1 > 0:
        ax.annotate(
            "",
            xy=(-D_s / 2, z_Q1),
            xytext=(-D_s / 2 - pil_längd_extra, z_Q1),
            arrowprops=dict(arrowstyle='->', color='red', linewidth=3)
        )
        ax.text(-D_s / 2 - pil_längd_extra / 2 - zQ1_x_offset, z_Q1 + 0.3,
                r"$Q_{k,H1}$", fontsize=14, color='red', ha='center')

        ax.annotate(
            "",
            xy=(-D_s / 2 - pil_längd_extra - 0.3 - zQ1_x_offset, 0),
            xytext=(-D_s / 2 - pil_längd_extra - 0.3 - zQ1_x_offset, z_Q1),
            arrowprops=dict(arrowstyle="<->", color='red')
        )
        ax.text(-D_s / 2 - pil_längd_extra - 0.1 - zQ1_x_offset, z_Q1 / 2,
                r"$z_{Q1}$", va='center', fontsize=12, color='red')

    if Qk_H2 > 0:
        ax.annotate(
            "",
            xy=(-D_s / 2, z_Q2),
            xytext=(-D_s / 2 - pil_längd_extra, z_Q2),
            arrowprops=dict(arrowstyle='->', color='red', linewidth=3)
        )
        ax.text(-D_s / 2 - pil_längd_extra / 2 - zQ2_x_offset, z_Q2 + 0.3,
                r"$Q_{k,H2}$", fontsize=14, color='red', ha='center')

        ax.annotate(
            "",
            xy=(-D_s / 2 - pil_längd_extra - 0.3 - zQ2_x_offset, 0),
            xytext=(-D_s / 2 - pil_längd_extra - 0.3 - zQ2_x_offset, z_Q2),
            arrowprops=dict(arrowstyle="<->", color='red')
        )
        ax.text(-D_s / 2 - pil_längd_extra - 0.1 - zQ2_x_offset, z_Q2 / 2,
                r"$z_{Q2}$", va='center', fontsize=12, color='red')

    # Vertikal last Gk,övrigt
    if Gk_ovr > 0:
        ax.annotate(
            "",
            xy=(0, 0),
            xytext=(0, pil_längd_extra_vert),
            arrowprops=dict(arrowstyle='->', color='red', linewidth=3)
        )
        ax.text(0, pil_längd_extra_vert + 0.3, r"$G_{k,\mathrm{övrigt}}$", fontsize=14, color='red', ha='center')

    # Justera x-axelgränser symmetriskt för att centrera figuren
    max_offset = max(pil_längd_extra + max(zQ1_x_offset, zQ2_x_offset) + 1, 1.5)
    ax.set_xlim(-max_diameter - max_offset, max_diameter + max_offset)

    ax.set_ylim(-pil_längd_extra_vert - 1, max(H_b + H_s, z_v if z_v else 0, z_Q1, z_Q2) + 1)
    ax.set_aspect('equal')
    ax.axis('off')
    st.pyplot(fig, use_container_width=True)

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

    # --- Lastkombinationer enligt SS-EN 1990 ---
    st.markdown("### Lastkombinationer enligt SS-EN 1990")

    st.markdown(r"""
    **STR 6.10**  
    $M_{Ed} = 1.35 \times M_{tot}$  
    $V_{Ed} = 1.35 \times G_{tot}$  

    **EQU 6.10**  
    $M_{Ed} = 1.0 \times M_{tot} + 1.5 \times 0.5 \times G_{tot}$  
    $V_{Ed} = 1.0 \times G_{tot}$  

    **SLS 6.14b**  
    $M_{Ed} = 1.0 \times M_{tot}$  
    $V_{Ed} = 1.0 \times G_{tot}$
    """)

    M_Str = 1.35 * M_tot
    V_Str = 1.35 * Gk_tot
    M_Equ = 1.0 * M_tot + 1.5 * 0.5 * Gk_tot
    V_Equ = 1.0 * Gk_tot
    M_SLS = 1.0 * M_tot
    V_SLS = 1.0 * Gk_tot

    df_varden = pd.DataFrame({
        "STR 6.10": [round(M_Str, 1), round(V_Str, 1)],
        "EQU 6.10": [round(M_Equ, 1), round(V_Equ, 1)],
        "SLS 6.14b": [round(M_SLS, 1), round(V_SLS, 1)],
    }, index=[r"$M_{Ed}$", r"$V_{Ed}$"])

    st.table(df_varden)
