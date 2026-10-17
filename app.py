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
    ["damo-vilab/text-to-video-ms-1.7b", "stabilityai/stable-diffusion-xl-base-1.0"]
)

prompt = st.text_area("Video Description (Prompt):", "A cinematic slow-motion shot of a confident young man in a sharp black suit walking out of a modern glass skyscraper, luxury sports cars parked in the background, 4k")

def query_huggingface(prompt, token, model_id):
    API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": prompt}
    
    try:
        # Timeout ko 120 seconds kar diya hai taake model load hone ka waqt mil jaye
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        return response
    except Exception as e:
        return str(e)

if st.button("Generate Video"):
    if not hf_token:
        st.error("Pehle sidebar mein apna Hugging Face Token daalein!")
    elif not prompt:
        st.warning("Koshish karein ke koi prompt zaroor daalein!")
    else:
        with st.spinner("AI video generate ho rahi hai... (Pehli dafa model warm-up hone mein 1-2 minute lag sakte hain, bara-e-karam intezar karein)"):
            res = query_huggingface(prompt, hf_token, model_choice)
            
            if isinstance(res, str):
                st.error(f"Connection Error: {res}")
            elif res.status_code == 200:
                with open("output.mp4", "wb") as f:
                    f.write(res.content)
                st.success("Video successfully generate ho gayi!")
                st.video("output.mp4")
            elif res.status_code == 503:
                st.info("Model warm-up ho raha hai. 30 seconds baad dobara 'Generate Video' button dabayein.")
            else:
                st.error(f"Hugging Face Error ({res.status_code}): {res.text}")
