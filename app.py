
import os
import shutil
import tempfile
from pathlib import Path

import streamlit as st
from gradio_client import Client

st.set_page_config(
    page_title="Free AI Video Generator",
    page_icon="🎬",
    layout="centered",
)

st.title("🎬 AI Cinematic Video Generator")
st.write("Text prompt se short AI video banayein.")

SPACE_ID = "Lightricks/ltx-video-distilled"

prompt = st.text_area(
    "Video Description",
    value=(
        "A cinematic shot of a confident young man walking "
        "outside a modern glass skyscraper, luxury cars in "
        "the background, realistic lighting, smooth camera movement"
    ),
    height=150,
)

negative_prompt = st.text_input(
    "Negative prompt (optional)",
    value="blurry, distorted, low quality",
)

duration = st.slider(
    "Video duration (seconds)",
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
            "AI video ban rahi hai. Queue ki wajah se waqt lag sakta hai..."
        ):
            client = Client(SPACE_ID)

            # Public Space ka text-to-video endpoint
            result = client.predict(
                prompt.strip(),
                negative_prompt.strip(),
                None,       # input image
                None,       # input video
                512,        # height
                704,        # width
                "text-to-video",
                float(duration),
                9,          # frames setting
                42,         # seed
                True,       # random seed
                3.0,        # guidance scale
                False,      # improve texture
                api_name="/text_to_video",
            )

        # Video output aam tor par result ka pehla item hota hai
        video = result[0] if isinstance(result, (tuple, list)) else result

        # Gradio Video kabhi filepath aur kabhi dictionary deta hai
        if isinstance(video, dict):
            video = video.get("path") or video.get("url")

        if not video:
            st.error("Space ne video file return nahi ki.")
            st.stop()

        video_path = Path(str(video))

        if not video_path.is_file():
            st.error(
                "Video file local path par nahi mili. "
                "Public Space ka response format change ho sakta hai."
            )
            st.stop()

        video_bytes = video_path.read_bytes()

        st.success("Video generate ho gayi!")
        st.video(video_bytes)

        st.download_button(
            "Download MP4",
            data=video_bytes,
            file_name="ai_video.mp4",
            mime="video/mp4",
        )

    except Exception as e:
        st.error("Video generate nahi ho saki.")
        st.code(str(e))
        st.info(
            "Public Space busy, unavailable ya API ke liye "
            "different inputs maang sakta hai. Error details check karein."
        )
