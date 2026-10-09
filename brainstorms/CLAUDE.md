# brainstorms/ — automatic entry point (dev writes TODOs only)

This is the **single entry point for the dev**. The dev does NOT hand-write design/spec/code.
The dev only:

1. Creates/opens a `<slug>.md` file in this folder.
2. Adds ideas as **TODO** items under `## TODO (dev)`.

The AI runs **everything else automatically**.

## Edit scope (user ↔ AI)

- User prompts **only** create/edit files inside `brainstorms/`. Every other directory
  (`designs/`, `openspec/`, `code/`, `.claude/`, `README.md`…) is **read-only to
  the user** or **AI-generated/owned** — the user does not edit it directly; the AI produces
  it through the pipeline.

## Brainstorm file structure (required)

```markdown
## TODO (dev)
- [ ] <task / idea the dev wants done>
- [ ] ...

## Summary (AI)
<!-- The AI writes/updates this block RIGHT BELOW the TODO section. The dev does not edit it by hand. -->
```

- The dev only touches `## TODO (dev)`. The `## Summary (AI)` block is owned by the AI.
- An unchecked TODO = the AI picks it up; the AI checks `[x]` once it has run the whole
  pipeline for that item.

## What the AI does automatically

When it sees an unprocessed TODO (unchecked, not yet in Summary), it runs the whole pipeline
**end to end**, WITHOUT stopping to ask between phases (continuous execution). Order:

```
brainstorm(TODO) → design → openspecs(spec) → code → review
```

1. **design** → create `../designs/<slug>.md`: approach, file/module boundary, data model, task plan.
2. **openspecs (spec)** → `/opsx:propose "<slug>"`: generate `openspec/changes/<slug>/` (proposal + specs + design + tasks).
3. **code** → implement under `../code/<slug>/` using **TDD** (write tests, watch them fail red, then make them green).
4. **review** → run `/code-review` + the tests; fix all CRITICAL/HIGH before reporting back to the dev.

After each item: check `[x]` that TODO and update the **Summary** with links + per-phase status.

## Summary block — format

| TODO | design | openspecs | code | review | status |
|---|---|---|---|---|---|
| <todo summary> | `../designs/<f>.md` | `openspec/changes/<slug>/` | `../code/<slug>/` | tests ✓ / findings | done / in-progress / blocked |

## One session = one topic file

- Each session **works on exactly 1 topic file** in `brainstorms/` (e.g. `setup.md`). Do not
  switch to another topic mid-session; a different topic → a new session.
- **Session name = topic file name** (e.g. file `setup.md` → session named `setup`). Claude
  Code does not support auto-renaming a session from an agent/hook, so: at the start of each
  session the AI **identifies the topic file and prompts** for the rename; the user types
  `/rename <slug>` (or starts with `claude -n <slug>`).

## Review loop (every new prompt)

The session runs as a loop: session start → user prompt → next prompt → **loop**.

- On every new prompt: **go back to the top of the loop and review the overall existing
  idea / plan / design FIRST**, then proceed — do not jump straight into execute.
- Reconcile the new prompt against the whole current brainstorm/design picture; if it drifts
  or conflicts → make it consistent (update the relevant TODO/Summary) before running the pipeline.

## Safety rules

- Ambiguous TODO (affecting scope/behavior/acceptance) → record an **assumption** in the design
  + one line in the Summary (`assumption: ...`) and keep going. Only **stop to ask the dev**
  when the ambiguity is truly blocking.
- TODO touching real product code (outside the `code/` demo) → stop, ask first (RED).
- Always TDD: never write code before there is a failing (red) test.
