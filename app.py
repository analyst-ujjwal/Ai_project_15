import streamlit as st
from dotenv import load_dotenv
import os
from src.pipeline import generate_music_from_prompt

load_dotenv()

st.set_page_config(page_title="Project 15 — Music Generation", layout="centered")

st.title("🎵 Project 15 — AI Music Generation (Groq Demo)")
st.markdown("Generate original AI-composed melodies using Groq inference or local synthesis.")

prompt = st.text_area("Describe your music:", "Lo-fi chill beats with warm synths", height=100)
genre = st.selectbox("Genre", ["Lo-fi", "Synthwave", "Ambient", "Jazz", "Classical", "Pop"])
tempo = st.slider("Tempo (BPM)", 60, 180, 90)
length_sec = st.slider("Length (seconds)", 5, 60, 15)
complexity = st.slider("Harmonic Complexity", 1, 10, 4)
prefer_groq = st.checkbox("Use Groq Inference (if available)", value=False)

if st.button("🎶 Generate Music"):
    with st.spinner("Synthesizing your track..."):
        output = generate_music_from_prompt(
            prompt=prompt,
            genre=genre,
            length_sec=length_sec,
            tempo=tempo,
            harmonic_complexity=complexity,
            prefer_groq=prefer_groq,
        )
    if output and os.path.exists(output):
        st.success(f"Generated: {output}")
        st.audio(output)
        st.download_button("Download WAV", open(output, "rb"), file_name=os.path.basename(output))
    else:
        st.error("Generation failed. Try adjusting parameters or disabling Groq mode.")
