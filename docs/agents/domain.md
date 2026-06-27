# Domain Docs

Engineering skills should use this repo's domain documentation before and during code exploration.

## Before Exploring, Read These

- Root `CONTEXT.md`: project context, vocabulary, and important conventions.
- `docs/adr/`: architecture decision records. Read ADRs relevant to the area being changed.

If either location is absent, continue quietly. Do not create missing docs unless the current task actually resolves terms or decisions that should be recorded.

## Layout

This repository is single-context:

```text
/
|-- CONTEXT.md
|-- docs/adr/
|   `-- 0001-placeholder.md
|-- main.py
`-- README.md
```

If this repo later becomes multi-context, add a root `CONTEXT-MAP.md` that points to each context-specific `CONTEXT.md`, and update this file.

## Vocabulary

Use terms from `CONTEXT.md` when naming issues, tests, hypotheses, refactor plans, and implementation concepts.

## ADR Conflicts

If a proposed change contradicts an existing ADR, call that out explicitly instead of silently overriding the decision.
