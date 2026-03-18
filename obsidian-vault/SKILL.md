---
name: obsidian-vault
description: Search, create, and manage notes in the Obsidian vault with wikilinks and index notes. Use when user wants to find, create, or organize notes in Obsidian.
---

# Obsidian Vault

## Vault location

`/Users/ningding/Documents/Obsidian Vault.nosync/`

Mostly flat at root level.

## Naming conventions

- **Index notes**: aggregate related topics (e.g., `Skills Index.md`, `RAG Index.md`)
- **Title case** for all note names
- No folders for organization - use links and index notes instead

## Linking

- Use Obsidian `[[wikilinks]]` syntax: `[[Note Title]]`
- Notes link to dependencies/related notes at the bottom
- Index notes are just lists of `[[wikilinks]]`

## Workflows

### Search for notes

Use Glob/Grep tools directly on the vault path:

```
Glob: /Users/ningding/Documents/Obsidian Vault.nosync/**/*.md
Grep: pattern in /Users/ningding/Documents/Obsidian Vault.nosync/
```

### Create a new note

1. Use **Title Case** for filename
2. Write content as a unit of learning
3. Add `[[wikilinks]]` to related notes at the bottom
4. If part of a numbered sequence, use the hierarchical numbering scheme

### Find related notes

Search for `[[Note Title]]` across the vault to find backlinks.

### Find index notes

Search for files with "Index" in the name.
