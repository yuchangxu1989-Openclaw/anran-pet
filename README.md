<p align="center">
  <img src="icon.png" width="112" alt="安燃">
</p>

<h1 align="center">安燃</h1>

<p align="center"><strong>住在桌面上的 Agent 小伙伴，让任务进度和情绪反应都看得见。</strong></p>

<p align="center">同一个角色，同一套互动，连接你正在使用的 Agent。</p>

## 认识安燃

安燃把原生桌宠、任务状态气泡和 Agent 连接放在同一个插件里。Kimi、WorkBuddy、vBuddy、千问和豆包共用同一份角色素材与原生运行器，不需要另装第二个 MCP 产品，也不需要手动解压运行器。

**当前公开版本：0.2.38｜Apple Silicon Mac｜Apache-2.0**

### 桌面上的一个伙伴

- **会回应你的动作**：单击跳跃、双击施法，连续点击会出现升级反应，左右拖动会切换动作。
- **眼睛会跟着你走**：在具备独立眼部数据的状态中追踪指针，动作与任务切换后继续保留追视。
- **有自己的状态**：日常、休息、互动和任务状态使用同一套角色素材，不会在不同 Agent 里换成另一个形象。

### 任务进展不用反复切换窗口

- 任务中、完成和错误都有对应的气泡与图标；只有豆包保留“等你确认”，其他 Agent 的权限或询问事件保持任务进行中，不显示带叹号的等待气泡。
- 多条任务默认完整展开；点击折叠按钮后显示进行中任务数量，再次点击恢复完整列表。
- 运行中点击气泡可打开所属 Agent；完成后点击状态图标可收起卡片。
- 不同 Agent 使用带身份的任务文案，同时开着几个桌宠时也能分清来源。

### 跟着 Agent 来，也跟着 Agent 走

Agent 连接时显示安燃，Agent 退出后关闭；任务结束不会把桌宠一并关掉。拖动后的位置会保留，不自动回到屏幕中央。

隐藏后不需要反复开关插件：点击菜单栏“安燃 → 显示安燃”，或运行 `~/Library/Application\ Support/Anran/current/anran show --host workbuddy`（其他宿主把 `workbuddy` 换成 `vbuddy`、`qwen` 或 `doubao`）。两种方式都会保留任务、屏幕和拖动后的位置；运行器未连接时命令会明确报错。

> 当前 WorkBuddy 连接能力可以打开宿主应用，暂不能定位到具体会话、代替你回复或取消任务。

## 快速开始

### 把这句话复制给你的 Agent

> 请在我这台 Apple Silicon Mac 上安装、启动并使用安燃，公开仓库是 https://github.com/yuchangxu1989-Openclaw/anran-pet 。不要让我替换宿主名、拼接命令、解压运行器或另装第二套 MCP。先读取当前公开 README。如果自动导入、命令执行或官方配置写入失败，不要停在报错，也不要把整段命令转交给我；继续读取 README 的“自动安装失败时的手动兜底”，按当前宿主的官方界面路径完成安装，官方没有受支持手动入口时明确报告限制。如果我是 KimiWork：通过官方 Plugin Builder 导入这个 GitHub 仓库，运行导入源目录中的 skills/anran-pet/scripts/install_plugin.py --id anran-pet，由官方插件接口安装并回读，再严格按已加载的 anran-pet 技能发现或创建正式安燃实例、启动并发布交互页面；不要运行面向其他宿主的原生 --host 安装。其他 Agent 通过 Node.js 原样运行 npx -y github:yuchangxu1989-Openclaw/anran-pet install --host auto --print；auto 只根据当前进程识别宿主，无法唯一识别时才按你的真实身份改用 workbuddy、vbuddy、qwen 或 doubao，不根据已安装应用猜测。WorkBuddy 用 --host workbuddy --apply 自动写入官方配置和任务 Hooks 并回读；vBuddy 用 --host vbuddy --apply 生成官方套件，只需引导我在“技能 · 扩展 → 专家套件 → 添加 → 上传套件”选择输出中的 vbuddy.archivePath，官方 Hooks 负责任务气泡，不能只装 MCP；千问个人版只需在官方“扩展 → 连接器 → 添加 → 粘贴 JSON 配置”中粘贴 configuration.officialJSON，连接后共享运行器只读监听本机桌面生命周期并自动显示任务中与完成气泡，不要求上传 Qoder 套件；桌面日志是唯一建卡来源，旧 HTTP、外部命令 Hooks 与模型主动 MCP 不再建卡；豆包引导我在“技能 · 连接器 · 伙伴 → 新建 → 新建自定义连接器”中填写 configuration，连接后共享运行器只读监听本机桌面生命周期并自动显示任务中、完成或失败，不要求模型主动上报。官方界面必须由我确认时，只告诉我这一项操作。安装后回读版本、资源哈希和七个工具并运行自测，再完成真实连接检查；任务气泡、单击、双击和拖拽未实际验证就明确标为未验收，无法完成的步骤不要假装成功。

