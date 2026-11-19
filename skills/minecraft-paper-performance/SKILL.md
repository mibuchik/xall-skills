---
name: minecraft-paper-performance
description: >-
  Оптимизация серверов Paper/Purpur/Leaf 1.21+: профилирование Spark, тюнинг `paper-world-defaults.yml`, Aikar/ZGC флаги и защита от просадок TPS/MSPT.
category: gamedev-media
tags: [minecraft, paper, purpur, tps, spark, optimization]
version: 1.0.0
---

# Minecraft Paper Performance

Оптимизация серверов Paper/Purpur/Leaf 1.21+: профилирование Spark, тюнинг `paper-world-defaults.yml`, Aikar/ZGC флаги и защита от просадок TPS/MSPT.

## Когда применять
- Лаги на сервере Minecraft, рост MSPT > 35–50ms, спайки GC и настройка конфигов Paper/Purpur
- Аудит плагинов и миров по профилям `spark profiler`

## Рабочий протокол
1. Начни со снятия профиля `/spark profiler --timeout 60` и `/spark gcmonitor` — оптимизируй строго реальные топ-пожиратели MSPT, а не «по гайдам из интернета».
2. Настрой `simulation-distance` (5–7) ниже `view-distance` (8–12), проверь `entity-activation-range`, `max-entity-collisions`, `alt-item-despawn-rate` и лимиты спавна мобов.
3. Проверь чанк-систему: предгенерация мира (`Chunky`), адекватное число IO/worker потоков и отсутствие синхронной загрузки чанков из плагинов.
4. Подбери JVM-флаги под Java 21 и объём RAM (Aikar G1GC для 6–16GB, Generational ZGC `-XX:+UseZGC -XX:+ZGenerational` для минимизации pause spikes).
5. После каждой правки сверяй MSPT (avg/p95/max) и GC pause под реальными игроками/тестом.

## Чеклист качества
- [ ] Средний MSPT < 25ms, p95 < 40ms, паузы GC не превышают 30–50ms
- [ ] Нет плагинов, делающих сетевые/SQL-запросы на основном тик-потоке
- [ ] Сделан бэкап конфигов перед тюнингом `bukkit.yml`/`spigot.yml`/`paper-world-defaults.yml`

## Антипаттерны (чего избегать)
- Выделять серверу 32 GB RAM без нужды, получая многосекундные GC-фризы
- Резать `spawn-limits` до нуля, убивая ванильные механики ферм, когда лагает 1 кривой плагин

## Верификация перед завершением
Сними повторный `/spark profiler` и `/spark tps` после изменений и сравни с базовым замером.
