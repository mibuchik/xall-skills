# XaLL Skills Marketplace

Official public registry of **100 curated agent skills** organized across **10 thematic categories** for **XaLL Desktop** and **XaLL Code**.

Every skill lives in its own directory under `skills/<id>/` (`SKILL.md` + optional helper `references/` and `scripts/`). The auto-generated [`marketplace.json`](./marketplace.json) index records every file path and its **SHA-256** digest so clients download individual skills directly from `raw.githubusercontent.com` with cryptographic integrity verification and zero GitHub API rate limits.

## Featured Skill

- **`skill-router`** (*Рекомендованный скилл*) — master dispatcher that analyzes each incoming request, routes to matching skills across all 10 categories, and enforces structured planning & verification before completion.

## Categories (10 × 10 = 100 Skills)

1. **Инженерия и Архитектура (`engineering`)** — 10 skills
2. **Отладка, Тесты и Качество (`debugging-qa`)** — 10 skills
3. **Frontend и UI/UX (`frontend-ui`)** — 10 skills
4. **Backend, API и Базы данных (`backend-db`)** — 10 skills
5. **AI, LLM и Агенты (`ai-agents`)** — 10 skills
6. **Linux, DevOps и Инфраструктура (`devops-linux`)** — 10 skills
7. **Безопасность и Аудит (`security`)** — 10 skills
8. **Данные, Python и Системы (`data-systems`)** — 10 skills
9. **Геймдев, Minecraft и Медиа (`gamedev-media`)** — 10 skills
10. **Продукт, Документация и Боты (`product-docs-bots`)** — 10 skills

## Adding or Updating a Skill

1. Create `skills/<skill-id>/SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: my-skill
   description: Concise summary of what the skill does and when to trigger it.
   category: engineering
   tags: [tag1, tag2]
   version: 1.0.0
   ---
   ```
2. Regenerate and validate `marketplace.json`:
   ```bash
   python3 scripts/build_manifest.py
   ```
3. Commit and push — **XaLL Desktop** picks up updates automatically on refresh.
