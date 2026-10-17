
import os
import shutil
import tempfile
from pathlib import Path

import streamlit as st
from gradio_client import Client

st.set_page_config(
    page_title="AI Cinematic Video Generator",
    page_icon="🎬",
    layout="centered",
)

st.title("🎬 AI Cinematic Video Generator")
st.write("Text prompt se short AI video banayein.")

SPACE_ID = "Lightricks/ltx-video-distilled"

prompt = st.text_area(
    "Video Description",
    value="A cinematic drone shot over green mountains at sunrise, realistic lighting, smooth camera movement",
    height=120,
)

negative_prompt = st.text_input(
    "Negative Prompt",
    value="blurry, distorted, low quality, jittery",
)

duration = st.slider(
    "Video Duration",
    min_value=1.0,
    max_value=4.0,
    value=2.0,
    step=1.0,
)

if st.button("Generate AI Video", type="primary"):
    if not prompt.strip():
        st.warning("Pehle prompt likhein.")
        st.stop()

    try:
        with st.spinner(
            "Video generate ho rahi hai. Thora waqt lag sakta hai..."
        ):
            client = Client(SPACE_ID)

            result = client.predict(
                prompt.strip(),       # prompt
                negative_prompt,      # negative_prompt
                None,                 # input image
                None,                 # input video
                512,                  # height
                704,                  # width
                "text-to-video",      # mode
                float(duration),      # duration
                9,                    # frames to use
                42,                   # seed
                True,                 # randomize seed
                3.0,                  # guidance scale
                False,                # improve texture
                api_name="/text_to_video",
            )

        st.write("API response type:", type(result).__name__)

        if not isinstance(result, (list, tuple)) or len(result) < 1:
            st.error("Unexpected API response.")
            st.write(result)
            st.stop()

        video = result[0]

        # Gradio output can be a filepath, URL, or file object.
        if isinstance(video, dict):
            video = video.get("path") or video.get("url")

        if not video:
            st.error("API ne video path ya URL return nahi ki.")
            st.write(result)
            st.stop()

        video_path = Path(str(video))

        if video_path.is_file():
            video_bytes = video_path.read_bytes()
        elif str(video).startswith(("http://", "https://")):
            import requests

            response = requests.get(str(video), timeout=120)
            response.raise_for_status()
            video_bytes = response.content
        else:
            st.error("Video file nahi mili. API response check karein.")
            st.write(result)
            st.stop()

        st.success("Video mil gayi!")
        st.video(video_bytes)

        st.download_button(
            "Download Video",
            data=video_bytes,
            file_name="ai_video.mp4",
            mime="video/mp4",
        )

    except Exception as e:
        st.error("Video generate nahi ho saki.")
        st.code(f"{type(e).__name__}: {e}")
        st.info(
            "Agar error API inputs, queue ya Space availability "
            "se related hai to uske mutabiq agla fix karenge."
        )
