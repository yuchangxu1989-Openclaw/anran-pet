#!/bin/bash
set -u

ROOT="$(cd "$(dirname "$0")" && pwd)"
PLUGIN="$ROOT/anran-pet"
RUNTIME="$PLUGIN/assets/runtime/anran"
WORKBUDDY_RECEIPT="$ROOT/workbuddy-install-receipt.json"
KIMI_RECEIPT="$ROOT/kimi-plugin-install-receipt.json"

finish() {
  CODE="$1"
  if [ -t 0 ]; then
    printf '\n按回车关闭此窗口。'
    read -r _
  fi
  exit "$CODE"
}

if [ ! -f "$PLUGIN/kimi.plugin.json" ] || [ ! -x "$RUNTIME" ]; then
  printf '安装失败：插件清单或原生运行器缺失。请完整解压后再运行。\n'
  finish 1
fi

printf '正在安装安燃运行器并配置 WorkBuddy……\n'
if "$RUNTIME" install --host workbuddy --apply \
  --install-root "$HOME/Library/Application Support/Anran" \
  --config "$HOME/.workbuddy/mcp.json" \
  --settings "$HOME/.workbuddy/settings.json" > "$WORKBUDDY_RECEIPT" 2>&1; then
  cat "$WORKBUDDY_RECEIPT"
  printf '\nWorkBuddy 安燃已安装到本机稳定目录，回执保存在：%s\n' "$WORKBUDDY_RECEIPT"
  printf '请手动重开 WorkBuddy，再验收常驻、任务气泡、拖拽和追视。\n'
else
  CODE=$?
  cat "$WORKBUDDY_RECEIPT" 2>/dev/null || true
  printf '\nWorkBuddy 安燃安装失败，退出码：%s。旧配置已由安装器恢复，请保留错误信息和回执。\n' "$CODE"
  finish "$CODE"
fi

if [ "${ANRAN_SKIP_KIMI:-0}" = "1" ]; then
  printf '\n已按测试要求跳过 Kimi 插件安装；WorkBuddy 安燃安装已完成。\n'
  finish 0
fi

BIN=""
if [ -n "${DAIMON_RUNTIME_BINARY_PATH:-}" ] && [ -x "${DAIMON_RUNTIME_BINARY_PATH}" ]; then
  BIN="$DAIMON_RUNTIME_BINARY_PATH"
elif command -v kimi-daimon >/dev/null 2>&1; then
  BIN="$(command -v kimi-daimon)"
fi

if [ -z "$BIN" ] && command -v mdfind >/dev/null 2>&1; then
  while IFS= read -r APP; do
    CANDIDATE="$APP/Contents/Resources/resources/daimon-bundle/bin/kimi-daimon"
    if [ -x "$CANDIDATE" ]; then
      BIN="$CANDIDATE"
      break
    fi
  done < <(mdfind "kMDItemFSName == 'Kimi.app'" 2>/dev/null)
fi

if [ -z "$BIN" ]; then
  for APP in "/Applications/Kimi.app" "$HOME/Applications/Kimi.app"; do
    CANDIDATE="$APP/Contents/Resources/resources/daimon-bundle/bin/kimi-daimon"
    if [ -x "$CANDIDATE" ]; then
      BIN="$CANDIDATE"
      break
    fi
  done
fi

if [ -z "$BIN" ]; then
  printf '\n未检测到 Kimi，已跳过 Kimi 原生桌宠安装；WorkBuddy 安燃可独立使用。\n'
  finish 0
fi

SHARE_DIR="${KIMI_SHARE_DIR:-$HOME/Library/Application Support/kimi-desktop/daimon-share}"
printf '\n检测到 Kimi，正在通过官方入口安装或更新安燃插件……\n'
if "$BIN" kimi-plugin install "$PLUGIN" --share-dir "$SHARE_DIR" --json > "$KIMI_RECEIPT" 2>&1; then
  cat "$KIMI_RECEIPT"
  printf '\nKimi 插件安装命令已完成，回执保存在：%s\n' "$KIMI_RECEIPT"
  printf '如果 Kimi 提示需要重启，请手动重启；然后对 Kimi 说：安装安燃桌宠。\n'
  finish 0
else
  CODE=$?
  cat "$KIMI_RECEIPT" 2>/dev/null || true
  printf '\nWorkBuddy 安燃已经安装，但 Kimi 插件安装失败，退出码：%s。请保留上方错误信息和两份回执。\n' "$CODE"
  finish "$CODE"
fi
