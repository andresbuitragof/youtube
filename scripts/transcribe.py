"""Transcribe audios con faster-whisper -> channels/_inbox/transcripts/<audio>.txt

Uso (en tu equipo, necesita acceso para descargar el modelo la primera vez):
  pip install faster-whisper
  python scripts/transcribe.py channels/_inbox/audio --lang es --model small
"""
import argparse
from pathlib import Path

from faster_whisper import WhisperModel


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("audio_dir")
    p.add_argument("--out", default="channels/_inbox/transcripts")
    p.add_argument("--lang", default="es")
    p.add_argument("--model", default="small")
    a = p.parse_args()

    model = WhisperModel(a.model, compute_type="int8")
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for f in sorted(Path(a.audio_dir).glob("*.m4a")):
        segs, _ = model.transcribe(str(f), language=a.lang, vad_filter=True)
        lines = [f"[{s.start:6.1f}-{s.end:6.1f}] {s.text.strip()}" for s in segs]
        (out / f"{f.stem}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"{f.name}: {len(lines)} segmentos")


if __name__ == "__main__":
    main()
