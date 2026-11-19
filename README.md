<p align="center">
  <img src="icon.png" width="112" alt="安燃">
</p>

<h1 align="center">安燃</h1>

<p align="center"><strong>住在桌面上的 Agent 小伙伴，让任务进度和情绪反应都看得见。</strong></p>

<p align="center">同一个角色，同一套互动，连接你正在使用的 Agent。</p>

## 认识安燃

安燃把原生桌宠、任务状态气泡和 Agent 连接放在同一个插件里。Kimi、WorkBuddy、vBuddy、千问和豆包共用同一份角色素材与原生运行器，不需要另装第二个 MCP 产品，也不需要手动解压运行器。

**当前公开版本：0.2.9｜Apple Silicon Mac｜Apache-2.0**

### 桌面上的一个伙伴

- **会回应你的动作**：单击跳跃、双击施法，连续点击会出现升级反应，左右拖动会切换动作。
- **眼睛会跟着你走**：在具备独立眼部数据的状态中追踪指针，动作与任务切换后继续保留追视。
- **有自己的状态**：日常、休息、互动和任务状态使用同一套角色素材，不会在不同 Agent 里换成另一个形象。

### 任务进展不用反复切换窗口

- 任务中、完成、等待确认和错误都有对应的气泡与图标。
- 多条任务可以计数、叠放和展开；桌宠右下角提供折叠按钮。
- 运行中点击气泡可打开所属 Agent；完成后点击状态图标可收起卡片。
- 不同 Agent 使用带身份的任务文案，同时开着几个桌宠时也能分清来源。

### 跟着 Agent 来，也跟着 Agent 走

Agent 连接时显示安燃，Agent 退出后关闭；任务结束不会把桌宠一并关掉。拖动后的位置会保留，不自动回到屏幕中央。

> 当前 WorkBuddy 连接能力可以打开宿主应用，暂不能定位到具体会话、代替你回复或取消任务。

## 快速开始

### Kimi

把[这个仓库](https://github.com/yuchangxu1989-Openclaw/anran-pet)的链接发给 Kimi，并说：

> 安装并启动这个仓库里的安燃

Kimi 会导入插件，发现并复用已有正式实例；确认不存在时才创建原生 DIY 桌宠并发布交互页面。插件详情页的“使用”按钮本身不会创建桌宠。

已经安装并启用安燃插件时，直接说：

> 安装安燃

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
        "github:yuchangxu1989-Openclaw/anran-pet#v0.2.9",
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
npx -y github:yuchangxu1989-Openclaw/anran-pet#v0.2.9 version
npx -y github:yuchangxu1989-Openclaw/anran-pet#v0.2.9 self-test
```

这两条命令分别回读版本和运行模型自测，不会代替真实桌面体验验收。

### vBuddy、千问和豆包

对已经装有安燃插件的 Agent 说：

> 把安燃连接到千问

也可以换成 vBuddy 或豆包。统一入口会生成对应配置，再通过该 Agent 的官方连接器界面保存。上述宿主的真实界面与交互尚未逐项验收。

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
| GitHub | 已公开，可直接获取 0.2.9；不需要企业认证 |
| Kimi 官方市场 | 个人插件可在详情页右上角「✉️」选择“申请发布到官方市场”，填写联系邮箱后由审核团队评估；申请不等于上架 |
| WorkBuddy Connector 市场 | 已准备 0.2.9 Connector 包；官方文档要求完成开发者或企业资质认证，个人账号能否提交仍需以账号页面与审核结果为准 |
| 千问办公公共扩展 | 官方文档写明当前版本暂不支持个人用户上传或发布自建技能 |
| 豆包 | 暂未找到支持个人公开发布此类桌宠插件的官方入口 |

参考：[Kimi 插件发布说明](https://www.kimi.com/help/plugins-and-skills/publish)、[WorkBuddy Connector 说明](https://open.workbuddy.cn/docs/connector)、[WorkBuddy 开放平台概述](https://open.workbuddy.cn/docs/what-is-open-platform)、[千问办公扩展说明](https://help.aliyun.com/zh/qwenwork/qwenwork-extensions-1)。

## 当前验收边界

0.2.9 已通过 12 组自动检查，包括 3089 项 Swift 模型检查、协议、独立安装、资源一致性、公开包结构和 Connector 内容检查。指定 Git 标签的公开安装、版本与哈希回读、自测也已通过。

以下项目仍需在真实环境单独验收：

- WorkBuddy 冷启动自动出现、气泡视觉、各状态图标点击与多气泡展开和折叠；
- 悬停光标、单击／连击、眼部追视和拖拽流畅度；
- vBuddy、千问和豆包的真实连接与桌面体验；
- 第二台无 Kimi Mac、Gatekeeper、签名与公证；
- 各公开市场的实际提交、审核和上架。

运行器当前未签名、未公证；如果 macOS 阻止打开，请保留系统提示并反馈，不建议绕过系统保护。

## 许可

代码、页面与随附安燃资产采用 [Apache License 2.0](LICENSE)。
