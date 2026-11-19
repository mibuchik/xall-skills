---
name: linux-devops-automation
description: >-
  Системное администрирование и автоматизация окружения (EndeavourOS / Arch
  Linux, Wayland, Git + Git LFS, GitHub CLI, сетевые порты, процессы, установка
  инструментов без sudo).
category: devops-linux
tags: [linux, arch, wayland, git, cli]
version: 1.0.0
---

# Linux & DevOps Automation (EndeavourOS / Arch)

Используй этот скилл для задач системного администрирования, работы с Git/GitHub, буфером обмена, процессами и установкой утилит.

## 1. Особенности рабочего окружения
- **ОС:** EndeavourOS (Arch Linux), графическая сессия **Wayland** (`WAYLAND_DISPLAY=wayland-1`).
- **Буфер обмена:** для мгновенного копирования ключей, кодов, ссылок или команд прямо в буфер обмена пользователя используй `wl-copy` (и `wl-paste` для проверки).
- **Открытие ссылок в браузере:** `xdg-open "https://..."`.
- **Установка утилит без `sudo`:**
  - `sudo pacman` требует пароль. Поэтому все CLI-инструменты (например, `gh`, `git-lfs`, `java`, `javac`) скачивай в виде официальных статических бинарников для `linux-amd64` и клади в `~/.local/bin/` (эта папка уже в `PATH`).
- **Гибридная графика и NVIDIA RTX 3070 Ti (Wayland / Niri):**
  - По умолчанию приложения стартуют на встроенной графике Intel Iris Xe.
  - Для полного выноса на дискретную графику NVIDIA (OpenGL + Vulkan) создана системная утилита `~/.local/bin/prime-run` (и алиас `nv`):
    `__NV_PRIME_RENDER_OFFLOAD=1 __NV_PRIME_RENDER_OFFLOAD_PROVIDER=NVIDIA-G0 __GLX_VENDOR_LIBRARY_NAME=nvidia __VK_LAYER_NV_optimus=NVIDIA_only "$@"`
  - Игровые лаунчеры (`tlauncher.desktop`, `millida-launcher.desktop`) запускаются через `prime-run`.
- **Игровая оптимизация и запись видео (Feral GameMode & GPU Screen Recorder):**
  - Установлен **Feral GameMode** (`gamemoderun`, `lib32-gamemode`, пользователь в группе `gamemode`). Встроен прямо в `prime-run` для динамического переключения ядер CPU в `performance` во время игр.
  - Установлен **GPU Screen Recorder** (`gsr-ui`, `gpu-screen-recorder.desktop`) — аналог NVIDIA ShadowPlay на Wayland/Niri: запись видео и Instant Replay по хоткею через аппаратный NVENC с 0% CPU.
  - Установлен **btop** (системный TUI-монитор с поддержкой NVIDIA GPU и ZRAM).
  - Включен таймер проверки целостности файловой системы **`btrfs-scrub@-.timer`** (ежемесячно).
- **Арсенал разработчика и AI-ассистента (Dev Power Tools):**
  - `idc` (`~/.local/bin/idc`): единая мастер-утилита Interactive Desktop Control (управление пакетами yay/pacman, запуск приложений с поддержкой NVIDIA RTX 3070 Ti через `prime-run`, системный дашборд CPU/GPU/RAM/SSD/портов, FZF process & port killer, очистка кэшей и интерактивное меню).
  - `cfr` (`~/.local/bin/cfr`): мгновенный консольный декомпилятор Java-классов и JAR-файлов Minecraft.
  - `yq` (`go-yq`): парсинг и редактирование YAML-конфигов плагинов сервера прямо в CLI.
  - `lazygit`: терминальный TUI для Git.
  - `shellcheck`: линтер и статический анализатор bash/sh-скриптов.
  - `ast-grep` (`sg`): структурный поиск и рефакторинг по AST-дереву (Java, TS, Python, Rust).
  - `delta` (`git-delta`): IDE/GitHub-style цветной пейджер для `git diff`.
  - `dust`: наглядное графическое дерево занятого дискового пространства.
  - `hyperfine`: высокоточный бенчмаркер CLI-команд.
  - `tokei`: ультрабыстрый анализатор объёма и строк кодовой базы.
- **Среда Java Temurin в `~/.local` и лаунчеры (Millida Launcher, Prism и др.):**
  - Java 21 установлена в `~/.local/share/jvm/temurin-21/`.
  - Бинарники `java`, `javac`, `jar` засимлинкованы в `~/.local/bin/`.
  - Для приложений и лаунчеров, копирующих исполняемый файл `java` в `~/.local/bin/<Name>` (например, `MillidaMinecraft`), библиотеки среды (`libjli.so`, `lib*.so`, `server/libjvm.so`, `jvm.cfg`, `modules`) засимлинкованы в `~/.local/lib/` и `~/.local/bin/` для автоматического разрешения RPATH `$ORIGIN:$ORIGIN/../lib`.

## 2. Git, Git LFS и GitHub (отдельный приватный репозиторий на проект)
- Авторизация GitHub CLI настроена через `~/.local/bin/gh`.
- **Обязательное правило:** под **каждый отдельный проект** создаётся и используется **свой отдельный приватный репозиторий** на GitHub (`gh repo create <project-name> --private --source=. --remote=origin --push`), без смешивания разных проектов в одном репо.
- Git LFS (`~/.local/bin/git-lfs`) при необходимости отслеживает тяжёлые бинарники (`*.jar`, `*.mca`, `*.dat`, `*.db`, `*.mp4`, `*.mp3`, `*.wav`, `*.onnx`).
- Кэши среды исполнения и сборки (`node_modules/`, `.venv/`, `dist/`, `build/`, `backups/*.tar.gz`) исключай в `.gitignore`, чтобы не раздувать репозиторий и не превышать бесплатный лимит GitHub LFS (1 ГБ).
