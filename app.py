import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# CSS för etiketter och inputfält
st.markdown(
    """
    <style>
    .latex-label {
        display: inline-block;
        margin-right: 6px;
        font-size: 16px;
        vertical-align: middle;
    }
    .unit-label {
        display: inline-block;
        font-size: 14px;
        color: #555;
        vertical-align: middle;
        margin-right: 10px;
    }
    div[data-testid="stTextInput"] > div > input {
        max-width: 120px;
        width: 100%;
        box-sizing: border-box;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def labeled_input(symbol_latex, unit="m", key=None, default=""):
    st.markdown(f"""
        <span class="latex-label">$$ {symbol_latex} $$</span>
        <span class="unit-label">({unit})</span>
        """, unsafe_allow_html=True)
    return st.text_input("", value=default, key=key)

# Layout: tre lika breda kolumner
col_in, col_out, col_res = st.columns([1, 1, 1])

with col_in:
    st.header("Indata")
    st.subheader("Geometri")

    st.markdown("**Bottenplatta**")
    D_b = labeled_input(r'D_b', unit="m", key="diameter_bottenplatta", default="5.0")
    h_b = labeled_input(r'H_b', unit="m", key="hojd_bottenplatta", default="1.0")

    st.markdown("**Skaft**")
    D_s = labeled_input(r'D_s', unit="m", key="diameter_skaft", default="1.0")
    h_s = labeled_input(r'h_s', unit="m", key="hojd_skaft", default="2.0")

    fundament_i_vatten = st.checkbox("Fundament delvis i vatten", value=False)
    if fundament_i_vatten:
        z_v = labeled_input(r'z_v', unit="m", key="z_vatten", default="0.0")
    else:
        z_v = None

    st.subheader("Laster")
    F = labeled_input(r'F', unit="kN", key="last_F", default="100")
    z_F = labeled_input(r'z_F', unit="m", key="last_zF", default="2.0")

    # Konvertera till float med avrundning
    try:
        D_b = round(float(D_b), 1)
        h_b = round(float(h_b), 1)
        D_s = round(float(D_s), 1)
        h_s = round(float(h_s), 1)
        F = round(float(F), 1)
        z_F = round(float(z_F), 1)
        if fundament_i_vatten and z_v is not None:
            z_v = round(float(z_v), 1)
        else:
            z_v = 0
    except ValueError:
        st.error("❌ Ange giltiga numeriska värden.")
        st.stop()

with col_out:
    st.header("Figur")

    fig, ax = plt.subplots(figsize=(6, 6))

    max_d = max(D_b, D_s)
    ax.set_xlim(-max_d, max_d)
    ax.set_ylim(-1, h_b + h_s + 2)
    ax.set_aspect('equal')
    ax.axis('off')

    # Vattenyta
    if fundament_i_vatten and z_v > 0:
        ax.fill_between([-max_d-1, max_d+1], 0, z_v, color='lightblue', alpha=0.5)
        ax.hlines(z_v, -max_d-1, max_d+1, colors='blue', linestyles='--', linewidth=2)
        ax.text(max_d, z_v, r'$z_v$', fontsize=12, verticalalignment='bottom')

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

    # Centrumlinje
    ax.plot([0, 0], [0, h_b + h_s], color='red', linestyle=':', linewidth=1)

    # Punktlast pil
    ax.annotate("",
                xy=(D_s/2 + 0.1, z_F),
                xytext=(max_d + 0.5, z_F),
                arrowprops=dict(facecolor='red', shrink=0, width=2, headwidth=8))
    ax.text(max_d + 0.6, z_F, r"$F$", color='red', fontsize=14, verticalalignment='bottom')

    # Måttsättning z_F från underkant bottenplatta
    ax.annotate("",
                xy=(max_d + 0.2, 0),
                xytext=(max_d + 0.2, z_F),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(max_d + 0.4, z_F/2, r"$z_F$", fontsize=12, verticalalignment='center')

    # Måttpilar och etiketter - diametrar och höjder
    ax.annotate("", xy=(D_b/2, -0.5), xytext=(-D_b/2, -0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, -0.7, r"$D_b$", ha='center', va='top', fontsize=12)

    ax.annotate("", xy=(D_s/2, h_b + h_s + 0.5), xytext=(-D_s/2, h_b + h_s + 0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, h_b + h_s + 0.7, r"$D_s$", ha='center', va='bottom', fontsize=12)

    ax.annotate("", xy=(D_b/2 + 0.5, 0), xytext=(D_b/2 + 0.5, h_b),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_b/2 + 0.6, h_b/2, r"$H_b$", va='center', fontsize=12)

    ax.annotate("", xy=(D_s/2 + 0.5, h_b), xytext=(D_s/2 + 0.5, h_b + h_s),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_s/2 + 0.6, h_b + h_s/2, r"$h_s$", va='center', fontsize=12)

    # Måttsättning zv (vattendjup)
    if fundament_i_vatten and z_v > 0:
        ax.annotate("", xy=(-max_d-1, 0), xytext=(-max_d-1, z_v),
                    arrowprops=dict(arrowstyle="<->"))
        ax.text(-max_d-1.2, z_v/2, r"$z_v$", fontsize=12, va='center')

    st.pyplot(fig)

with col_res:
    st.header("Resultat")

    pi = np.pi

    # Volymer
    vol_bottenplatta = pi * (D_b / 2) ** 2 * h_b
    vol_skaft = pi * (D_s / 2) ** 2 * h_s

    # Volymer under vatten och ovan vatten
    if fundament_i_vatten and z_v is not None and z_v > 0:
        under_vatten_botten = max(0, min(z_v, h_b)) * pi * (D_b / 2) ** 2
        ovan_vatten_botten = vol_bottenplatta - under_vatten_botten

        under_vatten_skaft = max(0, min(z_v - h_b, h_s)) * pi * (D_s / 2) ** 2
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
    df_volymer = pd.DataFrame({
        "Över vatten (m³)": [round(ovan_vatten_botten, 1), round(ovan_vatten_skaft, 1)],
        "Under vatten (m³)": [round(under_vatten_botten, 1), round(under_vatten_skaft, 1)]
    }, index=["Bottenplatta", "Skaft"])
    st.table(df_volymer)

    # Tabell med vikter
    df_vikter = pd.DataFrame({
        "Vikt (kN)": [round(vikt_ovan, 1), round(vikt_under, 1), round(vikt_tot, 1)]
    }, index=["Över vatten", "Under vatten", "Total egenvikt (Gk, fund)"])
    st.table(df_vikter)
