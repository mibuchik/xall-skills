---
name: sandbox-iframe-csp
description: >-
  Безопасная песочница для превью HTML/SVG/JS-артефактов: строгий `Content-Security-Policy`, `iframe sandbox` без `allow-same-origin` и UTF-8 Blob URLs.
category: security
tags: [csp, iframe, sandbox, blob, isolation]
version: 1.0.0
---

# Sandbox Iframe CSP

Безопасная песочница для превью HTML/SVG/JS-артефактов: строгий `Content-Security-Policy`, `iframe sandbox` без `allow-same-origin` и UTF-8 Blob URLs.

## Когда применять
- Отображение сгенерированных моделью HTML/JS/SVG/Mermaid превью внутри веб- или Electron-приложений
- Настройка CSP-заголовков для защиты от XSS и сетевой эксфильтрации данных

## Рабочий протокол
1. Для запуска недоверенного HTML/JS в `<iframe>` задавай `sandbox='allow-scripts'` и НИКОГДА не комбинируй `allow-scripts` с `allow-same-origin` (иначе скрипт снимет sandbox!).
2. Создавай Blob строго с кодировкой: `new Blob([html], { type: 'text/html;charset=utf-8' })` и обязательно вызывай `URL.revokeObjectURL(url)` в cleanup.
3. Вшивай в превью строгий `<meta http-equiv='Content-Security-Policy' content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: blob:; connect-src 'none';">` для полной блокировки сетевой эксфильтрации.
4. Для основного приложения задавай строгий CSP без `unsafe-eval`, ограничивая `connect-src` локальным/доверенным API.
5. Общайся с песочницей (если нужно) только через валидируемый `postMessage` с проверкой `event.source`.

## Чеклист качества
- [ ] Iframe-песочница не имеет доступа к `window.parent`, cookies, `localStorage` и `window.xallDesktop`
- [ ] `fetch`/`XMLHttpRequest`/внешние `<img>` из артефакта блокируются политикой CSP
- [ ] Кириллица и спецсимволы отображаются без кракозябр (`charset=utf-8`)

## Антипаттерны (чего избегать)
- Ставить `sandbox='allow-scripts allow-same-origin'` на пользовательский HTML
- Забывать `URL.revokeObjectURL`, устраивая утечку памяти при частых перерендерах

## Верификация перед завершением
Проверь в превью, что попытка `fetch('https://example.com')` и чтение `parent.document` блокируются браузером.
