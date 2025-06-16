with col_res:
    st.header("Resultat")

    pi = np.pi

    # Volymer
    vol_bottenplatta = pi * (D_b / 2) ** 2 * h_b
    vol_skaft = pi * (D_s / 2) ** 2 * h_s

    # Volymer under vatten och ovan vatten
    if fundament_i_vatten and z_niva is not None and z_niva > 0:
        under_vatten_botten = max(0, min(z_niva, h_b)) * pi * (D_b / 2) ** 2
        ovan_vatten_botten = vol_bottenplatta - under_vatten_botten

        under_vatten_skaft = max(0, min(z_niva - h_b, h_s)) * pi * (D_s / 2) ** 2
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
    st.subheader("Volym")
    df_volymer = pd.DataFrame({
        "Över vatten (m³)": [round(ovan_vatten_botten, 1), round(ovan_vatten_skaft, 1)],
        "Under vatten (m³)": [round(under_vatten_botten, 1), round(under_vatten_skaft, 1)]
    }, index=["Bottenplatta", "Skaft"])
    st.table(df_volymer)

    # Tabell med vikter
    st.subheader("Egenvikt fundament")
    df_vikter = pd.DataFrame({
        "Vikt (kN)": [round(vikt_ovan, 1), round(vikt_under, 1), round(vikt_tot, 1)]
    }, index=["Över vatten", "Under vatten", "Total egenvikt (Gk)"])
    st.table(df_vikter)


