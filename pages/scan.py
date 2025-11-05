import streamlit as st
from camera_input_live import camera_input_live

st.title("Scan")

image = camera_input_live()

if image:
  st.image(image)

if st.button("Back"):
    st.switch_page("main.py")

enable = st.checkbox("Enable camera")
picture = st.camera_input("Take a picture", disabled=not enable)

if picture:
    st.image(picture)