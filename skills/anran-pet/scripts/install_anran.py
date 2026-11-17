#!/usr/bin/env python3
"""Stage Anran assets and optionally publish the approved custom runtime page."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
ASSETS = PLUGIN_ROOT / "assets"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stage(workspace: Path, pet_id: str) -> dict:
    workspace = workspace.resolve()
    target = (workspace / "pets" / pet_id).resolve()
    if workspace not in target.parents:
        raise ValueError("Pet id escapes the active workspace")
    if target.exists() and any(target.iterdir()):
        raise FileExistsError(f"Refusing to overwrite a non-empty staged package: {target}")
    target.mkdir(parents=True, exist_ok=True)
    for name in ("pet.json", "spritesheet.webp"):
        shutil.copy2(ASSETS / "pet" / name, target / name)
    manifest_path = target / "pet.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["id"] = pet_id
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "status": "staged",
        "packagePath": f"pets/{pet_id}",
        "package": str(target),
        "manifestSha256": digest(manifest_path),
        "atlasSha256": digest(target / "spritesheet.webp"),
        "next": "Call Widget.installPet with packagePath, then Widget.read and finalize for a new Pet."
    }


def finalize(widget_root: Path, overwrite: bool) -> dict:
    widget_root = widget_root.resolve()
    target = widget_root / "index.html"
    if target.exists() and not overwrite:
        raise FileExistsError("index.html already exists; preserve user edits or obtain confirmation before overwriting")
    widget_root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ASSETS / "index.html", target)
    return {"status": "published", "index": str(target), "indexSha256": digest(target)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    stage_parser = sub.add_parser("stage")
    stage_parser.add_argument("--workspace", type=Path, required=True)
    stage_parser.add_argument("--pet-id", default="changxu-warm")
    finalize_parser = sub.add_parser("finalize")
    finalize_parser.add_argument("--widget-root", type=Path, required=True)
    finalize_parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    result = stage(args.workspace, args.pet_id) if args.command == "stage" else finalize(args.widget_root, args.overwrite)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
