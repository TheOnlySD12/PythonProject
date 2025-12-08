from datetime import datetime
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import cv2
import queue
from data_loader import get_worksheet

@st.cache_data
def get_data():
    return get_worksheet()

tabel = get_data()
qr_codes = queue.Queue()
last = None

if 'day' not in st.session_state:
    st.session_state.day = datetime.today().weekday()

st.title("Scan")


@st.dialog("Scan", on_dismiss="rerun")
def show(m, d):
    st.write(f"Masa: {m}")
    st.write(f"Desert: {d}")

def check(text):
    global last
    if last != text:
        qr_codes.put(text)
        last = text

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    info, _, _ = cv2.QRCodeDetector().detectAndDecode(img)

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
    rtc_configuration={
        'iceServers': [{'urls': ['stun:stun.l.google.com:19302']}]
    },
    async_processing=False,
)

if st.checkbox("Scaneaza", value=True):
    if webrtc_ctx.state.playing:
        while True:
            result = qr_codes.get()
            row = tabel[tabel["nume"] == result]
            if not row.empty:
                masa = row[tabel.columns[st.session_state.day + 5]].values[0]
                desert = row[tabel.columns[4]].values[0]
                show(masa, desert)

if st.button("Back"):
    st.switch_page("main.py")