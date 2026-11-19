---
name: remotion-video-scripting
description: >-
  Программное создание видео на Remotion: детерминированные кадры от `useCurrentFrame()`, физика `spring()`/`interpolate()`, композиции, субтитры и чистый рендер.
category: gamedev-media
tags: [remotion, video, react, motion-graphics, rendering]
version: 1.0.0
---

# Remotion Video Scripting

Программное создание видео на Remotion: детерминированные кадры от `useCurrentFrame()`, физика `spring()`/`interpolate()`, композиции, субтитры и чистый рендер.

## Когда применять
- Создание промо-роликов, туториалов, дата-визуализаций, титров и шортсов на Remotion
- Исправление рассинхронизации кадров, мигания шрифтов и медленного рендера

## Рабочий протокол
1. Вся анимация должна быть строго чистой функцией от `useCurrentFrame()` и `fps` — НИКАКИХ CSS `transition`/`animation`, `setTimeout` или `Math.random()` (используй `random(seed)` из Remotion!).
2. Разбивай ролик на читаемые `<Sequence>` / `<TransitionSeries>` сцены с константами длительности в кадрах и единой дизайн-системой.
3. Для движения используй `spring({ frame, fps, config })` и `interpolate(..., { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })`.
4. Дожидайся загрузки шрифтов и медиа через `delayRender()` / `continueRender()` (или `@remotion/google-fonts`), чтобы первый кадр не рендерился системным шрифтом.
5. Проверяй ключевые кадры через `remotion still` до запуска полного финального рендера `remotion render`.

## Чеклист качества
- [ ] Отсутствуют CSS-анимации и недетерминированный `Math.random()`/`Date.now()`
- [ ] Все `interpolate` защищены `clamp`, текст не выходит за safe-zone на целевом соотношении сторон
- [ ] Аудио синхронизировано по кадрам и не клиппит

## Антипаттерны (чего избегать)
- Пытаться анимировать элементы через CSS `@keyframes` в Remotion (при многопоточном рендере кадры рвутся!)
- Рендерить 60-секундное видео целиком без предварительной проверки 4–5 ключевых кадров через `still`

## Верификация перед завершением
Выполни `tsc --noEmit`, отрендери контрольные кадры `remotion still` и проверь финальный MP4 через `ffprobe`.
