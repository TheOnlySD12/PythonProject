import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2

st.title("Scan")

lastElev = ""


def check(text):
    global lastElev
    if lastElev != text:
        print(text)
        st.info(text)
        lastElev = text


def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    info, bbox, _ = cv2.QRCodeDetector().detectAndDecode(img)

    if len(info) > 0:
        check(info)

    return frame


webrtc_streamer(
    key="scan",
    video_frame_callback=video_frame_callback,
    media_stream_constraints={
        "video": True,
        "audio": False
    }
)

if st.button("Back"):
    st.switch_page("main.py")
