# Operational Domains

SCE-88 operates across four isolated domains.
Each domain implements the full 22-level stack independently.

## Domain A — Physical / Substrate
Primary emphasis:
- Levels 1–5, 15
Handles physics, timing, actuation, and environment limits.

## Domain B — Control / Computational
Primary emphasis:
- Levels 6–12, 16
Handles execution, correction, and runtime coordination.

## Domain C — Semantic / Interface
Primary emphasis:
- Levels 17–18
Handles representation, abstraction, and human alignment.

## Domain D — Temporal / Evolutionary
Primary emphasis:
- Levels 18, 20–22
Handles learning persistence, upgrades, and continuity over time.

Domains do not share internal state.
All cross-domain interaction is explicitly gated.

---
