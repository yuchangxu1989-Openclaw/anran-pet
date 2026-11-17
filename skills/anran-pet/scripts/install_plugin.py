#!/usr/bin/env python3
"""Install an already registered plugin through Kimi's official daemon RPC."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path
import shutil

LIST = "kimiPlugin.personal.listPlugins"
INSTALL = "kimiPlugin.personal.installPlugin"


def payload(response: dict) -> object:
    if not isinstance(response, dict) or "error" in response or response.get("result") is None:
        raise RuntimeError("Official plugin RPC returned no usable result")
    return response["result"]


def plugins(value: object) -> list[dict]:
    if not isinstance(value, list):
        raise RuntimeError("Official plugin list has an unexpected shape")
    rows: list[dict] = []
    for item in value:
        if not isinstance(item, dict):
            raise RuntimeError("Official plugin list contains an invalid entry")
        nested = item.get("plugins")
        rows.extend(nested if isinstance(nested, list) else [item])
    return rows


def select(value: object, plugin_id: str) -> dict:
    matches = [row for row in plugins(value) if row.get("id") == plugin_id]
    if len(matches) != 1:
        raise RuntimeError(f"Registered plugin not found or ambiguous: {plugin_id}")
    return matches[0]


class Official:
    def __init__(self) -> None:
        self.binary = os.environ.get("DAIMON_RUNTIME_BINARY_PATH") or shutil.which("kimi-daimon")
        share = os.environ.get("KIMI_SHARE_DIR")
        if not self.binary or not share:
            raise RuntimeError("Kimi runtime discovery is unavailable")
        self.share = Path(share).resolve()
        self.token = ""

    async def endpoint(self) -> dict:
        process = await asyncio.create_subprocess_exec(
            self.binary, "status", "--json",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
        output, _ = await process.communicate()
        if process.returncode != 0:
            raise RuntimeError("Kimi runtime status command failed")
        text = output.decode("utf-8")
        start = text.find("{")
        if start < 0:
            raise RuntimeError("Kimi runtime status returned no JSON")
        status, end = json.JSONDecoder().raw_decode(text[start:])
        if text[start + end:].strip():
            raise RuntimeError("Kimi runtime status returned unexpected trailing data")
        endpoint = status["control"]["endpoint"]
        self.token = endpoint["auth"]["token"]
        if not isinstance(endpoint.get("url"), str) or not self.token:
            raise RuntimeError("Kimi runtime endpoint is unavailable")
        return endpoint

    async def rpc(self, endpoint: dict, method: str, params: dict) -> object:
        import websockets

        async with websockets.connect(
            endpoint["url"],
            additional_headers={"Authorization": "Bearer " + self.token},
            open_timeout=5,
            close_timeout=1,
        ) as socket:
            await socket.send(json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}))
            while True:
                response = json.loads(await socket.recv())
                if response.get("id") == 1:
                    return payload(response)


async def install(plugin_id: str, backend: Official) -> dict:
    endpoint = await backend.endpoint()
    before = select(await backend.rpc(endpoint, LIST, {"allMarkets": True}), plugin_id)
    current = before.get("sourceVersion") == before.get("installedVersion") and before.get("status") == "installed" and before.get("health") == "ok"
    if current:
        result = {"alreadyInstalled": True}
    else:
        method = "kimiPlugin.personal.updatePlugin" if before.get("installedVersion") else INSTALL
        result = await backend.rpc(endpoint, method, {"id": before["id"]})
    endpoint = await backend.endpoint()
    after = select(await backend.rpc(endpoint, LIST, {"allMarkets": True}), plugin_id)
    readback = {key: after.get(key) for key in ("id", "sourceVersion", "installedVersion", "status", "health")}
    return {
        "ok": after.get("status") == "installed" and after.get("health") == "ok"
        and after.get("sourceVersion") == after.get("installedVersion"),
        "installResult": result,
        "readback": readback,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", default="anran-pet")
    args = parser.parse_args()
    backend = None
    try:
        backend = Official()
        result = asyncio.run(install(args.id, backend))
    except Exception:
        result = {"ok": False, "error": "official_install_failed"}
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if backend and backend.token:
        output = output.replace(backend.token, "[REDACTED]")
    print(output)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
