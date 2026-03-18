---
name: sync-skills
description: Sync all installed skills and commands to GitHub repo yalding8/skills. Run after installing new skills.
user-invokable: true
---

Run the sync script to push all current skills and commands to GitHub:

```bash
bash ~/.claude/scripts/sync-skills.sh
```

Report the result to the user. If it says "No skill changes detected", tell the user everything is already in sync. If it says "Skills synced to GitHub successfully", confirm the sync completed.
