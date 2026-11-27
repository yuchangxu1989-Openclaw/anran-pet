---
name: anran-pet
description: 安装、恢复、检查安燃，或把同一个安燃连接到 WorkBuddy、vBuddy、千问和豆包。用户说“安装安燃”“把安燃放到桌面”“打开安燃”“恢复安燃的交互页面”“把安燃连接到某个 Agent”时使用；一个插件统一提供原生桌宠、运行器与各宿主官方连接配置，不另装 MCP 产品。只制作其他桌宠或修改安燃素材时不使用，通用制作流程归 pet-plus。
---

# 安燃

本插件是安燃唯一的产品入口，提供当前图集、清单、交互页面、运行器与各 Agent 的连接配置。插件安装后不会自动弹出桌宠；用户提出安装请求时才执行。其他宿主中的“安燃连接器”只是同一产品的注册，不是另一套插件。

## Kimi：安装或恢复

用户直接说“安装安燃”“把安燃放到桌面”或“打开安燃”时，Kimi 优先使用插件市场；插件已安装则无需仓库，也不重复安装插件。GitHub 只承担公开源程序、版本证据及市场不可用时的备用安装。

1. 调用 `Widget.list`，筛选 `type=pet` 且标题为安燃的候选，逐个用 `Widget.read` 取得 `workspaceRoot`，读取其 `pet.json`。唯一候选且 `id` 与插件 `assets/pet/pet.json` 的正式 `id` 一致时复用；确认没有正式实例才创建。多个候选、身份不一致或无法读取时停止。
2. 复用时运行 `install_anran.py stage --workspace <当前工作区> --existing-root <正式实例的 workspaceRoot>`，禁止再调用 `Widget.installPet`。只有用户要求恢复页面且允许覆盖时才运行 `finalize --overwrite`。
3. 首次创建时运行 `install_anran.py stage --workspace <当前工作区>`，再调用 `Widget.installPet` 并传入返回的 `packagePath`。用 `Widget.read` 读取新实例，确认默认页面确由本次安装生成后运行 `finalize --overwrite`。
4. 读回 `pet.json`、图集和 `index.html` 哈希。真实桌面、输入和播放未观察时明确标为未验收，不用安装回执代替。

市场不可用或用户明确选择 GitHub 备用安装时，先通过内置 Plugin Builder 导入登记，再运行源目录 `scripts/install_plugin.py --id anran-pet`，由官方接口安装并回读。随后连续完成上述流程，不停在登记、安装回执或要求用户再点击。不要使用已实测不能完成 GitHub 安装的 `kimi-daimon kimi-plugin install <GitHub链接>`。

## 其他 Agent：连接同一个安燃

1. 从当前技能位置解析插件根，运行 `python3 <本技能目录>/scripts/install_anran.py connect --host auto`；无法唯一识别时，Agent 按自身真实身份改用 `workbuddy|vbuddy|qwen|doubao`，不让用户替换公开提示词或根据已安装应用猜测。脚本只委托插件内的原生 `assets/runtime/anran install`；运行器或资源缺失时非零失败，不输出假配置。
2. 原生安装入口先把运行器和资源复制到 `~/Library/Application Support/Anran/versions/<版本-哈希>/`，检查版本、资源与哈希后切换 `current`。所有宿主只引用 `current/anran`，上一代保留用于回滚；已安装运行器不依赖 Kimi 安装目录或源插件目录继续存在。
3. WorkBuddy 使用 `--apply`，由同一原生入口更新官方 MCP 数据文件和官方用户 hooks。更新前备份，只替换唯一的安燃项与安燃自己的任务事件 hooks，原子写入并回读，保留所有无关连接器、hooks 和配置；多个安燃候选项必须停止。任务气泡显示本次任务的短片段，完整提示词与工具正文不进入桌宠。
4. vBuddy 使用 `--apply` 生成官方 Qoder 套件 ZIP，由 Agent 引导用户在“技能 · 扩展 → 专家套件 → 添加 → 上传套件”选择输出中的 `vbuddy.archivePath`，再把 `configuration.officialJSON` 填入官方连接器界面。保存后重新启用或刷新，读取套件版本、连接器状态和真实运行进程。2026-11-26 的真实 vBuddy 负例已证明：连接器识别到七个工具，但 MCP-only 对话没有调用 `anran_task`，因此不能只装 MCP 就宣称支持自动任务气泡；随后已用指定免费模型实测 command Hooks 的任务中与完成气泡。千问只需把 `configuration.officialJSON` 填入官方连接器，共享运行器只读监听本机桌面生命周期，从当前日志末尾识别任务开始、完成、失败与取消，不修改千问应用或配置，也不要求上传 Qoder 套件。桌面日志是唯一任务建卡来源；旧 HTTP、外部命令 Hooks 与模型主动 MCP 不再建卡，避免重复卡片。失败文字卡可保留，失败表情在共享动画入口对所有宿主停用。候选运行器已隔离实测，正式进程仍须重连后由用户现场复验卡数、暂停与清卡。豆包由 Agent 填写官方连接器，MCP 主动上报不保证任务气泡。没有官方支持入口时停止并说明，不写私有配置或修改宿主。
5. 不另装 MCP 插件，不让用户解压运行器 ZIP，不让用户手工拼接命令。Kimi 插件“更新”只更新 Kimi 自己的插件副本，不再是 WorkBuddy 或其他宿主的前置步骤；各宿主通过同一安燃安装入口使用稳定目录中的运行器。

