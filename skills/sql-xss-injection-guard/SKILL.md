---
name: sql-xss-injection-guard
description: >-
  Надёжная защита от инъекций (SQLi, XSS, Command Injection, Path Traversal): параметризация, `execFile` вместо `shell`, DOMPurify и канонизация путей.
category: security
tags: [sqli, xss, command-injection, path-traversal, sanitization]
version: 1.0.0
---

# SQL XSS Injection Guard

Надёжная защита от инъекций (SQLi, XSS, Command Injection, Path Traversal): параметризация, `execFile` вместо `shell`, DOMPurify и канонизация путей.

## Когда применять
- Работа с SQL, рендером Markdown/HTML, запуском CLI-команд и доступом к файлам по имени
- Устранение потенциальных точек инъекций при ревью кода

## Рабочий протокол
1. SQL: только параметризованные запросы/prepared statements (`$1`, `?`) — никогда конкатенация или f-string с пользовательским вводом (даже для `ORDER BY` используй строгий allowlist колонок).
2. Shell/CLI: используй `execFile`/`spawn(bin, argsArray)` без `shell: true`, передавай `--` перед пользовательскими аргументами/путями, чтобы флаг `--force` не был воспринят как опция.
3. HTML/Markdown: санитизируй любой рендер HTML через `DOMPurify` (или нативный Sanitizer API), запрещай `javascript:` URL и небезопасные атрибуты `on*`.
4. Файловая система: разрешай путь через `path.resolve(root, rel)` и проверяй `resolved === root || resolved.startsWith(root + path.sep)` (плюс `realpath` против symlink escape).
5. Валидируй идентификаторы строгими регэкспами (`/^[a-z0-9][a-z0-9-_]*$/`) прямо на границе API/IPC.

## Чеклист качества
- [ ] Нигде нет `dangerouslySetInnerHTML` или `innerHTML` без проверенного санитайзера
- [ ] Нигде нет `exec(\`git checkout ${userInput}\`)` через shell-интерполяцию
- [ ] Покрыты юнит-тестами попытки `../etc/passwd`, `--flag`, `<script>alert(1)</script>` и `' OR 1=1--`

## Антипаттерны (чего избегать)
- Пытаться чистить HTML или SQL самописными `replace('<script>', '')`
- Проверять путь только через `!rel.includes('..')` без `path.resolve` и проверки префикса

## Верификация перед завершением
Напиши и запусти юнит-тесты с вредоносными входами (XSS, traversal, leading dash, SQL-кавычки).
