# License and provenance

Copyright 2026 security-lifecycle contributors. Licensed under [Apache-2.0](LICENSE).

Modified synthesis of [OpenAI security-best-practices](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/security-best-practices).
Source commit: `49f948faa9258a0c61caceaf225e179651397431`.
Source and [skill-local license](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/security-best-practices/LICENSE.txt)
checked on 2026-09-12. No relevant upstream NOTICE file exists in this skill.

Secure construction, runtime validation, identity and resource access, safe rendering,
query handling, sensitive output, deployment context and selective documentation.
The original language/framework references were rewritten into five surface-based
references; audit/reporting overlap was removed.

Instructions and examples are original rewrites, not verbatim upstream copies.
Preserve this attribution and the bundled license when redistributing the skill.

## Extended security surfaces

The identity-protocol, distributed-lifecycle, native/local, release/cloud, browser
and general AI additions are an original implementation synthesis informed by
[Cloudflare security-audit](https://github.com/cloudflare/security-audit-skill/tree/c1c8a8c1471069fb0e188eeaff69b8e8db6564a8/skills/security-audit),
commit `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`, checked 2026-09-19.
Copyright (c) 2025-2026 Cloudflare, Inc.; source MIT license preserved in
[full](licenses/Cloudflare-MIT.txt). Attack classes were rewritten as secure
construction and verification guidance; no source prompt was copied verbatim.

## Agent and tool sources

Modified original synthesis, checked 2026-09-12:

- [MCP security best practices, 2026-07-28](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/aa8ce049f089f92618340190d4ece141f663310d/docs/docs/2026-07-28/tutorials/security/security_best_practices.mdx),
  SHA `aa8ce049f089f92618340190d4ece141f663310d`, with related authorization,
  transport and tools specification sections. Copyright (c) 2024-2025 Model
  Context Protocol a Series of LF Projects, LLC. Documentation: CC-BY-4.0;
  specification contributions: Apache-2.0 or retained MIT as described by the
  [full source licensing notice](licenses/MCP-LICENSE.txt).
- [WebMCP security questionnaire](https://github.com/webmachinelearning/webmcp/blob/97da8f515427594c856307e3476c0a0db9698fbb/security-privacy-questionnaire.md)
  and index.bs security/privacy discussion, SHA
  `97da8f515427594c856307e3476c0a0db9698fbb`.
  [Source declaration](licenses/WebMCP-LICENSE.txt);
  [W3C Software and Document License, full terms](licenses/W3C-SOFTWARE-DOCUMENT.txt).

Reused topics: tool authority, recipient/scope/session binding, untrusted tool
content, information disclosure, browser origins and consequential actions.
Changes: concise phase-specific guidance, no copied implementation, clear
separation of protocol requirements, application recommendations and unverified
browser behavior. No separate upstream NOTICE files were found.

This document includes material derived from WebMCP Security and Privacy.
Copyright © 2026 World Wide Web Consortium and WebMCP Contributors. All Rights
Reserved. Distributed under the W3C Software and Document License, WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. Preserve the bundled terms and attribution.
