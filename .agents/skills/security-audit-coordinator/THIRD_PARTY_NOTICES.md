# License and provenance

Copyright 2026 security-lifecycle contributors. Original contributions are
licensed under [Apache-2.0](LICENSE).

The workflow and domain references are an original condensed synthesis informed
by [Cloudflare security-audit](https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit),
commit `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`, retrieved and license-checked
2026-09-19. Copyright (c) 2025-2026 Cloudflare, Inc.; source licensed MIT.
The [full permission and disclaimer](licenses/Cloudflare-MIT.txt) travels with
this independently installable skill.

Reused topics: coverage-led reconnaissance, bounded hunter assignments, fresh
adversarial verification, stable finding states, additive reruns, explicit
budgets, sandboxed local checks and domain-specific attack-surface selection.

Changes: rewritten as a smaller agent-neutral coordinator; preserved static
evidence as a valid confirmation method; replaced Node.js validators with one
Python-standard-library structural validator; removed fleet ingestion and any
dependency on another installed skill; consolidated attack classes into five
conditional concept references; kept source changes outside audit authorization.
No source implementation, schema or prompt block was copied verbatim.

Preserve this attribution and the bundled MIT text when redistributing the skill.
Cloudflare does not endorse this project.
