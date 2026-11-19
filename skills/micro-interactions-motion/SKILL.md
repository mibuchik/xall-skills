---
name: micro-interactions-motion
description: >-
  Тактильные микровзаимодействия и физика движения: только compositor-свойства (`transform`, `opacity`), `@starting-style`, `linear()` пружины и `prefers-reduced-motion`.
category: frontend-ui
tags: [motion, animations, css, spring, ux]
version: 1.0.0
---

# Micro Interactions Motion

Тактильные микровзаимодействия и физика движения: только compositor-свойства (`transform`, `opacity`), `@starting-style`, `linear()` пружины и `prefers-reduced-motion`.

## Когда применять
- Добавление анимаций открытия меню, диалогов, карточек, индикаторов загрузки и отклика кнопок
- Устранение дёрганых анимаций, layout thrashing и рывков при закрытии top-layer элементов

## Рабочий протокол
1. Анимируй строго GPU-compositor свойства (`transform`, `opacity`, `background-position`), никогда не анимируй `width`, `height`, `top`, `margin`.
2. Для top-layer элементов (`<dialog>`, `[popover]`) используй `@starting-style` + `transition-behavior: allow-discrete` с `display` и `overlay`.
3. Делай асимметричный тайминг: вход чуть выразительнее с мягким `linear()` spring на `transform` (220–300ms), выход быстрый `ease-out` (120–160ms). На `opacity` — никогда не ставь пружинный overshoot.
4. Выравнивай `transform-origin` к точке касания триггера и добавляй лёгкий тактильный `scale(0.97)` на `:active`.
5. Оборачивай пространственные движения в `@media (prefers-reduced-motion: no-preference)`, сохраняя мгновенный/мягкий opacity-отклик при `reduce`.

## Чеклист качества
- [ ] Отсутствуют глобальные костыли `animation-duration: 0.01ms !important`
- [ ] Все entrance-анимации используют `fill-mode: backwards`, гарантируя финальное `opacity: 1`
- [ ] Индикаторы ожидания (shimmer / calm pulse) спокойны и не раздражают при долгой работе

## Антипаттерны (чего избегать)
- Затянутые 600ms+ переходы на частых действиях (открытие меню, клик по вкладке)
- Отпрыгивание (`bounce`) на тексте, прозрачности или деструктивных действиях

## Верификация перед завершением
Проверь 60fps без layout shifts в DevTools Performance и протестируй режим `prefers-reduced-motion: reduce`.
