---
name: threejs-webgl-shaders
description: >-
  Интерактивная 3D-графика на Three.js / WebGL: контроль draw calls (InstancedMesh), корректный `dispose()` ресурсов GPU, освещение и GLSL-шейдеры.
category: gamedev-media
tags: [threejs, webgl, glsl, 3d, performance]
version: 1.0.0
---

# Threejs Webgl Shaders

Интерактивная 3D-графика на Three.js / WebGL: контроль draw calls (InstancedMesh), корректный `dispose()` ресурсов GPU, освещение и GLSL-шейдеры.

## Когда применять
- Создание 3D-сцен, вьюеров моделей, эффектов частиц и кастомных шейдеров в браузере
- Оптимизация FPS, устранение утечек WebGL-контекста и настройка камеры/освещения

## Рабочий протокол
1. Снижай число draw calls: объединяй повторяющуюся геометрию в `InstancedMesh` / `BatchedMesh`, используй текстурные атласы и `renderer.info.render.calls` для контроля.
2. Ограничивай `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))` — на 4K/HiDPI экранах DPR 3–4 без лимита убивает fill-rate.
3. Обязательно освобождай GPU-ресурсы (`geometry.dispose()`, `material.dispose()`, `texture.dispose()`, `renderer.dispose()`) при размонтировании компонента.
4. Используй `ResizeObserver` для синхронизации камеры/канваса, `Clock.getDelta()` с клампом (например `Math.min(dt, 0.05)`) для стабильной физики при переключении вкладки.
5. Настраивай корректное цветовое пространство (`SRGBColorSpace`, ACESFilmic tone mapping) и аккуратные тени с ограниченным frustum shadow camera.

## Чеклист качества
- [ ] Нет утечек памяти GPU при повторном открытии/закрытии 3D-вьюера
- [ ] Анимационный цикл `requestAnimationFrame` останавливается на unmount и при скрытой вкладке
- [ ] Нет ошибок компиляции GLSL в консоли и стабильные 60 FPS на целевом устройстве

## Антипаттерны (чего избегать)
- Создавать `new THREE.Vector3()` и `new THREE.Material()` внутри каждого кадра `animate()`
- Создавать 5000 отдельных `Mesh` вместо одного `InstancedMesh`

## Верификация перед завершением
Проверь `renderer.info` (geometries, textures, draw calls), отсутствие WebGL warnings и FPS.
