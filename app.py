import streamlit as st

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# Stil för tabell
st.markdown("""
<style>
table {
  border-collapse: collapse;
  width: 100%;
  max-width: 700px;
}
th, td {
  border: 1px solid #ddd;
  padding: 8px 12px;
  vertical-align: middle;
  text-align: left;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
th {
  background-color: #f2f2f2;
  font-weight: 600;
}
input[type="text"] {
  width: 100%;
  padding: 4px 8px;
  font-size: 14px;
  box-sizing: border-box;
}
</style>
""", unsafe_allow_html=True)

# Rubriker och layout
st.header("Indata")
st.subheader("Geometri")

# Vi skapar en HTML-tabell för rubrikerna
st.markdown("""
<table>
<tr>
  <th>Parameter</th>
  <th>Beteckning</th>
  <th>Värde</th>
  <th>Enhet</th>
</tr>
</table>
""", unsafe_allow_html=True)

# Funktion som skapar rad med streamlit-textinput
def tabellrad(parameter, beteckning, enhet, key, default):
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    col1.write(parameter)
    col2.write(beteckning)
    val = col3.text_input("", value=default, key=key)
    col4.write(enhet)
    return val

# Vi visar varje rad (blir snyggt rad för rad)
D_b = tabellrad("Diameter bottenplatta", "D_b", "m", "D_b", "5.0")
h_b = tabellrad("Höjd bottenplatta", "h_b", "m", "h_b", "1.0")
D_s = tabellrad("Diameter skaft", "D_s", "m", "D_s", "1.0")
h_s = tabellrad("Höjd skaft", "h_s", "m", "h_s", "2.0")

# För demonstration, visa värdena
st.write("Inmatade värden:")
st.write(f"D_b = {D_b}, h_b = {h_b}, D_s = {D_s}, h_s = {h_s}")
