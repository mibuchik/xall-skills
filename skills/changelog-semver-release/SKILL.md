---
name: changelog-semver-release
description: >-
  Аккуратные релизы по SemVer и Keep a Changelog: аудит `git log`, выделение breaking changes, генерация release notes и проверка артефактов перед тегом.
category: product-docs-bots
tags: [semver, changelog, release, git-tags, versioning]
version: 1.0.0
---

# Changelog Semver Release

Аккуратные релизы по SemVer и Keep a Changelog: аудит `git log`, выделение breaking changes, генерация release notes и проверка артефактов перед тегом.

## Когда применять
- Подготовка релиза, обновление `CHANGELOG.md`, выбор версии SemVer и публикация GitHub Release
- Сборка заметок о релизе из истории коммитов

## Рабочий протокол
1. Собери все коммиты с прошлого тега (`git log <last-tag>..HEAD --oneline`) и сгруппируй пользовательские изменения по Keep a Changelog: `Added`, `Changed`, `Fixed`, `Security`, `Breaking`.
2. Выбери версию строго по SemVer: `MAJOR` при breaking change, `MINOR` при обратно совместимой фиче, `PATCH` при багфиксе.
3. Обнови версию синхронно во всех манифестах (`package.json`, `pyproject.toml`, `Cargo.toml`) и добавь дату + раздел в `CHANGELOG.md`.
4. Прогони полный release-гейт (lint, typecheck, tests, production build) ДО создания тега `vX.Y.Z`.
5. Пиши release notes понятным языком для пользователя (что изменилось и как мигрировать), а не сырой дамп коммитов `wip`/`fix typo`.

## Чеклист качества
- [ ] Все breaking changes вынесены в начало с инструкцией миграции
- [ ] Версии синхронизированы во всех файлах проекта и совпадают с git-тегом
- [ ] Сборка и полный набор тестов зелёные на релизном коммите

## Антипаттерны (чего избегать)
- Выпускать breaking change в patch-релизе `1.2.3 -> 1.2.4`
- Публиковать тег без проверки production-сборки

## Верификация перед завершением
Проверь `git diff` манифестов, чистую сборку и текст release notes до `git push --tags`.
