from datetime import datetime
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer, VideoProcessorBase
import cv2
import queue
import gspread

link_test = "https://docs.google.com/spreadsheets/d/11_EX0jPsefpTAZnAzZtMq4dHjeg8qpZoN--wuQd8Fhg"


@st.cache_resource
def get_worksheet():
    g = st.secrets["bot"]
    creds = {
        "type": g["type"],
        "project_id": g["project_id"],
        "private_key_id": g["private_key_id"],
        "private_key": g["private_key"].replace("\\n", "\n"),
        "client_email": g["client_email"],
        "client_id": g["client_id"],
        "auth_uri": g["auth_uri"],
        "token_uri": g["token_uri"],
        "auth_provider_x509_cert_url": g["auth_provider_x509_cert_url"],
        "client_x509_cert_url": g["client_x509_cert_url"],
        "universe_domain": g["universe_domain"],
    }
    gc = gspread.service_account_from_dict(creds)
    return gc.open_by_url(link_test).get_worksheet(0)


tabel = get_worksheet()


class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.result_queue = queue.Queue()
        self.last_qr_code = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        info, _, _ = cv2.QRCodeDetector().detectAndDecode(img)

        if info and info != self.last_qr_code:
            self.last_qr_code = info
            self.result_queue.put(info)

        return frame


@st.cache_resource
def video_processor_factory():
    return VideoProcessor()


if 'day' not in st.session_state:
    st.session_state.day = datetime.today().weekday()

st.title("Scan")


@st.dialog("Scan", on_dismiss="rerun")
def show(m, d):
    st.write(f"Masa: {m}")
    st.write(f"Desert: {d}")


webrtc_ctx = webrtc_streamer(
    key="scan",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=video_processor_factory,
    media_stream_constraints={
        "video": True,
        "audio": False
    },
    rtc_configuration={
        'iceServers': [{'urls': ['stun:stun.l.google.com:19302']}]
    },
    async_processing=True,
)

if st.checkbox("Scaneaza", value=True):
    if webrtc_ctx.video_processor:
        while not webrtc_ctx.video_processor.result_queue.empty():
            result = webrtc_ctx.video_processor.result_queue.get()
            try:
                cell = tabel.find(result).row
                masa = tabel.cell(cell, st.session_state.day + 6).value
                desert = tabel.cell(cell, 5).value
                show(masa, desert)
            except gspread.exceptions.Any:
                st.error(f"Cod QR invalid: {result}")

if st.button("Back"):
    st.switch_page("main.py")
