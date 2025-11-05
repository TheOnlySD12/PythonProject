import streamlit as st
from camera_input_live import camera_input_live

st.title("Scan")

image = camera_input_live(debounce=0, height=300, width=300, show_controls=False)

if image:
  st.image(image)

"""
enable = st.checkbox("Enable camera")
picture = st.camera_input("Take a picture", disabled=not enable)

if picture:
    st.image(picture)

"""

if st.button("Back"):
    st.switch_page("main.py")