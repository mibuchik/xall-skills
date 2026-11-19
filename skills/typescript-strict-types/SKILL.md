---
name: typescript-strict-types
description: >-
  Строгий TypeScript без `any`: discriminated unions, `unknown` + сужение типов, `satisfies`, типобезопасные границы I/O и нулевой дрейф контрактов.
category: frontend-ui
tags: [typescript, strict, discriminated-unions, zod, type-safety]
version: 1.0.0
---

# Typescript Strict Types

Строгий TypeScript без `any`: discriminated unions, `unknown` + сужение типов, `satisfies`, типобезопасные границы I/O и нулевой дрейф контрактов.

## Когда применять
- Проектирование типов, рефакторинг JS -> TS, устранение `any` и сложных ошибок компилятора
- Типизация IPC-мостов, API-ответов, стейт-машин и конфигов

## Рабочий протокол
1. Включай `strict: true`, `noUncheckedIndexedAccess` (где применимо) и рассматривай `any` как запрещённый костыль.
2. Моделируй состояния приложения через discriminated unions (`{ status: 'loading' } | { status: 'ready'; data: T } | { status: 'error'; error: string }`), делая невалидные состояния непредставимыми.
3. Внешние данные (JSON, API, файлы, CLI) принимай как `unknown` и валидируй схемой или type guard перед использованием.
4. Используй `as const satisfies Record<...>` для словарей, конфигов и i18n, сохраняя автокомплит и проверку полноты (`exhaustiveness` через `never`).
5. Не дублируй типы вручную — выводи их из единого источника правды (`typeof`, `ReturnType`, схемы).

## Чеклист качества
- [ ] `tsc --noEmit` проходит с 0 ошибок и без подавляющих `@ts-ignore`
- [ ] Отсутствуют небезопасные касты `as Foo` на непроверенных внешних данных
- [ ] Все ветки union-типов закрыты проверкой исчерпываемости (`never`)

## Антипаттерны (чего избегать)
- Глушить ошибки компилятора через `as any` или `@ts-ignore` вместо исправления типа
- Хранить 4 независимых boolean-флага (`isLoading`, `isError`, `isDone`, `isEmpty`) вместо одного union

## Верификация перед завершением
Выполни `tsc --noEmit` и проверь `grep` на отсутствие новых `any` и `@ts-ignore`.
