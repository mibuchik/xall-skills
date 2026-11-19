---
name: python-modern-uv-ruff
description: >-
  Современная разработка на Python 3.12+: управление окружениями через `uv`, `pyproject.toml`, линтинг/форматинг `ruff`, строгие аннотации типов и `pytest`.
category: data-systems
tags: [python, uv, ruff, typing, pytest]
version: 1.0.0
---

# Python Modern Uv Ruff

Современная разработка на Python 3.12+: управление окружениями через `uv`, `pyproject.toml`, линтинг/форматинг `ruff`, строгие аннотации типов и `pytest`.

## Когда применять
- Создание, рефакторинг и поддержка Python-проектов, CLI, скриптов и ML-пайплайнов
- Настройка чистого `pyproject.toml`, `ruff`, `mypy`/`pyright` и изоляции `.venv`

## Рабочий протокол
1. Храни метаданные и зависимости в `pyproject.toml`, управляй окружением через `uv` (`uv venv`, `uv sync`, `uv run`) для мгновенной воспроизводимости.
2. Используй современный синтаксис типов Python 3.12+ (`list[str]`, `X | None`, `dataclass(slots=True)`, `TypedDict`, `Protocol`).
3. Настрой `ruff check` + `ruff format` и тайпчекер (`pyright`/`mypy`) в `pyproject.toml`.
4. Для путей используй `pathlib.Path`, для ресурсов — `with`-менеджеры, для логирования — `logging`, для ошибок — конкретные типы исключений (не голый `except:`).
5. Пиши быстрые изолированные тесты на `pytest` с фикстурой `tmp_path` и `monkeypatch`.

## Чеклист качества
- [ ] `ruff check .` и `pytest` проходят с 0 ошибок
- [ ] Нет мутабельных значений по умолчанию (`def f(items=[])`) и голых `except:`
- [ ] Точки входа используют `if __name__ == '__main__':` и корректные коды выхода

## Антипаттерны (чего избегать)
- Ставить пакеты в системный Python через `sudo pip install`
- Глушить исключения `except Exception: pass`, скрывая реальные баги

## Верификация перед завершением
Запусти `ruff check`, тайпчекер и `pytest -q` внутри проектного окружения.
