
import streamlit as st
from gradio_client import Client
from pathlib import Path
import requests

st.set_page_config(
    page_title="Free AI Cinematic Video Generator",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 AI Cinematic Video Generator")
st.write("Text prompt likhein aur AI se video generate karein.")

SPACE_ID = "Lightricks/ltx-video-distilled"

with st.sidebar:
    st.header("Video Settings")
    st.caption("Public AI Space use ho raha hai. Availability aur queue depend karte hain.")

prompt = st.text_area(
    "Video Description",
    value=(
        "A cinematic shot of a confident young man walking "
        "outside a modern glass skyscraper, luxury sports cars "
        "in the background, realistic lighting, smooth camera movement"
    ),
    height=150
)

negative_prompt = st.text_input(
    "Negative Prompt",
    value="blurry, distorted, low quality, flickering"
)

duration = st.slider(
    "Video Duration (seconds)",
    min_value=1.0,
    max_value=4.0,
    value=2.0,
    step=1.0
)

if st.button("Generate AI Video", type="primary"):

    if not prompt.strip():
        st.warning("Pehle video ka prompt likhein.")
        st.stop()

    try:
        with st.spinner(
            "AI video generate kar rahi hai. Please wait..."
        ):
            client = Client(SPACE_ID)

            result = client.predict(
                prompt.strip(),
                negative_prompt.strip(),
                None,
                None,
                512,
                704,
                "text-to-video",
                float(duration),
                9,
                42,
                True,
                3.0,
                False,
                api_name="/text_to_video"
            )

        # API response: ({'video': '/tmp/...mp4',
        #                 'subtitles': None}, seed)
        video_result = result[0] if isinstance(
            result, (list, tuple)
        ) else result

        if isinstance(video_result, dict):
            video_source = (
                video_result.get("video")
                or video_result.get("path")
                or video_result.get("url")
            )
        else:
            video_source = video_result

        if not video_source:
            st.error("API ne video file return nahi ki.")
            st.write("API response:", result)

        else:
            video_bytes = None

            # Local video file returned by Gradio
            video_path = Path(str(video_source))

            if video_path.is_file():
                video_bytes = video_path.read_bytes()

            # If API returns a URL instead
            elif str(video_source).startswith(
                ("http://", "https://")
            ):
                response = requests.get(
                    str(video_source),
                    timeout=180
                )
                response.raise_for_status()
                video_bytes = response.content

            if not video_bytes:
                st.error("Video file access nahi ho saki.")
                st.write("Returned video source:", video_source)
                st.stop()

            st.success("AI video successfully generate ho gayi!")

            st.video(video_bytes)

            st.download_button(
                label="⬇️ Download AI Video (MP4)",
                data=video_bytes,
                file_name="ai_cinematic_video.mp4",
                mime="video/mp4",
                type="primary"
            )

            st.caption(
                "Video generated using the public Hugging Face Space."
            )

    except Exception as e:
        st.error("Video generate nahi ho saki.")
        st.code(f"{type(e).__name__}: {e}")

        st.info(
            "Agar error queue, API inputs, ya Space availability "
            "se related hai, to public service busy ya unavailable "
            "ho sakti hai."
        )
