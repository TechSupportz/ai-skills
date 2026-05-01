# emoji-git-commit

A simple skill that drafts concise, emoji-prefixed commit messages

## What it does

- Reads your staged diff
- Picks an emoji prefix based on change type
- Drafts a concise message
- Asks for confirmation (with inline editing) before running `git commit`

## Emoji Guide

| Emoji | Type |
|-------|------|
| ✨ | New feature |
| ⚡ | Enhancement |
| 🐞 | Bug fix |
| 🛠️ | Chore/Misc |
