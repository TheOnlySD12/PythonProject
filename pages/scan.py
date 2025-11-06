import streamlit as st
from streamlit_webrtc import webrtc_streamer
from pyzbar.pyzbar import decode

st.title("Scan")

def check(text):
    return text


def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    decoded_objects = decode(img)

    if decoded_objects:
        try:
            text = decoded_objects[0].data.decode('utf-8')
            st.write(text)


        except Exception as e:
            st.error(f"Error decoding QR code: {e}")

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
