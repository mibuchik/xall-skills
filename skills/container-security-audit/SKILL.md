---
name: container-security-audit
description: >-
  Аудит безопасности контейнеров и песочниц запуска кода: drop capabilities, `read_only` rootfs, лимиты PIDs/RAM/CPU, `--network=none` и запрет `docker.sock`.
category: security
tags: [containers, docker, seccomp, rootless, isolation]
version: 1.0.0
---

# Container Security Audit

Аудит безопасности контейнеров и песочниц запуска кода: drop capabilities, `read_only` rootfs, лимиты PIDs/RAM/CPU, `--network=none` и запрет `docker.sock`.

## Когда применять
- Запуск недоверенного кода (eval-песочницы, CI-раннеры, плагины) или прод-контейнеров в Docker
- Проверка `Dockerfile` и `docker run` / `compose` на эскалацию привилегий

## Рабочий протокол
1. Запускай контейнеры с `--cap-drop=ALL`, `--security-opt=no-new-privileges:true` и под non-root пользователем.
2. Для песочниц выполнения кода включай `--network=none`, `--read-only` rootfs (с малым `tmpfs /tmp:size=64m,noexec`), `--pids-limit=128`, `--memory` и `--cpus`.
3. НИКОГДА не монтируй `/var/run/docker.sock` внутрь контейнера с приложением (это мгновенный root на хосте!).
4. Ограничивай bind-mount только минимальной директорией и монтируй входные данные как `:ro`.
5. Регулярно сканируй базовые образы на критичные CVE и пересобирай их с актуальными патчами.

## Чеклист качества
- [ ] Нет `--privileged`, `--pid=host`, `--net=host` без критически обоснованной причины
- [ ] Песочница не имеет выхода в сеть и ограничена по CPU/RAM/PIDs (защита от fork-bomb)
- [ ] Хостовые пути монтируются минимально и с `:ro`, где запись не требуется

## Антипаттерны (чего избегать)
- Запускать чужой код в контейнере от `root` с доступом к сети и хостовому `/home`
- Оставлять безлимитное число процессов (1 fork-bomb кладёт весь хост)

## Верификация перед завершением
Проверь `docker inspect` (CapDrop, ReadonlyRootfs, PidsLimit, NetworkMode) и попытку записи в `/` / выхода в сеть изнутри.
