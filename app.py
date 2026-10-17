import streamlit as st
from huggingface_hub import InferenceClient

st.set_page_config(page_title="Free AI Visual Generator", layout="centered")

st.title("🎬 Free AI Cinematic Visual Generator")
st.write("Hugging Face AI models se bilkul free cinematic visuals generate karein!")

# Sidebar for Token
hf_token = st.sidebar.text_input("Enter Hugging Face Token:", type="password")

# Model Selection (Active Free Models)
model_choice = st.sidebar.selectbox(
    "Select Model:",
    [
        "stabilityai/stable-diffusion-xl-base-1.0",
        "CompVis/stable-diffusion-v1-4"
    ]
)

prompt = st.text_area("Description (Prompt):", "A cinematic slow-motion shot of a confident young man in a sharp black suit walking out of a modern glass skyscraper, luxury sports cars parked in the background, 4k, ultra-realistic")

if st.button("Generate Visual"):
    if not hf_token:
        st.error("Pehle sidebar mein apna Hugging Face Token daalein!")
    elif not prompt:
        st.warning("Koshish karein ke koi prompt zaroor daalein!")
    else:
        with st.spinner("AI visual generate ho rahi hai... (10-30 seconds lag sakte hain)"):
            try:
                # Official Inference Client
                client = InferenceClient(model=model_choice, token=hf_token)
                image = client.text_to_image(prompt)
                
                image.save("output.jpg")
                st.success("Visual successfully generate ho gayi!")
                st.image("output.jpg", caption=prompt, use_column_width=True)
            except Exception as e:
                st.error(f"Error: {e}")
