#!/usr/bin/env python3
"""Offline regression for instance reuse and preview cleanup; never calls host APIs."""
import importlib.util
import json
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("install_anran.py")
spec = importlib.util.spec_from_file_location("install_anran", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

checks = []
with tempfile.TemporaryDirectory() as temporary:
    workspace = Path(temporary)
    production = workspace / "production"
    production.mkdir()
    (production / "pet.json").write_text(json.dumps({"id": module.production_id()}), encoding="utf-8")
    result = module.stage(workspace, False, [production])
    assert result["action"] == "finalize_existing_page_only"
    assert not (workspace / "pets" / module.production_id()).exists()
    checks.append("existing production is reused without staging a new package")

    other = workspace / "other"
    other.mkdir()
    (other / "pet.json").write_text(json.dumps({"id": "unknown-pet"}), encoding="utf-8")
    try:
        module.stage(workspace, False, [other])
        raise AssertionError("identity mismatch was not rejected")
    except ValueError:
        checks.append("unknown identity is rejected")

    try:
        module.stage(workspace, False, [production, production])
        raise AssertionError("multiple candidates were not rejected")
    except ValueError:
        checks.append("multiple candidates are rejected")

    fresh = module.stage(workspace, False, [])
    assert fresh["action"] == "install_new_production"
    assert fresh["petId"] == module.production_id()
    checks.append("confirmed absence allows one production installation")

    first = module.stage(workspace, True, [])
    second = module.stage(workspace, True, [])
    assert first["petId"] != second["petId"]
    assert first["cleanupRequired"] and second["cleanupRequired"]
    assert module.pending(workspace)["count"] == 2
    checks.append("previews have unique identities and pending cleanup")

    module.record_preview(workspace, first["petId"], "widget_preview", workspace / "preview")
    try:
        module.confirm_cleanup(workspace, first["petId"], "wrong_widget")
        raise AssertionError("wrong cleanup target was not rejected")
    except ValueError:
        checks.append("cleanup confirmation rejects a different Widget")

    cleaned = module.confirm_cleanup(workspace, first["petId"], "widget_preview")
    assert cleaned["status"] == "cleaned"
    assert module.pending(workspace)["count"] == 1
    module.record_preview(workspace, second["petId"], "widget_preview_2", workspace / "preview2")
    module.confirm_cleanup(workspace, second["petId"], "widget_preview_2")
    assert module.pending(workspace)["status"] == "no_pending_previews"
    checks.append("all previews must be explicitly confirmed cleaned")

    # The plugin delegates host installation to the native executable. Native
    # installation, JSON preservation and rollback are covered by its own tests.
    module.ASSETS = workspace / "plugin-assets"
    resources = module.ASSETS / "runtime" / "Resources" / "anran-assets"
    resources.mkdir(parents=True)
    binary = module.ASSETS / "runtime" / "anran"
    binary.write_text("#!/bin/sh\n", encoding="utf-8")
    binary.chmod(0o755)
    for name in ("pet.json", "spritesheet.webp", "index.html", "manifest.json"):
        (resources / name).write_text(name, encoding="utf-8")

    import subprocess
    calls = []
    real_run = subprocess.run

    def fake_run(command, capture_output, text, timeout):
        calls.append(command)
        return subprocess.CompletedProcess(
            command, 0,
            stdout=json.dumps({"status": "installed", "requiresKimi": False, "configuration": {}}),
            stderr="",
        )

    subprocess.run = fake_run
    try:
        install_root = workspace / "installed" / "Anran"
        for host in module.HOSTS:
            result = module.connection(host, install_root)
            assert result["requiresKimi"] is False
            assert calls[-1] == [
                str(binary.resolve()), "install", "--host", host, "--print",
                "--install-root", str(install_root.resolve()),
            ]
        config = workspace / "mcp.json"
        settings = workspace / "settings.json"
        module.apply_workbuddy(config, settings, install_root)
        assert calls[-1] == [
            str(binary.resolve()), "install", "--host", "workbuddy", "--apply",
            "--install-root", str(install_root.resolve()),
            "--config", str(config.resolve()),
            "--settings", str(settings.resolve()),
        ]
    finally:
        subprocess.run = real_run
    checks.append("every host connection delegates to the native installer with isolated paths")

    def failed_run(command, capture_output, text, timeout):
        return subprocess.CompletedProcess(command, 1, stdout="", stderr="native install failed")

    subprocess.run = failed_run
    try:
        try:
            module.connection("workbuddy", install_root)
            raise AssertionError("native installation failure was hidden")
        except RuntimeError as error:
            assert "native install failed" in str(error)
    finally:
        subprocess.run = real_run
    checks.append("native installer failures remain visible to the caller")

    package = workspace / "runtime-package"
    package_resources = package / "Resources" / "anran-assets"
    package_resources.mkdir(parents=True)
    package_binary = package / "anran"
    asset_names = ("pet.json", "spritesheet.webp", "index.html", "manifest.json")
    assert binary.is_file() and all((resources / name).is_file() for name in asset_names)
    for version in ("first", "second"):
        package_binary.write_text(f"#!/bin/sh\necho {version}\n", encoding="utf-8")
        package_binary.chmod(0o755)
        for name in asset_names:
            (package_resources / name).write_text(f"{name}:{version}", encoding="utf-8")
        previous_inode = binary.stat().st_ino
        previous_resource_inodes = {name: (resources / name).stat().st_ino for name in asset_names}
        module.bundle_runtime(package)
        assert binary.stat().st_ino != previous_inode
        assert binary.read_bytes() == package_binary.read_bytes()
        for name in asset_names:
            target_resource = resources / name
            assert target_resource.stat().st_ino != previous_resource_inodes[name]
            assert target_resource.read_bytes() == (package_resources / name).read_bytes()
        assert not list((module.ASSETS / "runtime").rglob("*.tmp"))
    checks.append("repeated runtime bundling atomically replaces existing binaries and resources")

    binary.unlink()
    try:
        module.connection("vbuddy")
        raise AssertionError("missing runtime was not rejected")
    except FileNotFoundError:
        checks.append("missing bundled runtime fails instead of invoking a broken installer")

print(json.dumps({"status": "PASS", "checks": checks}, ensure_ascii=False, indent=2))
