import streamlit as st

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# CSS för alla textinput-fält
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

col_in, col_out = st.columns([1, 3])

with col_in:
    st.header("Indata")
    st.subheader("Geometri")

    st.markdown("**Bottenplatta**")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        D_b_str = st.text_input("Diameter Dₐ (m)", value="5.0")
    with col_b2:
        h_b_str = st.text_input("Höjd hₐ (m)", value="1.0")

    st.markdown("**Skaft (centrerat ovanpå)**")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        D_s_str = st.text_input("Diameter Dₛ (m)", value="1.0")
    with col_s2:
        h_s_str = st.text_input("Höjd hₛ (m)", value="2.0")

    fundament_i_vatten = st.checkbox("Fundament delvis i vatten", value=False)

    if fundament_i_vatten:
        z_niva_str = st.text_input("Z-nivå vatten (m) från underkant fundament", value="0.0", key="z_niva")
        try:
            z_niva = float(z_niva_str)
        except ValueError:
            st.error("❌ Ange ett giltigt tal för Z-nivå.")
            st.stop()
    else:
        z_niva = None

    # Konvertera till float med avrundning till 1 decimal
    try:
        D_b = round(float(D_b_str), 1)
        h_b = round(float(h_b_str), 1)
        D_s = round(float(D_s_str), 1)
        h_s = round(float(h_s_str), 1)
    except ValueError:
        st.error("❌ Ange giltiga numeriska värden för geometri.")
        st.stop()
import matplotlib.pyplot as plt

with col_out:
    st.header("Måttkedjor")

    fig, ax = plt.subplots(figsize=(6, 6))

    # Ritning av bottenplatta och skaft som rektanglar
    ax.plot([-D_b/2, D_b/2], [0, 0], 'k-')           # Bottenplattans bottenlinje
    ax.plot([-D_b/2, -D_b/2], [0, h_b], 'k-')       # Bottenplattans vänsterkant
    ax.plot([D_b/2, D_b/2], [0, h_b], 'k-')         # Bottenplattans högerkant
    ax.plot([-D_b/2, D_b/2], [h_b, h_b], 'k-')       # Bottenplattans topp

    ax.plot([-D_s/2, D_s/2], [h_b, h_b], 'k-')       # Skaftets bottenlinje
    ax.plot([-D_s/2, -D_s/2], [h_b, h_b + h_s], 'k-') # Skaftets vänsterkant
    ax.plot([D_s/2, D_s/2], [h_b, h_b + h_s], 'k-')   # Skaftets högerkant
    ax.plot([-D_s/2, D_s/2], [h_b + h_s, h_b + h_s], 'k-') # Skaftets topp

    # Måttpilar och beteckningar (horisontella diametrar)
    ax.annotate("", xy=(D_b/2, -0.5), xytext=(-D_b/2, -0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, -0.7, r"$D_b$", ha='center', va='top', fontsize=12)

    ax.annotate("", xy=(D_s/2, h_b + h_s + 0.5), xytext=(-D_s/2, h_b + h_s + 0.5),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(0, h_b + h_s + 0.7, r"$D_s$", ha='center', va='bottom', fontsize=12)

    # Måttpilar och beteckningar (vertikala höjder)
    ax.annotate("", xy=(D_b/2 + 0.5, 0), xytext=(D_b/2 + 0.5, h_b),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_b/2 + 0.6, h_b/2, r"$h_b$", va='center', fontsize=12)

    ax.annotate("", xy=(D_s/2 + 0.5, h_b), xytext=(D_s/2 + 0.5, h_b + h_s),
                arrowprops=dict(arrowstyle="<->"))
    ax.text(D_s/2 + 0.6, h_b + h_s/2, r"$h_s$", va='center', fontsize=12)

    # Axlar och gränser
    ax.set_xlim(-max(D_b, D_s), max(D_b, D_s) + 1)
    ax.set_ylim(-1, h_b + h_s + 1)
    ax.set_aspect('equal')
    ax.axis('off')  # Dölj axlar

    st.pyplot(fig)

