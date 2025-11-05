import os, time, logging
import numpy as np
from scipy.io import wavfile
from datetime import datetime
from .groq_client import infer as groq_infer
from .utils import ensure_output_dir, mix_percussion

logger = logging.getLogger(__name__)
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "outputs")

def local_music_generator(prompt, length_sec=15, tempo=90, complexity=4):
    """Generates procedural sine-wave melody."""
    sr = 22050
    t = np.linspace(0, length_sec, int(sr * length_sec), endpoint=False)
    rng = np.random.default_rng(int(time.time()))
    freqs = [220, 330, 440, 550]
    idxs = [sum(map(ord, w)) % len(freqs) for w in prompt.split()[:5]]
    melody = np.zeros_like(t)
    for i, idx in enumerate(idxs):
        f = freqs[idx]
        segment = np.sin(2 * np.pi * f * t) * np.exp(-t * (i + 1) / (10 * complexity))
        melody += segment
    melody = mix_percussion(melody, sr)
    melody /= np.max(np.abs(melody))
    ensure_output_dir(OUTPUT_DIR)
    filename = f"{OUTPUT_DIR}/track_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    wavfile.write(filename, sr, (melody * 32767).astype(np.int16))
    return filename

def generate_music_from_prompt(prompt, genre="Lo-fi", length_sec=15, tempo=90, harmonic_complexity=4, prefer_groq=False):
    if prefer_groq:
        res = groq_infer(prompt, {"genre": genre, "length_sec": length_sec})
        if res.get("success") and res.get("audio_path"):
            return res["audio_path"]
    return local_music_generator(prompt, length_sec, tempo, harmonic_complexity)
