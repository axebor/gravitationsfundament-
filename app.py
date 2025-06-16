import streamlit as st
# Geometri
st.subheader("Geometri")

# Bottenplatta
st.markdown("**Bottenplatta**")
D_b = st.number_input("Diameter D\u2090 (m)", min_value=0.5, value=5.0, step=0.1)
h_b = st.number_input("Höjd h\u2090 (m)", min_value=0.1, value=1.0, step=0.1)

# Skaft
st.markdown("**Skaft (centrerat ovanpå)**")
D_s = st.number_input("Diameter D\u209B (m)", min_value=0.1, max_value=D_b, value=1.0, step=0.1)
h_s = st.number_input("Höjd h\u209B (m)", min_value=0.1, value=2.0, step=0.1)
