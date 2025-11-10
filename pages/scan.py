import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2

st.title("Scan")

def check(text):
    st.write(text)


def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    info, bbox, _ = cv2.QRCodeDetector().detectAndDecode(img)

    if bbox is not None:
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
