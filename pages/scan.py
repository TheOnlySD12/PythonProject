from datetime import datetime
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import cv2
import queue
import gspread

link = "https://docs.google.com/spreadsheets/d/11ambo2e9S4bbq_OL4FrGM9VUE9Rh6KS5IthFqbR0iTQ"

st.title("Scan")

qr_code = queue.Queue()
#gc = gspread.api_key("aici")
#tabel = gc.open_by_url(link).get_worksheet(0)

last = None

if 'day' not in st.session_state:
    st.session_state.day = datetime.today().weekday() + 6

@st.dialog("Scan")
def show(x):
    #if masa and desert:
    #    st.write("Elevul are si masa si desert")
    #elif masa:
    #    st.write("Elevul are doar masa")
    st.write(f"Elevul e {x}")
    if st.button("Submit"):
        st.rerun()

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
        while True:
            result = qr_code.get()

            #cell = tabel.find(result).row
            #placeholder.write(tabel.cell(cell, st.session_state.day).value)
            show(result)

if st.button("Back"):
    st.switch_page("main.py")

