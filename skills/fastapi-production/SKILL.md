---
name: fastapi-production
description: >-
  Продакшен-сервисы на FastAPI: Pydantic v2 схемы, lifespan-управление ресурсами, потоковый SSE, таймауты и корректная обработка `CancelledError`.
category: backend-db
tags: [fastapi, python, pydantic, uvicorn, sse]
version: 1.0.0
---

# Fastapi Production

Продакшен-сервисы на FastAPI: Pydantic v2 схемы, lifespan-управление ресурсами, потоковый SSE, таймауты и корректная обработка `CancelledError`.

## Когда применять
- Создание или ревью HTTP/SSE API на FastAPI и Pydantic v2
- Устранение блокировок event loop, утечек соединений и обрывов стриминга

## Рабочий протокол
1. Инициализируй и закрывай клиенты БД/HTTP/очереди строго через `@asynccontextmanager async def lifespan(app)` — никаких устаревших `on_event`.
2. Не вызывай блокирующий `requests`/тяжёлый CPU внутри `async def` роутов — используй `httpx.AsyncClient` или `anyio.to_thread.run_sync`.
3. Для SSE-стриминга оборачивай генератор в `try ... finally`, чтобы при отключении клиента (`asyncio.CancelledError`) мгновенно освобождать слоты/семафоры/апстримы.
4. Валидируй настройки через `pydantic-settings`, отделяй входные/выходные DTO от ORM-моделей.
5. Добавь `/healthz` (liveness) и `/readyz` (проверка зависимостей), структурные JSON-логи с `request_id` и единый обработчик ошибок.

## Чеклист качества
- [ ] Все внешние HTTP-клиенты имеют явные connect/read таймауты
- [ ] Обрыв клиентского соединения во время SSE гарантированно освобождает ресурсы в `finally`
- [ ] OpenAPI схема чиста, а тесты используют `httpx.AsyncClient` с `ASGITransport`

## Антипаттерны (чего избегать)
- Создавать новый `httpx.AsyncClient()` на каждый запрос вместо переиспользования пула
- Перехватывать `except Exception` без логирования или проглатывать `asyncio.CancelledError`

## Верификация перед завершением
Прогони `pytest` (включая тесты обрыва SSE и невалидных payload) и проверь `ruff` / `mypy`.
