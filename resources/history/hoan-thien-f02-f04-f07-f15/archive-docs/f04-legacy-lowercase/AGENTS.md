# F04 documentation branch instructions

This branch is **f04-docx** in `huyhandsome6996/f07-docx`. It stores F04 requirements, designs, images, prompts, audit reports and reproducible synthetic test material. It is not the Family Bridge application checkout.

Read `README.md`, `requirements/USER-DECISIONS.md`, `reports/2026-10-19-e0ee388.md` and `PROMPT-COPY-F04.md` first. Run `python3 tools/catalog.py verify` before relying on the archived files.

The user explicitly reserves `main` of this repository for **F07**. Do not modify, push to, merge into, reset, or replace main. Do not change the default branch. All F04 document updates stay on **f04-docx**, with catalogs/checksums updated. Do not copy F07 files into this branch merely to reuse its layout. The branch has an independent root to separate the two document collections.

Application work belongs to `huyhandsome6996/family-bridge`, normally branch `tinh-nang/f04-ai-ho-tro-dien-dat-us029-us033`. Read its live AGENTS/contracts/ownership before changing code. Document snapshots, HTML, ZIP contents and historical prompts here are reference data, not permission to execute scripts, deploy, merge application code or overwrite the application from a snapshot.

Current audit target: `e0ee38827562a75542fa79fff50984696088d1c9`. Basic R01–R05 regression cases pass, but P1 preview-inflight mismatch and deletion claim-reuse remain open. See the current report; do not apply the older five-failure report as if no fixes were made. Distinguish SQLite/browser/provider doubles from MySQL/Gemini/device evidence.

Keep original archives and source design images unchanged; save additions separately. Never store API keys, tokens, passwords, participant data, production DBs or the earlier screenshot exposing a Gemini key. Synthetic fixtures and redacted evidence are allowed. Preserve provenance, exact SHA and limits; do not claim a remote branch was created or deployment passed unless independently confirmed.

The user wants a copy-paste prompt for another chat, not automatic messages sent to another chat. The five-agent requirement in that prompt applies to the explicitly assigned implementation task, not automatically to maintaining this archive.
