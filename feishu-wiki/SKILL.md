---
name: feishu-wiki
description: 把本地 Markdown 文档推送到飞书知识库（Wiki），自动转换为飞书 Docs 格式。当用户说"推到飞书"、"发飞书 wiki"、"推到知识库"、"feishu wiki"、"把这份 md 推上去"、"把刚才生成的报告推到飞书"等需要将本地 .md 文件同步到飞书 Wiki 的场景时触发。skill 会自动找当前会话最近编辑的 md 文件，让用户确认后调 push.py 上传并转换。首次使用会引导从零创建飞书自建应用，凭证由所有 feishu-* skills 共享。
metadata:
  requires:
    bins: ["python3"]
  scriptPath: "~/.claude/skills/feishu-wiki/push.py"
  sharedLib: "~/.claude/skills/_feishu-core/feishu_lib.py"
  configPaths:
    credentials: "~/.config/feishu/credentials.json"  # 共享，所有 feishu-* skills 复用
    business: "~/.config/feishu/wiki.json"             # 仅本 skill
  cachePath: "~/.cache/feishu/token.json"
---

# 飞书知识库推送 (feishu-wiki)

把当前会话生成的 Markdown 文档推送到飞书 Wiki，自动转换为可在线协作的飞书 Docs。

> ⚠️ **限制：md 导入不携带本地图片/附件。** 飞书 `import_tasks` 只转文本结构，md 里 `![](本地图.png)` 这类**本地引用的图片不会被上传**，推上去的文档没有图。**要在 Wiki 文档里放长图（视觉报告长截图）或 PDF 附件**，两条路：
> 1. `python3 push.py --embed <wiki_url> --image <png> [--file <pdf>]` —— 程序化插入图片块/文件块到文档顶部。**需应用开通 `docx:document` 用户权限**（先跑 `--status` 看「图片嵌入」预检行）。
> 2. 在飞书界面**手动把长图/PDF 拖进文档**（无需任何权限，最稳）。

## 架构（重要：与未来 feishu-* skills 共享凭证）

```
~/.config/feishu/
├── credentials.json        # 共享：{app_id, app_secret} —— 所有 feishu-* skill 共用
└── wiki.json               # 仅本 skill：{wiki_space_id}

~/.cache/feishu/
└── token.json              # tenant_access_token 缓存（自动续期，多 skill 共享）

~/.claude/skills/
├── _feishu-core/           # 共享代码库（被 push.py import）
└── feishu-wiki/            # 本 skill
```

**含义**：未来加 `feishu-bitable` / `feishu-bot` 时，**App ID/Secret 只需配一次**，每个 skill 只补自己的业务字段（如 bitable 的 app_token、bot 的 chat_id）。

## 工作流总览

```
触发 skill
  ↓
查 setup 状态: python3 push.py --status
  ↓
┌────────────────────────────────────────────┐
│ 凭证 ✗  →  走「凭证 setup」（Step 1-3）    │
│ 业务 ✗  →  走「Wiki 业务 setup」（Step 4-6）│
│ 全 ✓    →  走「推送流程」                  │
└────────────────────────────────────────────┘
```

---

## 推送流程（已配置后的常规调用）

### 1. 找候选 md 文件

按 mtime 倒序在当前 cwd 列出最近 5 个 md，**排除常见噪音目录**：

```bash
find . -type f \( -name "*.md" -o -name "*.markdown" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" \
  -not -path "*/.next/*" \
  -not -path "*/.venv/*" \
  -exec ls -lt {} + 2>/dev/null | head -5
```

### 2. 让用户选

如果当前会话刚生成或修改过某个 md（从对话上下文中可见），把它作为「推荐选项」高亮列出，其他作为备选。

如果用户已经在指令里指明了路径（如 "推 docs/report.md"），跳过选择直接用。

### 3. 推送

```bash
python3 ~/.claude/skills/feishu-wiki/push.py <md_path>
```

