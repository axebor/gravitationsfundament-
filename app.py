with col_in:
    st.header("Indata")
    st.subheader("Geometri")

    # Rubrikrad
    col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
    col1.markdown("**Parameter**")
    col2.markdown("**Beteckning**")
    col3.markdown("**Värde**")
    col4.markdown("**Enhet**")

    # Diameter bottenplatta
    with st.container():
        col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
        col1.write("Diameter bottenplatta")
        col2.write("D_b")
        D_b = float(col3.text_input(label="", value="5.0", key="D_b"))
        col4.write("m")

    # Höjd bottenplatta
    with st.container():
        col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
        col1.write("Höjd bottenplatta")
        col2.write("h_b")
        h_b = float(col3.text_input(label="", value="1.0", key="h_b"))
        col4.write("m")

    # Diameter skaft
    with st.container():
        col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
        col1.write("Diameter skaft")
        col2.write("D_s")
        D_s = float(col3.text_input(label="", value="1.0", key="D_s"))
        col4.write("m")

    # Höjd skaft
    with st.container():
        col1, col2, col3, col4 = st.columns([2.5, 1, 1.2, 1])
        col1.write("Höjd skaft")
        col2.write("h_s")
        h_s = float(col3.text_input(label="", value="2.0", key="h_s"))
        col4.write("m")