同一段文字可原样复制到 KimiWork、WorkBuddy、vBuddy、千问办公或豆包，不需要替换宿主名。KimiWork 通过官方 Plugin Builder 导入公开插件并创建桌宠；其他 Agent 识别当前宿主并安装同一原生运行器。只有官方界面强制要求时才请你确认或粘贴已生成的完整配置。宿主没有任务事件入口或真实任务气泡未通过时，Agent 必须明确报告，不能把连接成功说成全部体验已对齐。

### 自动安装失败时的手动兜底

自动导入、下载、命令执行或配置写入失败时，Agent 不应只把报错交还给用户，也不应让用户自己研究命令。Agent 要先保留错误、判断失败发生在哪一步，再按下表继续引导官方界面操作；只有界面必须本人确认的步骤才交给用户，其余步骤仍由 Agent 完成。不得直接写宿主的受管目录或私有配置。

| 当前 Agent | 自动安装失败后的官方手动路径 | 完成后怎样确认 |
|---|---|---|
| KimiWork | 让 Agent 通过官方 Plugin Builder 重新导入本仓库，并由官方插件接口安装；随后对 Kimi 说“安装安燃”，创建或复用正式桌宠。若当前客户端没有受支持的 GitHub 导入入口，明确报告限制，不改受管插件目录。 | 回读官方插件安装状态，再确认正式桌宠和交互页面已发布；导入回执本身不算桌宠已启动。 |
| WorkBuddy | 打开官方 MCP 设置，粘贴下方 WorkBuddy 完整 JSON，保存并重新连接。随后让 Agent 回读 MCP 与任务 Hooks；若 Hooks 仍未写入，只算连接器已配置，任务气泡继续标为未完成。 | 回读运行器版本、资源哈希、七个工具和任务 Hooks，不用“已连接”代替任务气泡验收。 |
| vBuddy | 由 Agent 运行下方 `install --host vbuddy --apply`，读取输出中的 `vbuddy.archivePath`；用户只需在“专家套件 → 添加 → 上传套件”选择该 ZIP。若提示同名冲突，确认替换的是当前安燃套件。 | 在套件详情页回读目标版本并确认已启用；只生成 ZIP、只装 MCP 都不等于完成。 |
| 千问办公 | 由 Agent 运行 `install --host qwen --apply`，读取 `qwen.archivePath`；用户在“技能 · 扩展 → 专家套件 → 添加 → 上传套件”选择该 ZIP，若提示同名冲突，确认替换当前安燃套件。再由 Agent 读取 `configuration.officialJSON`，引导用户在“扩展 → 连接器 → 添加 → 粘贴 JSON 配置”粘贴完整 JSON；不要拆分含空格的 `command` 路径。 | 在套件详情页回读目标版本并确认启用，再回读连接器“已连接”和七个工具；发送无工具短任务，确认任务中与完成事件。只生成 ZIP、只装 MCP 都不等于完成。 |
| 豆包 | 由 Agent 运行 `install --host doubao --print`，读取 `configuration`；用户在“技能 · 连接器 · 伙伴 → 新建 → 新建自定义连接器”填写该配置。 | 回读连接器与七个工具；连接后由共享运行器只读监听桌面任务生命周期，发送无工具短任务确认任务中与完成气泡。真实视觉未通过时仍须明确报告。 |

如果下载本身失败，先保留网络或权限错误，再重试公开仓库读取；如果平台没有上述受支持入口，就明确写出“当前没有已核实的手动安装兜底”，不要编造配置路径。手动安装完成后仍须执行版本、资源哈希、七个工具和真实连接检查。

