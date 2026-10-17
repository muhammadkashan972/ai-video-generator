import streamlit as st
import requests

st.set_page_config(page_title="Free AI Visual Generator", layout="centered")

st.title("🎬 Free AI Cinematic Visual Generator")
st.write("Hugging Face AI models se bilkul free cinematic visuals generate karein!")

# Sidebar for Token
hf_token = st.sidebar.text_input("Enter Hugging Face Token:", type="password")

# Model Selection (Supported Serverless Models)
model_choice = st.sidebar.selectbox(
    "Select Model:",
    [
        "black-forest-labs/FLUX.1-schnell",
        "stabilityai/stable-diffusion-xl-base-1.0",
        "runwayml/stable-diffusion-v1-5"
    ]
)

prompt = st.text_area("Description (Prompt):", "A cinematic slow-motion shot of a confident young man in a sharp black suit walking out of a modern glass skyscraper, luxury sports cars parked in the background, 4k, ultra-realistic")

def query_huggingface(prompt, token, model_id):
    API_URL = f"https://router.huggingface.co/hf-inference/models/{model_id}"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": prompt}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        return response
    except Exception as e:
        return str(e)

if st.button("Generate Visual"):
    if not hf_token:
        st.error("Pehle sidebar mein apna Hugging Face Token daalein!")
    elif not prompt:
        st.warning("Koshish karein ke koi prompt zaroor daalein!")
    else:
        with st.spinner("AI visual generate ho rahi hai... (10-20 seconds lag sakte hain)"):
            res = query_hungeon = query_huggingface(prompt, hf_token, model_choice)
            
            if isinstance(res, str):
                st.error(f"Connection Error: {res}")
            elif res.status_code == 200:
                with open("output.jpg", "wb") as f:
                    f.write(res.content)
                st.success("Visual successfully generate ho gayi!")
                st.image("output.jpg", caption=prompt, use_column_width=True)
            elif res.status_code == 503:
                st.info("Model warm-up ho raha hai. 30 seconds baad dobara 'Generate Visual' button dabayein.")
            else:
                st.error(f"Hugging Face Error ({res.status_code}): {res.text}")
