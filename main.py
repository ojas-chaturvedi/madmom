import os
import argparse
import subprocess
import sys

def convert_mp3_to_wav(input_path):
    wav_path = os.path.splitext(input_path)[0] + ".wav"
    print(f"Converting {input_path} to {wav_path}...")
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path, "-ac", "1", "-ar", "44100", wav_path
    ], check=True)
    return wav_path

def run_transcription(input_path, output_path, output_format="midi"):
    script_path = os.path.join(os.path.dirname(__file__), "bin", "PianoTranscriptor")
    if not os.path.exists(script_path):
        print(f"Error: {script_path} not found.")
        sys.exit(1)

    cmd = [
        script_path,
        "--" + output_format,
        "single", input_path,
        "-o", output_path
    ]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wrapper for Madmom's PianoTranscriptor")
    parser.add_argument('-i', '--input', required=True, help='Input WAV or MP3 file')
    parser.add_argument('-o', '--output', required=True, help='Output MIDI file path')
    parser.add_argument('--format', choices=['midi', 'mirex'], default='midi', help='Output format')
    args = parser.parse_args()

    input_path = args.input
    if input_path.lower().endswith(".mp3"):
        input_path = convert_mp3_to_wav(input_path)

    run_transcription(input_path, args.output, args.format)