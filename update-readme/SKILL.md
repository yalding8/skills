---
name: update-readme
description: Update README.md to reflect recent code changes, keeping existing format intact. Scans git history and changed files to identify what needs documenting — new features, API changes, env vars, deployment updates. Use when user says "更新readme", "update readme", "同步readme", after completing a feature module, or when asked to document changes in README.
---

# Update README

## Workflow

### 1. Understand what changed
```bash
git log --oneline -20
git diff HEAD~5..HEAD --stat
git status
```

### 2. Read current README
- Read the full README.md
- Note existing sections and format style

### 3. Identify what needs updating
Check these areas based on recent commits:

| Area | Triggers |
|------|----------|
| Installation | new deps, env vars added, Docker changes |
| Usage / Quick Start | new CLI flags, new commands, workflow changes |
| API | new endpoints, changed request/response shapes |
| Architecture | new services, containers, infra changes |
| Environment Variables | new `.env` keys required |
| Deployment | CI/CD, Docker compose, nginx changes |
| Features | new user-facing functionality |

### 4. Update README
- **Keep existing format and structure** — do not restructure sections
- Add new env vars to the env table (or create one if missing)
- Add new API endpoints to the API section
- Update version numbers if relevant
- Mark deprecated items clearly

### 5. Output summary
After updating, output:
```
## README 更新完成

**更新了哪些内容：**
- [ ] 新功能：...
- [ ] 环境变量：新增 `VAR_NAME`
- [ ] API：新增 `POST /endpoint`
- [ ] 部署：...

**未变动章节：** Installation / Architecture / ...
```

## Rules

- Never rewrite or restructure existing sections — only append or update
- If a section doesn't exist yet and is needed, add it at the end
- Keep language consistent with existing README (中文/英文)
- Do not add sections for things that didn't change
- Env vars must match exactly what's in `.env.example` or `docker-compose.yml`
- If unsure about a change, note it as a comment rather than silently omitting
