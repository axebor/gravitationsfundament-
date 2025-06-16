import streamlit as st

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

st.header("Indata")
st.subheader("Geometri")

# Diameter bottenplatta
D_b = st.text_input(" ", value="5.0", key="D_b")
st.latex(r"D_b = \text{" + D_b + r"\text{ m}}")

# Höjd bottenplatta
h_b = st.text_input(" ", value="1.0", key="h_b")
st.latex(r"h_b = \text{" + h_b + r"\text{ m}}")

# Diameter skaft
D_s = st.text_input(" ", value="1.0", key="D_s")
st.latex(r"D_s = \text{" + D_s + r"\text{ m}}")

# Höjd skaft
h_s = st.text_input(" ", value="2.0", key="h_s")
st.latex(r"h_s = \text{" + h_s + r"\text{ m}}")
