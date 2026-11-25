"""Publish the competition entry image to the make.fun output location.

Copies the committed ``news.png`` (a 1024x1024 RGB PNG front page for
Wednesday 25 November 2026) byte-for-byte to ``/output/entry.png``.

Determinism
-----------
The entry is a *static file committed to this repository*. ``main.py`` performs
a plain byte-level copy and performs no network access, no randomness, no
timestamps and no image processing of its own, so running it twice always
produces ``/output/entry.png`` with identical bytes (same SHA-256) as the
committed source. The only inputs are the repository contents; nothing about
the runtime environment can change the output.
"""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SOURCE = REPO_ROOT / "news.png"
OUTPUT = Path("/output/entry.png")


def sha256(path: Path) -> str:
    """Return the SHA-256 hex digest of a file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_entry(src: Path = SOURCE, dst: Path = OUTPUT) -> Path:
    """Copy ``src`` to ``dst`` byte-for-byte, creating parent directories.

    Uses shutil.copyfile semantics: no metadata, no transformation — the
    destination bytes are identical to the source bytes.
    """
    src = Path(src)
    if not src.is_file():
        raise FileNotFoundError(f"source image missing: {src}")
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return dst


def main() -> None:
    dst = copy_entry()
    print(f"wrote {dst} ({dst.stat().st_size} bytes, sha256={sha256(dst)})")


if __name__ == "__main__":
    main()
