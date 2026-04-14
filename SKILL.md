---
name: expert-distiller
description: Build a reusable, source-gated expert forum from public materials for any domain. Use when Codex needs to distill industry leaders, scholars, founders, reviewers, or domain specialists into advisor profiles; detect expert coverage gaps; create promotion-gated expert rosters; or turn public sources into reusable council skills without imitating private personality.
---

# Expert Distiller

Use this skill to turn public expertise into reusable Codex advisor profiles. It generalizes the old submission-advisor "AI luminary autogrowth" loop so it can build expert forums for any field, not just AI research.

## Core Rule

Distill methods, evidence preferences, reasoning habits, critique patterns, and blind spots. Do not impersonate a living person, invent private beliefs, or treat an expert profile as primary evidence.

## Default Workflow

1. Define the domain and decision task: what the forum must judge, create, critique, or forecast.
2. Check coverage: list current experts, missing subfields, and why the gap matters.
3. Discover candidates from public sources, preferring official pages, papers, books, lectures, standards, and high-quality interviews.
4. Build a source dossier for each candidate using the tier rules in `references/source-gates.md`.
5. Run promotion audit before creating an active expert profile.
6. Distill promoted experts into the contract in `references/profile-contract.md`.
7. Build or refresh the forum index so downstream workflows can route by topic, subfield, and critique style.
8. Use the forum as an analysis lens only; current artifacts, current data, and current literature remain primary truth.

## Fast Commands

Initialize a portable expert knowledge root:

```bash
python3 scripts/expert_distiller.py init --root knowledge/expert_forums --domain ai-reliability --topic "LLM hallucination and evaluation"
```

Queue a candidate:

```bash
python3 scripts/expert_distiller.py candidate --root knowledge/expert_forums --domain ai-reliability --name "Example Expert" --reason "Covers retrieval evaluation gap"
```

Add source evidence:

```bash
python3 scripts/expert_distiller.py source --root knowledge/expert_forums --expert-id example-expert --tier A --title "Official faculty profile" --url "https://example.edu/profile" --note "Official biography and publication list"
python3 scripts/expert_distiller.py source --root knowledge/expert_forums --expert-id example-expert --tier B --title "Long-form interview" --url "https://example.com/interview" --note "Public reasoning and methodological preferences"
```

Audit and create a profile skeleton:

```bash
python3 scripts/expert_distiller.py audit --root knowledge/expert_forums --expert-id example-expert
python3 scripts/expert_distiller.py profile --root knowledge/expert_forums --domain ai-reliability --expert-id example-expert --name "Example Expert"
python3 scripts/expert_distiller.py index --root knowledge/expert_forums
```

Validate before publishing or syncing:

```bash
python3 scripts/expert_distiller.py validate --root knowledge/expert_forums --strict
```

## Output Structure

Use this layout for portable expert forums:

```text
knowledge/expert_forums/
├── forum_index.json
├── domains/<domain_id>.json
├── candidates/<expert_id>.json
├── source_dossiers/<expert_id>.json
├── promotion_audits/<expert_id>.json
├── experts/<expert_id>/profile.json
├── experts/<expert_id>/distillate.md
└── councils/<council_id>.json
```

## Distillation Depth

For each promoted expert, capture:

- What they reliably know: canonical works, tools, concepts, and domain-specific strengths.
- How they think: core questions, preferred abstractions, proof habits, evidence bars, and failure detectors.
- How they critique: what they attack first, what they forgive, what they over-index on.
- Where they are risky: blind spots, stale areas, conflicts of interest, and source uncertainty.
- How to route them: topics, artifacts, questions, and council roles where they add distinct value.

## Safety And Trust

- Require at least one Tier A and one Tier B source before promotion.
- Never use Tier C sources to define core beliefs.
- Mark stale or weakly sourced fields as tentative.
- Preserve source refs and freshness metadata with every profile.
- Downgrade conclusions that rely only on expert memory.
- Keep private project evidence outside the generic expert knowledge base.

