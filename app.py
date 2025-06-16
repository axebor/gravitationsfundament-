import streamlit as st

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

st.markdown("""
<style>
  table, th, td {
    border: 1px solid #ddd;
    border-collapse: collapse;
    padding: 6px 10px;
    font-family: Arial, sans-serif;
  }
  th {
    background-color: #f4f4f4;
    font-weight: bold;
  }
  input[type=number] {
    width: 100%;
    box-sizing: border-box;
    font-size: 1rem;
    padding: 4px 6px;
  }
</style>
""", unsafe_allow_html=True)

# Tabell med HTML-inputfält för varje parameter
html_table = """
<table style="width: 100%; max-width: 700px;">
  <tr>
    <th>Parameter</th>
    <th>Beteckning</th>
    <th>Värde</th>
    <th>Enhet</th>
  </tr>
  <tr>
    <td>Diameter bottenplatta</td>
    <td>D_b</td>
    <td><input id="D_b" type="number" value="5.0" step="0.1"></td>
    <td>m</td>
  </tr>
  <tr>
    <td>Höjd bottenplatta</td>
    <td>h_b</td>
    <td><input id="h_b" type="number" value="1.0" step="0.1"></td>
    <td>m</td>
  </tr>
  <tr>
    <td>Diameter skaft</td>
    <td>D_s</td>
    <td><input id="D_s" type="number" value="1.0" step="0.1"></td>
    <td>m</td>
  </tr>
  <tr>
    <td>Höjd skaft</td>
    <td>h_s</td>
    <td><input id="h_s" type="number" value="2.0" step="0.1"></td>
    <td>m</td>
  </tr>
</table>
"""

st.markdown(html_table, unsafe_allow_html=True)

# Notera: för att kunna läsa värden från dessa inputfält i Python krävs mer avancerad JS-integration
st.info("⚠️ Denna tabell visar inmatningsfält, men Streamlit kan inte direkt läsa värden från dessa utan extra JavaScript.")

