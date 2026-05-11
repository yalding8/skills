# _feishu-core — 飞书 skills 共享库

> ⚠️ **这不是一个独立的 skill**，目录前缀 `_` 是为了避免被 skill 系统识别。

## 用途

为所有 `feishu-*` skills 提供共享代码：
- 凭证管理（`~/.config/feishu/credentials.json`）
- Token 缓存（`~/.cache/feishu/token.json`，自动续期）
- HTTP / multipart 工具
- 带认证的请求封装（token 过期自动重试）
- 通用 API（云空间上传、Wiki 列表等）

## 使用方法

在 skill 的 Python 脚本里：

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "_feishu-core"))
import feishu_lib as fs

# 业务代码
token = fs.get_tenant_token()              # 带缓存
fs.upload_file("/path/to/file.md", root)   # 通用上传
fs.authed_request(url, method="POST", data={...})  # 自动带 token
```

## 文件布局规范

```
~/.config/feishu/
├── credentials.json        # 全局凭证（共享）
├── wiki.json               # feishu-wiki 业务配置
├── bitable.json            # feishu-bitable 业务配置
└── bot.json                # feishu-bot 业务配置

~/.cache/feishu/
└── token.json              # tenant_access_token 缓存

~/.claude/skills/
├── _feishu-core/           # 本目录
└── feishu-*/               # 各业务 skill
```

## 新增 feishu-* skill 时的清单

1. `~/.claude/skills/feishu-<name>/SKILL.md` —— 触发关键词、setup 文档、推送流程
2. `~/.claude/skills/feishu-<name>/<script>.py` —— 业务逻辑，import `feishu_lib`
3. 在脚本里加 `--init-<name>` 子命令保存业务配置（调用 `fs.save_business_config("<name>", {...})`）
4. 飞书开放平台为同一个 App 申请该业务需要的额外权限（已发布的 App 改权限要重新发布版本）

## 现有 skills

- `feishu-wiki` — md 推到 Wiki 知识库（已实现）
