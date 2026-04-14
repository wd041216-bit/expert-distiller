#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REQUIRED_PROFILE_FIELDS = {
    "id",
    "name",
    "domains",
    "roles",
    "routing_keywords",
    "bio_arc",
    "canonical_works",
    "signature_ideas",
    "reasoning_kernel",
    "preferred_evidence",
    "critique_style",
    "blind_spots",
    "advantage_knowledge_base",
    "question_playbook",
    "domain_relevance",
    "source_refs",
    "source_confidence",
    "freshness",
    "usage_boundaries",
}


def now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "unknown"


def read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def ensure_layout(root: Path) -> None:
    for name in (
        "domains",
        "candidates",
        "source_dossiers",
        "promotion_audits",
        "experts",
        "councils",
    ):
        (root / name).mkdir(parents=True, exist_ok=True)


def init_root(args: argparse.Namespace) -> None:
    root = args.root.expanduser()
    ensure_layout(root)
    domain_id = slugify(args.domain)
    domain_path = root / "domains" / f"{domain_id}.json"
    if not domain_path.exists():
        write_json(
            domain_path,
            {
                "id": domain_id,
                "name": args.domain,
                "topic": args.topic or args.domain,
                "created_at": now_iso(),
                "updated_at": now_iso(),
                "coverage_axes": [],
                "active_experts": [],
                "candidate_experts": [],
            },
        )
    rebuild_index(root)
    print(f"Initialized expert forum root: {root}")


