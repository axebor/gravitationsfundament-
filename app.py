import streamlit as st
import math

st.set_page_config(page_title="Fundamentsberäkning", layout="centered")
st.title("Stabilitetsberäkning – Cirkulärt gravitationsfundament")

st.header("1. Indata")

D = st.number_input("Diameter D (meter)", value=5.0, min_value=0.1)
H = st.number_input("Höjd H (meter)", value=1.5, min_value=0.1)
rho_betong = st.number_input("Densitet betong (kg/m³)", value=2400)
rho_vatten = st.number_input("Densitet vatten (kg/m³)", value=1000)
g = 9.81  # tyngdacceleration

# Val av friktion och lyft
friktion = st.number_input("Friktionskoefficient (jord-fundament)", value=0.5)
lyftkraft = st.checkbox("Räkna med uppåtriktad lyftkraft (ex. flytkraft)?", value=True)

st.header("2. Beräkningar")

A = math.pi * (D/2)**2
V = A * H
vikt = V * rho_betong * g
lyft = V * rho_vatten * g if lyftkraft else 0

