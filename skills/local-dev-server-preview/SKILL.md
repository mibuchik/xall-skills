---
name: local-dev-server-preview
description: >-
  Надёжный запуск локальных веб-приложений, dev-серверов (Vite, Node, Bun, Python) и превью в браузере из AI-агента: setsid + nohup без BrokenPipeError, контроль PID/порта, проверка HTTP 200 после detach и открытие браузера без зависания.
category: devops-linux
tags: [dev-server, browser, localhost, setsid, preview, http]
version: 1.0.0
---

# Local Dev Server & Browser Preview

Надёжный запуск локальных веб-приложений, dev-серверов (Vite, Node, Bun, Python) и превью в браузере из AI-агента без `BrokenPipeError`, зависаний оболочки и ложных отчётов «200 OK».

## Когда применять
- Запуск локального HTTP/dev-сервера (`python3 -m http.server`, `vite`, `bun`, `node`, `uvicorn`) для просмотра веб-приложения в браузере
- Открытие `http://localhost:<port>` в браузере пользователя из автономного CLI/агента
- Диагностика `curl: (52) Empty reply from server`, занятых портов (`EADDRINUSE`) или «сервер упал сразу после ответа агента»

## Рабочий протокол (Spawn -> Redirect -> Track -> Verify -> Open)
1. **Проверь порт и директорию:**
   - Перед стартом проверь, свободен ли порт: `ss -tlnp | grep ":3000" || true`. Если порт занят твоим же старым процессом — аккуратно останови его по PID; иначе выбери свободный порт (`3000`, `5173`, `8080`).
   - Не прячь рабочие проекты в `/tmp`, если пользователь не просил временный прототип.
2. **Всегда делай полный detach (`setsid` + `nohup` + редирект всех трёх потоков `0/1/2`):**
   ```bash
   setsid nohup python3 -m http.server 3000 --directory . >/tmp/dev-3000.log 2>&1 </dev/null &
   echo $! > /tmp/dev-3000.pid
   ```
   Для Vite / Node / Bun аналогично:
   ```bash
   setsid nohup bun run dev -- --host 127.0.0.1 --port 5173 >/tmp/dev-5173.log 2>&1 </dev/null &
   echo $! > /tmp/dev-5173.pid
   ```
   *Почему это обязательно:* обычный `&` без `>log 2>&1 </dev/null` оставляет `stdout/stderr` привязанными к `pipe` shell-инструмента. Как только команда завершается, pipe закрывается, и сервер (особенно `python3 -m http.server`, пишущий access-лог в `stderr`) при следующем запросе падает с `BrokenPipeError` и рвёт соединение (`Empty reply from server`).
3. **Проверяй HTTP 200 ОТДЕЛЬНЫМ вызовом `shell` после завершения команды запуска:**
   ```bash
   curl -sSI --max-time 3 http://127.0.0.1:3000/ | head -n 5
   ```
   Если в ответе нет `200 OK` или `Content-Length: 0`, сразу прочитай `/tmp/dev-3000.log` и почини причину — никогда не пиши пользователю «работает», пока отдельный `curl` не прошёл.
4. **Открывай браузер тоже detached, чтобы shell-инструмент не завис:**
   ```bash
   setsid nohup xdg-open "http://localhost:3000" >/dev/null 2>&1 </dev/null &
   ```
   Если пользователь упоминает конкретный браузер (например Firefox), проверь `xdg-settings get default-web-browser` или запусти нужный браузер напрямую с `setsid nohup <browser> "http://localhost:3000" >/dev/null 2>&1 </dev/null &`.
5. **Не делай банальные ИИ-заглушки:**
   Для интерактивных браузерных приложений подключай `ui-ux-pro-max`, `css-modern-layout`, `micro-interactions-motion`, `threejs-webgl-shaders` или `game-loop-physics` — избегай шаблонного фиолетового градиента и статичных карточек без реального интерактива.

## Чеклист качества
- [ ] Сервер запущен через `setsid nohup ... >/tmp/<name>.log 2>&1 </dev/null &` с записью PID в `.pid`-файл
- [ ] Отдельный вызов `curl -sSI http://127.0.0.1:<port>/` ПОСЛЕ команды запуска возвращает `200 OK`
- [ ] В лог-файле `/tmp/<name>.log` нет ошибок (`Traceback`, `EADDRINUSE`, `BrokenPipeError`)
- [ ] Браузер запущен detached и не блокирует завершение хода агента

## Антипаттерны (чего избегать)
- Запускать `python3 -m http.server 3000 &` без `setsid` и перенаправления `>log 2>&1 </dev/null`
- Проверять `curl` только внутри той же команды, где был `&` (пока pipe ещё открыт, баг маскируется)
- Спамить повторными `xdg-open` без проверки дефолтного браузера и живого HTTP-ответа
- Оставлять зомби-серверы на портах без PID-файла

## Верификация перед завершением
Сделай отдельный `curl -sSI http://127.0.0.1:<port>/`, проверь `ps -p "$(cat /tmp/dev-<port>.pid)"` и отсутствие ошибок в `/tmp/dev-<port>.log`.
