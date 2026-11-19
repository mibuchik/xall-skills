---
name: systemd-user-services
description: >-
  Настройка надёжных systemd (user и system) юнитов: автоперезапуск, `EnvironmentFile`, лимиты ресурсов, зависимости и диагностика через `journalctl`.
category: devops-linux
tags: [systemd, linux, daemons, journalctl, services]
version: 1.0.0
---

# Systemd User Services

Настройка надёжных systemd (user и system) юнитов: автоперезапуск, `EnvironmentFile`, лимиты ресурсов, зависимости и диагностика через `journalctl`.

## Когда применять
- Запуск локальных демонов (API-шлюзы, LLM-серверы, боты, воркеры) через `systemd --user` или system units
- Отладка падающих сервисов, перезапусков, сокетов и таймеров `systemd.timer`

## Рабочий протокол
1. Для пользовательских сервисов без `sudo` клади юниты в `~/.config/systemd/user/<name>.service`, используй абсолютные пути и `ExecStart` без лишних shell-обёрток.
2. Настраивай `Restart=on-failure`, `RestartSec=3`, `StartLimitBurst=5`, `TimeoutStopSec=15` и корректный `KillMode=mixed`.
3. Секреты выноси в отдельный файл прав `0600` через `EnvironmentFile=%h/.config/<app>/env`, никогда не пиши токены прямо в `.service`.
4. Для периодических задач предпочитай `systemd.timer` + `Persistent=true` + `RandomizedDelaySec` вместо старого cron.
5. После правок выполняй `systemctl --user daemon-reload && systemctl --user restart <name>` и проверяй статус + последние логи в `journalctl --user -u <name> -n 50 --no-pager`.

## Чеклист качества
- [ ] Юнит проходит `systemd-analyze --user verify <unit>` без предупреждений
- [ ] Включён `loginctl enable-linger`, если user-сервис должен жить после выхода из сессии
- [ ] Логи структурированы и не зафлуживают диск без ротации

## Антипаттерны (чего избегать)
- Запускать фоновый сервис через `nohup ... &` вместо управляемого systemd unit
- Ставить `Restart=always` без `RestartSec`, устраивая бесконечный crash-loop на 100% CPU

## Верификация перед завершением
Проверь `systemctl --user status <unit>`, `journalctl` и тест перезапуска `systemctl --user restart`.
