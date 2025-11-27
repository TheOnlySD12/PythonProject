import streamlit as st

st.title("Bine ai venit 👋")

st.markdown(
    """ 
    Aici e pagina principala

    **Sara e :rainbow[asa] !**

    """
)

if st.button("Send balloons!"):
    st.balloons()

if st.button("Scan"):
    st.switch_page("pages/scan.py")

if st.button("Tabel"):
    st.switch_page("pages/tabel.py")