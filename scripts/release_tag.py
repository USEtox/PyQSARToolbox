#!/usr/bin/env python3
import argparse
import re
import subprocess
import sys
from pathlib import Path

SEMVER_RE = re.compile(r"^(?:v)?(?P<version>\d+\.\d+\.\d+)$")


def run(command: list[str], dry_run: bool = False) -> None:
    printable = " ".join(command)
    print(f"$ {printable}")
    if dry_run:
        return
    completed = subprocess.run(command, check=False, text=True)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def git_output(command: list[str]) -> str:
    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise SystemExit(completed.stderr.strip() or completed.returncode)
    return completed.stdout.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create and push an annotated Git release tag (vX.Y.Z)."
    )
    parser.add_argument(
        "version",
        help="Version in X.Y.Z or vX.Y.Z format.",
    )
    parser.add_argument(
        "--remote",
        default="origin",
        help="Git remote to push to (default: origin).",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow tagging with uncommitted changes.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without executing them.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    match = SEMVER_RE.match(args.version)
    if not match:
        raise SystemExit("Version must be X.Y.Z (or vX.Y.Z).")

    version = match.group("version")
    tag = f"v{version}"

    repo_root = git_output(["git", "rev-parse", "--show-toplevel"])
    if Path.cwd().resolve() != Path(repo_root).resolve():
        print(f"Note: running from {Path.cwd()} (repo root: {repo_root})")

    if not args.allow_dirty and not args.dry_run:
        status = git_output(["git", "status", "--porcelain"])
        if status:
            raise SystemExit(
                "Working tree is not clean. Commit/stash changes first or use --allow-dirty."
            )

    existing = subprocess.run(["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"], check=False)
    if existing.returncode == 0:
        raise SystemExit(f"Tag {tag} already exists.")

    run(["git", "tag", "-a", tag, "-m", f"Release {tag}"], dry_run=args.dry_run)
    run(["git", "push", args.remote, tag], dry_run=args.dry_run)

    if args.dry_run:
        print("Dry run complete.")
    else:
        print(f"Release tag {tag} created and pushed to {args.remote}.")


if __name__ == "__main__":
    main()