- stdout：飞书文档 URL
- stderr：进度日志

成功示例：
```
→ 推送 报告.md 到 Wiki space 7xxxxx...
  ✓ 已上传到云空间，file_token=boxcnxxxx...
  ✓ 创建导入任务 ticket=7yyyyyy
  任务状态: 1
  任务状态: 2
  任务状态: 0

✅ 推送完成
https://xxx.feishu.cn/wiki/yyyyyy
```

把 URL 直接展示给用户。

---

## 凭证 Setup（Step 1-3，仅首次配置 / 与所有 feishu-* skills 共享）

> **如果之前已经为其他 feishu-* skill 配过凭证（`~/.config/feishu/credentials.json` 存在），直接跳到 Step 4。**

### Step 1: 创建自建应用

引导用户：

1. 打开 https://open.feishu.cn/app
2. 点「创建企业自建应用」
3. 应用名称建议：`md-tools`（通用名，因为这套凭证后续会给多个 skill 用）
4. 上传一个图标
5. 创建后进入应用详情页，记下「凭证与基础信息」标签里的 **App ID** 和 **App Secret**

让用户回复 App ID 和 App Secret。

### Step 2: 申请权限

进入「权限管理」标签 → 搜索并开通：

**当前 feishu-wiki 必需**：
- `drive:drive` —— 云空间访问
- `drive:file:upload` —— 文件上传
- `wiki:wiki` —— 知识库读写
- `docx:document` —— 文档读写

**给未来其他 skill 预留**（**强烈建议一并申请**，避免后面改权限要重新发版）：
- `bitable:app` —— 多维表格（用户已规划做 feishu-bitable）
- `im:message` —— 发消息（如果未来要做 bot）
- `im:chat` —— 群聊操作（同上）

### Step 3: 创建版本并发布

「版本管理与发布」标签：

1. 创建版本（版本号 `1.0.0` 之类）
2. 可用范围选「全部成员」或自己
3. 提交申请
4. 个人版/试用版立即生效；企业版需管理员审批

让用户确认「应用状态：已发布」后，写入凭证：

```bash
python3 ~/.claude/skills/feishu-wiki/push.py --init-credentials <app_id> <app_secret>
```

`--init-credentials` 会自动验证 token 能拿到。失败的话回 Step 1-3 排查。

---

## Wiki 业务 Setup（Step 4-6，每个 skill 各做一次）

### Step 4: 把应用加为 Wiki 协作者

> ⚠️ **这一步飞书没有 API 能做**，必须在 Wiki 界面手动加。

引导用户：

1. 飞书里打开目标 Wiki 知识库的首页
2. 右上角「设置」→「成员管理」/「协作者管理」
3. 「添加成员」→ 切到「应用」标签 → 搜索 Step 1 创建的应用名 → 选「可管理」或「可编辑」
4. 确认应用出现在协作者列表里

### Step 5: 获取 Wiki space_id

让用户在浏览器打开目标 Wiki 首页，URL 里就有：

```
https://xxxx.feishu.cn/wiki/space/7123456789012345678
                                  ^^^^^^^^^^^^^^^^^^^
                                  这串数字
```

如果只看到节点 URL（`https://xxxx.feishu.cn/wiki/RandomToken`），让用户点 Wiki 左上角「知识库名」回到首页。

或者**直接让脚本列出来**（前提是 Step 4 已完成）：

```bash
python3 ~/.claude/skills/feishu-wiki/push.py --list-wikis
```

输出格式：`<space_id>\t<name>\t<type>`，让用户从中选一个。

### Step 6: 写入业务配置

```bash
python3 ~/.claude/skills/feishu-wiki/push.py --init-wiki <wiki_space_id>
```

会自动验证 wiki 在可访问列表里。**通过即配置完成**。

---

## 常见错误排障

