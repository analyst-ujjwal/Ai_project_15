import os
import numpy as np

def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)
    return path

def mix_percussion(signal, sr, density=0.5):
    rng = np.random.default_rng()
    for _ in range(int(density * sr)):
        pos = rng.integers(0, len(signal))
        if pos + 200 < len(signal):
            click = np.exp(-np.linspace(0, 1, 200))
            signal[pos:pos + 200] += click * 0.2
    return signal
