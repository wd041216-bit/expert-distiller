# Expert Distiller

Build reusable expert forums from public sources.

`expert-distiller` is a Codex skill for turning public expert knowledge into source-gated advisor profiles. It helps you detect coverage gaps, queue candidate experts, collect tiered sources, audit promotion readiness, and produce reusable expert profiles for research, product, strategy, engineering, policy, or any other domain.

It does **not** imitate private personality. It distills public methods, evidence preferences, critique habits, reasoning kernels, and blind spots.

## Why This Exists

LLM workflows often need more than one generic "expert" voice. They need a reliable way to ask:

- Which experts should pressure-test this problem?
- What public sources support this expert profile?
- Is this candidate ready to join the active forum?
- What reasoning style, evidence bar, and blind spots should downstream agents use?
- Where is the current forum weak, stale, or overconfident?

This skill makes that process explicit and reusable.

## Install

Copy this repository into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/wd041216-bit/expert-distiller.git ~/.codex/skills/expert-distiller
```

Restart Codex after installing so the skill list reloads.

## Quick Start

Initialize a forum:

```bash
python3 scripts/expert_distiller.py init \
  --root knowledge/expert_forums \
  --domain "AI Reliability" \
  --topic "LLM hallucination and evaluation"
```

Queue a candidate:

```bash
python3 scripts/expert_distiller.py candidate \
  --root knowledge/expert_forums \
  --domain "AI Reliability" \
  --name "Example Expert" \
  --reason "Covers a retrieval-evaluation gap"
```

Add Tier A and Tier B sources:

```bash
python3 scripts/expert_distiller.py source \
  --root knowledge/expert_forums \
  --expert-id example-expert \
  --tier A \
  --title "Official profile" \
  --url "https://example.edu/profile" \
  --note "Official biography and publication list"

python3 scripts/expert_distiller.py source \
  --root knowledge/expert_forums \
  --expert-id example-expert \
  --tier B \
  --title "Long-form interview" \
  --url "https://example.com/interview" \
  --note "Public reasoning style and methodology"
```

Audit and create the profile skeleton:

```bash
python3 scripts/expert_distiller.py audit --root knowledge/expert_forums --expert-id example-expert
python3 scripts/expert_distiller.py profile --root knowledge/expert_forums --domain "AI Reliability" --expert-id example-expert --name "Example Expert"
python3 scripts/expert_distiller.py validate --root knowledge/expert_forums --strict
```

## Source Gates

The promotion gate is intentionally conservative:

- Tier A: official pages, institutional profiles, papers, books, formal lectures, standards.
- Tier B: high-quality interviews, edited essays, course notes, reputable long-form profiles.
- Tier C: social posts, forums, short clips, secondhand summaries.

A candidate needs at least one Tier A and one Tier B source before promotion. Tier C can add context, but cannot define core beliefs or reasoning style.

## Output Layout

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

## Profile Contract

Each promoted profile captures:

- public career and idea arc
- canonical works
- signature ideas
- reasoning kernel
- preferred evidence
- critique style
- blind spots
- advantage knowledge base
- question playbook
- source confidence
- freshness metadata
- usage boundaries

See [`references/profile-contract.md`](references/profile-contract.md) for the full JSON contract.

## Use Cases

- Build a research review board for a new scientific domain.
- Create a product strategy expert panel from public founder/operator knowledge.
- Distill industry specialists into reusable critique lenses.
- Detect when your current expert roster does not cover a new problem.
- Keep expert memory separate from private project evidence.

## Trust Model

Expert profiles are analysis lenses, not primary evidence. Current artifacts, current data, current literature, and direct user constraints always outrank the distilled expert forum.

