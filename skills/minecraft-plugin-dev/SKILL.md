---
name: minecraft-plugin-dev
description: >-
  Разработка и доработка плагинов и расширений под Paper / Purpur / Leaf 1.21.11 на Java 21
  (включая PlaceholderAPI-расширения, интеграции с AuraSkills, MythicMobs, NotQuests, DeluxeMenus,
  TAB и кастомные механики): потокобезопасность, асинхронные задачи, защита от лагов TPS.
category: gamedev-media
tags: [minecraft, paper, java21, tps]
version: 1.0.0
---

# Minecraft Paper / Purpur / Leaf 1.21.11 Plugin Development

Используй этот скилл при разработке, компиляции и интеграции Java-плагинов и расширений PlaceholderAPI для серверов Minecraft на базе Paper / Purpur / Leaf 1.21.11.

## 1. Среда разработки и компиляция (Java 21)
- Компилятор: `~/.local/share/jvm/temurin-21/bin/javac`
- Архиватор: `~/.local/share/jvm/temurin-21/bin/jar`
- Ядро сервера (API): JAR ядра Paper / Leaf 1.21.11 (или папка `libraries/` в директории целевого сервера)
- Стандарт компиляции: `--release 21 -proc:none`

## 2. Ключевые RPG-интеграции
1. **PlaceholderAPI расширения (`Expansion-<Name>.jar`)**:
   - Расположение: `plugins/PlaceholderAPI/expansions/` в директории сервера
   - Плейсхолдеры здоровья, маны, уровней, активных квестов и баланса.
2. **AuraSkills API (`AuraSkills-2.4.0.jar`)**:
   - Получение и изменение маны игрока (`ManaManager`).
   - Получение уровней навыков и статов (`SkillsUser`, `Stats`).
3. **MythicMobs API (`MythicMobs-5.14.0.jar`)**:
   - Кастомные спавнеры боссов, триггеры фаз боя и кастомные эффекты.
4. **NotQuests & FancyNpcs**:
   - Триггеры выполнения квестовых этапов и диалоги с NPC.

## 3. Правила потокобезопасности и TPS
- Никогда не вызывай синхронные методы работы с миром (`getBlockAt`, `getEntities`, `teleport`) из асинхронных потоков — это вызывает мгновенный `IllegalStateException: Asynchronous Chunk call!`.
- Для тяжелых вычислений (поиск путей, парсинг данных) используй асинхронный поток (`runTaskAsynchronously`), а для применения изменений в мир возвращайся в главный поток через `runTask`.
- Для телепортации всегда используй Paper-нативный `player.teleportAsync()`.

## 4. Minecraft 1.21.11 Механики Fabric
- **Карта и навигация (JourneyMap 1.21.11 Fabric)**:
  - Мод `journeymap-fabric-1.21.11-6.0.0.jar`: установлен в сборку клиента `smaka/mods/` и на сервер в `mods/`. Включает встроенные библиотеки `common-networking-fabric`, миникарту, полноэкранную карту (`J`), смерть-поинты и путевые точки.

- **Кастомные рецепты и утилиты**:
  - Датапак `dndlns_wool_to_strings.zip` (DNDLN's Wool to Strings): бесформенный крафт 1 любого блока шерсти (`#minecraft:wool`) в 4 нити (`minecraft:string` x4). Установлен на сервер в `world/datapacks/` и в локальные миры.

  1) Датапак `zero_level_enchanting.zip`: переопределяет все 43 зачарования (`anvil_cost: 0`, `min_cost: 1`, `max_cost: 100`), открывает сокровищные чары (Починка/Mending) на столе через `tags/enchantment/in_enchanting_table.json`, а также включает тег `#power_all:all_weapons` с поддержкой булавы (`#minecraft:enchantable/mace`), мечей, топоров и трезубцев. Зачарование «Сила» (Power I–V) увеличивает урон ближнего боя, а «Быстрая перезарядка» (Quick Charge I–III) добавляет атрибут `minecraft:attack_speed` (+25% за уровень), разгоняя скорость ударов меча и булавы.
  2) Fabric-мод `zerocostenchant-1.0.0.jar`:
     - Наковальня: убирает лимит 40 уровней («Слишком дорого!»), устанавливает стоимость 0 уровней, разрешает забирать предмет при 0 XP (`canTakeOutput`), предотвращает накопление штрафа починки.
     - Стол зачарований: перенаправляет проверки уровня и лазурита, позволяя чарить без опыта и лазурита, не списывает XP, усиливает 3-й слот до максимальной мощности (power 30).
     - Разблокировка `/tp` и `/teleport` без OP (`TeleportCommandMixin`): перехватывает вызовы `LiteralArgumentBuilder.requires` в `net.minecraft.class_3143.method_13760`, заменяя проверку оператора (level 2) на `source -> true`. Это позволяет обычным игрокам без OP использовать `/tp` с полным серверным автодополнением, оставляя все остальные команды закрытыми.

