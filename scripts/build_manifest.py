#!/usr/bin/env python3
"""Build and validate marketplace.json for the XaLL Skills Marketplace."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
OUT_FILE = ROOT / "marketplace.json"

CATEGORIES = [
    {
        "id": "engineering",
        "name": {"ru": "Инженерия и Архитектура", "en": "Engineering & Architecture"},
        "description": {
            "ru": "Чистый код, проектирование модулей, ревью, API и архитектурные решения",
            "en": "Clean code, deep modules, code review, API design, and architecture",
        },
        "icon": "layers",
    },
    {
        "id": "debugging-qa",
        "name": {"ru": "Отладка, Тесты и Качество", "en": "Debugging, QA & Testing"},
        "description": {
            "ru": "Поиск первопричин, TDD, профилирование, нагрузочное и E2E-тестирование",
            "en": "Root-cause debugging, TDD, profiling, load testing, and E2E verification",
        },
        "icon": "bug",
    },
    {
        "id": "frontend-ui",
        "name": {"ru": "Frontend и UI/UX", "en": "Frontend & UI/UX"},
        "description": {
            "ru": "React 19, TypeScript, CSS, дизайн-системы, доступность и десктопные интерфейсы",
            "en": "React 19, TypeScript, modern CSS, design systems, a11y, and desktop UI",
        },
        "icon": "palette",
    },
    {
        "id": "backend-db",
        "name": {"ru": "Backend, API и Базы данных", "en": "Backend, APIs & Databases"},
        "description": {
            "ru": "FastAPI, Bun/Node, PostgreSQL, SQLite, Redis, авторизация и real-time сервисы",
            "en": "FastAPI, Bun/Node, PostgreSQL, SQLite, Redis, auth, and realtime systems",
        },
        "icon": "database",
    },
    {
        "id": "ai-agents",
        "name": {"ru": "AI, LLM и Агенты", "en": "AI, LLMs & Agents"},
        "description": {
            "ru": "Роутинг скиллов, субагенты, RAG, дообучение LoRA/GRPO, GGUF и MCP-серверы",
            "en": "Skill routing, subagents, RAG, LoRA/GRPO fine-tuning, GGUF, and MCP servers",
        },
        "icon": "cpu",
    },
    {
        "id": "devops-linux",
        "name": {"ru": "Linux, DevOps и Инфраструктура", "en": "Linux, DevOps & Infra"},
        "description": {
            "ru": "Linux-администрирование, Docker, systemd, CI/CD, Git worktree и мониторинг",
            "en": "Linux administration, Docker, systemd, CI/CD, Git worktrees, and observability",
        },
        "icon": "terminal",
    },
    {
        "id": "security",
        "name": {"ru": "Безопасность и Аудит", "en": "Security & Auditing"},
        "description": {
            "ru": "OWASP-аудит, секреты, CSP/песочницы, криптография и защита инфраструктуры",
            "en": "OWASP audits, secrets hygiene, sandbox CSP, cryptography, and hardening",
        },
        "icon": "shield",
    },
    {
        "id": "data-systems",
        "name": {"ru": "Данные, Python и Системы", "en": "Data, Python & Systems"},
        "description": {
            "ru": "Python, Rust, Go, дата-пайплайны, бенчмарки, парсеры и оптимизация GPU VRAM",
            "en": "Python, Rust, Go, data pipelines, benchmarks, parsers, and GPU optimization",
        },
        "icon": "bar-chart",
    },
    {
        "id": "gamedev-media",
        "name": {"ru": "Геймдев, Minecraft и Медиа", "en": "GameDev, Minecraft & Media"},
        "description": {
            "ru": "Плагины Paper/Purpur, Blockbench 3D, WebGL/Three.js, Remotion и FFmpeg",
            "en": "Minecraft Paper plugins, Blockbench 3D, WebGL/Three.js, Remotion, and FFmpeg",
        },
        "icon": "gamepad",
    },
    {
        "id": "product-docs-bots",
        "name": {"ru": "Продукт, Документация и Боты", "en": "Product, Docs & Bots"},
        "description": {
            "ru": "Техдокументация, Telegram/Discord-боты, i18n, спецификации и редактура текстов",
            "en": "Technical docs, Telegram/Discord bots, i18n, PRDs, and crisp human editing",
        },
        "icon": "book-open",
    },
]

VALID_CATEGORY_IDS = {c["id"] for c in CATEGORIES}
SKILL_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
FORBIDDEN_PATTERNS = [
    re.compile(r"/home/[a-zA-Z0-9_-]+/"),
    re.compile(
        r"\b(antigravity|anthropic|openai|endeavouros|tlauncher|millida|temurin-21|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,})\b",
        re.IGNORECASE,
    ),
]


def parse_frontmatter(text: str, fallback_id: str) -> dict:
    m = re.match(r"^---\r?\n([\s\S]*?)\r?\n---", text)
    if not m:
        raise ValueError(f"{fallback_id}: missing YAML frontmatter")
    block = m.group(1)
    data: dict = {
        "name": fallback_id,
        "description": "",
        "category": "",
        "tags": [],
        "version": "1.0.0",
        "featured": False,
    }
    lines = block.splitlines()
    collecting_key: str | None = None
    collected: list[str] = []

    def flush() -> None:
        nonlocal collecting_key, collected
        if collecting_key and collected:
            data[collecting_key] = " ".join(x.strip() for x in collected if x.strip()).strip()
        collecting_key = None
        collected = []

    for line in lines:
        if collecting_key:
            if line.startswith(" ") or line.startswith("\t") or not line.strip():
                collected.append(line.strip())
                continue
            flush()

        km = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if not km:
            continue
        key, val = km.group(1).strip(), km.group(2).strip()
        if val in (">", ">-", "|", "|-"):
            collecting_key = key
            collected = []
        elif key == "tags":
            inner = val.strip("[]")
            data["tags"] = [
                t.strip().strip("'\"")
                for t in inner.split(",")
                if t.strip().strip("'\"")
            ]
        elif key == "featured":
            data["featured"] = val.lower() in ("true", "yes", "1")
        else:
            data[key] = val.strip("'\"")
    flush()
    return data


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest() -> dict:
    if not SKILLS_DIR.is_dir():
        raise SystemExit(f"Missing skills directory: {SKILLS_DIR}")

    skills: list[dict] = []
    errors: list[str] = []

    for skill_dir in sorted(SKILLS_DIR.iterdir(), key=lambda p: p.name):
        if not skill_dir.is_dir() or skill_dir.name.startswith("."):
            continue
        sid = skill_dir.name
        if not SKILL_ID_RE.match(sid):
            errors.append(f"Invalid skill directory id: {sid}")
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{sid}: missing SKILL.md")
            continue

        raw_md = skill_md.read_text(encoding="utf-8")
        try:
            meta = parse_frontmatter(raw_md, sid)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        if meta["category"] not in VALID_CATEGORY_IDS:
            errors.append(f"{sid}: invalid category '{meta['category']}'")
        if not meta["description"]:
            errors.append(f"{sid}: empty description")

        files: list[dict] = []
        total_bytes = 0
        for fpath in sorted(skill_dir.rglob("*")):
            if not fpath.is_file():
                continue
            rel = fpath.relative_to(skill_dir).as_posix()
            if rel.startswith(".") or "/." in rel:
                continue
            content_bytes = fpath.read_bytes()
            total_bytes += len(content_bytes)
            try:
                txt = content_bytes.decode("utf-8")
                for pat in FORBIDDEN_PATTERNS:
                    if pat.search(txt):
                        errors.append(f"{sid}/{rel}: matched forbidden pattern {pat.pattern}")
            except UnicodeDecodeError:
                pass
            files.append(
                {
                    "path": rel,
                    "sha256": sha256_file(fpath),
                    "bytes": len(content_bytes),
                }
            )

        skills.append(
            {
                "id": sid,
                "name": meta["name"] or sid,
                "description": meta["description"],
                "category": meta["category"],
                "tags": meta["tags"],
                "version": meta["version"] or "1.0.0",
                "featured": bool(meta["featured"]),
                "path": f"skills/{sid}",
                "totalBytes": total_bytes,
                "files": files,
            }
        )

    if errors:
        print("Manifest validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    # Sort featured skills first, then alphabetically by id
    skills.sort(key=lambda s: (0 if s["featured"] else 1, s["id"]))

    manifest = {
        "schemaVersion": 1,
        "name": "XaLL Skills Marketplace",
        "repo": "mibuchik/xall-skills",
        "branch": "main",
        "updatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "categories": CATEGORIES,
        "skills": skills,
    }
    OUT_FILE.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    cat_counts: dict[str, int] = {}
    for s in skills:
        cat_counts[s["category"]] = cat_counts.get(s["category"], 0) + 1

    print(f"Built {OUT_FILE} with {len(skills)} skills across {len(cat_counts)} categories:")
    for c in CATEGORIES:
        print(f"  - {c['id']}: {cat_counts.get(c['id'], 0)}")
    return manifest


if __name__ == "__main__":
    build_manifest()
