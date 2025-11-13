import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2

st.title("Scan")

success = False


def check(text):
    st.write(text)


def video_frame_callback(frame):
    global success
    img = frame.to_ndarray(format="bgr24")

    info, bbox, _ = cv2.QRCodeDetector().detectAndDecode(img)

    if len(info) > 0:
        print(info)
        success = True
        st.write(info)

    return frame

print(success)

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
