import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Gravitationsfundament", layout="wide")

# --- Ditt befintliga CSS och input-kod etc här ---
# (Kopiera in din existerande kod för col_in, col_out, col_res rakt av här)

# --- Exempel: Inmatning (col_in) ---
col_in, col_out, col_res = st.columns([1,1,1])

with col_in:
    st.header("Indata")
    st.subheader("Geometri")
    # Din indata enligt tidigare...

    # (Sätt in all input som i din existerande kod här)

# --- Exempel: Figur (col_out) ---
with col_out:
    st.header("Figur")
    # Din figurkod som du hade, t.ex. skapa fig med matplotlib...

    fig, ax = plt.subplots(figsize=(8,8))
    # Rita din figur enligt existerande logik
    # ...
    st.pyplot(fig, use_container_width=True)

# --- Exempel: Resultat (col_res) ---
with col_res:
    st.header("Resultat")
    # Din resultatberäkning och visning av tabeller
    # ...

# --- Spara figuren till en bytes-buffer för PDF ---
buf = io.BytesIO()
fig.savefig(buf, format="png")
buf.seek(0)

# --- PDF-generator ---

class PDFBerakning(FPDF):
    def header(self):
        pass
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial','I',8)
        self.cell(0,10,f'Sida {self.page_no()}',0,0,'C')

def skapa_pdf_rapport(projekt, beskrivning, datum,
                      D_b, H_b, D_s, H_s,
                      fundament_i_vatten, z_v,
                      Qk_H1, z_Q1, Qk_H2, z_Q2,
                      Gk_ovr, figur_bytes):
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
    M_Q1 = Qk_H1 * z_Q1
    M_Q2 = Qk_H2 * z_Q2
    M_tot = M_Q1 + M_Q2

    pdf = PDFBerakning()
    pdf.add_page()

    # Projektinfo ruta
    pdf.set_fill_color(230,230,230)
    pdf.rect(10,10,190,40,'F')
    pdf.set_xy(15,15)
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,f"Projekt: {projekt}",ln=True)
    pdf.set_font("Arial","",12)
    pdf.cell(0,8,f"Beskrivning: {beskrivning}",ln=True)
    pdf.cell(0,8,f"Datum: {datum}",ln=True)
    pdf.ln(12)

    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,"Beräkningar Gravitationsfundament",ln=True,align="C")
    pdf.ln(6)

    pdf.set_font("Arial","B",12)
    pdf.cell(0,8,"Geometri:",ln=True)
    pdf.set_font("Arial","",12)
    pdf.cell(0,8,f"Bottenplatta: Diameter = {D_b:.2f} m, Höjd = {H_b:.2f} m",ln=True)
    pdf.cell(0,8,f"Skaft: Diameter = {D_s:.2f} m, Höjd = {H_s:.2f} m",ln=True)
    pdf.ln(4)

    if fundament_i_vatten:
        pdf.cell(0,8,f"Fundament delvis i vatten, vattennivå z_v = {z_v:.2f} m från underkant",ln=True)
    else:
        pdf.cell(0,8,"Fundament ej i vatten",ln=True)
    pdf.ln(6)

    pdf.set_font("Arial","B",12)
    pdf.cell(0,8,"Laster:",ln=True)
    pdf.set_font("Arial","",12)
    pdf.cell(0,8,f"Huvudlast horisontell Q_k,H1 = {Qk_H1:.2f} kN vid z_Q1 = {z_Q1:.2f} m",ln=True)
    pdf.cell(0,8,f"Övrig last horisontell Q_k,H2 = {Qk_H2:.2f} kN vid z_Q2 = {z_Q2:.2f} m",ln=True)
    pdf.cell(0,8,f"Vertikal last G_k,övrigt = {Gk_ovr:.2f} kN",ln=True)
    pdf.ln(6)

    pdf.cell(0,8,"Figur av fundament och laster:",ln=True)
    # Spara figur temporärt och lägg in i PDF
    with open("fig_temp.png","wb") as f:
        f.write(figur_bytes.getbuffer())
    pdf.image("fig_temp.png", x=pdf.get_x(), y=pdf.get_y(), w=150)
    pdf.ln(85)

    pdf.set_font("Arial","B",12)
    pdf.cell(0,8,"Volym och vikt:",ln=True)
    pdf.set_font("Arial","",12)
    pdf.cell(0,8,f"Volym bottenplatta = {vol_bottenplatta:.2f} m³",ln=True)
    pdf.cell(0,8,f"Volym skaft = {vol_skaft:.2f} m³",ln=True)
    pdf.cell(0,8,f"Vikt ovan vatten = {vikt_ovan:.2f} kN",ln=True)
    pdf.cell(0,8,f"Vikt under vatten = {vikt_under:.2f} kN",ln=True)
    pdf.cell(0,8,f"Total vikt = {vikt_tot:.2f} kN",ln=True)
    pdf.ln(6)

    pdf.set_font("Arial","B",12)
    pdf.cell(0,8,"Moment:",ln=True)
    pdf.set_font("Arial","",12)
    pdf.cell(0,8,f"M_Q1 = {M_Q1:.2f} kNm (Huvudlast)",ln=True)
    pdf.cell(0,8,f"M_Q2 = {M_Q2:.2f} kNm (Övrig last)",ln=True)
    pdf.cell(0,8,f"Totalt moment M_tot = {M_tot:.2f} kNm",ln=True)

    pdf_output = pdf.output(dest='S').encode('latin1')
    return pdf_output

# --- Projektinfo och PDF-knapp längst ner ---

st.markdown("---")
st.header("Projektinformation för PDF-rapport")

projekt = st.text_input("Projektnamn", value="Projekt X")
beskrivning = st.text_area("Beskrivning av projektet", value="Beskrivning av beräkningar för fundament.")
datum = st.date_input("Datum", value=datetime.date.today())

if st.button("Generera och ladda ner PDF-rapport"):
    pdf_bytes = skapa_pdf_rapport(
        projekt, beskrivning, datum.strftime("%Y-%m-%d"),
        D_b, H_b, D_s, H_s,
        fundament_i_vatten, z_v,
        Qk_H1, z_Q1, Qk_H2, z_Q2,
        Gk_ovr, buf
    )
    st.download_button(
        label="Ladda ner PDF",
        data=pdf_bytes,
        file_name="berakningsrapport.pdf",
        mime="application/pdf"
    )
