---
name: css-modern-layout
description: >-
  Современная CSS-вёрстка: Grid/Subgrid, Container Queries, нативные `<dialog>` и `[popover]`, CSS Anchor Positioning и защита от overflow.
category: frontend-ui
tags: [css, grid, container-queries, popover, anchor-positioning]
version: 1.0.0
---

# Css Modern Layout

Современная CSS-вёрстка: Grid/Subgrid, Container Queries, нативные `<dialog>` и `[popover]`, CSS Anchor Positioning и защита от overflow.

## Когда применять
- Сложные раскладки, дашборды, сплит-панели, выпадающие меню, модалки и адаптивный UI
- Исправление багов со скроллом, обрезанием текста, z-index и переполнением flex/grid

## Рабочий протокол
1. Для вложенных flex/grid-контейнеров со скроллом всегда задавай `min-width: 0` и `min-height: 0` — это 90% причин «сломанного скролла».
2. Используй нативные top-layer элементы (`<dialog>` + `showModal()`, `popover='auto'`) вместо хрупких `z-index: 99999`.
3. Для контекстных меню используй CSS Anchor Positioning внутри `@supports (position-area: block-end)` с `position-try-fallbacks`.
4. Адаптируй переиспользуемые карточки через `@container` queries, а не только через глобальные `@media`.
5. Настраивай скроллбары через стандартные `scrollbar-color` и `scrollbar-width` с контрастом >= 3:1.

## Чеклист качества
- [ ] Нет горизонтального переполнения (`scrollWidth <= clientWidth`) на узких и широких экранах
- [ ] Длинные строки и пути корректно обрезаются (`text-overflow: ellipsis` или `overflow-wrap: anywhere`)
- [ ] Тёмная, светлая и системная темы используют единые CSS custom properties без захардкоженных цветов

## Антипаттерны (чего избегать)
- Войны `z-index: 999999` вместо нативного top-layer (`popover` / `<dialog>`)
- Фиксированные высоты `height: 40px` на многострочных блоках с локализованным текстом

## Верификация перед завершением
Проверь рендер на нескольких разрешениях (1280×720, 1440×900, 390×844) и в обеих темах.
