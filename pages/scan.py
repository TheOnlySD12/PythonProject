import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import cv2
import queue

st.title("Scan")

qr_code = queue.Queue()

last = None

def check(text):
    global last
    if last != text:
        qr_code.put(text)
        last = text

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    info, bbox, _ = cv2.QRCodeDetector().detectAndDecode(img)

    if len(info) > 0:
       check(info)

    return frame


webrtc_ctx = webrtc_streamer(
    key="scan",
    mode=WebRtcMode.SENDRECV,
    video_frame_callback=video_frame_callback,
    media_stream_constraints={
        "video": True,
        "audio": False
    },
    async_processing=True
)

if st.checkbox("Scaneaza", value=True):
    if webrtc_ctx.state.playing:
        labels_placeholder = st.empty()
        while True:
            result = qr_code.get()
            labels_placeholder.write(result)

if st.button("Back"):
    st.switch_page("main.py")

