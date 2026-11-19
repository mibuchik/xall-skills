---
name: rust-safe-systems
description: >-
  Идиоматичный и безопасный Rust: чистый borrow checker без лишних `.clone()`, явная обработка ошибок (`thiserror`/`anyhow`), `clippy` и нулевой `unwrap()` в проде.
category: data-systems
tags: [rust, cargo, clippy, ownership, systems]
version: 1.0.0
---

# Rust Safe Systems

Идиоматичный и безопасный Rust: чистый borrow checker без лишних `.clone()`, явная обработка ошибок (`thiserror`/`anyhow`), `clippy` и нулевой `unwrap()` в проде.

## Когда применять
- Разработка CLI, сетевых сервисов, парсеров и системных утилит на Rust
- Ревью unsafe-блоков, владения памятью, async Tokio и ошибок компилятора Rust

## Рабочий протокол
1. Проектируй структуры данных с учётом владения: передавай `&str` / `&[T]` на чтение, используй `Cow<'_, str>` там, где аллокация нужна редко.
2. В библиотечном коде определяй типизированные ошибки (`thiserror`), в бинарниках/CLI используй `anyhow::Context` — избегай `.unwrap()`/`.expect()` на внешних данных.
3. Для каждого блока `unsafe` (если он вообще неизбежен) пиши комментарий `// SAFETY: ...` с доказательством инвариантов.
4. В async Tokio никогда не держи `std::sync::MutexGuard` через `.await` и выноси CPU-тяжёлые задачи в `spawn_blocking`.
5. Регулярно прогоняй `cargo clippy --all-targets -- -D warnings` и `cargo test`.

## Чеклист качества
- [ ] `cargo check`, `cargo clippy -- -D warnings` и `cargo test` проходят чисто
- [ ] В продакшен-ветках нет паникующих `.unwrap()` на пользовательском/сетевом вводе
- [ ] Релизные профили настроены осознанно (`lto`, `strip` при необходимости для CLI)

## Антипаттерны (чего избегать)
- Лечить каждую ошибку borrow checker бездумным `.clone()` в горячем цикле
- Использовать `unsafe` для обхода компилятора вместо исправления архитектуры владения

## Верификация перед завершением
Запусти `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings` и `cargo test`.
