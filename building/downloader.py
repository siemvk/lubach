# TODO: dit verbeteren zodat we dingen niet elke keer hoeven te downloaden. zodat buildtimes lager zijn
from pathlib import Path
from yt_dlp import YoutubeDL
from typing import Any, cast
import os
import time

# LUBACH_PLAYLIST = "https://www.youtube.com/watch?list=PLgOZoAtHo6ThWUOTVLYm0jA4PxKFE4uyP"
# LUBACH_PLAYLIST = "https://www.youtube.com/watch?list=PLgOZoAtHo6TglNt4-PTzn_Sv_iSVIRwJG"
LUBACH_PLAYLIST = "https://www.youtube.com/channel/UCn7xknPbWDjGQCzBLhtubiA"

os.system("rm -rf lubach")

def main() -> int:
    outdir = Path("lubach")
    outdir.mkdir(parents=True, exist_ok=True)

    def _sleep_after_finished(d: dict[str, Any]) -> None:
        if d.get("status") == "finished":
            time.sleep(5)

    ydl_opts = {
        "outtmpl": str(outdir / "%(id)s.%(ext)s"),
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["nl.*"],
        "subtitlesformat": "vtt/best",
        "ignoreerrors": True,
        "progress_hooks": [_sleep_after_finished],
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
