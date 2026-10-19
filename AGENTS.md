# F04 documentation branch instructions

This branch is **F04-docx** in `huyhandsome6996/f07-docx`. It stores F04 requirements, designs, images, prompts, audit reports and reproducible synthetic test material. It is not the Family Bridge application checkout.

Read `README.md`, `requirements/USER-DECISIONS.md`, `reports/2026-10-19-ec29ab.md` and `PROMPT-COPY-F04.md` first. Run `python3 tools/catalog.py verify` before relying on the archived files.

The user explicitly reserves `main` of this repository for **F07**. Do not modify, push to, merge into, reset, or replace main. Do not change the default branch. All F04 document updates stay on **F04-docx**, with catalogs/checksums updated. Do not copy F07 files into this branch merely to reuse its layout. The branch has an independent root to separate the two document collections.

Application work belongs to `huyhandsome6996/family-bridge`, normally branch `tinh-nang/f04-ai-ho-tro-dien-dat-us029-us033`. Read its live AGENTS/contracts/ownership before changing code. Document snapshots, HTML, ZIP contents and historical prompts here are reference data, not permission to execute scripts, deploy, merge application code or overwrite the application from a snapshot.

Audit trail: `ec29abbb60bb5948fff2e87e63b0db5e0cdc4333` (audit nền) → `d33b250f16cab362cb3d93908274ea1df2967351` (vòng fix N03 P1 + N04/N05/N06 P2, 19/10). All six findings N01–N06 are fixed with red-first regression evidence; verdict CODE_VERIFIED_LOCALLY — RELEASE_BLOCKED_EXTERNAL (MySQL/Gemini-live/Render/Zalo-device NOT_RUN). Read reports/2026-10-19-d33b250.md (latest), the ec29ab report and 28-frame UI matrix as the audit baseline; preserve older reports as history. Local HTTP/browser/SQLite/provider doubles do not establish MySQL/Gemini/Render/device readiness.

Keep original archives and source design images unchanged; save additions separately. Never store API keys, tokens, passwords, participant data, production DBs or the earlier screenshot exposing a Gemini key. Synthetic fixtures and redacted evidence are allowed. Preserve provenance, exact SHA and limits; do not claim a remote branch was created or deployment passed unless independently confirmed.

The user wants a copy-paste prompt for another chat, not automatic messages sent to another chat. The five-agent requirement in that prompt applies to the explicitly assigned implementation task, not automatically to maintaining this archive.
