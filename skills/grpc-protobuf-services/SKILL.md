---
name: grpc-protobuf-services
description: >-
  Проектирование и эксплуатация gRPC/Protobuf сервисов: эволюция `.proto` без поломок, deadlines, статусы, streaming и кодогенерация.
category: backend-db
tags: [grpc, protobuf, rpc, deadlines, contracts]
version: 1.0.0
---

# GRPC Protobuf Services

Проектирование и эксплуатация gRPC/Protobuf сервисов: эволюция `.proto` без поломок, deadlines, статусы, streaming и кодогенерация.

## Когда применять
- Создание межсервисных контрактов на Protobuf v3 и gRPC (Go, Python, Rust, TS)
- Ревью `.proto` схем на обратную совместимость и настройку дедлайнов/интерсепторов

## Рабочий протокол
1. Никогда не переиспользуй номера удалённых полей в `.proto` — помечай их как `reserved 4, 5;` и `reserved 'old_field';`.
2. Прокидывай `deadline` (таймаут) на каждый клиентский вызов и проверяй его на сервере до старта тяжёлой работы.
3. Используй канонические gRPC статус-коды (`INVALID_ARGUMENT`, `NOT_FOUND`, `DEADLINE_EXCEEDED`, `UNAVAILABLE`) вместо общего `UNKNOWN`/`INTERNAL`.
4. Упаковывай аргументы в выделенные `*Request` / `*Response` сообщения, чтобы добавлять поля без ломки сигнатур.
5. Вынеси сквозные задачи (логи, метрики, trace, auth, panic recovery) в interceptors.

## Чеклист качества
- [ ] Линтер `buf lint` и проверка совместимости `buf breaking` проходят без ошибок
- [ ] Потоковые RPC обрабатывают backpressure и отмену контекста
- [ ] Сгенерированные стабы актуальны и не редактируются вручную

## Антипаттерны (чего избегать)
- Менять номер или wire-тип существующего поля в `.proto`
- Отправлять многомегабайтные бинарники в одном unary-сообщении вместо client/server streaming

## Верификация перед завершением
Запусти `buf lint`, `buf breaking` и интеграционный тест с коротким deadline.
