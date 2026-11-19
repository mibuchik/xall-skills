---
name: postgresql-query-tuning
description: >-
  Тюнинг PostgreSQL по `EXPLAIN (ANALYZE, BUFFERS)`: составные/частичные индексы, устранение Seq Scan и N+1, безопасные пулы соединений.
category: backend-db
tags: [postgresql, sql, indexes, explain, performance]
version: 1.0.0
---

# Postgresql Query Tuning

Тюнинг PostgreSQL по `EXPLAIN (ANALYZE, BUFFERS)`: составные/частичные индексы, устранение Seq Scan и N+1, безопасные пулы соединений.

## Когда применять
- Медленные SQL-запросы, рост нагрузки на PostgreSQL, проектирование индексов и схем
- Анализ планов выполнения `EXPLAIN (ANALYZE, BUFFERS)` и блокировок

## Рабочий протокол
1. Всегда запускай `EXPLAIN (ANALYZE, BUFFERS)` на реалистичном объёме данных — смотри `actual time`, `rows removed by filter` и `shared hit/read`.
2. Проектируй составные индексы по правилу равенство -> сортировка -> диапазон (`WHERE a = ? ORDER BY b` -> `(a, b)`); используй `INCLUDE` и partial indexes (`WHERE deleted_at IS NULL`).
3. Убирай функции над индексированной колонкой в `WHERE` (или создавай expression index) и устраняй N+1 через `JOIN` / `WHERE id = ANY($1)`.
4. Выставляй `statement_timeout`, `lock_timeout` и ограничивай размер пула соединений (или используй PgBouncer).
5. Создавай индексы на живых таблицах строго через `CREATE INDEX CONCURRENTLY`.

## Чеклист качества
- [ ] Критичные запросы используют Index Scan / Index Only Scan с малым числом прочитанных буферов
- [ ] Нет неиспользуемых дублирующихся индексов, замедляющих `INSERT`/`UPDATE`
- [ ] Внешние ключи (`FOREIGN KEY`), по которым идут частые `JOIN`/`DELETE`, проиндексированы

## Антипаттерны (чего избегать)
- Бездумно навешивать отдельный B-tree индекс на каждую колонку
- Использовать глубокий `OFFSET 100000` вместо keyset pagination (`WHERE (created_at, id) < ($1, $2)`)

## Верификация перед завершением
Сравни `EXPLAIN (ANALYZE, BUFFERS)` до и после изменения индекса/запроса.
