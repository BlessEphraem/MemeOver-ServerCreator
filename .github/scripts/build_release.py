"""
build_release.py — called by the GitHub Actions release workflow.
Usage: python .github/scripts/build_release.py <version>
"""

import os
import sys
import zipfile
from pathlib import Path


def build(version: str) -> None:
    root = Path(__file__).resolve().parents[2]  # repo root
    dist = root / "dist"
    dist.mkdir(exist_ok=True)

    archive_name = f"MemeOver-ServerCreator-v{version}.zip"
    archive_path = dist / archive_name

    files_to_include = [
        root / "MemeOver-ServerCreator.py",
        root / "README.md",
        root / "LICENSE",
    ]

    missing = [f for f in files_to_include if not f.exists()]
    if missing:
        for m in missing:
            print(f"[ERROR] Missing file: {m}")
        sys.exit(1)

    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files_to_include:
            zf.write(f, f.name)
            print(f"  + {f.name}")

    print(f"\n[OK] Archive created: dist/{archive_name}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python build_release.py <version>")
        sys.exit(1)
    build(sys.argv[1])
