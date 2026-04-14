# Expert Distiller

Build reusable expert forums from public sources, then use them to autonomously drive projects to production maturity.

`expert-distiller` is a Claude Code skill that turns public expert knowledge into source-gated advisor profiles, forms expert councils, scores project maturity on a 0-100 rubric, builds code guided by expert lenses, and iterates until the council awards a perfect score — then submits to GitHub.

It does **not** imitate private personality. It distills public methods, evidence preferences, critique habits, reasoning kernels, and blind spots.

## Why This Exists

LLM workflows often need more than one generic "expert" voice. They need a reliable way to:

- Discover and validate domain experts from public sources
- Distill their reasoning patterns into reusable lenses
- Form councils that collectively evaluate and guide projects
- Score maturity across breadth, depth, thickness, and effectiveness
- Iterate build-debug-score cycles until production quality
- Automatically submit polished work to GitHub

## Install

```bash
git clone https://github.com/wd041216-bit/expert-distiller.git ~/.claude/skills/expert-distiller
```

Restart Claude Code after installing.

## Autonomous Pipeline

The skill runs a 10-phase pipeline:

```
INIT → DISCOVER → DISTILL → COUNCIL → SCORE
                                        │
                             score < 100│
                                        ▼
          GAP_FILL ← RESCORE ← DEBUG ← BUILD
              │
              │ score = 100 + all pass
              ▼
           SUBMIT (GitHub PR)
```

**Phases 1-4** (setup): Initialize domain, discover experts via web search, distill profiles, form council.

**Phases 5-9** (loop): Score artifact, build code, debug, re-score, fill gaps. Repeat until 100/100.

**Phase 10** (submit): Push to GitHub with maturity report.

Experts can be dynamically added mid-loop when the gap analyst identifies uncovered sub-domains.

## Maturity Scoring

Four axes, each scored 0-25 by the expert council:

| Axis | What It Measures |
|------|-----------------|
| **Breadth** (0-25) | Domain coverage completeness |
| **Depth** (0-25) | Expert profile richness and detail |
| **Thickness** (0-25) | Practical implementability |
| **Effectiveness** (0-25) | Problem-solution fit |

Total: 0-100. Convergence requires 100/100 with all verification stages passing.

See [`references/scoring-rubric.md`](references/scoring-rubric.md) for the full rubric.

## Quick Start (Manual Mode)

All 15 CLI commands work standalone:

```bash
# Initialize forum
python3 scripts/expert_distiller.py init \
  --root knowledge/expert_forums \
  --domain "AI Reliability" \
  --topic "LLM hallucination and evaluation"

# Add candidate with sources
python3 scripts/expert_distiller.py candidate \
  --root knowledge/expert_forums \
  --domain "AI Reliability" \
  --name "Example Expert" \
  --reason "Covers retrieval evaluation gap"

python3 scripts/expert_distiller.py source \
  --root knowledge/expert_forums \
  --expert-id example-expert \
  --tier A \
  --title "Official profile" \
  --url "https://example.edu/profile" \
  --note "Official biography and publication list"

# Audit and promote
python3 scripts/expert_distiller.py audit --root knowledge/expert_forums --expert-id example-expert
python3 scripts/expert_distiller.py profile --root knowledge/expert_forums --domain "AI Reliability" --expert-id example-expert --name "Example Expert"

# Form council
python3 scripts/expert_distiller.py council create --root knowledge/expert_forums --domain "AI Reliability"

# Score and analyze
python3 scripts/expert_distiller.py score --root knowledge/expert_forums --domain "AI Reliability" --artifact ./my-project
python3 scripts/expert_distiller.py coverage --root knowledge/expert_forums --domain "AI Reliability"
python3 scripts/expert_distiller.py report --root knowledge/expert_forums --domain "AI Reliability" --format markdown

# Validate
python3 scripts/expert_distiller.py validate --root knowledge/expert_forums --strict
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize forum root and domain |
| `candidate` | Queue an expert candidate |
| `source` | Add a tiered source to a dossier |
| `audit` | Audit candidate for promotion readiness |
| `profile` | Create expert profile skeleton |
| `index` | Rebuild forum index |
| `validate` | Validate profile completeness |
| `discover` | Discover candidates from file or SKILL mode |
| `fill` | Output fill prompt for profile distillation |
| `council` | Manage councils (create/add-member/list/show) |
| `score` | Score artifact against expert council |
| `coverage` | Analyze expert coverage gaps |
| `refresh` | Check source freshness |
| `build` | Record build context |
| `report` | Generate maturity report (JSON or Markdown) |

## Output Layout

```text
knowledge/expert_forums/
├── forum_index.json
├── pipeline_state.json
├── domains/<domain_id>.json
├── candidates/<expert_id>.json
├── source_dossiers/<expert_id>.json
├── promotion_audits/<expert_id>.json
├── experts/<expert_id>/profile.json
├── experts/<expert_id>/distillate.md
├── councils/<council_id>.json
├── scoring_reports/<domain_id>_<timestamp>.json
├── gap_analyses/<domain_id>_<timestamp>.json
└── build_logs/<domain_id>_<timestamp>.json
```

## Source Gates

Promotion is intentionally conservative:

- **Tier A**: official pages, institutional profiles, papers, books, formal lectures, standards
- **Tier B**: high-quality interviews, edited essays, course notes, reputable long-form profiles
- **Tier C**: social posts, forums, short clips, secondhand summaries

A candidate needs at least 1 Tier A + 1 Tier B source. Tier C cannot define core beliefs or reasoning style.

## Agents

| Agent | Role |
|-------|------|
| `expert-researcher` | Web discovery and source collection |
| `profile-distiller` | LLM-driven profile filling |
| `forum-moderator` | Council debate orchestration |
| `project-builder` | Code generation with expert lenses |
| `maturity-scorer` | Adversarial 4-axis scoring |
| `gap-analyst` | Coverage gap detection |

## References

- [`references/profile-contract.md`](references/profile-contract.md) — Full JSON profile contract
- [`references/source-gates.md`](references/source-gates.md) — Source tier rules
- [`references/scoring-rubric.md`](references/scoring-rubric.md) — 4-axis maturity rubric
- [`references/council-protocol.md`](references/council-protocol.md) — Council debate rules
- [`references/loop-state-machine.md`](references/loop-state-machine.md) — Pipeline state machine
- [`references/build-integration.md`](references/build-integration.md) — Build/debug cycle spec
- [`references/github-submission.md`](references/github-submission.md) — Submission protocol

## Trust Model

Expert profiles are analysis lenses, not primary evidence. Current artifacts, current data, current literature, and direct user constraints always outrank the distilled expert forum. Never fabricate quotes, invent private beliefs, or treat expert memory as truth.

## License

MIT
