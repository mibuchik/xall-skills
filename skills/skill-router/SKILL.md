---
name: skill-router
description: >-
  Главный рекомендованный диспетчер скиллов XaLL. При каждом запросе анализирует задачу,
  подключает подходящие скиллы по 10 тематическим категориям, сверяет важные решения с актуальной
  документацией и проводит поэтапное планирование перед правками.
category: ai-agents
tags: [router, recommended, workflow, planning, dispatch]
version: 1.0.0
featured: true
---

# Skill Router — Рекомендованный диспетчер скиллов XaLL

Это базовый рекомендованный скилл для `XaLL Desktop` и `XaLL Code`. Подключай его первым, чтобы модель системно выбирала профильные скиллы вместо работы «наобум».

## Обязательный порядок работы на любую нетривиальную задачу

1. **Определи домен задачи** и проверь, какие установленные скиллы подходят (через нативный инструмент `skill` в XaLL Code).
2. **Проверь факты напрямую в коде и конфигах** — не угадывай структуру файлов, флаги CLI или версии библиотек по памяти.
3. **Сверь важные архитектурные и библиотечные решения** с актуальной документацией, прежде чем фиксировать стек.
4. **План и развилки до правок**: для сложных задач сначала составь краткий пошаговый план (`/plan`), уточни ключевые развилки по одному вопросу (`/grill`), а затем реализуй.
5. **Делегируй независимые подзадачи субагентам** (`subagent` / `xall__spawn_subagent` с `worktree: true` при правках файлов), если работа распадается на непересекающиеся части.
6. **Верифицируй результат до отчёта**: сборка, тайпчек, тесты и визуальная проверка обязательны перед заявлением «готово».

## Карта 10 тем Магазина скиллов XaLL

| Тема | Когда подключать | Ключевые скиллы |
| :--- | :--- | :--- |
| **Инженерия и Архитектура** | Проектирование модулей, чистый код, ревью, API, рефакторинг | `clean-code-engineer`, `codebase-design`, `code-review`, `grilling`, `verification-before-completion`, `refactoring-legacy`, `api-design-rest-graphql` |
| **Отладка, Тесты и Качество** | Баги, регрессии, TDD, E2E, профилирование, утечки памяти | `diagnosing-bugs`, `tdd`, `webapp-testing`, `fast-batch-ops`, `flaky-test-hunter`, `performance-profiling`, `memory-leak-detective` |
| **Frontend и UI/UX** | React 19, TypeScript, CSS Grid/Popover, WCAG, Electron, анимации | `react-19-patterns`, `typescript-strict-types`, `css-modern-layout`, `web-accessibility-wcag`, `design-system-tokens`, `electron-wayland-desktop`, `micro-interactions-motion` |
| **Backend, API и БД** | FastAPI, Bun/Node, PostgreSQL, SQLite, Redis, OAuth/JWT, SSE | `fastapi-production`, `nodejs-bun-services`, `postgresql-query-tuning`, `sqlite-local-first`, `redis-caching-queues`, `auth-oauth-jwt-passkeys`, `websockets-sse-realtime` |
| **AI, LLM и Агенты** | Субагенты, ресёрч, RAG, LoRA/GRPO, GGUF/llama.cpp, MCP | `skill-router`, `dispatching-parallel-agents`, `research`, `prompt-engineering-evals`, `rag-hybrid-search`, `lora-qlora-finetuning`, `rlvr-grpo-posttraining`, `gguf-quantization-llamacpp`, `mcp-server-builder` |
| **Linux, DevOps и Инфра** | Linux CLI, локальные dev-серверы и превью в браузере, Docker, systemd, Nginx/Caddy, CI/CD, Git worktree, Niri | `local-dev-server-preview`, `linux-devops-automation`, `docker-multi-stage`, `systemd-user-services`, `nginx-caddy-reverse-proxy`, `github-actions-cicd`, `git-worktree-workflows`, `bash-strict-scripting`, `wayland-niri-poweruser` |
| **Безопасность и Аудит** | OWASP, секреты, SHA-256 цепочка поставок, SQLi/XSS, CSP, Docker | `owasp-web-audit`, `secrets-hygiene-scanner`, `dependency-supply-chain`, `sql-xss-injection-guard`, `sandbox-iframe-csp`, `crypto-hashing-best-practices`, `container-security-audit` |
| **Данные, Python и Системы** | Python/uv/ruff, Rust, Go, Polars, очистка JSONL, бенчмарки, VRAM | `python-modern-uv-ruff`, `rust-safe-systems`, `go-concurrent-backends`, `pandas-polars-pipelines`, `data-cleaning-dedup`, `benchmark-harness-design`, `gpu-vram-optimization` |
| **Геймдев, Minecraft и Медиа** | Paper/Purpur Java 21, MythicMobs, датапаки, Blockbench, Three.js, Remotion, FFmpeg | `minecraft-plugin-dev`, `minecraft-paper-performance`, `minecraft-mythicmobs-configs`, `minecraft-datapacks-commands`, `blockbench-3d-modeling`, `threejs-webgl-shaders`, `remotion-video-scripting`, `ffmpeg-media-pipelines` |
| **Продукт, Доки и Боты** | Документация, README, релизы, Telegram/Discord боты, i18n, редактура | `technical-writing-docs`, `readme-open-source-polish`, `changelog-semver-release`, `telegram-bot-aiogram`, `discord-bot-architecture`, `prd-spec-writer`, `i18n-localization-ru-en`, `human-prose-editor` |

## Комбинирование скиллов
Для комплексных задач подключай 2–3 скилла одновременно:
- *Фича в веб/десктоп приложении:* `clean-code-engineer` + `react-19-patterns` + `verification-before-completion`
- *Интерактивное демо / веб-приложение в браузере:* `local-dev-server-preview` + `css-modern-layout` + `micro-interactions-motion` (+ `threejs-webgl-shaders` / `game-loop-physics` / `audio-dsp-sfx`)
- *Сложный баг или просадка скорости:* `diagnosing-bugs` + `performance-profiling` + `tdd`
- *Публичный релиз или хранилище данных:* `owasp-web-audit` + `secrets-hygiene-scanner` + `changelog-semver-release`
