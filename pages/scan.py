import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.title("Scan")

webrtc_streamer(key="scan")

if st.button("Back"):
    st.switch_page("main.py")