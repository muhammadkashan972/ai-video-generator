
import os
import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(
    page_title="AI Video Generator",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 AI Cinematic Video Generator")
st.write("Apna prompt likhein aur AI se video generate karein.")

# Token ko environment variable ya Streamlit Secrets se read karein
saved_token = os.getenv("HF_TOKEN", "")

if not saved_token:
    try:
        saved_token = st.secrets.get("HF_TOKEN", "")
    except Exception:
        saved_token = ""

with st.sidebar:
    st.header("Settings")
    user_token = st.text_input(
        "Hugging Face Token",
        type="password",
        help="Token ko GitHub code mein kabhi save na karein."
    )

    st.caption("Supported provider aur model ki availability zaroor check karein.")

    model_id = "Wan-AI/Wan2.2-TI2V-5B"

prompt = st.text_area(
    "Video Description",
    value=(
        "A cinematic shot of a young man walking out of a "
        "modern glass skyscraper, luxury cars in the background, "
        "realistic lighting, smooth camera movement."
    ),
    height=140
)

if st.button("Generate AI Video", type="primary"):
    token = user_token.strip() or saved_token.strip()

    if not token:
        st.error("Sidebar mein Hugging Face token enter karein.")
    elif not prompt.strip():
        st.warning("Pehle video ka prompt likhein.")
    else:
        try:
            with st.spinner(
                "Video generate ho rahi hai. Is mein kuch waqt lag sakta hai..."
            ):
                client = InferenceClient(
                    provider="fal-ai",
                    api_key=token,
                    timeout=600
                )

                video_bytes = client.text_to_video(
                    prompt=prompt.strip(),
                    model=model_id
                )

            if not video_bytes:
                st.error("Provider ne empty video return ki.")
            else:
                st.success("Video generate ho gayi!")
                st.video(video_bytes)
                st.download_button(
                    label="Download MP4 Video",
                    data=video_bytes,
                    file_name="ai_generated_video.mp4",
                    mime="video/mp4"
                )

        except Exception as e:
            error_text = str(e)
            st.error("Video generate nahi ho saki.")
            st.code(error_text[:1500])

            st.info(
                "Token permission, provider/model availability aur "
                "account ki usage limits check karein."
            )