| 错误 | 原因 | 解决 |
|---|---|---|
| `获取 tenant_access_token 失败` | app_id/app_secret 错或应用未发布 | 回 Step 1-3 复核，或运行 `--init-credentials` 重写 |
| `获取个人云空间根目录失败` | 缺 drive 权限 | 检查 Step 2 的 drive 权限，重新发版 |
| `wiki_space_id ... 不在可访问列表里` | 应用未加为 Wiki 协作者 / space_id 写错 | 跑 `--list-wikis` 看真实可访问空间，对照 Step 4-5 |
| `创建导入任务失败` | 缺 wiki 写权限 | 检查 Step 2 的 `wiki:wiki` 权限 |
| `导入失败: error=...` | md 含飞书不支持的语法（罕见） | 检查 md 的畸形 HTML / 特殊嵌入 |

---

## 工具命令速查

```bash
# 查 setup 状态（先跑这个判断走哪一段流程）
python3 ~/.claude/skills/feishu-wiki/push.py --status

# 推送
python3 ~/.claude/skills/feishu-wiki/push.py <md_path>

# 完整验证
python3 ~/.claude/skills/feishu-wiki/push.py --verify

# 列出可访问的 Wiki 空间
python3 ~/.claude/skills/feishu-wiki/push.py --list-wikis

# 删除 Wiki 节点（换版删旧用，移入回收站可恢复）
python3 ~/.claude/skills/feishu-wiki/push.py --delete <wiki_url|token>

# 把长图/PDF 嵌进已存在的 Wiki 文档顶部（md 导入不带图，要图用这个）
# 需 docx:document 用户权限；缺权限会优雅降级给出开通指引（退出码 2）
python3 ~/.claude/skills/feishu-wiki/push.py --embed <wiki_url|token> --image <png> [--file <pdf>]

# 写共享凭证（首次）
python3 ~/.claude/skills/feishu-wiki/push.py --init-credentials <app_id> <app_secret>

# 写 wiki 业务配置
python3 ~/.claude/skills/feishu-wiki/push.py --init-wiki <wiki_space_id>
```

## 注意事项

1. **配置文件权限自动设为 0600**，凭证不会泄露到其他用户
2. **凭证变更时 token 缓存自动清除**（save_credentials 会清缓存）
3. **md 上传到云空间根后保留**，飞书会留原始文件便于回溯
4. **导入是异步任务**，飞书后端处理 5-30 秒，poll 最多等 180 秒
5. **mount_type=1 挂到 Wiki 根**——`import_tasks` 接口不支持指定父节点，新文档在 Wiki 顶层。需要分类让用户在飞书界面拖
6. **重复推送同名 md 会建新文档**（飞书 Wiki 没"按 title 替换"语义）。**换版流程 = 推新 → `--delete <旧 wiki_url>` 删旧 → 验证**：`--delete` 用 OAuth 用户身份 token 删自己创建的文档（取 node 的 obj_token → drive 文件删除 → 移入回收站可恢复），无需人工进飞书 UI。注意 user_token 删的是**自己创建**的文档；删非本人文档可能无权限
7. **共享凭证场景**：未来加 feishu-bitable 时，复用 `~/.config/feishu/credentials.json` 即可，setup 流程会自动跳过 Step 1-3
8. **`--embed` 把视觉报告放进文档**：流程是「解析 wiki node → 取 docx obj_token → 文档顶部插图片块(block_type 27)/文件块(23) → 上传媒体绑到块 → PATCH 回填 token」。**前提是该 wiki 节点本身是 docx 文档**（非 docx 节点会报错）。`--embed` 操作的是**已存在**的文档——典型用法是先 `push.py <md>` 推出文档，再 `--embed <返回的 wiki_url> --image 长图.png`。缺 `docx:document` 用户权限时不会糊 traceback，而是打印「开权限 → 重新发版 → 重新 `--login`」三步指引并以退出码 2 退出。`--status` 的「图片嵌入」行会提前告诉你这个能力是否就绪。
