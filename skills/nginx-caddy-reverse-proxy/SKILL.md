---
name: nginx-caddy-reverse-proxy
description: >-
  Конфигурация обратных прокси Nginx и Caddy: авто-TLS, стриминг SSE/WebSockets без буферизации, заголовки безопасности и rate limiting.
category: devops-linux
tags: [nginx, caddy, reverse-proxy, tls, sse, websockets]
version: 1.0.0
---

# Nginx Caddy Reverse Proxy

Конфигурация обратных прокси Nginx и Caddy: авто-TLS, стриминг SSE/WebSockets без буферизации, заголовки безопасности и rate limiting.

## Когда применять
- Публикация веб-приложений, API, SSE-стримов и WebSockets за Nginx или Caddy
- Устранение 502/504, обрывов долгих стримов, сломанных заголовков `X-Forwarded-*` и CORS

## Рабочий протокол
1. Всегда передавай `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto` и проверяй, что backend доверяет только локальному прокси.
2. Для SSE/LLM-стримов в Nginx явно задавай `proxy_http_version 1.1`, `proxy_buffering off`, `proxy_cache off`, `proxy_read_timeout 300s`, `chunked_transfer_encoding on`.
3. Для WebSockets добавляй `proxy_set_header Upgrade $http_upgrade` и `Connection 'upgrade'`.
4. Включай базовую защиту: `client_max_body_size`, `limit_req_zone`, сжатие gzip/brotli (выключая для SSE), HSTS и security headers.
5. Перед перезагрузкой ВСЕГДА валидируй конфиг (`nginx -t` / `caddy validate`) и делай zero-downtime `reload`, а не жёсткий `restart`.

## Чеклист качества
- [ ] `nginx -t` / `caddy validate` проходит чисто до `reload`
- [ ] SSE-чанки доходят до клиента мгновенно без задержки на буферизацию
- [ ] Внутренние порты апстрима слушают `127.0.0.1`, а не `0.0.0.0`

## Антипаттерны (чего избегать)
- Оставлять `proxy_buffering on` перед стриминговым AI API
- Открывать админские/метрик эндпоинты наружу без allowlist или авторизации

## Верификация перед завершением
Проверь `nginx -t`, тест `curl -N` на SSE-стрим и заголовки ответа `curl -I`.
