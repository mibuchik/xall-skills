---
name: minecraft-plugin-dev
description: >-
  Разработка и оптимизация Java 21 плагинов под Paper / Purpur 1.21+: Paper API, Adventure/MiniMessage,
  PersistentDataContainer (PDC), безопасные асинхронные задачи, защита TPS/MSPT и чистые soft-depend интеграции.
category: gamedev-media
tags: [minecraft, paper, purpur, java21, adventure, tps]
version: 1.1.0
---

# Minecraft Plugin Development (Paper / Purpur 1.21+, Java 21)

Стандарт создания надёжных, быстрых и потокобезопасных плагинов для современных серверов Minecraft на базе Paper / Purpur (Java 21).

## Когда применять
- Разработка новых Java-плагинов, команд, ивентов, кастомных предметов, GUI-меню и механик под Paper/Purpur 1.21+.
- Интеграция с экосистемой плагинов (PlaceholderAPI, Vault, WorldGuard, MythicMobs и др.) через `softdepend` / `paper-plugin.yml`.
- Оптимизация существующих плагинов для устранения просадок TPS / MSPT и ошибок многопоточности.

## Рабочий протокол
1. **Сборка и зависимости:** используй Gradle (`io.papermc.paper:paper-api:1.21.x-R0.1-SNAPSHOT`) или Maven с `--release 21`. Храни метаданные в `paper-plugin.yml` (или `plugin.yml` с явным `api-version: '1.21'`), внешние API подключай как `compileOnly` + `softdepend` с проверкой `PluginManager#isPluginEnabled`.
2. **Тексты через Adventure / MiniMessage:** используй `Component` и `MiniMessage.miniMessage().deserialize(...)` вместо устаревших `ChatColor` и legacy-кодов `§`.
3. **Данные на предметах и сущностях:** храни кастомные теги в `PersistentDataContainer` (`NamespacedKey`) и актуальных Paper Data Components, а не парся `displayName` или строки `lore`.
4. **Потокобезопасность и TPS:**
   - **Никогда** не выполняй SQL, HTTP, дисковый I/O или тяжёлые вычисления на главном тик-потоке сервера — выноси в async scheduler (`getAsyncScheduler()` / `runTaskAsynchronously`).
   - **Никогда** не изменяй мир, блоки, сущности или инвентари из асинхронного потока — возвращай мутации на главный/региональный поток (совместимо с Paper и Folia).
5. **Защита краевых случаев:** проверяй `player.isOnline()`, `null` для `ItemMeta` / `Block` / `OfflinePlayer`, права (`hasPermission`), защиту от дюпов в `InventoryClickEvent`/`InventoryDragEvent` (отмена shift-click, number keys, offhand swap) и очистку `Map<UUID, ...>` на `PlayerQuitEvent`.
6. **Конфиги и локализация:** валидируй YAML-конфиги при `onEnable()` / `/reload`, задавай безопасные дефолты и не глотай исключения молча — логируй через `getLogger()` / SLF4J.

## Чеклист качества
- [ ] Нет синхронных БД/HTTP/файловых вызовов в слушателях событий (`PlayerMoveEvent`, `BlockBreakEvent`, `EntityDamageEvent`)
- [ ] Все per-player кэши и задачи очищаются при выходе игрока и в `onDisable()`
- [ ] Кастомные GUI-меню идентифицируются через собственный `InventoryHolder` (а не по заголовку строки!) и защищены от дюпа
- [ ] Все строки локализуемы через Adventure/MiniMessage без хардкода `§`

## Антипаттерны (чего избегать)
- Запускать `Bukkit.getOfflinePlayer(name)` синхронно (может делать блокирующий сетевой запрос Mojang!)
- Хранить сильные ссылки на объекты `Player` в `Map<Player, ...>` вместо `Map<UUID, ...>` (утечка памяти после выхода игрока)
- Использовать `PlayerMoveEvent` для тяжёлых проверок без фильтрации смены блока (`hasChangedBlock()`)

## Верификация перед завершением
Собери JAR (`./gradlew build` или `mvn package`), убедись в 0 ошибок компиляции на Java 21, проверь `paper-plugin.yml`/`plugin.yml` и прогони юнит-тесты логики (MockBukkit / JUnit 5) или тестовый запуск на локальном Paper-сервере без ошибок в консоли.
