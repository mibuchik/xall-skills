---
name: electron-wayland-desktop
description: >-
  Разработка безопасных и нативных Electron-приложений под Linux/Wayland: изоляция контекста, тонкий IPC-мост, обход багов Wayland popup и clean shutdown.
category: frontend-ui
tags: [electron, wayland, ipc, security, linux-desktop]
version: 1.0.0
---

# Electron Wayland Desktop

Разработка безопасных и нативных Electron-приложений под Linux/Wayland: изоляция контекста, тонкий IPC-мост, обход багов Wayland popup и clean shutdown.

## Когда применять
- Разработка Electron-приложений под Linux (Wayland/Niri/Sway/Hyprland/GNOME)
- Проектирование безопасного `preload.ts`, IPC, трей/окна и встроенного WebView/iframe

## Рабочий протокол
1. Всегда включай `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true` (где совместимо) и никогда не передавай сырой `ipcRenderer` в `window`.
2. Держи секреты, API-ключи, файловые операции и `child_process` строго в main-процессе с валидацией путей (`resolveSafePath`).
3. Под Linux/Wayland добавляй `--ozone-platform-hint=auto` и заменяй нативные `<select>` (ломаются из-за `xdg_popup` в Chromium) на кастомные `[popover]` + Anchor Positioning.
4. Для превью недоверенного HTML используй `blob:` URL с `charset=utf-8` внутри `<iframe sandbox='allow-scripts'>` (БЕЗ `allow-same-origin`) и строгий CSP.
5. Гарантируй корректное завершение всех дочерних процессов (`shutdown()`) на `before-quit` и `window-all-closed`.

## Чеклист качества
- [ ] Renderer не имеет доступа к Node API, переменным окружения и файлам ключей
- [ ] Дым-тест запуска (`electron . --smoke-exit --disable-gpu`) проходит чисто с кодом 0
- [ ] Все дочерние процессы и MCP-серверы корректно завершаются при выходе

## Антипаттерны (чего избегать)
- Включать `nodeIntegration: true` или передавать API-ключ в React-рендерер
- Оставлять осиротевшие дочерние процессы после закрытия окна

## Верификация перед завершением
Прогони `tsc`, сборку main/preload/renderer и `--smoke-exit` в headless/Wayland окружении.