### Kimi

Kimi 的主分发渠道是插件市场。用户可以直接安装“桌宠安燃”，也可以对 Kimi 说“安装安燃”，由 Kimi 调起市场入口。当前插件仅在个人市场登记，尚未完成官方公开上架；在公开市场上线前，陌生用户使用 GitHub 公开安装入口。

已经安装并启用安燃插件时，直接说：

> 安装安燃

Kimi 会发现并复用已有正式实例；确认不存在时才创建 Kimi 中的安燃桌宠并发布交互页面。插件详情页的“使用”按钮本身不会创建桌宠。

陌生 KimiWork 用户直接复制上方同一句安装提示词。Kimi 应通过官方 Plugin Builder 导入这个公开仓库，再运行导入源目录中的 `skills/anran-pet/scripts/install_plugin.py --id anran-pet`，由官方插件接口安装并回读；随后按安燃技能发现并复用唯一正式实例，确认不存在才创建并发布交互页面。不要把插件导入回执当作桌宠已经启动。GitHub 同时保存公开版本与安装证据。

### WorkBuddy

WorkBuddy 5.0.0 及以上版本可以在官方 MCP 配置中使用下面的公开连接。它会让 WorkBuddy 准备 Node.js，从指定 Git 标签获取安燃，并启动本地 MCP 服务；不需要安装 Kimi。

```json
{
  "mcpServers": {
    "anran-desktop-pet": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "github:yuchangxu1989-Openclaw/anran-pet#v0.2.38",
        "mcp",
        "--stdio",
        "--host",
        "workbuddy"
      ],
      "runtime": {
        "type": "node",
        "version": ">=18.0.0"
      },
      "timeout": 120000
    }
  }
}
```

保存后重新连接 WorkBuddy。首次连接会从 GitHub 下载运行器和资源，并将它们安装到 `~/Library/Application Support/Anran/`；以后不依赖这个仓库的本地副本。

如果只需先检查公开包能否在自己的 Mac 上安装，可以运行：

```sh
npx -y github:yuchangxu1989-Openclaw/anran-pet#v0.2.38 version
npx -y github:yuchangxu1989-Openclaw/anran-pet#v0.2.38 self-test
```

这两条命令分别回读版本和运行模型自测，不会代替真实桌面体验验收。

### vBuddy、千问和豆包

对已经装有安燃插件的 Agent 说：

> 把安燃连接到千问

也可以换成 vBuddy 或豆包。统一入口会生成对应配置，再通过该 Agent 的官方连接器界面保存。

vBuddy 使用官方 Qoder 套件 command Hooks 自动上报任务状态，MCP 提供工具并作为备用。千问个人版连接官方 MCP 后，由共享运行器只读监听本机桌面生命周期并自动显示任务中与完成气泡，不要求上传 Qoder 套件。分别运行：

```sh
npx -y github:yuchangxu1989-Openclaw/anran-pet#v0.2.38 install --host vbuddy --apply
npx -y github:yuchangxu1989-Openclaw/anran-pet#v0.2.38 install --host qwen --print
```

vBuddy 再打开“技能 · 扩展 → 专家套件 → 添加 → 上传套件”，选择输出中的 `vbuddy.archivePath`。不要用已证实不可用的 `install_from_path`，也不要直接写 `plugins-custom` 或私有注册表。千问个人版不需要上传套件；只有自动链路失败时，才按上方“自动安装失败时的手动兜底”使用 `qwen.archivePath` 走官方上传入口。

千问需在官方“扩展 → 连接器 → 添加 → 粘贴 JSON 配置”中粘贴安装输出里的 `configuration.officialJSON`，不要改用手动命令表单。完整 JSON 会保留含空格的 `command` 路径和独立 `args`；下面的千问示例仅用于说明结构，实际安装以命令输出为准：

```json
{
  "mcpServers": {
    "安燃": {
      "command": "/Users/YOUR_USERNAME/Library/Application Support/Anran/current/anran",
      "args": ["mcp", "--stdio", "--host", "qwen"]
    }
  }
}
```

vBuddy 的 MCP 备用配置也使用相同结构，将最后一个参数改为 `vbuddy`；不要手动拼接或拆分命令。

