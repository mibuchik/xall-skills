---
name: github-actions-cicd
description: >-
  Быстрые и безопасные GitHub Actions пайплайны: минимальные `permissions`, кэширование зависимостей, concurrency-отмена и матрица проверок.
category: devops-linux
tags: [github-actions, cicd, workflows, caching, security]
version: 1.0.0
---

# Github Actions CICD

Быстрые и безопасные GitHub Actions пайплайны: минимальные `permissions`, кэширование зависимостей, concurrency-отмена и матрица проверок.

## Когда применять
- Настройка CI/CD в `.github/workflows/*.yml` для тестов, линтинга, сборок и релизов
- Ускорение долгих джобов и аудит безопасности workflow-файлов

## Рабочий протокол
1. Задавай минимальные права в корне workflow (`permissions: contents: read`) и расширяй их только на конкретной джобе релиза.
2. Добавляй `concurrency: { group: '${{ github.workflow }}-${{ github.ref }}', cancel-in-progress: true }` на PR, чтобы не тратить минуты на устаревшие коммиты.
3. Кэшируй менеджеры пакетов (`actions/setup-node`/`oven-sh/setup-bun`/`astral-sh/setup-uv` с встроенным cache) и выставляй `timeout-minutes` на каждую джобу.
4. Никогда не подставляй недоверенные `${{ github.event.pull_request.title }}` напрямую в `run:` shell — передавай через `env:` против script injection.
5. Закрепляй сторонние экшены на конкретный commit SHA (или стабильный мажорный тег от проверенных авторов).

## Чеклист качества
- [ ] У каждой джобы стоит `timeout-minutes`, чтобы зависший тест не сжигал квоту 6 часов
- [ ] Секреты не печатаются в логах и не доступны форкам в `pull_request_target`
- [ ] PR-пайплайн запускает lint + typecheck + tests параллельными джобами

## Антипаттерны (чего избегать)
- Использовать `pull_request_target` с `actions/checkout` кода PR (уязвимость захвата секретов!)
- Писать `permissions: write-all` без необходимости

## Верификация перед завершением
Провалидируй YAML (`actionlint` / dry-check) и проверь прогон workflow на тестовой ветке.
