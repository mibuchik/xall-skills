---
name: gpu-vram-optimization
description: >-
  Оптимизация GPU VRAM и пропускной способности (CUDA/PyTorch/инференс): бюджет памяти, BF16/FP8, gradient checkpointing, 8-bit AdamW и защита от OOM.
category: data-systems
tags: [gpu, vram, cuda, pytorch, oom, training]
version: 1.0.0
---

# GPU VRAM Optimization

Оптимизация GPU VRAM и пропускной способности (CUDA/PyTorch/инференс): бюджет памяти, BF16/FP8, gradient checkpointing, 8-bit AdamW и защита от OOM.

## Когда применять
- Обучение или инференс LLM/CV на 8–24 GB VRAM (например, RTX 4070–5090)
- Устранение `CUDA out of memory`, фрагментации памяти и простоя GPU из-за медленного DataLoader

## Рабочий протокол
1. Рассчитай точный бюджет VRAM до запуска: веса + градиенты + состояния оптимизатора (AdamW FP32 = 8 байт/парам, 8-bit AdamW = 2 байта) + активации (пропорциональны `batch × seq_len^2`) + запас 1.5 GB.
2. Используй `bf16` (на Ampere/Ada/Blackwell), FlashAttention/SDPA, gradient checkpointing, gradient accumulation и 8-bit/paged оптимизатор.
3. Включи `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`, чтобы резко снизить фрагментацию при переменной длине последовательностей.
4. Не запускай конкурирующие GPU-процессы (инференс-сервер, Chromium GPU, рендер) одновременно с обучением — останавливай/выгружай модель перед тренировкой и используй `--disable-gpu` для фоновых проверок.
5. Контролируй `nvidia-smi` (температуру, энергопотребление, утилизацию SM и пик VRAM) на первых 10 шагах — узкое место по CPU-data loading сразу видно по пиле GPU Util.

## Чеклист качества
- [ ] Пиковый VRAM укладывается с запасом >= 10% без вылетов на самых длинных батчах
- [ ] Нет утечек тензоров с графом градиентов (`loss.item()` при логировании, `torch.no_grad()`/`inference_mode()` на eval)
- [ ] Освобождается кэш между фазами (`del model; gc.collect(); torch.cuda.empty_cache()`)

## Антипаттерны (чего избегать)
- Сохранять тензор `losses.append(loss)` вместо `loss.item()`, держа в VRAM весь граф вычислений
- Обучать на полной длине без gradient checkpointing, когда можно сэкономить 60% VRAM ценой ~20% времени

## Верификация перед завершением
Прогони dry-run на максимально длинном синтетическом батче и сними `torch.cuda.max_memory_allocated()`.
