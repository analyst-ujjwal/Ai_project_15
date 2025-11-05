import argparse
from src.pipeline import generate_music_from_prompt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI Music Generator")
    parser.add_argument("prompt", type=str, help="Music prompt")
    parser.add_argument("--length", type=int, default=15)
    parser.add_argument("--tempo", type=int, default=90)
    parser.add_argument("--groq", action="store_true", help="Use Groq inference")
    args = parser.parse_args()

    output = generate_music_from_prompt(
        prompt=args.prompt,
        length_sec=args.length,
        tempo=args.tempo,
        prefer_groq=args.groq,
    )
    print(f"Generated file: {output}")
