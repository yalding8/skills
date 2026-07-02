# Skills 仓库项目盘点报告

- **日期**: 2026-07-02
- **范围**: `~/Projects/skills` 全仓库(147 个 skill + 1 个共享库),对照同步源 `~/.claude/skills/`(137)+ `~/.claude/commands/`(16)
- **可信度声明**: 本报告由 AI 生成。所有数字均通过实际命令(`ls`/`diff`/`comm`/`grep`/`stat`)当场验证,标注 `[已核实]`;无估算数字。最终责任人为项目负责人,本报告仅供参考。

---

## 一、总体规模 `[已核实]`

| 指标 | 数值 | 验证方式 |
|---|---|---|
| 仓库 skill 目录 | 148 个(147 skill + `_feishu-core` 共享库) | `ls -d */ \| wc -l` |
| 仓库体积 | 25 MB(最大 `lark-slides/` 5 MB) | `du -sh` |
| 同步源技能 | skills 137 + commands 16 = 153 | `ls ~/.claude/{skills,commands}` |
| 最后提交 | 2026-06-19(距盘点日 13 天) | `git log -1` |
| 工作区状态 | 干净,无未提交改动 | `git status` |

## 二、发现清单

### F1 · 4 个新 skill 未同步进仓库 — 中 · ✅ 已修 `[已核实]`

源目录里存在、仓库缺失,且创建时间均晚于最后一次同步(06-19):

| Skill | 安装日期 |
|---|---|
| `guizang-ppt-skill` | 2026-06-29 |
| `kubo-deploy-e2e` | 2026-07-01 |
| `kubo-publish-e2e` | 2026-07-01 |
| `publish-artifact` | 2026-07-01 |

验证:`comm -23 <(源清单) <(仓库清单)` + `stat -f '%SB'`。
另有 `~/.claude/skills/learned/` 为 2026-03-09 遗留**空目录**(0 个文件),属良性,建议顺手删除。

**修复**:已随 commit `f85d1ff`(2026-07-02)同步进仓库;`learned` 空目录已删除。

### F2 · README 只收录 88/147 个技能,59 个无入口 — 高 · ✅ 已修 `[已核实]`

README 标称"88 个技能,9 大分类",实际仓库 147 个。缺口 59 个,按族群:

- **lark-\*** 27 个(lark-base / lark-doc / lark-im / lark-sheets …)
- **wecomcli-\*** 12 个
- **Cloudflare 系** 5 个(cloudflare / cloudflare-email-service / durable-objects / workers-best-practices / wrangler)
- **前端补充** 3 个(mobile-design / responsive-design / web-perf / platform-check 计 4 个)
- **其他** 11 个(agents-sdk / baoyu-\*×2 / born-traceable / feishu-wiki / guizang-social-card-skill / insight-report / interview-copilot / miniprogram-development / sandbox-sdk / update-readme)

验证:`comm -23 <(仓库目录) <(README 链接)`,README 链接数 88(中英各一份共 176 条)。
**反向检查:README 无死链**(0 个"README 有但目录不存在")。✅

README 由 `sync-skills.sh` 自动生成 → 已修脚本:分类 9→14(新增 前端工程 / Cloudflare 开发 / 飞书 Lark / 企业微信 WeCom / 业务工作流),63 个新条目补齐中英文描述,技能总数改为动态计算。修复后 README 收录 151/151,验证零死链、零空描述(commit `f85d1ff`)。

### F3 · CLAUDE.md 分类体系与 README 已脱节 — 中 · ✅ 已修 `[已核实]`

项目 CLAUDE.md 原为 8 类旧体系。已回写为与脚本一致的 14 类新体系,并加注"改分类先改脚本再回写本节"。

### F4 · Git 历史噪音:11 条同 message 提交 — 低 · ✅ 已修(根因) `[已核实]`

根因:`sync-skills.sh` 第 552 行 commit message 硬编码为 6-18 重组时的临时文案。已改回规范格式 `Sync skills from ~/.claude/ (日期)`,本次同步提交 `f85d1ff` 已验证生效。历史提交不回改。

### F5 · 内容零漂移 — ✅ 无需修 `[已核实]`

已同步的全部 skill,仓库内 `SKILL.md` 与 `~/.claude/skills/` 源逐一 `diff`,**0 个不一致**。
除 `_feishu-core`(共享库,预期无入口)外,148 个目录全部有 `SKILL.md`。

## 三、修复状态跟踪表

| # | 发现 | 严重度 | 状态 | 动作 |
|---|---|---|---|---|
| F1 | 4 个新 skill 未同步 | 中 | ✅ 已修 | commit `f85d1ff`,`learned` 空目录已删 |
| F2 | 59 个技能不在 README | 高 | ✅ 已修 | 脚本分类 9→14,151/151 收录,零死链 |
| F3 | CLAUDE.md 分类过时 | 中 | ✅ 已修 | 回写 14 类体系并注明维护规则 |
| F4 | 提交 message 不规范 | 低 | ✅ 已修根因 | 脚本 message 改回规范格式,历史不回改 |
| F5 | 内容漂移 | — | ✅ 零漂移 | 无 |

## 四、下一步行动项

全部发现已于 2026-07-02 当天闭环(F1–F4 ✅,F5 本无问题)。遗留观察项:
1. 下次安装新 skill 后,`sync-skills.sh` 的 `cn_desc`/`en_desc` 需要补对应条目,否则回退到 frontmatter 英文截断(`head -c 120` 有多字节截断风险)——新增 skill 时顺手补描述。
2. 新增分类时,需同时改脚本数组、`NUM_CATEGORIES`、CLAUDE.md 三处。

---

*最终责任人: 项目负责人(AI 报告仅供参考,不构成专业审计意见)*
