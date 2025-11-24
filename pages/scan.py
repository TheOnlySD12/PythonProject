from datetime import datetime
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import cv2
import queue
import gspread

link = "https://docs.google.com/spreadsheets/d/11ambo2e9S4bbq_OL4FrGM9VUE9Rh6KS5IthFqbR0iTQ"

st.title("Scan")

qr_code = queue.Queue()
gc = gspread.service_account()
tabel = gc.open_by_url(link).get_worksheet(0)

last = None

if st.session_state.day is None:
    st.session_state.day = datetime.today().weekday() + 6

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
            cell = tabel.find(result).row
            labels_placeholder.write(tabel.cell(cell, st.session_state.day).value)

if st.button("Back"):
    st.switch_page("main.py")

