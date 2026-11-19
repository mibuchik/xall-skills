---
name: go-concurrent-backends
description: >-
  Надёжный Go: `context.Context` в каждой I/O-функции, `errgroup` для горутин без утечек, обёртывание ошибок `%w`, `golangci-lint` и `go test -race`.
category: data-systems
tags: [golang, goroutines, context, race-detector, backend]
version: 1.0.0
---

# Go Concurrent Backends

Надёжный Go: `context.Context` в каждой I/O-функции, `errgroup` для горутин без утечек, обёртывание ошибок `%w`, `golangci-lint` и `go test -race`.

## Когда применять
- Разработка высоконагруженных HTTP/gRPC сервисов, прокси и CLI-инструментов на Go
- Устранение утечек горутин, гонок данных и настройка graceful shutdown

## Рабочий протокол
1. Передавай `ctx context.Context` первым параметром во все I/O-функции и проверяй отмену в циклах/каналах.
2. Каждая запущенная горутина должна иметь гарантированное условие завершения; используй `golang.org/x/sync/errgroup` с `SetLimit` для управляемого параллелизма.
3. Оборачивай ошибки контекстом (`fmt.Errorf('load config %s: %w', path, err)`), проверяй через `errors.Is`/`errors.As`, не игнорируй возвращаемые `err` (включая `Close()` при записи!).
4. Проектируй маленькие интерфейсы на стороне потребителя (1–3 метода), а не гигантские интерфейсы на стороне реализации.
5. Всегда прогоняй `go test -race ./...` и `go vet ./...`.

## Чеклист качества
- [ ] `go vet ./...` и `go test -race ./...` проходят с 0 гонок и ошибок
- [ ] У `http.Client` и `http.Server` заданы явные таймауты (`ReadHeaderTimeout`, `Timeout`)
- [ ] Закрывается `resp.Body.Close()` после проверки ошибки каждого HTTP-запроса

## Антипаттерны (чего избегать)
- Использовать дефолтный `http.DefaultClient` (у него бесконечный таймаут!)
- Стартовать горутины без `WaitGroup`/`errgroup`, которые продолжают жить после выхода из хендлера

## Верификация перед завершением
Выполни `go vet ./...` и `go test -race -count=1 ./...`.
