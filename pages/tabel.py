import streamlit as st
from data_loader import get_worksheet

st.title("Tabel")

@st.cache_data
def get_data():
    return get_worksheet()

tabel = get_data()

st.dataframe(tabel)

if st.button("Back"):
    st.switch_page("main.py")