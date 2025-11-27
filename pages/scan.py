from datetime import datetime
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import cv2
import queue
import gspread

link = "https://docs.google.com/spreadsheets/d/11ambo2e9S4bbq_OL4FrGM9VUE9Rh6KS5IthFqbR0iTQ"

g = st.secrets["bot"]
creds = {
    "type": g["type"],
    "project_id": g["project_id"],
    "private_key_id": g["private_key_id"],
    "private_key": g["private_key"].replace("\\n", "\n"),  # if stored escaped
    "client_email": g["client_email"],
    "client_id": g["client_id"],
    "auth_uri": g["auth_uri"],
    "token_uri": g["token_uri"],
    "auth_provider_x509_cert_url": g["auth_provider_x509_cert_url"],
    "client_x509_cert_url": g["client_x509_cert_url"],
    "universe_domain": g["universe_domain"],
}

gc = gspread.service_account_from_dict(creds)
tabel = gc.open_by_url(link).get_worksheet(0)
qr_codes = queue.Queue()
last = None

if 'day' not in st.session_state:
    st.session_state.day = datetime.today().weekday() + 6

st.title("Scan")

@st.dialog("Scan", on_dismiss="rerun")
def show(x):
    #if masa and desert:
    #    st.write("Elevul are si masa si desert")
    #elif masa:
    #    st.write("Elevul are doar masa")
    st.write(f"Elevul e {x}")

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    info, bbox, _ = cv2.QRCodeDetector().detectAndDecode(img)

    if len(info) > 0:
        global last
        if last != info:
            qr_codes.put(info)
            last = info

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
            result = qr_codes.get()
            cell = tabel.find(result).row #dupa nume
            show(tabel.cell(cell, st.session_state.day).value)

if st.button("Back"):
    st.switch_page("main.py")