def add_candidate(args: argparse.Namespace) -> None:
    root = args.root.expanduser()
    ensure_layout(root)
    expert_id = args.expert_id or slugify(args.name)
    payload = {
        "id": expert_id,
        "name": args.name,
        "domain": slugify(args.domain),
        "reason": args.reason or "",
        "status": "candidate",
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    write_json(root / "candidates" / f"{expert_id}.json", payload)
    print(f"Queued candidate: {expert_id}")


def add_source(args: argparse.Namespace) -> None:
    root = args.root.expanduser()
    ensure_layout(root)
    expert_id = args.expert_id
    dossier_path = root / "source_dossiers" / f"{expert_id}.json"
    dossier = read_json(
        dossier_path,
        {
            "expert_id": expert_id,
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "sources": [],
        },
    )
    source_id = args.source_id or slugify(f"{expert_id}-{args.tier}-{args.title}")[:80]
    source = {
        "id": source_id,
        "title": args.title,
        "url": args.url,
        "tier": args.tier.upper(),
        "note": args.note or "",
        "added_at": now_iso(),
    }
    dossier["sources"] = [item for item in dossier.get("sources", []) if item.get("id") != source_id]
    dossier["sources"].append(source)
    dossier["updated_at"] = now_iso()
    write_json(dossier_path, dossier)
    print(f"Added Tier {source['tier']} source for {expert_id}: {source_id}")


def audit_candidate(args: argparse.Namespace) -> None:
    root = args.root.expanduser()
    dossier_path = root / "source_dossiers" / f"{args.expert_id}.json"
    dossier = read_json(dossier_path, {"expert_id": args.expert_id, "sources": []})
    counts = {"A": 0, "B": 0, "C": 0}
    for source in dossier.get("sources", []):
        tier = str(source.get("tier", "")).upper()
        if tier in counts:
            counts[tier] += 1
    blockers: list[str] = []
    if counts["A"] < 1:
        blockers.append("missing_tier_a_source")
    if counts["B"] < 1:
        blockers.append("missing_tier_b_source")
    promotion_allowed = not blockers
    weighted_score = round(min(1.0, (counts["A"] * 0.45) + (counts["B"] * 0.3) + min(counts["C"], 2) * 0.05), 3)
    audit = {
        "expert_id": args.expert_id,
        "generated_at": now_iso(),
        "promotion_status": "promotion_allowed" if promotion_allowed else "blocked",
        "promotion_allowed": promotion_allowed,
        "blockers": blockers,
        "source_counts": counts,
        "source_confidence": {
            "level": "high" if weighted_score >= 0.75 else "medium" if weighted_score >= 0.45 else "low",
            "weighted_score": weighted_score,
            "rationale": "Computed from source-tier coverage; human review should still check claim-source alignment.",
        },
        "tier_c_core_claim_allowed": False,
    }
    write_json(root / "promotion_audits" / f"{args.expert_id}.json", audit)
    print(json.dumps(audit, indent=2, ensure_ascii=False))


def write_profile_skeleton(args: argparse.Namespace) -> None:
    root = args.root.expanduser()
    audit = read_json(root / "promotion_audits" / f"{args.expert_id}.json", {})
    if not audit.get("promotion_allowed") and not args.allow_unpromoted:
        raise SystemExit(
            f"Candidate {args.expert_id} has not passed promotion audit. "
            "Run audit or pass --allow-unpromoted for a candidate skeleton."
        )
    dossier = read_json(root / "source_dossiers" / f"{args.expert_id}.json", {"sources": []})
    source_refs = [source.get("id") for source in dossier.get("sources", []) if source.get("id")]
    profile = {
        "id": args.expert_id,
        "name": args.name,
        "domains": [slugify(args.domain)],
        "roles": ["domain_reviewer"],
        "routing_keywords": [],
        "bio_arc": "",
        "canonical_works": [],
        "signature_ideas": [],
        "reasoning_kernel": {
            "core_questions": [],
            "decision_rules": [],
            "failure_taxonomy": [],
            "preferred_abstractions": [],
        },
        "preferred_evidence": [],
        "critique_style": [],
        "blind_spots": [],
        "advantage_knowledge_base": {
            "canonical_concepts": [],
            "favorite_benchmarks": [],
            "known_debates": [],
            "anti_patterns": [],
        },
        "question_playbook": [],
        "domain_relevance": {
            "summary": "",
            "best_used_for": [],
            "avoid_using_for": [],
        },
        "quote_bank": [],
        "source_refs": source_refs,
        "source_confidence": audit.get("source_confidence", {"level": "low", "weighted_score": 0, "rationale": ""}),
        "freshness": {
            "status": "mixed",
            "last_checked": now_iso()[:10],
            "notes": "Skeleton generated; fill from source dossier before active use.",
        },
        "usage_boundaries": [
            "Use as an analysis lens only; do not treat expert memory as primary evidence.",
            "Do not imitate private personality or fabricate beliefs.",
        ],
    }
    expert_root = root / "experts" / args.expert_id
    write_json(expert_root / "profile.json", profile)
    write_text(
        expert_root / "distillate.md",
        f"# {args.name}\n\n"
        "## Public Evidence Base\n\n"
        f"- Fill from `source_dossiers/{args.expert_id}.json`.\n\n"
        "## Career And Idea Arc\n\n"
        "TODO\n\n"
        "## Signature Reasoning Kernel\n\n"
        "TODO\n\n"
        "## What This Expert Will Catch\n\n"
        "TODO\n\n"
        "## What This Expert May Miss\n\n"
        "TODO\n\n"
        "## Best Routing Situations\n\n"
        "TODO\n\n"
        "## Source Notes And Freshness\n\n"
        "TODO\n",
    )
    rebuild_index(root)
    print(f"Wrote profile skeleton: {expert_root / 'profile.json'}")


def rebuild_index(root: Path) -> dict[str, Any]:
    ensure_layout(root)
    domains = sorted(path.stem for path in (root / "domains").glob("*.json"))
    candidates = sorted(path.stem for path in (root / "candidates").glob("*.json"))
    experts: list[dict[str, Any]] = []
    for profile_path in sorted((root / "experts").glob("*/profile.json")):
        profile = read_json(profile_path, {})
        experts.append(
            {
                "id": profile.get("id", profile_path.parent.name),
                "name": profile.get("name", profile_path.parent.name),
                "domains": profile.get("domains", []),
                "roles": profile.get("roles", []),
                "source_confidence": profile.get("source_confidence", {}),
                "freshness": profile.get("freshness", {}),
            }
        )
    index = {
        "version": "expert_forum_index_v1",
        "generated_at": now_iso(),
        "domains": domains,
        "candidate_count": len(candidates),
        "expert_count": len(experts),
        "experts": experts,
    }
    write_json(root / "forum_index.json", index)
    return index


def index_root(args: argparse.Namespace) -> None:
    index = rebuild_index(args.root.expanduser())
    print(json.dumps(index, indent=2, ensure_ascii=False))


def validate_root(args: argparse.Namespace) -> None:
    root = args.root.expanduser()
    errors: list[str] = []
    warnings: list[str] = []
    for profile_path in sorted((root / "experts").glob("*/profile.json")):
        profile = read_json(profile_path, {})
        missing = sorted(REQUIRED_PROFILE_FIELDS - set(profile))
        if missing:
            errors.append(f"{profile_path}: missing fields {', '.join(missing)}")
        source_confidence = profile.get("source_confidence", {})
        if args.strict and source_confidence.get("level") == "low":
            warnings.append(f"{profile_path}: low source confidence")
        source_refs = profile.get("source_refs", [])
        if args.strict and not source_refs:
            errors.append(f"{profile_path}: no source_refs")
    result = {
        "status": "failed" if errors else "passed",
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build source-gated expert forums for Codex skills.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init")
    init.add_argument("--root", type=Path, required=True)
    init.add_argument("--domain", required=True)
    init.add_argument("--topic")
    init.set_defaults(func=init_root)

    candidate = subparsers.add_parser("candidate")
    candidate.add_argument("--root", type=Path, required=True)
    candidate.add_argument("--domain", required=True)
    candidate.add_argument("--name", required=True)
    candidate.add_argument("--expert-id")
    candidate.add_argument("--reason")
    candidate.set_defaults(func=add_candidate)

    source = subparsers.add_parser("source")
    source.add_argument("--root", type=Path, required=True)
    source.add_argument("--expert-id", required=True)
    source.add_argument("--source-id")
    source.add_argument("--tier", choices=("A", "B", "C", "a", "b", "c"), required=True)
    source.add_argument("--title", required=True)
    source.add_argument("--url", required=True)
    source.add_argument("--note")
    source.set_defaults(func=add_source)

    audit = subparsers.add_parser("audit")
    audit.add_argument("--root", type=Path, required=True)
    audit.add_argument("--expert-id", required=True)
    audit.set_defaults(func=audit_candidate)

    profile = subparsers.add_parser("profile")
    profile.add_argument("--root", type=Path, required=True)
    profile.add_argument("--domain", required=True)
    profile.add_argument("--expert-id", required=True)
    profile.add_argument("--name", required=True)
    profile.add_argument("--allow-unpromoted", action="store_true")
    profile.set_defaults(func=write_profile_skeleton)

    index = subparsers.add_parser("index")
    index.add_argument("--root", type=Path, required=True)
    index.set_defaults(func=index_root)

    validate = subparsers.add_parser("validate")
    validate.add_argument("--root", type=Path, required=True)
    validate.add_argument("--strict", action="store_true")
    validate.set_defaults(func=validate_root)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
