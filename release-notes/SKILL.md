---
name: release-notes
description: Release notes for Transito's Play Store and App Store, drafted from the commits between two Git refs. Use when the user asks for store, Play Store, App Store, or release notes.
---

# Release notes

Create a **store draft**: release notes that tell an everyday app user what they will notice. This skill drafts only; the user publishes.

## 1. Set the release range

1. Take `from` and `to` from the user; `to` defaults to `HEAD`.
2. Without `from`, use the latest version tag reachable before `to` (`git describe --tags --abbrev=0 <to>^`); with no tag, ask the user for the start ref.
3. Run `git log --reverse <from>..<to>` on the resolved refs.

Completion: a non-empty Git range, stated in the output.

## 2. Build the user-change inventory

1. Read every commit subject and body. Fold related commits into one change.
2. Open the diff for any commit whose user impact is unclear (UI, routing, API, data, settings).
3. Keep changes a user can *notice*: new capability, changed behaviour, material polish, accessibility, reliability, a specific bug fix.
4. Drop refactors, formatting, tests, CI, version bumps, dependency-only work, and implementation detail unless the diff proves a user-visible effect.
5. Keep a change only when its benefit shows up in the diff; weak evidence is omitted.
6. Tag each change `both`, `android`, or `ios` by the platform code it touches.

Completion: every kept change has a concrete user-facing claim, its supporting commits, and a platform tag.

## 3. Write the store draft

Write in the house style, distilled from every note published on both stores (2.1.0 to 5.3.0).

**Section anatomy.** A note is a stack of sections: title line, one or two sentences, blank line between sections.

- **Title**: 2-5 words naming the benefit or feature the user will notice ("Better favourites", "Steady Navigation"). Sentence case, no trailing punctuation.
- **Body**: the outcome in plain words, second person ("You can now...", "Give stops your own names..."). One sentence is the norm; two is the ceiling.
- **Count and order**: 2-4 sections, headline feature first, polish next, `Bug fixes` last. The 5.x releases settled on 3.
- **Voice**: British spelling (favourites, personalised, colour), warm and plain.
- **Patch release** (x.y.1, one small fix): a single plain line, no title (`Removed LTA system maintenance alert`).

**Android emoji.** One emoji leads each title, then a space. It defaults to the section's kind: ✨ new feature, ⚡ enhancement, 🐞 bug fix. A topic emoji replaces the default when it names the section better to a stranger at a glance (past picks: 🚌 buses, 🗺️ maps, 🔍 search, 🚨 alerts, 📍 location, 🎨 theming, 👋 onboarding, ⭐ favourites).

**iOS.** The Android sections with the emoji removed, in ASCII (straight quotes, `-` for dashes); titles and bodies match Android word for word.

**Platform-only changes.** A change that lands on one platform is written for that platform alone: `Fixed location prompts` (Android 5.1.0) and `"Sign in with Apple" fixes` (iOS 5.2.0) each sit in their own store's notes.

Example, Android then iOS (shared sections stay word-identical):

```text
⭐ Better favourites
Give stops your own names, collapse cards to reduce clutter, and keep everything organised.

🗺️ Updated MRT Map
The Circle Line is finally a circle!

👋 A friendlier welcome
The refreshed Quick Start tour makes it easier to get familiar with the app.
```

```text
Better favourites
Give stops your own names, collapse cards to reduce clutter, and keep everything organised.

Updated MRT Map
The Circle Line is finally a circle!

A friendlier welcome
The refreshed Quick Start tour makes it easier to get familiar with the app.
```

Then build the output:

```text
Release range: <from>..<to>

Android — Google Play (≤500 characters)
<copy-ready release notes>
Characters: <count>

iOS — App Store (≤4,000 characters; ASCII)
<copy-ready release notes>
Characters: <count>

Evidence
- <short commit> — <why it supports the included change>
```

Count Unicode characters of each draft body (label and count line excluded). When Android exceeds 500, tighten sentences before dropping a headline change. Check the iOS draft is ASCII (U+0020 to U+007E plus line breaks) before returning it.

Completion: both drafts fit their limits, the iOS draft is ASCII, every section follows the section anatomy, and each section appears under Evidence.
