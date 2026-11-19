---
name: docker-multi-stage
description: >-
  Сборка компактных и безопасных Docker-образов: multi-stage builds, кэш слоёв BuildKit, non-root пользователь и минимальный runtime.
category: devops-linux
tags: [docker, containers, multi-stage, buildkit, optimization]
version: 1.0.0
---

# Docker Multi Stage

Сборка компактных и безопасных Docker-образов: multi-stage builds, кэш слоёв BuildKit, non-root пользователь и минимальный runtime.

## Когда применять
- Написание и оптимизация `Dockerfile`, `.dockerignore` и `docker-compose.yml`
- Уменьшение размера образов, ускорение пересборок и настройка healthcheck

## Рабочий протокол
1. Всегда добавляй строгий `.dockerignore` (`.git`, `node_modules`, `.venv`, `dist`, `.env`, кэши), чтобы не слать гигабайты в build context.
2. Разделяй `Dockerfile` на стадии: `builder` (компиляторы/SDK) -> тонкий `runtime` (`slim`/`alpine`/`distroless`) только с артефактами и прод-зависимостями.
3. Копируй lock-файлы (`package.json`/`bun.lock`, `pyproject.toml`/`uv.lock`) и ставь зависимости ДО копирования исходников для максимального кэш-хита слоёв.
4. Запускай процесс от непривилегированного `USER` (non-root), закрепляй версии базовых образов и добавляй `HEALTHCHECK`.
5. Никогда не запекай секреты в слои образа (`ENV`/`ARG`) — используй `--mount=type=secret` на сборке и runtime env/volumes.

## Чеклист качества
- [ ] Итоговый образ не содержит компиляторов, `.git`, `.env` и временных кешей пакетов
- [ ] Контейнер стартует под non-root UID и корректно обрабатывает `SIGTERM` (PID 1 / `exec` форма `CMD`)
- [ ] Повторная сборка при правке 1 файла исходников переиспользует слой зависимостей

## Антипаттерны (чего избегать)
- Писать `COPY . .` в первой строке до `npm ci` / `pip install`
- Запускать приложение через shell-форму `CMD npm start`, теряя `SIGTERM`

## Верификация перед завершением
Собери образ, проверь размер `docker images`, `docker inspect` (User/Healthcheck) и запуск контейнера.
