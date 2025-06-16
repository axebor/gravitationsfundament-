import streamlit as st

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

st.markdown("""
<style>
.table-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.5rem;
}
.label {
    width: 220px;
}
.symbol {
    width: 80px;
    font-family: 'Computer Modern', serif;
}
.input {
    width: 100px;
}
.unit {
    width: 40px;
}
input[type="number"] {
    padding: 4px;
    font-size: 15px;
    width: 80px;
}
</style>
""", unsafe_allow_html=True)

# En rad (hårdkodad) – justera/förläng för fler
st.markdown("""
<div class="table-row">
    <div class="label">Diameter bottenplatta</div>
    <div class="symbol">\( D_b \)</div>
    <div class="input">
        <input type="number" name="D_b" value="5.0" step="0.1">
    </div>
    <div class="unit">m</div>
</div>
""", unsafe_allow_html=True)

st.info("⚠️ Värdet ovan kan inte direkt användas i Python – endast visning.")
