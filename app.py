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

# Alla kolumner lika breda
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
        F_H_str = st.text_input(r"Horisontell last $Q_{k,H1}$ (kN)", value="0.0")
    with col_zf:
        z_F_str = st.text_input(r"Angreppsplan $z_{Q1}$ (m)", value="0.0")

    F_H2_str = st.text_input(r"Horisontell last $Q_{k,H2}$ (kN)", value="0.0")
    z_F2_str = st.text_input(r"Angreppsplan $z_{Q2}$ (m)", value="0.0")

    F_V_str = st.text_input(r"Vertikal last $G_{k,övrigt}$ (kN)", value="0.0")

    # Konvertera till float med avrundning till 1 decimal
    try:
        D_b = round(float(D_b_str), 1)
        H_b = round(float(H_b_str), 1)
        D_s = round(float(D_s_str), 1)
        H_s = round(float(H_s_str), 1)
        if fundament_i_vatten:
            z_v = float(z_niva_str)
        else:
            z_v = None
        Q_k_H1 = float(F_H_str)
        z_Q1 = float(z_F_str)
        Q_k_H2 = float(F_H2_str)
        z_Q2 = float(z_F2_str)
        G_k_ovr = float(F_V_str)
    except ValueError:
        st.error("❌ Ange giltiga numeriska värden för geometri, vattennivå och laster.")
        st.stop()

with col_out:
    st.header("Figur")

    fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)

    max_diameter = max(D_b, D_s)

    if fundament_i_vatten and z_v is not None and z_v > 0:
        ax.fill_between(
            x=[-max_diameter - 1, max_diameter + 1],
            y1=0, y2=z_v, color='lightblue', alpha=0.5)
        ax.hlines(y=z_v, xmin=-max_diameter - 1, xmax=max_diameter + 1,
                  colors='blue', linestyles='--', linewidth=2, label='Vattenlinje')

        # Måttpil och etikett för z_v
        ax.annotate("", xy=(max_diameter + 0.5, 0), xytext=(max_diameter + 0.5, z_v),
                    arrowprops=dict(arrowstyle="<->", color='blue'))
        ax.text(max_diameter + 0.7, z_v / 2, r"$z_{v}$", va='center', fontsize=12, color='blue')

    # Bottenplatta
    ax.plot([-D_b/2, D_b/2], [0, 0], 'k-')
    ax.plot([-D_b/2, -D_b/2], [0, H_b], 'k-')
    ax.plot([D_b/2, D_b/2], [0, H_b], 'k-')
    ax.plot([-D_b/2, D_b/2], [H_b, H_b], 'k-')

    # Skaft
    ax.plot([-D_s/2, D_s/2], [H_b, H_b], 'k-')
    ax.plot([-D_s/2, -D_s/2], [H_b, H_b + H_s], 'k-')
    ax.plot([D_s/2, D_s/2], [H_b, H_b + H_s], 'k-')
    ax.plot([-D_s/2, D_s/2], [H_b + H_s, H_b + H_s], 'k-')

    # Måttpilar och etiketter - diametrar
    ax.annotate("", xy=(D_b/2, -0.5), xytext=(-D_b/2, -0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, -0.7, r"$D_b$", ha='center', va='top', fontsize=12)

    ax.annotate("", xy=(D_s/2, H_b + H_s + 0.5), xytext=(-D_s/2, H_b + H_s + 0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, H_b + H_s + 0.7, r"$D_s$", ha='center', va='bottom', fontsize=12)

    # Måttpilar och etiketter - höjder
    ax.annotate("", xy=(D_b/2 + 0.5, 0), xytext=(D_b/2 + 0.5, H_b),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_b/2 + 0.6, H_b/2, r"$H_b$", va='center', fontsize=12)

    ax.annotate("", xy=(D_s/2 + 0.5, H_b), xytext=(D_s/2 + 0.5, H_b + H_s),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_s/2 + 0.6, H_b + H_s/2, r"$H_s$", va='center', fontsize=12)

    # Last Qk,H1
    if Q_k_H1 > 0:
        ax.annotate(
            r"$Q_{k,H1}$", 
            xy=(D_s/2, z_Q1), 
            xytext=(-max_diameter - 1, z_Q1),
            ha='center', va='bottom', fontsize=12, color='red',
            arrowprops=dict(arrowstyle="->", color='red', linewidth=2)
        )

    # Last Qk,H2
    if Q_k_H2 > 0:
        ax.annotate(
            r"$Q_{k,H2}$", 
            xy=(D_s/2, z_Q2), 
            xytext=(-max_diameter - 1.5, z_Q2),
            ha='center', va='bottom', fontsize=12, color='red',
            arrowprops=dict(arrowstyle="->", color='red', linewidth=2)
        )
        
    # Last Gk,övrigt (vertikal, nedåt)
    if G_k_ovr > 0:
        ax.annotate(
            r"$G_{k,övrigt}$", 
            xy=(0, 0), 
            xytext=(0, 2),
            ha='center', va='bottom', fontsize=12, color='red',
            arrowprops=dict(arrowstyle="|-|>", color='red', linewidth=2)
        )

    ax.set_xlim(-max_diameter - 2, max_diameter + 1.5)
    ax.set_ylim(-1, max(H_b + H_s, z_v if z_v else 0) + 2)
    ax.set_aspect('equal')
    ax.axis('off')

    st.pyplot(fig, use_container_width=True)

with col_res:
    st.header("Resultat")

    # Konstanter
    pi = np.pi
    vikt_betong_ovan = 25
    vikt_betong_under = 15

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
    G_k_b = (ovan_vatten_botten) * vikt_betong_ovan
    G_k_s = (ovan_vatten_skaft) * vikt_betong_ovan
    G_k_b_u = (under_vatten_botten) * vikt_betong_under
    G_k_s_u = (under_vatten_skaft) * vikt_betong_under

    # Total egenvikt (Gk,fund)
    G_k_tot = G_k_b + G_k_s + G_k_b_u + G_k_s_u

    # Horisontella moment (Qk,H1 och Qk,H2) i bottenplattan
    M_k_H1 = Q_k_H1 * (z_Q1)
    M_k_H2 = Q_k_H2 * (z_Q2)

    # Underrubrik Egenvikt
    st.markdown("### Egenvikt")

    # Tabell med vikter (avrundat till 1 decimal och formaterat)
    df_vikter = pd.DataFrame({
        "Vikt (kN)": [G_k_b + G_k_b_u, G_k_s + G_k_s_u, G_k_tot]
    }, index=["Bottenplatta (Gk,b)", "Skaft (Gk,s)", "Total egenvikt (Gk,fund)"])
    st.table(df_vikter.style.format("{:.1f}"))

    # Underrubrik Horisontella moment
    st.markdown("### Horisontella moment i bottenplattan")

    # Tabell med moment (avrundat till 1 decimal och formaterat)
    df_moment = pd.DataFrame({
        "Moment (kNm)": [M_k_H1, M_k_H2]
    }, index=[r"$M_{k,H1}$", r"$M_{k,H2}$"])
    st.table(df_moment.style.format("{:.1f}"))

    # Vertikala laster (Gk,övrigt)
    st.markdown("### Vertikala laster")
    st.write(f"$G_{{k,övrigt}}$ = {G_k_ovr:.1f} kN")
