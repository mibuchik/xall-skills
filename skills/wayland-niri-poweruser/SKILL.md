---
name: wayland-niri-poweruser
description: >-
  Настройка и отладка рабочего окружения Wayland и композитора Niri: KDL-конфиг, биндинги, Ozone-флаги Electron/Chromium, `wl-clipboard` и порталы.
category: devops-linux
tags: [wayland, niri, kdl, linux-desktop, ozone, clipboard]
version: 1.0.0
---

# Wayland Niri Poweruser

Настройка и отладка рабочего окружения Wayland и композитора Niri: KDL-конфиг, биндинги, Ozone-флаги Electron/Chromium, `wl-clipboard` и порталы.

## Когда применять
- Настройка `~/.config/niri/config.kdl`, правил окон, горячих клавиш и автозапуска в Niri/Wayland
- Исправление размытия HiDPI, буфера обмена, скриншотов и нативного рендера Electron/Chromium на Wayland

## Рабочий протокол
1. Проверяй синтаксис конфига Niri командой `niri validate` ДО применения правок.
2. Для Electron/Chromium приложений включай нативный Wayland: `--ozone-platform-hint=auto --enable-features=UseOzonePlatform,WaylandWindowDecorations`.
3. Используй `wl-copy` / `wl-paste` для буфера обмена, `xdg-desktop-portal` для диалогов файлов и скринкастов, и `niri msg -j windows|workspaces|outputs` для инспекции окон.
4. Для вспомогательных окон (Quick Entry / spotlight) задавай `window-rule` с `open-floating true` и стабильным `app-id`.
5. Проверяй `.desktop` файлы в `~/.local/share/applications/` через `desktop-file-validate` и обновляй базу иконок/приложений.

## Чеклист качества
- [ ] `niri validate` проходит без ошибок
- [ ] Приложения не падают в размытый XWayland без необходимости
- [ ] Собственные `.desktop` лаунчеры используют валидные `Exec=`, `Icon=` и `StartupWMClass=`

## Антипаттерны (чего избегать)
- Использовать `xclip`/`xdotool` на чистом Wayland вместо `wl-copy`/нативных протоколов
- Править `config.kdl` без бэкапа и проверки `niri validate`

## Верификация перед завершением
Выполни `niri validate` и проверь запуск целевого приложения/биндинга в живой Wayland-сессии.
