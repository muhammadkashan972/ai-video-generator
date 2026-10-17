import streamlit as st
import requests

st.set_page_config(page_title="Free AI Video Generator", layout="centered")

st.title("🎬 Free AI Video Generator")
st.write("Hugging Face AI models se bilkul free videos generate karein!")

# Sidebar for Token
hf_token = st.sidebar.text_input("Enter Hugging Face Token:", type="password")

# Model Selection
model_choice = st.sidebar.selectbox(
    "Select Model:",
    ["damo-vilab/text-to-video-ms-1.7b", "guoyww/animatediff-motion-adapter-v1-5-2"]
)

prompt = st.text_area("Video Description (Prompt):", "A cinematic shot of a robot coding on a laptop, 4k quality")

def query_huggingface(prompt, token, model_id):
    API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": prompt}
    
    response = requests.post(API_URL, headers=headers, json=payload)
    return response

if st.button("Generate Video"):
    if not hf_token:
        st.error("Pehle sidebar mein apna Hugging Face Token daalein!")
    elif not prompt:
        st.warning("Koshish karein ke koi prompt zaroor daalein!")
    else:
        with st.spinner("AI Video bana raha hai... (Pehli baar 1-2 minute lag sakte hain)"):
            res = query_huggingface(prompt, hf_token, model_choice)
            
            if res.status_code == 200:
                with open("output.mp4", "wb") as f:
                    f.write(res.content)
                st.success("Video successfully generate ho gayi!")
                st.video("output.mp4")
            elif res.status_code == 503:
                st.info("Model load ho raha hai, bara-e-karam 30 seconds baad dobara try karein.")
            else:
                st.error(f"Error ({res.status_code}): {res.text}")