vBuddy 已于 2026-11-26 固定“【M4安全】vivo企业专属模型”完成真实任务验收，观察到“正在处理”与“已完成”气泡，没有“等你确认”或叹号气泡。千问个人版已完成官方 JSON 导入，回读“已连接”、开关开启和七个工具；宿主日志确认当前 OpenCode 策略不执行 Qoder command Hooks，因此改用共享运行器只读监听本机桌面生命周期。候选运行器已在隔离环境中实测任务开始、带真实标题的完成卡片与自动隐藏；正式共享进程仍需重连加载新版后复验。

千问的桌面日志是唯一任务建卡来源，旧 HTTP、外部命令 Hooks 与模型主动 MCP 不再建卡，避免同一任务出现重复气泡；无需再到企业后台配置补充事件。豆包由共享运行器只读监听桌面 `agent_task_status` 与会话结束记录，自动显示任务中、完成或失败，不依赖模型主动调用 MCP。真实日志副本已通过隔离回放；当前任务标题使用“豆包工作任务”安全回退，真实桌面视觉和正式共享进程仍需复验。

## 一次升级，各端使用同一份产品

原生运行器、角色素材和体验约定由同一份产品源生成。公开包、Kimi 插件源包和 WorkBuddy Connector 使用相同产品版本；安装后还会核对版本与文件哈希，避免不同端各自维护、逐渐出现功能差异。

Kimi 插件“更新”只更新 Kimi 自己的插件副本。其他 Agent 的运行器由安燃统一安装入口升级，上一代会保留用于失败回滚。

## 隐私与安全

- 核心功能离线运行，不索取 Agent 账号、模型密钥或远程控制权限。
- 气泡只显示经过截断的任务片段；完整提示词和工具正文不进入桌宠，也不写入任务事件正文日志。
- 只使用官方桌宠接口、官方连接器界面和 WorkBuddy 官方 MCP 数据文件，不修改宿主程序包。
- 安装或配置写入失败会明确报错，并恢复旧配置与旧运行器。

## 发布渠道

| 渠道 | 当前状态 |
|---|---|
| GitHub | 已公开，可直接获取 0.2.38；不需要企业认证 |
| Kimi 官方市场 | 个人插件可在详情页右上角「✉️」选择“申请发布到官方市场”，填写联系邮箱后由审核团队评估；申请不等于上架 |
| WorkBuddy Connector 市场 | 需要企业认证；没有经营主体无法发布。0.2.38 Connector 本地候选已生成，未提交、未上架 |
| 千问办公公共扩展 | 官方文档写明当前版本暂不支持个人用户上传或发布自建技能 |
| 豆包 | 暂未找到支持个人公开发布此类桌宠插件的官方入口 |

参考：[Kimi 插件发布说明](https://www.kimi.com/help/plugins-and-skills/publish)、[WorkBuddy Connector 说明](https://open.workbuddy.cn/docs/connector)、[WorkBuddy 开放平台概述](https://open.workbuddy.cn/docs/what-is-open-platform)、[千问办公扩展说明](https://help.aliyun.com/zh/qwenwork/qwenwork-extensions-1)、[千问办公 Hooks](https://help.aliyun.com/zh/qwenwork/qw-hooks)。

## 当前验收边界

0.2.38 公开版只有在指定 Git 标签下完成 WorkBuddy、vBuddy、千问和豆包的隔离安装、版本与哈希回读和自测后才发布为可用；KimiWork 使用官方插件导入与桌宠创建路线。公开安装结果、本机插件更新和真实宿主体验分别记录，任何一项都不冒充另外两项。

以下项目仍需在真实环境单独验收：

- 真实视觉、hover 动作、白色手型、系统忙碌光标、单击／连击、眼部追视和拖拽流畅度；vBuddy 官方 Hooks 任务气泡已通过，完整指针交互仍待验收；
- 千问个人版只读任务适配已通过候选隔离验收，正式共享进程重连后的新版任务气泡与完整桌面体验仍待复验；豆包的真实连接与桌面体验；
- 第二台无 Kimi Mac、Gatekeeper、签名与公证、跨显示器和 macOS 13；
- 各公开市场的实际提交、审核和上架。

运行器当前未签名、未公证；如果 macOS 阻止打开，请保留系统提示并反馈，不建议绕过系统保护。

## 许可

代码、页面与随附安燃资产采用 [Apache License 2.0](LICENSE)。
