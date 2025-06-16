import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stabilitets­kontroll – cirkulärt gravitations­fundament",
                   layout="wide")

# ───────────────────────────────
# 1. Skapa två kolumner
# ───────────────────────────────
col_in, col_out = st.columns(2)

# ───────────────────────────────
# 2. Vänstra kolumnen – indata
# ───────────────────────────────
with col_in:
    st.header("Indata")

    # Geometri
    st.subheader("Geometri")
    D = st.number_input("Diameter D (m)", min_value=0.5, value=5.0)
    H = st.number_input("Höjd H (m)", min_value=0.5, value=3.0)

    # Material
    st.subheader("Material")
    gamma_c = st.number_input("Betongens torrvolymvikt γc (kN/m³)", value=24.0)
    # Om du i stället vill mata in densitet (kg/m³):
    # rho_c = st.number_input("Densitet (kg/m³)", value=2400.0)

    # Last & miljö
    st.subheader("Laster & Miljö")
    water_depth = st.number_input("Vattendjup (m)", value=0.0)
    uplift = st.number_input("Extern lyftkraft (kN)", value=0.0)
    phi = st.number_input("Friktionskoefficient φ", value=0.6)

    st.write("---")
    st.caption("Lägg till fler fält allt eftersom du behöver dem.")

# ───────────────────────────────
# 3. Högra kolumnen – resultat & figur
# ───────────────────────────────
with col_out:
    st.header("Resultat")

    # --- Här kommer beräkningar senare ---
    st.info("Resultaten visas här när vi har lagt in beräknings­kod.")

    # Rita en enkel skalenlig planfigur
    st.subheader("Figur (planvy)")

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.add_patch(plt.Circle((0, 0), radius=D/2, fill=False, lw=2))
    ax.set_aspect("equal")
    ax.set_xlim(-(D/2)*1.2, (D/2)*1.2)
    ax.set_ylim(-(D/2)*1.2, (D/2)*1.2)
    ax.axis("off")
    ax.set_title(f"D = {D:.2f} m")
    st.pyplot(fig)
