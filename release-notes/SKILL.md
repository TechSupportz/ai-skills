---
name: release-notes
description: Draft Android and iOS release notes from the user-facing changes between two Git refs. Use when the user asks for app-store, Play Store, App Store, or release notes based on commits.
---

# Release notes

Create a **store draft**: concise, accurate release notes that explain what users will notice. This skill drafts only; it never edits a store listing or publishes a release.

## 1. Set the release range

1. Use the supplied `from` and `to` Git refs. Default `to` to `HEAD`.
2. If `from` is omitted, use the latest reachable version tag before `to` (`git describe --tags --abbrev=0 <to>^`). If no such tag exists, ask the user for the start ref.
3. Confirm both refs resolve and inspect the exact range with `git log --reverse <from>..<to>`.

Completion: the draft is based on a non-empty, explicitly stated Git range.

## 2. Build the user-change inventory

1. Read every commit subject and body in the range. Group related commits into one change.
2. Inspect the diff for commits whose user impact is ambiguous, especially UI, routing, API, data, or settings changes.
3. Include only changes a user can notice: new capability, changed behaviour, material polish, accessibility, reliability, or a specific bug fix.
4. Exclude refactors, formatting, tests, CI, version bumps, dependency-only work, and implementation details unless the diff proves a user-visible effect.
5. Do not invent a benefit. When evidence is weak, omit the change rather than rephrase a commit message as a promise.

Completion: every included bullet has a concrete user-facing claim and one or more supporting commits.

## 3. Write the store draft

Use the requested house style. If none is provided, write clear, concise, user-facing prose:

- On Android, use emoji-led headings only when they match the requested house style.
- On iOS, use basic-Latin text only: ASCII letters, digits, standard punctuation, spaces, and line breaks. Do not use emoji or any other non-ASCII character.
- Start each section with a short, human title.
- Follow it with one or two plain-language sentences. Be specific about the outcome, not the implementation.
- Prefer 2–4 sections. Include a bug-fix section only when the range supports it.
- Avoid Markdown headings, commit IDs, developer vocabulary, hype, and a changelog-style list of every internal change.
- Reuse the same user-facing substance for Android and iOS. Diverge only for genuinely platform-specific behaviour or wording.

Produce exactly this structure:

```text
Release range: <from>..<to>

Android — Google Play (≤500 characters; emoji allowed when requested)
<copy-ready release notes>
Characters: <count>

iOS — App Store (≤4,000 characters; basic-Latin only; no emoji)
<copy-ready release notes>
Characters: <count>

Evidence
- <short commit> — <why it supports the included user change>
```

Count Unicode characters in each store draft, excluding the label and character-count line. If the Android draft exceeds 500 characters, tighten descriptions before removing the most important user-facing change. Before returning the iOS draft, verify every character is ASCII (U+0020 through U+007E) or a line break.

Completion: both drafts meet their character limits, the iOS draft contains only permitted characters, neither draft contains an unsupported claim, and the Evidence section accounts for every included section.
