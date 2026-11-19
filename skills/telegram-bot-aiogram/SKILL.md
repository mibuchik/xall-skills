---
name: telegram-bot-aiogram
description: >-
  Продакшен Telegram-боты на aiogram 3 (Python): модульные роутеры, FSM-состояния, безопасный HTML-формат, анти-флуд middleware и graceful polling/webhook.
category: product-docs-bots
tags: [telegram, aiogram, bots, fsm, python]
version: 1.0.0
---

# Telegram Bot Aiogram

Продакшен Telegram-боты на aiogram 3 (Python): модульные роутеры, FSM-состояния, безопасный HTML-формат, анти-флуд middleware и graceful polling/webhook.

## Когда применять
- Создание и доработка Telegram-ботов на `aiogram 3` (или `python-telegram-bot`)
- Организация роутеров, inline-клавиатур, callback_data, FSM и устойчивости к лимитам Telegram API

## Рабочий протокол
1. Структурируй бота через `Router` по фичам (`handlers/`, `keyboards/`, `middlewares/`, `services/`), вынося бизнес-логику и БД из хендлеров.
2. Используй `CallbackData` фабрики (лимит Telegram `<= 64` байта!) вместо хрупкого парсинга строк `split(':')`.
3. Всегда экранируй пользовательский текст при `ParseMode.HTML` (`html.escape`) и отвечай `await callback.answer()`, чтобы убрать вечный спиннер на кнопке.
4. Добавь throttling/anti-flood middleware, храни FSM в Redis/SQLite (не в `MemoryStorage` на проде) и обрабатывай `TelegramRetryAfter` / `TelegramForbiddenError` при рассылках.
5. Настрой graceful shutdown, обработку `SIGTERM` и хранение `BOT_TOKEN` строго в `.env` / `EnvironmentFile` (`0600`).

## Чеклист качества
- [ ] Каждый callback-хендлер вызывает `callback.answer()` и валидирует длину `callback_data <= 64B`
- [ ] Длинные сообщения (> 4096 символов) безопасно разбиваются на чанки без поломки HTML-тегов
- [ ] Токен бота не захардкожен в коде и не попадает в логи

## Антипаттерны (чего избегать)
- Складывать все 1500 строк хендлеров и SQL в один файл `bot.py`
- Делать массовую рассылку без пауз и без обработки заблокировавших бота пользователей

## Верификация перед завершением
Прогони юнит-тесты сервисов/клавиатур, проверь обработку ошибок API и тестовый запуск бота.
