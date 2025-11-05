import streamlit as st

st.title("Tabel")

st.table([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

if st.button("Back"):
    st.switch_page("main.py")