---
name: emoji-git-commit
description: Drafts concise, emoji-prefixed commit messages and confirms before executing
---

# emoji-git-commit

Instructions for the agent to follow when this skill is activated.

## When to use

Any time the user wants to commit code, or when unstaged/staged changes are present and a commit is implied.

## Instructions

1. Inspect the working tree by running `git status --short`.

2. Stage changes conditionally. If there are unstaged files, default to `git add .` unless you detect red flags such as secrets, `.env` files, unrelated files, or build artifacts. State clearly what you are staging before you do it.

3. Analyze the staged changes by running `git diff --cached`. Understand the actual diff; do not guess.

4. Draft the commit message following these rules:
  - One line.
  - Prefix with an emoji:
    - ✨ = new feature
    - ⚡ = enhancement
    - 🐞 = bug fix
    - 🛠️ = misc / chore
  - For multiple distinct changes, use multiple `-m` flags. Each flag is a separate change, not a paragraph.
    - Example: `git commit -m "✨ Add dark mode toggle" -m "🐞 Fix login redirect"`

5. Confirm with the user. Present the proposed commit exactly as:
  📝 "✨ Add dark mode toggle" | "🐞 Fix login redirect"

  Then prompt for a single response that can be one of three things:
  - **"yes"** → proceed to step 6.
  - **"cancel"** → stop immediately. Do not commit.
  - **Any other text** → treat it as direct edit instructions. Apply the feedback to the draft, then repeat step 5 with the updated message.

  If your environment has a user question/confirmation tool, use it to display the draft and prompt. Do not offer a separate "Edit" option or button; let the user type their change directly.

  If you do not have a confirmation tool, print the exact `git commit` command you intend to run and prompt: `Reply 'yes' to commit, 'cancel' to abort, or tell me how to change the message.`

6. Execute the commit only after receiving an explicit "yes".

## Constraints

- Never auto-commit.
- Never auto-stage secrets, `.env`, or build artifacts.
- If unsure about scope, ask rather than assume.
