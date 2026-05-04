from pathlib import Path
from yt_dlp import YoutubeDL
from typing import Any, cast
import os

LUBACH_PLAYLIST = "https://www.youtube.com/watch?list=PLgOZoAtHo6ThWUOTVLYm0jA4PxKFE4uyP"

os.system("rm -rf lubach")

def main() -> int:
    outdir = Path("lubach")
    outdir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "outtmpl": str(outdir / "%(id)s.%(ext)s"),
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["nl.*"],
        "subtitlesformat": "vtt/best",
        "ignoreerrors": True,
    }

    try:
        with YoutubeDL(cast(Any, ydl_opts)) as ydl:
            return_code = ydl.download([LUBACH_PLAYLIST])
            return int(return_code or 0)
    except Exception as exc:
        print(f"[!] Download failed: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
