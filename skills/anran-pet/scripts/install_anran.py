#!/usr/bin/env python3
"""Stage Anran safely: reuse production by default; track every preview until removal."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
ASSETS = PLUGIN_ROOT / "assets"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def production_id() -> str:
    return json.loads((ASSETS / "pet" / "pet.json").read_text(encoding="utf-8"))["id"]


def state_path(workspace: Path, pet_id: str) -> Path:
    return workspace.resolve() / "pets" / ".anran-previews" / f"{pet_id}.json"


def write_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    state["updatedAt"] = datetime.now(timezone.utc).isoformat()
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def inspect_existing(widget_root: Path) -> dict:
    root = widget_root.resolve()
    manifest_path = root / "pet.json"
    if not manifest_path.is_file():
        raise ValueError(f"Existing Pet has no readable pet.json: {root}")
    actual = json.loads(manifest_path.read_text(encoding="utf-8")).get("id")
    expected = production_id()
    if actual != expected:
        raise ValueError(f"Existing Pet identity mismatch: expected {expected!r}, got {actual!r}; do not overwrite or delete it")
    return {
        "status": "reuse_existing",
        "action": "finalize_existing_page_only",
        "widgetRoot": str(root),
        "petId": actual,
        "next": "Preserve this Widget. Run finalize only with page-overwrite authorization; do not call Widget.installPet."
    }


def stage(workspace: Path, preview: bool, existing_roots: list[Path]) -> dict:
    if len(existing_roots) > 1:
        raise ValueError("Multiple Anran candidates found; stop and ask the user to identify the production Pet")
    if existing_roots:
        if preview:
            raise ValueError("A preview must not reuse or modify the production Pet")
        return inspect_existing(existing_roots[0])
    workspace = workspace.resolve()
    pet_id = f"anran-plugin-preview-{uuid.uuid4().hex[:12]}" if preview else production_id()
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
    result = {
        "status": "staged_preview" if preview else "staged_new_production",
        "action": "install_preview" if preview else "install_new_production",
        "petId": pet_id,
        "packagePath": f"pets/{pet_id}",
        "package": str(target),
        "manifestSha256": digest(manifest_path),
        "atlasSha256": digest(target / "spritesheet.webp"),
        "cleanupRequired": preview,
        "next": "Call Widget.installPet with packagePath; then record-preview, finalize and verify. Delete this exact preview after testing."
        if preview else
        "No verified existing production Pet was supplied. Call Widget.installPet once, then Widget.read and finalize."
    }
    if preview:
        ledger = state_path(workspace, pet_id)
        write_state(ledger, {**result, "state": "awaiting_install", "ledger": str(ledger)})
        result["ledger"] = str(ledger)
    return result


def record_preview(workspace: Path, pet_id: str, widget_id: str, widget_root: Path) -> dict:
    if not pet_id.startswith("anran-plugin-preview-"):
        raise ValueError("Only a uniquely named preview can be registered for cleanup")
    ledger = state_path(workspace, pet_id)
    state = json.loads(ledger.read_text(encoding="utf-8"))
    state.update({"state": "cleanup_required", "widgetId": widget_id, "widgetRoot": str(widget_root.resolve())})
    write_state(ledger, state)
    return {"status": "cleanup_required", **state}


def confirm_cleanup(workspace: Path, pet_id: str, widget_id: str) -> dict:
    ledger = state_path(workspace, pet_id)
    state = json.loads(ledger.read_text(encoding="utf-8"))
    if state.get("widgetId") != widget_id:
        raise ValueError("Widget id does not match the preview ledger; refusing to mark cleanup complete")
    write_state(ledger, {**state, "state": "cleaned"})
    return {"status": "cleaned", "petId": pet_id, "widgetId": widget_id, "ledger": str(ledger)}


def pending(workspace: Path) -> dict:
    root = workspace.resolve() / "pets" / ".anran-previews"
    items = []
    if root.is_dir():
        for path in sorted(root.glob("anran-plugin-preview-*.json")):
            state = json.loads(path.read_text(encoding="utf-8"))
            if state.get("state") != "cleaned":
                items.append(state)
    return {"status": "cleanup_required" if items else "no_pending_previews", "count": len(items), "previews": items}


def finalize(widget_root: Path, overwrite: bool) -> dict:
    widget_root = widget_root.resolve()
    target = widget_root / "index.html"
    if target.exists() and not overwrite:
        raise FileExistsError("index.html already exists; preserve user edits or obtain confirmation before overwriting")
    widget_root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ASSETS / "index.html", target)
    return {"status": "published", "index": str(target), "indexSha256": digest(target)}


HOSTS = ("workbuddy", "vbuddy", "qwen", "doubao")
HOST_ENTRIES = {
    "workbuddy": "插件 → MCP 服务器 → 配置 MCP",
    "vbuddy": "连接器 → 添加 → 粘贴 JSON 配置",
    "qwen": "扩展 → 连接器 → 添加 → 手动填写配置",
    "doubao": "技能 · 连接器 · 伙伴 → 新建 → 新建自定义连接器",
}


def runtime_binary() -> Path:
    binary = (ASSETS / "runtime" / "anran").resolve()
    if ASSETS.resolve() not in binary.parents or not binary.is_file() or not binary.stat().st_mode & 0o111:
        raise FileNotFoundError("The unified Anran plugin has no executable bundled runtime; update the plugin before connecting")
    for name in ("pet.json", "spritesheet.webp", "index.html", "manifest.json"):
        if not (ASSETS / "runtime" / "Resources" / "anran-assets" / name).is_file():
            raise FileNotFoundError(f"Bundled Anran runtime resource is missing: {name}")
    return binary


def run_installer(host: str, apply: bool, config: Path | None = None,
                  settings: Path | None = None, install_root: Path | None = None) -> dict:
    """Delegate every installation and host write to the single native entry point."""
    import subprocess
    command = [str(runtime_binary()), "install", "--host", host, "--apply" if apply else "--print"]
    if install_root is not None:
        command += ["--install-root", str(install_root.expanduser().resolve())]
    if config is not None:
        command += ["--config", str(config.expanduser().resolve())]
    if settings is not None:
        command += ["--settings", str(settings.expanduser().resolve())]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=60)
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or "Anran native installation failed")
    result = json.loads(completed.stdout)
    if result.get("requiresKimi") is not False:
        raise RuntimeError("Installed Anran runtime did not confirm independence from Kimi")
    return result


def connection(host: str, install_root: Path | None = None) -> dict:
    return run_installer(host, False, install_root=install_root)


def apply_workbuddy(config_path: Path, settings_path: Path | None = None,
                    install_root: Path | None = None) -> dict:
    """Compatibility wrapper; the native installer owns both official JSON files."""
    settings = settings_path or config_path.expanduser().resolve().with_name("settings.json")
    return run_installer("workbuddy", True, config_path, settings, install_root)


def replace_atomically(source: Path, target: Path) -> None:
    """Replace an existing file without truncating its signed executable in place."""
    temporary = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp")
    try:
        shutil.copy2(source, temporary)
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)


def bundle_runtime(package: Path) -> dict:
    source = package.resolve()
    binary = source / "anran"
    resources = source / "Resources" / "anran-assets"
    if not binary.is_file() or not binary.stat().st_mode & 0o111:
        raise ValueError("Runtime package has no executable anran binary")
    asset_names = ("pet.json", "spritesheet.webp", "index.html", "manifest.json")
    for name in asset_names:
        if not (resources / name).is_file():
            raise FileNotFoundError(resources / name)
    target = ASSETS / "runtime"
    target.mkdir(parents=True, exist_ok=True)
    replace_atomically(binary, target / "anran")
    target_resources = target / "Resources" / "anran-assets"
    target_resources.mkdir(parents=True, exist_ok=True)
    for name in asset_names:
        replace_atomically(resources / name, target_resources / name)
    return {"status": "bundled", "binary": str(target / "anran"), "binarySha256": digest(target / "anran")}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    stage_parser = sub.add_parser("stage")
    stage_parser.add_argument("--workspace", type=Path, required=True)
    stage_parser.add_argument("--preview", action="store_true")
    stage_parser.add_argument("--existing-root", type=Path, action="append", default=[])
    for name in ("record-preview", "confirm-cleanup"):
        command = sub.add_parser(name)
        command.add_argument("--workspace", type=Path, required=True)
        command.add_argument("--pet-id", required=True)
        command.add_argument("--widget-id", required=True)
        if name == "record-preview":
            command.add_argument("--widget-root", type=Path, required=True)
    pending_parser = sub.add_parser("pending")
    pending_parser.add_argument("--workspace", type=Path, required=True)
    finalize_parser = sub.add_parser("finalize")
    finalize_parser.add_argument("--widget-root", type=Path, required=True)
    finalize_parser.add_argument("--overwrite", action="store_true")
    connect_parser = sub.add_parser("connect")
    connect_parser.add_argument("--host", choices=HOSTS, required=True)
    connect_parser.add_argument("--apply", action="store_true", help="Install independently, then write WorkBuddy's official MCP data and task-event hooks")
    connect_parser.add_argument("--config", type=Path, default=Path.home() / ".workbuddy" / "mcp.json")
    connect_parser.add_argument("--settings", type=Path, default=Path.home() / ".workbuddy" / "settings.json")
    connect_parser.add_argument("--install-root", type=Path)
    bundle_parser = sub.add_parser("bundle-runtime")
    bundle_parser.add_argument("--package", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "stage":
        result = stage(args.workspace, args.preview, args.existing_root)
    elif args.command == "record-preview":
        result = record_preview(args.workspace, args.pet_id, args.widget_id, args.widget_root)
    elif args.command == "confirm-cleanup":
        result = confirm_cleanup(args.workspace, args.pet_id, args.widget_id)
    elif args.command == "pending":
        result = pending(args.workspace)
    elif args.command == "connect":
        if args.apply and args.host != "workbuddy":
            parser.error("--apply is supported only for WorkBuddy; use the official connector editor for other hosts")
        if args.apply:
            result = apply_workbuddy(args.config, args.settings, args.install_root)
        else:
            result = connection(args.host, args.install_root)
    elif args.command == "bundle-runtime":
        result = bundle_runtime(args.package)
    else:
        result = finalize(args.widget_root, args.overwrite)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
