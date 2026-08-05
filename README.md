# PJ-CORE Control Dashboard

## Запуск

```bash
cd pj-core-control-dashboard
python3 -m http.server 8080
```

Открыть `http://localhost:8080`.

## Работает

- пять размеров карточек по давности активности;
- закреплённые проекты остаются крупными;
- раскрытие старых карточек;
- поиск, фильтр, полноэкранный режим;
- MVP/PROD прогресс;
- перечитывание `data/projects.json` раз в минуту;
- адаптация под монитор и мобильные устройства.

## Градации

- 0–3 дня — крупная;
- 4–14 — средняя;
- 15–30 — компактная;
- 31–90 — маленькая;
- старше 90 дней — иконка.

## Обновление

```bash
python3 scripts/update_project.py stickerpack-ai mvp 55
python3 scripts/update_project.py stickerpack-ai currentWork "Собирается Mini App"
```

Любое изменение через скрипт обновляет дату активности. Для автоматизации ChatGPT/OpenClaw должны дважды в день пересобирать `data/projects.json` и коммитить его в репозиторий, откуда Dashboard читает данные.