所有受支持宿主必须遵循同一体验合同：宿主客户端启动并连接时显示安燃；任务结束或 stdio 断开不再关闭，宿主客户端退出时才关闭；右键提供“打开 <宿主名>”和“关闭桌面宠物”；拖动位置持久保存，屏幕变化只收回到可见边缘，不自动回中央。逐项在真实宿主验收，未测不得宣称一致；连接器绿色、宠物可见或离线工具调用都不能代替真实对话中的任务气泡验收。

## 发布与更新

以项目登记的当前原生资产和 `experience-contract.json` 为唯一体验来源，以 `anran_product_repair_20261117/release-contract.json` 为唯一渠道与版本口径。统一发布入口 `anran_product_repair_20261117/release_anran.py` 读取发布合同，同步素材与体验合同、生成参考光标、构建运行器并放入本插件；所有宿主共用这一产物，不分别维护视觉或交互分支。任何宿主安装或升级都先写入安燃自己的稳定安装目录，再更新该宿主的官方连接配置；Python 连接脚本不另维护一套写入逻辑。

公开版本只能在全部离线检查通过后，由同一入口使用 `--publish` 提交当前插件源包、创建不覆盖旧版本的 Git 标签并推送 GitHub。随后必须从公开标签在隔离 HOME 与 npm 缓存中重新安装，回读版本、原生二进制哈希、体验合同哈希和 `requiresKimi=false`，再运行公开包自检；任一项失败都不得记为已发布。`--check` 只核查已有产物，不执行公开发布。

公开 README 以 `anran_product_repair_20261117/README.template.md` 为输入，由统一发布器把 `{{ANRAN_VERSION}}` 替换为当前产品版本；完整 Agent 安装指令只维护在 `anran_product_repair_20261117/public-install.json`，README 的 `{{ANRAN_AGENT_PROMPT}}` 与官网 `src/public-install.json` 都由它生成。官网构建、发布器检查和真实浏览器复制均须核对同一段文字，禁止在任一渠道单独改提示词。只修正文档时使用 `--publish-docs`，它只允许 README 改动、更新主分支并保持已测试运行器标签不变；随后仍需完成本机插件同步与多端回读，不手工提交 GitHub。

回读原生生产文件、插件源包、稳定安装目录和其他 Agent 的真实连接，核对资产哈希与加载版本。任一端不一致都使发布失败并列出阻塞；随后才能做真实桌面或宿主交互验收。旧手工 ZIP、手工提交 GitHub 和独立 MCP 安装流程不再作为发布或用户主路线。

## 测试副本

只有明确要求隔离测试时才运行 `stage --preview`。创建后立即运行 `record-preview`；验收后先用 `Widget.delete --preview` 核对影响，只删除台账登记的实例，回读不存在后运行 `confirm-cleanup`，最终 `pending` 必须为 `no_pending_previews`。失败也保留并报告 `cleanup_required`，不删除正式实例。

## 出现问题时

- 暂存目录非空或页面已有用户修改：停止覆盖并报告冲突。
- 插件目录无法定位：从已加载技能位置重新解析，不猜固定路径。
- 运行器缺失、配置重复、保存或连接失败：非零退出或保留错误状态，明确说明哪一步未完成。
- 安装或配置写入失败：恢复旧配置与旧 `current`，报告回读结果。
- 官方接口要求重启：如实报告，不擅自重启。
- 真实窗口、输入或播放未观察：明确列为未验收。

## 内容边界

角色身份、配色、动作与当前资产属于安燃项目。本技能负责统一分发、安装和连接，不包含通用桌宠制作方法，也不要求用户安装 `pet-plus`。本工具型技能的宿主与动作由用户指令决定，无需额外构思澄清；对象不明或会覆盖用户修改时才停止澄清。
