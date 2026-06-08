"""
release.py — run locally to suggest the next version and trigger the GitHub Actions release.

Requirements: pip install requests
Usage: python release.py [--patch | --minor | --major]
"""

import argparse
import json
import subprocess
import sys
import urllib.request

REPO = "OWNER/REPO"  # ← replace with your GitHub repo (e.g. "Ephraem/MemeOverBotInstaller")


def get_latest_version() -> tuple[int, int, int] | None:
    url = f"https://api.github.com/repos/BlessEphraem/MemeOver-ServerCreator/releases/latest"
    try:
        req = urllib.request.Request(
            url, headers={"Accept": "application/vnd.github+json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                tag = json.loads(r.read())["tag_name"].lstrip("v")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None  # no release yet
            raise
        parts = tag.split(".")
        return int(parts[0]), int(parts[1]), int(parts[2])
    except Exception as e:
        print(f"[ERROR] Could not fetch latest release: {e}")
        sys.exit(1)


def bump(version: tuple[int, int, int], bump_type: str) -> tuple[int, int, int]:
    major, minor, patch = version
    if bump_type == "major":
        return major + 1, 0, 0
    elif bump_type == "minor":
        return major, minor + 1, 0
    else:  # patch
        return major, minor, patch + 1


def fmt(version: tuple[int, int, int]) -> str:
    return ".".join(str(v) for v in version)


def ok_print(msg):
    print(f"  [OK] {msg}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Trigger a MemeOverBotInstaller release."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--patch", action="store_true", help="Bump patch version (default)"
    )
    group.add_argument("--minor", action="store_true", help="Bump minor version")
    group.add_argument("--major", action="store_true", help="Bump major version")
    args = parser.parse_args()

    bump_type = "major" if args.major else "minor" if args.minor else "patch"

    print("\n  Fetching latest release from GitHub...")
    latest = get_latest_version()

    if latest is None:
        suggested = (0, 1, 0)
        print("  No release found. First release will be:")
    else:
        suggested = bump(latest, bump_type)
        print(f"  Latest release : v{fmt(latest)}")
        print(f"  Bump type      : {bump_type}")
        print(f"  Suggested next :")

    print(f"\n  → v{fmt(suggested)}\n")

    user_input = input(
        f"  Version to release [press ENTER for v{fmt(suggested)}]: "
    ).strip()
    version = user_input if user_input else fmt(suggested)

    confirm = (
        input(f"\n  Release v{version}? This will trigger GitHub Actions. [y/N]: ")
        .strip()
        .lower()
    )
    if confirm != "y":
        print("  Aborted.")
        sys.exit(0)

    # ── Push to GitHub first ─────────────────────────────────────────────────
    print("\n  Pushing to GitHub...")

    # Check if there's anything to commit
    status = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )
    if status.stdout.strip():
        commit_msg = input(
            f"  Commit message [press ENTER for 'Release v{version}']: "
        ).strip()
        if not commit_msg:
            commit_msg = f"Release v{version}"
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", commit_msg])

    push = subprocess.run(["git", "push"], capture_output=True, text=True)
    if push.returncode != 0:
        print(f"[ERROR] git push failed:\n{push.stderr}")
        input("\nPress ENTER to exit.")
        sys.exit(1)
    ok_print("Pushed to GitHub.")

    print(f"\n  Triggering release v{version}...")
    result = subprocess.run(
        [
            "gh",
            "workflow",
            "run",
            "release.yml",
            "--field",
            f"version={version}",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"[ERROR] gh cli failed:\n{result.stderr}")
        print("  Make sure 'gh' is installed and authenticated: https://cli.github.com")
        sys.exit(1)

    print(f"\n  [OK] Workflow triggered for v{version}.")
    print(f"  Follow progress at: https://github.com/{REPO}/actions\n")


if __name__ == "__main__":
    main()
