import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# CSS för lika breda inputfält + vertikala linjer mellan kolumner (ej indata-kolumn)
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
    /* Vertikala linjer mellan kolumner - endast mellan mitt och höger */
    [data-testid="stColumns"] > div:nth-child(2) {
        border-right: 1px solid #cccccc;
        padding-right: 15px;
    }
    [data-testid="stColumns"] > div:nth-child(3) {
        padding-left: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

pil_längd_extra = 2
pil_längd_extra_vert = 1.5
zQ1_x_offset = 1.2
zQ2_x_offset = 0.9

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
        fundament_i_vatten = st.checkbox("Fundament delvis i vatten", value=True)
    with col_zv:
        if fundament_i_vatten:
            z_niva_str = st.text_input(r"$z_{v}$ (m) från underkant fundament", value="3.0", key="z_niva")
        else:
            z_niva_str = None

    st.subheader("Laster")

    sk_col1, sk_col2 = st.columns([1, 1])
    with sk_col1:
        säkerhetsklass_val = st.selectbox(
            "Välj säkerhetsklass",
            options=["1", "2", "3"],
            index=2
        )
    with sk_col2:
        gamma_d_dict = {"1": 0.83, "2": 0.91, "3": 1.00}
        gamma_d = gamma_d_dict[säkerhetsklass_val]
        st.markdown(
            f'<div style="padding-top: 24px;">γ<sub>d</sub> = <b>{gamma_d:.2f}</b></div>',
            unsafe_allow_html=True
        )

    # Horisontella laster och lastkombinationsfaktor med angreppsplan på samma rad
    col_q1, col_psi, col_zq1 = st.columns([1, 1, 1])
    with col_q1:
        Qk_H1_str = st.text_input(r"Huvudlast horisontell $Q_{k,H1}$ (kN)", value="0.0")
    with col_psi:
        st.markdown("")  # Ingen lastkombinationsfaktor för huvudlast
    with col_zq1:
        z_Q1_str = st.text_input(r"Angreppsplan $z_{Q1}$ (m)", value="0.0")

    col_q2, col_psi2, col_zq2 = st.columns([1, 1, 1])
    with col_q2:
        Qk_H2_str = st.text_input(r"Övrig last horisontell $Q_{k,H2}$ (kN)", value="0.0")
    with col_psi2:
        psi_ovr = st.number_input("Lastkombinationsfaktor $\psi_0$", min_value=0.0, max_value=1.0, value=1.0, step=0.05)
    with col_zq2:
        z_Q2_str = st.text_input(r"Angreppsplan $z_{Q2}$ (m)", value="0.0", key="z_Q2")

    Gk_ovr_str = st.text_input(r"Vertikal last $G_{k,\mathrm{övrigt}}$ (kN)", value="0.0")

try:
    D_b = round(float(D_b_str), 1)
    H_b = round(float(H_b_str), 1)
    D_s = round(float(D_s_str), 1)
    H_s = round(float(H_s_str), 1)

    Qk_H1 = float(Qk_H1_str)
    Qk_H2 = float(Qk_H2_str)
    z_Q1 = round(float(z_Q1_str), 1)
    z_Q2 = round(float(z_Q2_str), 1)
    Gk_ovr = float(Gk_ovr_str)

    if fundament_i_vatten:
        z_v = float(z_niva_str)
    else:
        z_v = None
except ValueError:
    st.error("❌ Ange giltiga numeriska värden för geometri, vattennivå och laster.")
    st.stop()

# Flytta här beräkningarna så variablerna blir globala

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

Gk_b = (ovan_vatten_botten * 25) + (under_vatten_botten * 15)
Gk_s = (ovan_vatten_skaft * 25) + (under_vatten_skaft * 15)
Gk_tot = Gk_b + Gk_s + Gk_ovr

M_Q1 = Qk_H1 * z_Q1
M_Q2 = Qk_H2 * z_Q2

with col_out:
    st.header("Figur")

    fig, ax = plt.subplots(figsize=(8, 8))
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

    ax.plot([-D_b / 2, D_b / 2], [0, 0], 'k-')
    ax.plot([-D_b / 2, -D_b / 2], [0, H_b], 'k-')
    ax.plot([D_b / 2, D_b / 2], [0, H_b], 'k-')
    ax.plot([-D_b / 2, D_b / 2], [H_b, H_b], 'k-')

    ax.plot([-D_s / 2, D_s / 2], [H_b, H_b], 'k-')
    ax.plot([-D_s / 2, -D_s / 2], [H_b, H_b + H_s], 'k-')
    ax.plot([D_s / 2, D_s / 2], [H_b, H_b + H_s], 'k-')
    ax.plot([-D_s / 2, D_s / 2], [H_b + H_s, H_b + H_s], 'k-')

    ax.annotate("", xy=(D_b / 2, -0.5), xytext=(-D_b / 2, -0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, -0.7, r"$D_b$", ha='center', va='top', fontsize=12)

    ax.annotate("", xy=(D_s / 2, H_b + H_s + 0.5), xytext=(-D_s / 2, H_b + H_s + 0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, H_b + H_s + 0.7, r"$D_s$", ha='center', va='bottom', fontsize=12)

    ax.annotate("", xy=(D_b / 2 + 0.5, 0), xytext=(D_b / 2 + 0.5, H_b),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_b / 2 + 0.6, H_b / 2, r"$H_b$", va='center', fontsize=12)

    ax.annotate("", xy=(D_s / 2 + 0.5, H_b), xytext=(D_s / 2 + 0.5, H_b + H_s),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_s / 2 + 0.6, H_b + H_s / 2, r"$H_s$", va='center', fontsize=12)

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

    if Gk_ovr > 0:
        ax.annotate(
            "",
            xy=(0, 0),
            xytext=(0, pil_längd_extra_vert),
            arrowprops=dict(arrowstyle='->', color='red', linewidth=3)
        )
        ax.text(0, pil_längd_extra_vert + 0.3, r"$G_{k,\mathrm{övrigt}}$", fontsize=14, color='red', ha='center')

    ax.fill_between(
        x=[-max_diameter - 1, max_diameter + 1],
        y1=-pil_längd_extra_vert - 1,
        y2=0,
        color='#d2b48c', alpha=0.5
    )
    
    ax.fill_between(
        x=[-D_b/2, D_b/2],
        y1=0,
        y2=H_b,
        color='lightgrey',
        alpha=0.8
    )
    
    ax.fill_between(
        x=[-D_s/2, D_s/2],
        y1=H_b,
        y2=H_b + H_s,
        color='lightgrey',
        alpha=0.8
    )
    
    max_offset = max(pil_längd_extra + max(zQ1_x_offset, zQ2_x_offset) + 1, 1.5)
    ax.set_xlim(-max_diameter - max_offset, max_diameter + max_offset)

    ax.set_ylim(-pil_längd_extra_vert - 1, max(H_b + H_s, z_v if z_v else 0, z_Q1, z_Q2) + 1)
    ax.set_aspect('equal')
    ax.axis('off')

    st.pyplot(fig, use_container_width=True)

    # Lastsammanställning under figuren
    st.header("Lastsammanställning")

    col_vert, col_moment = st.columns(2)

    with col_vert:
        st.subheader("Permanenta laster")
        df_vertikala = pd.DataFrame({
            "Värde (kN)": [Gk_b, Gk_s, Gk_ovr, Gk_tot]
        }, index=[r"$G_{k,b}$ (Bottenplatta)", r"$G_{k,s}$ (Skaft)", r"$G_{k,\mathrm{övrigt}}$", r"$G_{k,\mathrm{tot}}$"])
        st.table(df_vertikala.style.format("{:.1f}"))

    with col_moment:
        st.subheader("Variabla laster")
        df_moment = pd.DataFrame({
            "Moment (kNm)": [M_Q1, M_Q2, M_Q1 + M_Q2]
        }, index=[r"$M_{Q1} = Q_{k,H1} \cdot z_{Q1}$", r"$M_{Q2} = Q_{k,H2} \cdot z_{Q2}$", r"$M_{\mathrm{tot}}$"])

        styled_df_moment = df_moment.style.format("{:.1f}").set_table_styles([
            {'selector': 'th.col0', 'props': [('white-space', 'nowrap'), ('min-width', '60px')]},
            {'selector': 'td.col0', 'props': [('white-space', 'nowrap')]},
            {'selector': 'th.col1', 'props': [('white-space', 'nowrap'), ('min-width', '300px')]},
            {'selector': 'td.col1', 'props': [('white-space', 'nowrap')]}
        ])
        st.table(styled_df_moment)


with col_res:
    st.header("Resultat")

    st.markdown(
        """
        Kombination av laster görs enligt SS-EN 1990 samt de svenska reglerna i BFS 2024:6.<br>
        I denna app används <b>Lastkombination 3</b> för kontroll av statisk jämvikt och <b>Lastkombination 4</b> för dimensionering av geotekniska laster.<br><br>
        <b>Permanent last:</b> inkluderar egenvikt och andra permanenta laster.<br>
        <b>Variabel last:</b> inkluderar laster som kan variera, t.ex. is och våg-last.<br>
        """
    , unsafe_allow_html=True
    )

    VEd_LK3 = 0.9 * Gk_tot  # gynnsam vertikal last utan gamma_d
    VEd_LK4 = max(1.1 * gamma_d * Gk_tot, Gk_tot)

    MEd_LK3 = gamma_d * (1.5 * M_Q1 + 1.5 * psi_ovr * M_Q2)
    MEd_LK4 = gamma_d * (1.4 * M_Q1 + 1.4 * psi_ovr * M_Q2)

    lastkombination_md = f"""
    | Parameter                               | Lastkombination 3 (Jämvikt)         | Lastkombination 4 (Geoteknisk)       |
    |---------------------------------------|------------------------------------|--------------------------------------|
    | Permanent last, ogynnsam               | $1.10$                             | $1.10 \\times \\gamma_d$              |
    | Permanent last, gynnsam                | $0.90$                             | $1.00$                              |
    | Variabel last, ogynnsam huvudlast     | $1.50 \\times \\gamma_d$           | $1.40 \\times \\gamma_d$              |
    | Variabel last, ogynnsam övriga laster | $1.50 \\times \\gamma_d \\times \\psi_0$ | $1.40 \\times \\gamma_d \\times \\psi_0$ |
    | $V_{{Ed}}$                              | {VEd_LK3:.1f} kN                   | {VEd_LK4:.1f} kN                     |
    | $M_{{Ed}}$                              | {MEd_LK3:.1f} kNm                  | {MEd_LK4:.1f} kNm                    |
    """

    st.markdown(lastkombination_md)
